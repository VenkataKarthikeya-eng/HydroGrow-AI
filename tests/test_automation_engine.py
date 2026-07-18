import unittest
import os
from backend.database.connection import engine, Base, SessionLocal
from backend.database import crud, schemas, models
from backend.services.automation.automation_engine import AutomationEngine

class TestAutomationEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.db = SessionLocal()

        cls.db.query(models.User).delete()
        cls.db.commit()

        user_schema = schemas.UserCreate(
            username="autoenginegrower",
            email="autoengine@example.com",
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

    def setUp(self):
        self.db.query(models.AutomationEvent).delete()
        self.db.query(models.AutomationRule).delete()
        self.db.commit()

    def test_evaluate_condition(self):
        self.assertTrue(AutomationEngine.evaluate_condition(25.0, "above", 20.0))
        self.assertFalse(AutomationEngine.evaluate_condition(15.0, "above", 20.0))
        self.assertTrue(AutomationEngine.evaluate_condition(5.4, "below", 5.5))
        self.assertFalse(AutomationEngine.evaluate_condition(6.0, "below", 5.5))

    def test_sensor_triggered_automation(self):
        rule = models.AutomationRule(
            user_id=self.user.id,
            rule_name="Cooling Trigger",
            parameter="temperature",
            condition="above",
            threshold_value=30.0,
            action_type="activate",
            action_value="Cooling Fan",
            enabled=True
        )
        self.db.add(rule)
        self.db.commit()

        events = AutomationEngine.process_sensor_update(self.db, self.user.id, 1, {"temperature": 25.0})
        self.assertEqual(len(events), 0)

        events = AutomationEngine.process_sensor_update(self.db, self.user.id, 1, {"temperature": 32.5})
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["device"], "Cooling Fan")
        self.assertEqual(events[0]["status"], "activated")

        db_events = self.db.query(models.AutomationEvent).filter(models.AutomationEvent.user_id == self.user.id).all()
        self.assertEqual(len(db_events), 1)
        self.assertEqual(db_events[0].rule_id, rule.id)
