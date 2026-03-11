import json
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, parse, request

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.settings import get_settings


def post_form(url: str, data: dict[str, str], *, allow_error_payload: bool = False) -> dict[str, Any]:
    payload = parse.urlencode(data).encode("utf-8")
    req = request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return json.loads(response.read().decode(charset))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        if allow_error_payload:
            try:
                return json.loads(detail)
            except json.JSONDecodeError:
                pass
        raise RuntimeError(f"Request failed with status {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from exc


def rewrite_env_value(path: Path, key: str, value: str) -> None:
    if not path.exists():
        raise RuntimeError(f"Cannot write token because {path} does not exist.")
    lines = path.read_text(encoding="utf-8").splitlines()
    updated = False
    for index, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[index] = f"{key}={value}"
            updated = True
            break
    if not updated:
        lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    settings = get_settings()
    if not settings.outlook_tenant_id or not settings.outlook_client_id:
        print("Missing OUTLOOK_TENANT_ID or OUTLOOK_CLIENT_ID in .env.", file=sys.stderr)
        return 1

    tenant_id = settings.outlook_tenant_id
    client_id = settings.outlook_client_id
    scopes = settings.outlook_graph_scopes
    device_code_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/devicecode"
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    device_code = post_form(
        device_code_url,
        {
            "client_id": client_id,
            "scope": scopes,
        },
    )
    if "device_code" not in device_code:
        print(json.dumps(device_code, indent=2), file=sys.stderr)
        return 1
    print(device_code.get("message", "Open the verification URL and enter the device code."))

    interval = int(device_code.get("interval", 5))
    expires_in = int(device_code.get("expires_in", 900))
    deadline = time.time() + expires_in

    while time.time() < deadline:
        time.sleep(interval)
        token = post_form(
            token_url,
            {
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "client_id": client_id,
                "device_code": device_code["device_code"],
            },
            allow_error_payload=True,
        )
        if "access_token" in token:
            rewrite_env_value(ROOT / ".env", "MICROSOFT_GRAPH_ACCESS_TOKEN", token["access_token"])
            print("Saved MICROSOFT_GRAPH_ACCESS_TOKEN to .env")
            if "refresh_token" in token:
                print("Refresh token received but not persisted.")
            return 0

        if token.get("error") == "authorization_pending":
            continue
        if token.get("error") == "slow_down":
            interval += 5
            continue

        print(json.dumps(token, indent=2), file=sys.stderr)
        return 1

    print("Device-code flow expired before approval completed.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
