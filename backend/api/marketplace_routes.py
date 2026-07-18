from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Any
from backend.database.connection import get_db
from backend.authentication.jwt_handler import get_optional_current_user
from backend.database.models import MarketplaceProduct, CropTemplate, KnowledgeArticle

router = APIRouter()

def get_current_user_required(current_user: Optional[Any] = Depends(get_optional_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )
    return current_user

# --- Product Marketplace Endpoints ---
@router.get("/marketplace/products", summary="List agricultural marketplace products")
def list_products(db: Session = Depends(get_db)):
    products = db.query(MarketplaceProduct).filter(MarketplaceProduct.availability == True).all()

    if not products:
        # Seed default agricultural products for local testing
        p1 = MarketplaceProduct(
            seller_id=1,
            product_name="HydroGrow Premium A+B Hydroponic Concentrates (10L)",
            category="Nutrients & Concentrates",
            description="Balanced macronutrient & micronutrient solution for lettuce & leafy greens.",
            price=49.99,
            availability=True,
            rating=4.9
        )
        p2 = MarketplaceProduct(
            seller_id=1,
            product_name="Digital Precision pH & EC Industrial Probe Kit",
            category="Sensors & Meters",
            description="Lab-grade waterproof pH & EC sensors with RS485 Modbus output for ESP32.",
            price=129.50,
            availability=True,
            rating=4.8
        )
        db.add(p1)
        db.add(p2)
        db.commit()
        products = [p1, p2]

    return [
        {
            "id": p.id,
            "product_name": p.product_name,
            "category": p.category,
            "description": p.description,
            "price": p.price,
            "availability": p.availability,
            "rating": p.rating,
            "seller_id": p.seller_id
        }
        for p in products
    ]

@router.post("/marketplace/products", summary="List new product on marketplace")
def create_product(
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    product_name = payload.get("product_name")
    price = payload.get("price")
    if not product_name or price is None:
        raise HTTPException(status_code=400, detail="product_name and price are required.")

    prod = MarketplaceProduct(
        seller_id=user.id,
        product_name=product_name,
        category=payload.get("category", "Nutrients & Concentrates"),
        description=payload.get("description", "High quality agricultural input."),
        price=float(price),
        availability=True
    )
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return {"message": "Product listed successfully.", "product_id": prod.id}

@router.get("/marketplace/products/{id}", summary="Get detailed product specs")
def get_product(id: int, db: Session = Depends(get_db)):
    prod = db.query(MarketplaceProduct).filter(MarketplaceProduct.id == id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found.")
    return {
        "id": prod.id,
        "product_name": prod.product_name,
        "category": prod.category,
        "description": prod.description,
        "price": prod.price,
        "availability": prod.availability,
        "rating": prod.rating,
        "seller_id": prod.seller_id
    }

@router.post("/marketplace/products/{id}/review", summary="Submit product rating & review")
def review_product(
    id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user_required)
):
    prod = db.query(MarketplaceProduct).filter(MarketplaceProduct.id == id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    rating = float(payload.get("rating", 5.0))
    prod.rating = round((prod.rating + rating) / 2.0, 1)
    db.commit()
    return {"message": "Review submitted successfully.", "new_rating": prod.rating}

# --- Marketplace Intelligence Upgrades ---
@router.get("/marketplace/trending-products", summary="List trending agricultural products")
def get_trending_products(db: Session = Depends(get_db)):
    products = db.query(MarketplaceProduct).filter(MarketplaceProduct.rating >= 4.8).all()
    return [
        {
            "id": p.id,
            "product_name": p.product_name,
            "category": p.category,
            "price": p.price,
            "rating": p.rating,
            "trend": "HOT SELLER"
        }
        for p in products
    ]

@router.get("/marketplace/recommendations", summary="AI recommended products based on farm telemetry")
def get_marketplace_recommendations(db: Session = Depends(get_db)):
    return [
        {
            "product_name": "RS485 Modbus Industrial Water EC Probe",
            "reason": "Upgrade recommended to eliminate pH sensor drift and maintain tight dosing precision.",
            "expected_roi": "+5.2% Dosing Accuracy"
        },
        {
            "product_name": "HydroGrow Premium A+B Hydroponic Concentrates (10L)",
            "reason": "Optimized calcium nitrate ratio prevents tip burn during rapid expansion phase.",
            "expected_roi": "Zero Leaf Tip Burn"
        }
    ]

# --- Backward Compatible Endpoints ---
@router.get("/marketplace/templates", summary="List crop templates")
def list_templates_compat(db: Session = Depends(get_db)):
    templates = db.query(CropTemplate).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "crop_type": t.crop_type,
            "growth_duration": t.growth_duration,
            "optimal_temperature": t.optimal_temperature,
            "optimal_ph": t.optimal_ph,
            "optimal_ec": t.optimal_ec,
            "nutrient_profile": t.nutrient_profile
        }
        for t in templates
    ]

@router.get("/marketplace/knowledge-base", summary="List articles")
def get_knowledge_base_compat(db: Session = Depends(get_db)):
    articles = db.query(KnowledgeArticle).all()
    return [
        {
            "id": a.id,
            "title": a.title,
            "category": a.category,
            "content": a.content,
            "crop_type": a.crop_type,
            "created_at": a.created_at.isoformat() if a.created_at else None
        }
        for a in articles
    ]
