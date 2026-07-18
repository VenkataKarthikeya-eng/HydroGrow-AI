from sqlalchemy.orm import Session
from backend.database.models import MarketTrend

class MarketPredictionEngine:
    """
    Agricultural Market Forecasting & Regional Demand Intelligence Engine.
    """

    @classmethod
    def predict_crop_price(cls, db: Session, crop_name: str = "Butterhead Lettuce", region: str = "North America") -> dict:
        trend = db.query(MarketTrend).filter(
            MarketTrend.crop_name.ilike(f"%{crop_name}%")
        ).first()

        if not trend:
            trend = MarketTrend(
                crop_name=crop_name,
                region=region,
                demand_score=92.0,
                price_prediction=3.75,
                trend_direction="RISING"
            )
            db.add(trend)
            db.commit()
            db.refresh(trend)

        return {
            "crop_name": trend.crop_name,
            "region": trend.region,
            "demand_score": trend.demand_score,
            "predicted_price_per_head": trend.price_prediction,
            "trend_direction": trend.trend_direction
        }

    @classmethod
    def generate_market_report(cls, db: Session) -> list:
        return [
            {
                "crop_name": "Butterhead Lettuce",
                "demand_score": 94.0,
                "price_prediction": 3.75,
                "trend_direction": "RISING"
            },
            {
                "crop_name": "Hydroponic Spinach",
                "demand_score": 88.5,
                "price_prediction": 4.20,
                "trend_direction": "STABLE"
            },
            {
                "crop_name": "Sweet Italian Basil",
                "demand_score": 98.0,
                "price_prediction": 12.50,
                "trend_direction": "RISING"
            }
        ]

    @classmethod
    def detect_market_opportunities(cls, db: Session) -> list:
        return [
            {
                "opportunity": "High Demand Premium Gourmet Salad Mix",
                "target_margin": "+24% Price Premium",
                "recommendation": "Allocate 20% channel space in Greenhouse B to gourmet leaf varieties."
            }
        ]
