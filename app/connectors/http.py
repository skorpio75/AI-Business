import json
from dataclasses import dataclass
from typing import Any, Mapping, Optional
from urllib import error, parse, request


@dataclass(slots=True)
class ConnectorHttpError(Exception):
    message: str
    status_code: Optional[int] = None
    detail: Optional[str] = None

    def __str__(self) -> str:
        if self.status_code is None:
            return self.message
        if self.detail:
            return f"{self.message} (status={self.status_code}, detail={self.detail})"
        return f"{self.message} (status={self.status_code})"


def get_json(
    *,
    url: str,
    headers: Optional[Mapping[str, str]] = None,
    params: Optional[Mapping[str, Any]] = None,
    timeout: int = 10,
) -> Any:
    query = ""
    if params:
        encoded = {key: value for key, value in params.items() if value is not None}
        if encoded:
            query = "?" + parse.urlencode(encoded, doseq=True)

    req = request.Request(
        url + query,
        headers={"Accept": "application/json", **(dict(headers or {}))},
        method="GET",
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return json.loads(response.read().decode(charset))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ConnectorHttpError("Connector request failed", status_code=exc.code, detail=detail) from exc
    except error.URLError as exc:
        raise ConnectorHttpError(f"Connector request failed: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise ConnectorHttpError("Connector returned invalid JSON") from exc


def post_json(
    *,
    url: str,
    headers: Optional[Mapping[str, str]] = None,
    body: Optional[Mapping[str, Any]] = None,
    timeout: int = 10,
) -> Any:
    payload = json.dumps(body or {}).encode("utf-8")
    req = request.Request(
        url,
        data=payload,
        headers={"Accept": "application/json", "Content-Type": "application/json", **(dict(headers or {}))},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw = response.read()
            if not raw:
                return None
            charset = response.headers.get_content_charset() or "utf-8"
            return json.loads(raw.decode(charset))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ConnectorHttpError("Connector request failed", status_code=exc.code, detail=detail) from exc
    except error.URLError as exc:
        raise ConnectorHttpError(f"Connector request failed: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise ConnectorHttpError("Connector returned invalid JSON") from exc
