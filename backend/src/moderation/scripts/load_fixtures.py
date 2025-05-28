# bandit: skip=B105
import os
import random
import uuid
from collections import defaultdict
from datetime import timedelta

from faker import Faker
from moderation.db.analysis import ContentAnalysis
from moderation.db.client_api_key import ClientApiKey
from moderation.db.content import Content
from moderation.db.customer_user import CustomerContentCreatorUser
from moderation.db.moderation import ModerationAction
from moderation.db.session import get_db
from moderation.db.user import User
from moderation.jwt.jwt_handler import JwtTokenHandler
from moderation.service.auth import AuthService

fake = Faker()


def generate_fake_api_key():
    return str(uuid.uuid4())


def generate_hash_password(password):
    return AuthService.hash_password(password)


def generate_analysis_metadata(content_type):
    """
    Generate structured metadata based on the content type.
    """
    if content_type in ["text", "document/text"]:
        return {
            "toxicity": round(random.uniform(0.2, 0.95), 3),
            "severe_toxicity": round(random.uniform(0.0, 0.1), 3),
            "obscenity": round(random.uniform(0.1, 0.5), 3),
            "threat": round(random.uniform(0.0, 0.1), 3),
            "insult": round(random.uniform(0.5, 0.9), 3),
            "identity_hate": round(random.uniform(0.0, 0.1), 3),
        }
    elif content_type == "image":
        nsfw = round(random.uniform(0.2, 0.95), 3)
        normal = round(1.0 - nsfw, 3)
        return {
            "nsfw": nsfw,
            "normal": normal,
        }
    elif content_type in ["text/pii", "document/pii"]:
        # Define possible PII entity types
        pii_entity_types = ["URL", "EMAIL", "CREDIT_CARD", "PERSON", "LOCATION", "PASSWORD", "SSN"]

        # Randomly decide how many PII entities to include (0 to len(pii_entity_types))
        num_pii_entities = random.randint(0, 40)

        # Randomly select PII entity types and generate their metadata
        pii_entities = [
            {
                "start": random.randint(0, 100),
                "end": random.randint(101, 200),
                "entity_type": random.choice(pii_entity_types),
                "score": round(random.uniform(0.2, 0.95), 3),
            }
            for _ in range(num_pii_entities)
        ]

        return {
            "results": pii_entities,
        }
    elif content_type in ["document/url", "text/url"]:
        return {
            "results": [
                {
                    "url": "http://allegro.pl-bilety-sprzedaz-resale.icu",
                    "safe": False,
                    "details": [
                        {
                            "threatType": "SOCIAL_ENGINEERING",
                            "platformType": "ANY_PLATFORM",
                            "threat": {"url": "http://allegro.pl-bilety-sprzedaz-resale.icu"},
                            "cacheDuration": "300s",
                            "threatEntryType": "URL",
                        }
                    ],
                }
            ]
        }

    else:
        return {}


def load_fixtures():
    with get_db() as db:
        # Delete child tables first due to foreign keys
        db.query(ContentAnalysis).delete(synchronize_session=False)
        db.query(ModerationAction).delete(synchronize_session=False)
        db.query(Content).delete(synchronize_session=False)
        db.query(CustomerContentCreatorUser).delete(synchronize_session=False)
        db.query(ClientApiKey).delete(synchronize_session=False)
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
            password_hash=generate_hash_password(admin_password),  # NOTE: hash in prod
            role="admin",
        )
        primary_moderator = User(
            id=uuid.uuid4(),
            username="moderator",
            email="moderator@example.com",
            password_hash=generate_hash_password(moderator_password),
            role="moderator",
        )
        handler = JwtTokenHandler()
        admin_jwt = handler.generate_token(
            user_id=str(admin.id), scopes=["admin", "moderator"], expires_in_minutes=3600
        )
        moderator_jwt = handler.generate_token(
            user_id=str(primary_moderator.id), scopes=["moderator"], expires_in_minutes=3600
        )

        print(f"🔐 Admin 'admin' admin@example.com:{admin_password}:{admin_jwt}")
        print(f"🔐 Moderator 'moderator' moderator@example.com:{moderator_password}:{moderator_jwt}")

        # Add admin and primary moderator to the database
        db.add_all([admin, primary_moderator])
        db.flush()  # Flush to get persisted IDs

        # Collect IDs of moderators
        moderator_ids = [primary_moderator.id]

        # Generate 30 additional moderators
        moderators = []
        for _ in range(30):
            moderator_name = fake.user_name()
            moderator_email = fake.email()
            moderator = User(
                id=uuid.uuid4(),
                username=moderator_name,
                email=moderator_email,
                password_hash=generate_hash_password(moderator_password),  # All moderators share the same password
                role="moderator",
            )
            moderators.append(moderator)
            moderator_ids.append(moderator.id)  # Collect the ID

        # Add all moderators to the database
        db.add_all(moderators)
        db.commit()

        # Select 3/4 of the moderators for moderation actions
        selected_moderator_ids = random.sample(moderator_ids, k=(len(moderator_ids) * 3) // 4)

        contents = []
        analyses = []
        sources = [fake.url() for _ in range(30)]
        status_count = defaultdict(int)

        for _ in range(5000):
            content_id = uuid.uuid4()
            content_created_at = fake.date_time_this_month()
            status = random.choice(["pending", "approved", "rejected", "flagged"])
            status_count[status] += 1
            content = Content(
                id=content_id,
                user_id=uuid.uuid4(),
                username=fake.user_name(),
                title=fake.sentence(),
                body=fake.paragraph(nb_sentences=20),
                tags=[fake.word() for _ in range(3)],
                localization={"lang": "en", "region": "US"},
                source=random.choice(sources),
                status=status,
                image_paths=["/uploads/" + fake.file_name(extension="jpg")],
                created_at=content_created_at,
            )
            contents.append(content)

            # Generate analyses for different content types
            for content_type in [
                "text",
                "image",
                "document/text",
                "text/pii",
                "document/pii",
                "document/url",
                "text/url",
            ]:
                analysis = ContentAnalysis(
                    id=uuid.uuid4(),
                    content_id=content_id,
                    content_type=content_type,
                    automated_flag=random.choice([True, False]),
                    automated_flag_reason="auto_flag" if random.random() > 0.5 else None,
                    model_version="v1.0.1",
                    analysis_metadata=generate_analysis_metadata(content_type),
                    analyzed_at=content_created_at,
                )
                analyses.append(analysis)

        print(f"Created contents: {len(contents)}")
        print(f"Content statuses: {str(status_count)}")

        db.add_all(contents)
        db.flush()
        db.add_all(analyses)
        db.commit()

        # Create moderation actions for half of the content
        moderation_actions = []
        half_content = random.sample(contents, k=len(contents) // 2)  # Select half of the content
        for content in half_content:
            moderator_id = random.choice(selected_moderator_ids)  # Randomly assign a moderator
            action = random.choice(["approve", "reject", "flagged"])  # Randomly choose an action
            reason = fake.sentence()  # Generate a random reason

            random_time_offset = timedelta(
                days=random.randint(0, 7), hours=random.randint(0, 23), minutes=random.randint(0, 59)
            )
            moderation_action = ModerationAction(
                id=uuid.uuid4(),
                content_id=content.id,
                moderator_id=moderator_id,
                action=action,
                reason=reason,
                created_at=content.created_at + random_time_offset,
            )
            moderation_actions.append(moderation_action)

        # Add all moderation actions to the database
        db.add_all(moderation_actions)
        db.commit()

        frontend_id = "10000"
        frontend_api_key = os.getenv("FRONTEND_API_KEY")
        api_key_frontend = ClientApiKey(
            client_id=frontend_id,
            source="frontend",
            api_key=frontend_api_key,
            current_scope=["create_content", "delete_content", "read_content", "edit_content"],
            access_count=0,
            is_active=True,
        )

        # Create API keys
        client_id_1 = "123"
        client_id_2 = "456"

        api_key_1 = ClientApiKey(
            client_id=client_id_1,
            source=fake.url(),
            api_key=fake.password(length=32),
            current_scope=["create_content"],
            access_count=random.randint(3, 10000),
            is_active=True,
        )

        api_key_2 = ClientApiKey(
            client_id=client_id_2,
            source=fake.url(),
            api_key=fake.password(length=32),
            current_scope=["create_content"],
            access_count=random.randint(30, 10000),
            is_active=False,
        )

        # Print the created API keys
        print(f"🔐 Created frontend API key: {frontend_api_key}")
        print(f"🔐 Created API key 1: client_id: {client_id_1}, api_key: {api_key_1.api_key} -> Active")
        print(f"🔐 Created API key 2: client_id: {client_id_2}, api_key: {api_key_2.api_key} -> Deactivated")

        # Add both API keys to the database
        db.add(api_key_1)
        db.add(api_key_2)
        db.add(api_key_frontend)
        db.commit()

        # Create 20 API keys
        api_keys = []
        for _ in range(200):
            api_key = ClientApiKey(
                client_id=str(uuid.uuid4()),  # Generate a unique client ID for each key
                source=random.choice(sources),  # Randomly select one of the 4 sources
                api_key=fake.password(length=32),  # Generate a random API key
                current_scope=random.choice([["create_content"], ["read_content"]]),
                access_count=random.randint(100, 30000),  # Random access count
                is_active=random.choice([True, False]),  # Randomly set active or inactive
            )
            api_keys.append(api_key)

        # Add all API keys to the database
        db.add_all(api_keys)
        db.commit()

        print("✅ Fixtures successfully loaded.")


if __name__ == "__main__":
    load_fixtures()
