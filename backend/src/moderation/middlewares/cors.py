from starlette.types import ASGIApp, Receive, Scope, Send


class CORSMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        *,
        allow_origins: list[str] | None = None,
        allow_methods: list[str] | None = None,
        allow_headers: list[str] | None = None,
        allow_credentials: bool = False
    ) -> None:
        self.app = app
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "PUT"]
        self.allow_headers = allow_headers or ["*"]
        self.allow_credentials = allow_credentials

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        if scope["method"] == "OPTIONS":
            await self.handle_preflight(scope, send)
            return

        async def custom_send(event) -> Send:
            if event["type"] == "http.response.start":
                headers = event.setdefault("headers", [])
                headers.extend(self.cors_headers())
            await send(event)

        await self.app(scope, receive, custom_send)

    async def handle_preflight(self, scope: Scope, send: Send) -> None:
        """Handle OPTIONS preflight requests."""
        headers = self.cors_headers()
        response = {
            "type": "http.response.start",
            "status": 200,
            "headers": headers,
        }
        await send(response)
        await send({"type": "http.response.body", "body": b""})

    def cors_headers(self):
        """Generate CORS headers."""
        headers = [
            (b"access-control-allow-origin", b", ".join((x.encode() for x in self.allow_origins))),
            (b"access-control-allow-methods", b", ".join((x.encode() for x in self.allow_methods))),
            (b"access-control-allow-headers", b", ".join((x.encode() for x in self.allow_headers))),
        ]
        if self.allow_credentials:
            headers.append((b"access-control-allow-credentials", b"true"))
        return headers
