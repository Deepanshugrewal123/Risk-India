from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from app.models.disaster_event import DisasterEvent
from app.models.location import Location
from app.services.disaster_provider import disaster_feed_manager, NormalizedDisasterEvent

class DisasterService:
    @staticmethod
    def get_disasters(
        db: Optional[Session] = None,
        state: Optional[str] = None,
        disaster_type: Optional[str] = None,
        status: Optional[str] = None,
        freshness: Optional[str] = None,
        live_only: bool = False
    ) -> List[Dict[str, Any]]:
        # Retrieve events from provider feed manager
        events = disaster_feed_manager.get_events(
            state=state,
            hazard_type=disaster_type,
            status=status,
            freshness=freshness,
            live_only=live_only
        )
        
        output = [e.to_dict() for e in events]

        # If not strictly live_only and DB is provided, merge any persistent DB records
        if not live_only and db is not None:
            try:
                db_query = db.query(DisasterEvent)
                if state:
                    s_clean = state.lower().strip()
                    db_query = db_query.join(Location).filter(
                        (Location.id == s_clean) |
                        (Location.name.ilike(f"%{s_clean}%")) |
                        (Location.state_code == s_clean.upper())
                    )
                if disaster_type:
                    db_query = db_query.filter(DisasterEvent.disaster_type.ilike(f"%{disaster_type.strip()}%"))
                if status:
                    db_query = db_query.filter(DisasterEvent.status.ilike(f"%{status.strip()}%"))

                existing_ids = {e["id"] for e in output}
                for row in db_query.all():
                    if row.id not in existing_ids:
                        output.append({
                            "id": row.id,
                            "hazard_type": row.disaster_type,
                            "disaster_type": row.disaster_type,
                            "title": row.title,
                            "state": row.location.name if row.location else "Regional",
                            "district": "Monitored Zone",
                            "location": row.location.name if row.location else "India",
                            "latitude": row.location.latitude if row.location else 20.0,
                            "longitude": row.location.longitude if row.location else 78.0,
                            "coordinates": [
                                row.location.latitude if row.location else 20.0,
                                row.location.longitude if row.location else 78.0
                            ],
                            "severity": row.severity,
                            "status": row.status,
                            "description": row.description,
                            "source": row.source,
                            "source_url": row.source_url,
                            "verified": False,
                            "is_demo": row.is_demo,
                            "observed_at": row.started_at.isoformat() if row.started_at else None,
                            "retrieved_at": row.created_at.isoformat() if row.created_at else None,
                            "freshness": "STALE",
                            "risk_score": 70
                        })
            except Exception:
                pass

        return output

    @staticmethod
    def get_live_disasters(
        state: Optional[str] = None,
        disaster_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        events = disaster_feed_manager.get_live_events(state=state, hazard_type=disaster_type)
        return [e.to_dict() for e in events]

    @staticmethod
    def get_disaster_by_id(db: Optional[Session], disaster_id: str) -> Optional[Dict[str, Any]]:
        ev = disaster_feed_manager.get_event_by_id(disaster_id)
        if ev:
            return ev.to_dict()

        if db is not None:
            try:
                row = db.query(DisasterEvent).filter(DisasterEvent.id == disaster_id).first()
                if row:
                    return {
                        "id": row.id,
                        "hazard_type": row.disaster_type,
                        "disaster_type": row.disaster_type,
                        "title": row.title,
                        "state": row.location.name if row.location else "Regional",
                        "district": "Monitored Zone",
                        "location": row.location.name if row.location else "India",
                        "latitude": row.location.latitude if row.location else 20.0,
                        "longitude": row.location.longitude if row.location else 78.0,
                        "coordinates": [
                            row.location.latitude if row.location else 20.0,
                            row.location.longitude if row.location else 78.0
                        ],
                        "severity": row.severity,
                        "status": row.status,
                        "description": row.description,
                        "source": row.source,
                        "source_url": row.source_url,
                        "verified": False,
                        "is_demo": row.is_demo,
                        "observed_at": row.started_at.isoformat() if row.started_at else None,
                        "retrieved_at": row.created_at.isoformat() if row.created_at else None,
                        "freshness": "STALE",
                        "risk_score": 70
                    }
            except Exception:
                pass

        return None

    @staticmethod
    def refresh() -> Dict[str, Any]:
        return disaster_feed_manager.refresh(force=True)

disaster_service = DisasterService()
