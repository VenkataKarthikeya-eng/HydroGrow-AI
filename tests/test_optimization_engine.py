import unittest
import os
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.services.automation.optimization_engine import OptimizationEngine

class TestOptimizationEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()

        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="optenginegrower",
            email="optengine@example.com",
            password="growerpassword"
        )
        cls.user = crud.create_user(cls.db, user=user_schema, password_hash="hashed")
        cls.db.commit()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("test_hydrogrow.db"):
            try:
                os.remove("test_hydrogrow.db")
            except Exception:
                pass

    def test_optimization_recommendations(self):
        recs = OptimizationEngine.generate_recommendations(self.db, self.user.id)
        self.assertIn("yield_improvement", recs)
        self.assertIn("nutrient_optimization", recs)
        self.assertIn("water_saving", recs)
