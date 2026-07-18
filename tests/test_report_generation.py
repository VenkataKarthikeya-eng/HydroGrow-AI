import unittest
import os
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.services.analytics.farm_report_generator import FarmReportGenerator

class TestFarmReportGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()
        
        # Clear database to isolate test states
        cls.db.query(models.Prediction).delete()
        cls.db.query(models.Message).delete()
        cls.db.query(models.Conversation).delete()
        cls.db.query(models.User).delete()
        cls.db.commit()

        # Create user
        user_schema = schemas.UserCreate(
            username="reportgrower",
            email="reportgrower@example.com",
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

    def test_report_empty_state(self):
        report = FarmReportGenerator.generate_farm_report(self.db, self.user.id)
        self.assertIn("No harvest cycles recorded", report)
        self.assertIn("Recommendation", report)

    def test_report_populated_state(self):
        crud.create_prediction(
            db=self.db,
            user_id=self.user.id,
            input_parameters={"water_ph": 6.0, "water_ec": 4.5, "air_temperature": 22.0},
            predicted_weight=240.0,
            growth_category="Poor",
            recommendations=[
                {"parameter": "Water EC", "status": "Critical", "action": "Flush solution."}
            ]
        )
        self.db.commit()

        report = FarmReportGenerator.generate_farm_report(self.db, self.user.id)
        self.assertIn("Analysis", report)
        self.assertIn("Evidence", report)
        self.assertIn("Recommendation", report)
        self.assertIn("EC", report)
