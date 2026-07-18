from sqlalchemy.orm import Session
from backend.database.models import Farm, FarmMember, FarmSubscription, Greenhouse

class FarmManager:
    """
    Multi-Farm SaaS Tenant Manager.
    Handles multi-farm lifecycle, user data isolation, and default farm provisioning.
    """

    @classmethod
    def create_farm(
        cls, 
        db: Session, 
        owner_id: int, 
        farm_name: str, 
        location: str = "Main Hydroponic Site",
        farm_size: float = 100.0,
        farm_type: str = "Hydroponic NFT",
        description: str = None
    ) -> Farm:
        # 1. Create Farm object
        farm = Farm(
            owner_id=owner_id,
            farm_name=farm_name,
            location=location,
            farm_size=farm_size,
            farm_type=farm_type,
            description=description
        )
        db.add(farm)
        db.commit()
        db.refresh(farm)

        # 2. Add owner as FarmMember with OWNER role
        member = FarmMember(
            farm_id=farm.id,
            user_id=owner_id,
            role="OWNER"
        )
        db.add(member)

        # 3. Initialize Subscription tier (Default FREE)
        sub = FarmSubscription(
            farm_id=farm.id,
            plan="FREE",
            max_devices=3,
            max_users=2
        )
        db.add(sub)

        # 4. Provision default Greenhouse
        gh = Greenhouse(
            farm_id=farm.id,
            name="Greenhouse A",
            area_size=farm_size * 0.5,
            environment_type=farm_type
        )
        db.add(gh)

        db.commit()
        db.refresh(farm)
        return farm

    @classmethod
    def get_user_farms(cls, db: Session, user_id: int) -> list:
        # Returns all farms where user is either owner or member
        member_farm_ids = db.query(FarmMember.farm_id).filter(FarmMember.user_id == user_id).all()
        farm_ids = [f[0] for f in member_farm_ids]
        
        farms = db.query(Farm).filter(Farm.id.in_(farm_ids)).all() if farm_ids else []

        # Auto-provision default farm if existing user has no farms
        if not farms:
            default_farm = cls.create_farm(db, owner_id=user_id, farm_name="My Smart Farm")
            farms = [default_farm]

        return farms

    @classmethod
    def get_farm_by_id(cls, db: Session, farm_id: int, user_id: int) -> Farm:
        member = db.query(FarmMember).filter(
            FarmMember.farm_id == farm_id,
            FarmMember.user_id == user_id
        ).first()
        if not member:
            return None
        return db.query(Farm).filter(Farm.id == farm_id).first()

    @classmethod
    def update_farm(cls, db: Session, farm_id: int, user_id: int, updates: dict) -> Farm:
        farm = cls.get_farm_by_id(db, farm_id, user_id)
        if not farm:
            return None
        for key, val in updates.items():
            if hasattr(farm, key) and val is not None:
                setattr(farm, key, val)
        db.commit()
        db.refresh(farm)
        return farm

    @classmethod
    def delete_farm(cls, db: Session, farm_id: int, user_id: int) -> bool:
        farm = db.query(Farm).filter(Farm.id == farm_id, Farm.owner_id == user_id).first()
        if not farm:
            return False
        db.delete(farm)
        db.commit()
        return True
