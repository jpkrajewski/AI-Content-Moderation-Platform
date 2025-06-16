from authlib.integrations.flask_client import OAuth
from flask import Flask
from moderation.core.settings import settings
from moderation.service.oauth.models import UserInfo


class OAuthService(OAuth):
    def init_and_register_app(self, app: Flask):
        self.init_app(app)
        self.register(
            name="google",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            access_token_url="https://oauth2.googleapis.com/token",  # nosec
            authorize_url="https://accounts.google.com/o/oauth2/auth",
            api_base_url="https://www.googleapis.com/oauth2/v1/",
            client_kwargs={"scope": "openid email profile"},
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        )

    def authorize(self) -> UserInfo:
        self.google.authorize_access_token()
        user = self.google.get("userinfo").json()
        user_info = UserInfo(**user)
        return user_info
