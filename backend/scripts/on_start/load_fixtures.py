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
        if drop_db:
            # Delete child tables first due to foreign keys
            db.query(ContentAnalysis).delete(synchronize_session=False)
            db.query(ModerationAction).delete(synchronize_session=False)
            db.query(Content).delete(synchronize_session=False)
            db.query(CustomerContentCreatorUser).delete(synchronize_session=False)
            db.query(ClientAccess).delete(synchronize_session=False)
            db.query(User).delete(synchronize_session=False)
            db.commit()

    with get_db() as db:
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

        print(f"🔐 Admin 'admin' password: {admin_password}")
        print(f"🔐 Moderator 'moderator' password: {moderator_password}")

        # Ensure admin & moderator exist before FK references
        db.add_all([admin, moderator])
        db.flush()  # 🔐 Flush to get persisted IDs

        clients = []
        content_creators = []
        contents = []
        analyses = []
        moderation_actions = []

        # 10 Clients
        for _ in range(10):
            client = ClientAccess(
                id=uuid.uuid4(),
                source=fake.company().lower().replace(" ", "_"),
                api_key=generate_fake_api_key(),
                current_scope=["moderation", "content"],
                is_active=True,
                access_count=random.randint(0, 100),
            )
            clients.append(client)
            print(f"🔑 Client API Key: {client.api_key}")

        db.add_all(clients)
        db.flush()  # Make sure client IDs are persisted

        # 10 Content Creators & related data
        for client in clients:
            creator_id = uuid.uuid4()
            creator = CustomerContentCreatorUser(
                id=uuid.uuid4(),
                source=client.source,
                user_id=creator_id,
                username=fake.user_name(),
                reputation_score=random.randint(50, 100),
                flagged_count=random.randint(0, 5),
            )
            content_creators.append(creator)

            content_id = uuid.uuid4()
            content = Content(
                id=content_id,
                user_id=creator_id,
                username=creator.username,
                title=fake.sentence(),
                body=fake.paragraph(),
                tags=[fake.word() for _ in range(3)],
                localization={"lang": "en", "region": "US"},
                source=creator.source,
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
                analysis_metadata={"toxicity": round(random.uniform(0.2, 0.95), 2)},
            )
            analyses.append(analysis)

            action = ModerationAction(
                id=uuid.uuid4(),
                content_id=content_id,
                moderator_id=moderator.id,
                action=random.choice(["approve", "reject", "flag"]),
                reason=fake.sentence(),
            )
            moderation_actions.append(action)

        db.add_all(content_creators)
        db.add_all(contents)
        db.add_all(analyses)
        db.add_all(moderation_actions)

        db.commit()
        print("✅ Fixtures successfully loaded.")


if __name__ == "__main__":
    load_fixtures()
