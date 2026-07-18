from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import FarmerCommunity, CommunityPost, User

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

@router.get("/community/groups", summary="List farmer community discussion groups")
def list_community_groups(db: Session = Depends(get_db)):
    groups = db.query(FarmerCommunity).all()

    if not groups:
        # Seed default farmer groups
        g1 = FarmerCommunity(
            title="Commercial Hydroponic Lettuce Growers Network",
            description="Discussion group for large scale NFT & DWC lettuce growers.",
            category="NFT Hydroponics",
            created_by=1
        )
        g2 = FarmerCommunity(
            title="Indoor Vertical Farming & Lighting Automation",
            description="Best practices for LED spectrums, DLI, and climate control.",
            category="Vertical Farming",
            created_by=1
        )
        db.add(g1)
        db.add(g2)
        db.commit()
        groups = [g1, g2]

    return [
        {
            "id": g.id,
            "title": g.title,
            "description": g.description,
            "category": g.category,
            "created_by": g.created_by,
            "posts_count": len(g.posts) if g.posts else 0,
            "created_at": g.created_at.isoformat() if g.created_at else None
        }
        for g in groups
    ]

@router.post("/community/create", summary="Create new farmer discussion community")
def create_community_group(
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    title = payload.get("title")
    description = payload.get("description")
    if not title or not description:
        raise HTTPException(status_code=400, detail="title and description are required.")

    group = FarmerCommunity(
        farm_id=payload.get("farm_id"),
        title=title,
        description=description,
        category=payload.get("category", "General Farming"),
        created_by=user.id
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return {"message": "Community group created successfully.", "group_id": group.id}

@router.get("/community/{id}/posts", summary="List posts in a community group")
def list_community_posts(id: int, db: Session = Depends(get_db)):
    posts = db.query(CommunityPost).filter(CommunityPost.community_id == id).all()

    if not posts:
        # Seed default discussion post
        p1 = CommunityPost(
            community_id=id,
            user_id=1,
            content="Has anyone noticed Pythium resistance at 22°C reservoir water temperature in NFT channels?",
            likes=5
        )
        db.add(p1)
        db.commit()
        posts = [p1]

    return [
        {
            "id": p.id,
            "community_id": p.community_id,
            "user_id": p.user_id,
            "username": p.user.username if p.user else "Farmer",
            "content": p.content,
            "image_url": p.image_url,
            "likes": p.likes,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in posts
    ]

@router.post("/community/{id}/post", summary="Publish post to community group")
def create_community_post(
    id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    content = payload.get("content")
    if not content:
        raise HTTPException(status_code=400, detail="content is required.")

    post = CommunityPost(
        community_id=id,
        user_id=user.id,
        content=content,
        image_url=payload.get("image_url")
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message": "Post published successfully.", "post_id": post.id}

@router.post("/community/{id}/like", summary="Like a community post")
def like_post(
    id: int,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    post = db.query(CommunityPost).filter(CommunityPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    post.likes += 1
    db.commit()
    return {"message": "Post liked.", "likes": post.likes}
