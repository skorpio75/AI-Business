# Copyright (c) Dario Pizzolante
import json
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib import parse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.settings import get_settings
from app.services.provider_auth import persist_provider_tokens, post_form


class CallbackHandler(BaseHTTPRequestHandler):
    authorization_code: str | None = None
    error_detail: str | None = None
    received_event = threading.Event()

    def do_GET(self) -> None:  # noqa: N802
        parsed = parse.urlparse(self.path)
        params = parse.parse_qs(parsed.query)
        if "error" in params:
            self.error_detail = params["error"][0]
        elif "code" in params:
            self.authorization_code = params["code"][0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        if self.authorization_code:
            self.wfile.write(b"<html><body><h1>Google authorization received.</h1><p>You can close this window.</p></body></html>")
        else:
            self.wfile.write(b"<html><body><h1>Google authorization failed.</h1><p>Return to the terminal for details.</p></body></html>")
        self.received_event.set()

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def main() -> int:
    settings = get_settings()
    if not settings.google_client_id or not settings.google_client_secret:
        print("Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET in .env.", file=sys.stderr)
        return 1

    redirect = parse.urlparse(settings.google_oauth_redirect_uri)
    if redirect.hostname not in {"127.0.0.1", "localhost"} or redirect.port is None:
        print("GOOGLE_OAUTH_REDIRECT_URI must be a local loopback URL such as http://127.0.0.1:8765/oauth/google/callback.", file=sys.stderr)
        return 1

    auth_query = parse.urlencode(
        {
            "client_id": settings.google_client_id,
            "redirect_uri": settings.google_oauth_redirect_uri,
            "response_type": "code",
            "scope": settings.google_oauth_scopes,
            "access_type": "offline",
            "prompt": "consent",
        }
    )
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{auth_query}"

    server = HTTPServer((redirect.hostname, redirect.port), CallbackHandler)
    server.timeout = 1
    print("Open this URL in your browser if it does not open automatically:")
    print(auth_url)
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    while not CallbackHandler.received_event.is_set():
        server.handle_request()

    if CallbackHandler.error_detail:
        print(f"Google OAuth returned an error: {CallbackHandler.error_detail}", file=sys.stderr)
        return 1
    if not CallbackHandler.authorization_code:
        print("No Google authorization code was received.", file=sys.stderr)
        return 1

    token_payload = post_form(
        settings.google_token_uri,
        {
            "code": CallbackHandler.authorization_code,
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uri": settings.google_oauth_redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    if "access_token" not in token_payload:
        print(json.dumps(token_payload, indent=2), file=sys.stderr)
        return 1

    persist_provider_tokens("google", token_payload, settings=settings)
    print("Saved GOOGLE_ACCESS_TOKEN to the active runtime env file or configured secret store.")
    if "refresh_token" in token_payload:
        print("Saved GOOGLE_REFRESH_TOKEN to the active runtime env file or configured secret store.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
