import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, User
from backend.services.decision_engine import DecisionEngine

class TestDecisionEngine(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

        self.user = User(
            username="copilotuser",
            email="copilot@hydrogrow.ai",
            password_hash="hashedpass"
        )
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)

    def tearDown(self):
        self.db.close()

    def test_evaluate_farm_decisions(self):
        res = DecisionEngine.evaluate_farm_decisions(self.db, self.user.id)
        self.assertIn("farm_health", res)
        self.assertIn("decisions", res)
        self.assertIn("agent_statuses", res)
        self.assertEqual(len(res["agent_statuses"]), 5)

if __name__ == "__main__":
    unittest.main()
