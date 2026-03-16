# Copyright (c) Dario Pizzolante
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.settings import get_settings
from app.services.microsoft_graph_auth import persist_tokens, post_form


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
            persist_tokens(token, settings=settings)
            print("Saved MICROSOFT_GRAPH_ACCESS_TOKEN to the active runtime env file")
            if "refresh_token" in token:
                print("Saved MICROSOFT_GRAPH_REFRESH_TOKEN to the active runtime env file")
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
