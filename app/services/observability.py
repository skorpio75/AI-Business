# Copyright (c) Dario Pizzolante
import logging
from contextlib import contextmanager
from typing import Any, Iterator

from app.core.settings import Settings

try:
    from langfuse import Langfuse
except Exception:  # pragma: no cover
    Langfuse = None


logger = logging.getLogger(__name__)


class ObservationHandle:
    def __init__(self, observation: Any | None = None) -> None:
        self._observation = observation

    def update(self, **kwargs: Any) -> None:
        if self._observation is None or not kwargs:
            return
        try:
            self._observation.update(**kwargs)
        except Exception as exc:  # pragma: no cover
            logger.warning("Langfuse observation update failed: %s", exc)


class NullObservabilityService:
    enabled = False

    @contextmanager
    def start_span(
        self,
        *,
        name: str,
        input: Any | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Iterator[ObservationHandle]:
        del name, input, metadata
        yield ObservationHandle()

    @contextmanager
    def start_generation(
        self,
        *,
        name: str,
        input: Any | None = None,
        metadata: dict[str, Any] | None = None,
        model: str | None = None,
        model_parameters: dict[str, Any] | None = None,
    ) -> Iterator[ObservationHandle]:
        del name, input, metadata, model, model_parameters
        yield ObservationHandle()

    def flush(self) -> None:
        return


class LangfuseObservabilityService(NullObservabilityService):
    def __init__(self, settings: Settings, client: Any | None = None) -> None:
        self.settings = settings
        self._client = client or self._build_client()
        self.enabled = self._client is not None

    def _build_client(self) -> Any | None:
        if not self.settings.langfuse_enabled:
            return None
        if Langfuse is None:
            logger.warning("Langfuse tracing is enabled in settings, but the Langfuse SDK is not installed.")
            return None
        if not self.settings.langfuse_public_key or not self.settings.langfuse_secret_key:
            logger.warning(
                "Langfuse tracing is enabled in settings, but LANGFUSE_PUBLIC_KEY or LANGFUSE_SECRET_KEY is missing."
            )
            return None
        try:
            return Langfuse(
                public_key=self.settings.langfuse_public_key,
                secret_key=self.settings.langfuse_secret_key,
                host=self.settings.langfuse_host,
                release=self.settings.langfuse_release,
            )
        except Exception as exc:  # pragma: no cover
            logger.warning("Langfuse client initialization failed: %s", exc)
            return None

    @contextmanager
    def start_span(
        self,
        *,
        name: str,
        input: Any | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Iterator[ObservationHandle]:
        with self._start_observation(
            name=name,
            as_type="span",
            input=input,
            metadata=metadata,
        ) as handle:
            yield handle

    @contextmanager
    def start_generation(
        self,
        *,
        name: str,
        input: Any | None = None,
        metadata: dict[str, Any] | None = None,
        model: str | None = None,
        model_parameters: dict[str, Any] | None = None,
    ) -> Iterator[ObservationHandle]:
        with self._start_observation(
            name=name,
            as_type="generation",
            input=input,
            metadata=metadata,
            model=model,
            model_parameters=model_parameters,
        ) as handle:
            yield handle

    @contextmanager
    def _start_observation(
        self,
        *,
        name: str,
        as_type: str,
        input: Any | None = None,
        metadata: dict[str, Any] | None = None,
        model: str | None = None,
        model_parameters: dict[str, Any] | None = None,
    ) -> Iterator[ObservationHandle]:
        if self._client is None:
            yield ObservationHandle()
            return

        merged_metadata = self._merge_metadata(metadata)
        try:
            with self._client.start_as_current_observation(
                name=name,
                as_type=as_type,
                input=input,
                metadata=merged_metadata,
                model=model,
                model_parameters=model_parameters,
            ) as observation:
                handle = ObservationHandle(observation)
                try:
                    yield handle
                except Exception as exc:
                    handle.update(
                        level="ERROR",
                        status_message=f"{name} failed: {exc.__class__.__name__}",
                    )
                    raise
        except Exception as exc:  # pragma: no cover
            logger.warning("Langfuse observation start failed for %s: %s", name, exc)
            yield ObservationHandle()

    def _merge_metadata(self, metadata: dict[str, Any] | None) -> dict[str, Any]:
        return {
            "app_name": self.settings.app_name,
            "environment": self.settings.env,
            "primary_track": self.settings.primary_track,
            "tenant_id": self.settings.tenant_id,
            **(metadata or {}),
        }

    def flush(self) -> None:
        if self._client is None:
            return
        try:
            self._client.flush()
        except Exception as exc:  # pragma: no cover
            logger.warning("Langfuse flush failed: %s", exc)
