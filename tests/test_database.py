import unittest
from sqlalchemy.orm import Session
from backend.database.connection import engine, SessionLocal, Base, get_db
from backend.database import models, schemas, crud

class TestDatabaseLayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create all tables in the temporary in-memory SQLite database
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Drop all tables after testing
        Base.metadata.drop_all(bind=engine)
        import os
        if os.path.exists("test_hydrogrow.db"):
            try:
                os.remove("test_hydrogrow.db")
            except Exception:
                pass

    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_database_connection(self):
        # Verify db session can be created and queried
        self.assertIsInstance(self.db, Session)

    def test_user_creation_and_retrieval(self):
        user_schema = schemas.UserCreate(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        # Create user
        db_user = crud.create_user(self.db, user=user_schema, password_hash="hashed_password_val")
        self.assertIsNotNone(db_user.id)
        self.assertEqual(db_user.username, "testuser")
        self.assertEqual(db_user.email, "testuser@example.com")
        self.assertEqual(db_user.password_hash, "hashed_password_val")

        # Retrieve user
        retrieved_user = crud.get_user(self.db, user_id=db_user.id)
        self.assertEqual(retrieved_user.username, "testuser")

        # Retrieve by username
        retrieved_by_uname = crud.get_user_by_username(self.db, username="testuser")
        self.assertEqual(retrieved_by_uname.id, db_user.id)

        # Retrieve by email
        retrieved_by_email = crud.get_user_by_email(self.db, email="testuser@example.com")
        self.assertEqual(retrieved_by_email.id, db_user.id)

    def test_prediction_creation_and_history(self):
        # Create user first for foreign key link
        user_schema = schemas.UserCreate(
            username="preduser",
            email="preduser@example.com",
            password="testpassword"
        )
        db_user = crud.create_user(self.db, user=user_schema, password_hash="hashed_pwd")
        
        input_params = {
            "air_temperature": 22.0,
            "humidity": 60.0,
            "co2": 450.0,
            "water_ph": 6.2,
            "water_ec": 2.0,
            "water_temperature": 23.0,
            "nutrient_solution": 400.0,
            "water_consumption": 170.0,
            "seedling_height": 12.0,
            "seedling_weight": 4.0,
            "root_length": 7.0
        }
        recommendations = [{"parameter": "pH", "status": "Optimal", "action": "Maintain"}]
        explanation = {"summary": "Optimal conditions"}

        db_pred = crud.create_prediction(
            db=self.db,
            user_id=db_user.id,
            input_parameters=input_params,
            predicted_weight=350.5,
            growth_category="Excellent",
            recommendations=recommendations,
            explanation=explanation
        )

        self.assertIsNotNone(db_pred.id)
        self.assertEqual(db_pred.user_id, db_user.id)
        self.assertEqual(db_pred.predicted_weight, 350.5)
        self.assertEqual(db_pred.growth_category, "Excellent")
        self.assertEqual(db_pred.input_parameters["co2"], 450.0)

        # Query history
        history = crud.get_predictions_by_user_id(self.db, user_id=db_user.id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].id, db_pred.id)
