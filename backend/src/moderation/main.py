import uvicorn
from moderation.core.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "moderation.app:create_app",
        factory=True,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
    )
