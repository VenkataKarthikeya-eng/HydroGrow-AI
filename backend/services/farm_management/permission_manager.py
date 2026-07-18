from sqlalchemy.orm import Session
from backend.database.models import FarmMember

class PermissionManager:
    """
    Role-Based Access Control (RBAC) Permission Verifier.
    Roles: OWNER, MANAGER, WORKER, VIEWER.
    """

    ROLE_HIERARCHY = {
        "OWNER": 4,
        "MANAGER": 3,
        "WORKER": 2,
        "VIEWER": 1
    }

    @classmethod
    def get_user_role(cls, db: Session, farm_id: int, user_id: int) -> str:
        member = db.query(FarmMember).filter(
            FarmMember.farm_id == farm_id,
            FarmMember.user_id == user_id
        ).first()
        return member.role if member else None

    @classmethod
    def has_permission(cls, db: Session, farm_id: int, user_id: int, required_role: str) -> bool:
        user_role = cls.get_user_role(db, farm_id, user_id)
        if not user_role:
            return False
        
        user_level = cls.ROLE_HIERARCHY.get(user_role.upper(), 0)
        req_level = cls.ROLE_HIERARCHY.get(required_role.upper(), 1)
        return user_level >= req_level
