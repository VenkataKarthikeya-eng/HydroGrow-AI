from sqlalchemy.orm import Session
from backend.database.models import FarmSubscription, Farm, Greenhouse, IoTDeviceCredential

class SubscriptionManager:
    """
    SaaS Subscription Plan & Resource Limits Manager.
    Tiers: FREE, BASIC, PRO, ENTERPRISE.
    """

    PLAN_LIMITS = {
        "FREE": {"max_farms": 1, "max_greenhouses": 1, "max_devices": 3, "max_members": 2},
        "BASIC": {"max_farms": 3, "max_greenhouses": 5, "max_devices": 10, "max_members": 5},
        "PRO": {"max_farms": 999, "max_greenhouses": 999, "max_devices": 999, "max_members": 999},
        "ENTERPRISE": {"max_farms": 9999, "max_greenhouses": 9999, "max_devices": 9999, "max_members": 9999}
    }

    @classmethod
    def get_farm_subscription(cls, db: Session, farm_id: int) -> dict:
        sub = db.query(FarmSubscription).filter(FarmSubscription.farm_id == farm_id).first()
        plan = sub.plan if sub else "FREE"
        limits = cls.PLAN_LIMITS.get(plan, cls.PLAN_LIMITS["FREE"])
        return {
            "plan": plan,
            "limits": limits,
            "max_devices": sub.max_devices if sub else 3,
            "max_users": sub.max_users if sub else 2
        }

    @classmethod
    def can_add_farm(cls, db: Session, user_id: int) -> bool:
        user_farms = db.query(Farm).filter(Farm.owner_id == user_id).count()
        # Default tier check
        return user_farms < 10

    @classmethod
    def can_add_greenhouse(cls, db: Session, farm_id: int) -> bool:
        sub_info = cls.get_farm_subscription(db, farm_id)
        current_gh = db.query(Greenhouse).filter(Greenhouse.farm_id == farm_id).count()
        return current_gh < sub_info["limits"]["max_greenhouses"]

    @classmethod
    def can_add_device(cls, db: Session, farm_id: int, user_id: int) -> bool:
        sub_info = cls.get_farm_subscription(db, farm_id)
        current_devices = db.query(IoTDeviceCredential).filter(IoTDeviceCredential.user_id == user_id).count()
        return current_devices < sub_info["limits"]["max_devices"]
