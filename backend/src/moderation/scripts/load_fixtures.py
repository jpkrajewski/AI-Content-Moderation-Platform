# bandit: skip=B105
import random
import uuid

from faker import Faker
from moderation.db.access import ClientAccess
from moderation.db.analysis import ContentAnalysis
from moderation.db.content import Content
from moderation.db.customer_user import CustomerContentCreatorUser
from moderation.db.moderation import ModerationAction
from moderation.db.session import get_db
from moderation.db.user import User

fake = Faker()


def generate_fake_api_key():
    return str(uuid.uuid4())


def load_fixtures(drop_db: bool = True):
    with get_db() as db:
        # Delete child tables first due to foreign keys
        db.query(ContentAnalysis).delete(synchronize_session=False)
        db.query(ModerationAction).delete(synchronize_session=False)
        db.query(Content).delete(synchronize_session=False)
        db.query(CustomerContentCreatorUser).delete(synchronize_session=False)
        db.query(ClientAccess).delete(synchronize_session=False)
        db.query(User).delete(synchronize_session=False)
        db.commit()
        print("🚀 Loading fixtures...")
        # Admin & Moderator passwords (plaintext for logging only)
        admin_password = "admin"
        moderator_password = "moderator"
        admin = User(
            id=uuid.uuid4(),
            username="admin",
            email="admin@example.com",
            password_hash=admin_password,  # NOTE: hash in prod
            role="admin",
        )
        moderator = User(
            id=uuid.uuid4(),
            username="moderator",
            email="moderator@example.com",
            password_hash=moderator_password,
            role="moderator",
        )

        print(f"🔐 Admin 'admin' password: {admin_password}, email: admin@example.com")
        print(f"🔐 Moderator 'moderator' password: {moderator_password}, email: moderator@example.com")

        # Ensure admin & moderator exist before FK references
        db.add_all([admin, moderator])
        db.flush()  # 🔐 Flush to get persisted IDs

        contents = []
        analyses = []

        for _ in range(100):

            content_id = uuid.uuid4()
            content = Content(
                id=content_id,
                user_id=uuid.uuid4(),
                username=fake.name(),
                title=fake.sentence(),
                body=fake.paragraph(),
                tags=[fake.word() for _ in range(3)],
                localization={"lang": "en", "region": "US"},
                source=fake.url(),
                status=random.choice(["pending", "approved", "rejected"]),
                image_paths=["/uploads/" + fake.file_name(extension="jpg")],
            )
            contents.append(content)

            analysis = ContentAnalysis(
                id=uuid.uuid4(),
                content_id=content_id,
                content_type="text",
                automated_flag=random.choice([True, False]),
                automated_flag_reason="auto_flag" if random.random() > 0.5 else None,
                model_version="v1.0.1",
                analysis_metadata={
                    "toxicity": round(random.uniform(0.2, 0.95), 2),
                    "spam": round(random.uniform(0.2, 0.95), 2),
                    "hate_speech": round(random.uniform(0.2, 0.95), 2),
                },
            )
            analyses.append(analysis)
            analysis = ContentAnalysis(
                id=uuid.uuid4(),
                content_id=content_id,
                content_type="image",
                automated_flag=random.choice([True, False]),
                automated_flag_reason="auto_flag" if random.random() > 0.5 else None,
                model_version="v1.0.1",
                analysis_metadata={
                    "nudity": round(random.uniform(0.2, 0.95), 2),
                    "violence": round(random.uniform(0.2, 0.95), 2),
                    "spam": round(random.uniform(0.2, 0.95), 2),
                },
            )
            analyses.append(analysis)
            analysis = ContentAnalysis(
                id=uuid.uuid4(),
                content_id=content_id,
                content_type="document",
                automated_flag=random.choice([True, False]),
                automated_flag_reason="auto_flag" if random.random() > 0.5 else None,
                model_version="v1.0.1",
                analysis_metadata={
                    "violence": round(random.uniform(0.2, 0.95), 2),
                    "spam": round(random.uniform(0.2, 0.95), 2),
                },
            )
            analyses.append(analysis)
            analysis = ContentAnalysis(
                id=uuid.uuid4(),
                content_id=content_id,
                content_type="text/plain",
                automated_flag=random.choice([True, False]),
                automated_flag_reason="auto_flag" if random.random() > 0.5 else None,
                model_version="v1.0.1",
                analysis_metadata={"hate_speech": round(random.uniform(0.2, 0.95), 2)},
            )
            analyses.append(analysis)

        db.add_all(contents)
        db.flush()
        db.add_all(analyses)
        db.commit()
        print("✅ Fixtures successfully loaded.")


if __name__ == "__main__":
    load_fixtures()
