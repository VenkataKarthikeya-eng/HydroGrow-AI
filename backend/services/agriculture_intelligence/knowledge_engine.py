from sqlalchemy.orm import Session
from backend.database.models import KnowledgeArticle

class KnowledgeEngine:
    """
    Global Agriculture Intelligence & Knowledge Retrieval Engine.
    Combines agronomic research database, best practices, and crop guidelines.
    """

    @staticmethod
    def search_crop_knowledge(db: Session, query: str = "", crop_type: str = "Lettuce") -> list:
        articles = db.query(KnowledgeArticle).filter(
            KnowledgeArticle.crop_type.ilike(f"%{crop_type}%")
        ).all()

        if not articles:
            return [
                {
                    "id": 1,
                    "title": "Lettuce NFT Solution Chemistry & EC Ranges",
                    "category": "Nutrition",
                    "content": "Optimal EC for butterhead lettuce ranges from 1.6 to 2.2 mS/cm depending on ambient solar radiation."
                }
            ]

        return [
            {
                "id": a.id,
                "title": a.title,
                "category": a.category,
                "content": a.content,
                "crop_type": a.crop_type
            }
            for a in articles
        ]

    @staticmethod
    def get_best_practices(crop_type: str = "Lettuce") -> dict:
        return {
            "crop_type": crop_type,
            "optimal_temperature_day": "20.0 - 23.0 °C",
            "optimal_temperature_night": "16.0 - 18.0 °C",
            "optimal_ph": "5.8 - 6.4",
            "optimal_ec": "1.6 - 2.2 mS/cm",
            "target_dissolved_oxygen": "8.0 - 10.0 mg/L",
            "photoperiod_hours": "16 - 18 hours/day"
        }

    @classmethod
    def generate_crop_guidelines(cls, crop_type: str = "Lettuce") -> dict:
        bp = cls.get_best_practices(crop_type)
        return {
            "title": f"Enterprise Production Guidelines for {crop_type}",
            "best_practices": bp,
            "key_risks": ["Tip burn during rapid expansion", "Pythium root rot if water temp > 24°C"],
            "preventative_actions": ["Maintain VPD between 0.8 and 1.1 kPa", "Run aeration dissolved oxygen bubblers"]
        }
