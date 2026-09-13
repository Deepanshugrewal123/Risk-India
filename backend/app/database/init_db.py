from sqlalchemy.orm import Session
import logging
from app.models.location import Location
from app.models.risk_assessment import RiskAssessment
from app.models.risk_factor import RiskFactor
from app.utils.risk_classifier import classify_risk_score

logger = logging.getLogger("db-init")

INITIAL_LOCATIONS = [
  {"id": "andhra-pradesh", "name": "Andhra Pradesh", "administrative_type": "STATE", "state_code": "AP", "capital": "Amaravati", "region": "South India", "latitude": 15.9129, "longitude": 79.7400},
  {"id": "arunachal-pradesh", "name": "Arunachal Pradesh", "administrative_type": "STATE", "state_code": "AR", "capital": "Itanagar", "region": "Northeast India", "latitude": 28.2180, "longitude": 94.7278},
  {"id": "assam", "name": "Assam", "administrative_type": "STATE", "state_code": "AS", "capital": "Dispur", "region": "Northeast India", "latitude": 26.1445, "longitude": 91.7362},
  {"id": "bihar", "name": "Bihar", "administrative_type": "STATE", "state_code": "BR", "capital": "Patna", "region": "East India", "latitude": 25.0961, "longitude": 85.3131},
  {"id": "chhattisgarh", "name": "Chhattisgarh", "administrative_type": "STATE", "state_code": "CG", "capital": "Raipur", "region": "Central India", "latitude": 21.2787, "longitude": 81.8661},
  {"id": "goa", "name": "Goa", "administrative_type": "STATE", "state_code": "GA", "capital": "Panaji", "region": "West India", "latitude": 15.2993, "longitude": 74.1240},
  {"id": "gujarat", "name": "Gujarat", "administrative_type": "STATE", "state_code": "GJ", "capital": "Gandhinagar", "region": "West India", "latitude": 22.2587, "longitude": 71.1924},
  {"id": "haryana", "name": "Haryana", "administrative_type": "STATE", "state_code": "HR", "capital": "Chandigarh", "region": "North India", "latitude": 29.0588, "longitude": 76.0856},
  {"id": "himachal-pradesh", "name": "Himachal Pradesh", "administrative_type": "STATE", "state_code": "HP", "capital": "Shimla", "region": "North India", "latitude": 31.1048, "longitude": 77.1734},
  {"id": "jharkhand", "name": "Jharkhand", "administrative_type": "STATE", "state_code": "JH", "capital": "Ranchi", "region": "East India", "latitude": 23.6102, "longitude": 85.2799},
  {"id": "karnataka", "name": "Karnataka", "administrative_type": "STATE", "state_code": "KA", "capital": "Bengaluru", "region": "South India", "latitude": 15.3173, "longitude": 75.7139},
  {"id": "kerala", "name": "Kerala", "administrative_type": "STATE", "state_code": "KL", "capital": "Thiruvananthapuram", "region": "South India", "latitude": 10.8505, "longitude": 76.2711},
  {"id": "madhya-pradesh", "name": "Madhya Pradesh", "administrative_type": "STATE", "state_code": "MP", "capital": "Bhopal", "region": "Central India", "latitude": 22.9734, "longitude": 78.6569},
  {"id": "maharashtra", "name": "Maharashtra", "administrative_type": "STATE", "state_code": "MH", "capital": "Mumbai", "region": "West India", "latitude": 19.7515, "longitude": 75.7139},
  {"id": "manipur", "name": "Manipur", "administrative_type": "STATE", "state_code": "MN", "capital": "Imphal", "region": "Northeast India", "latitude": 24.6637, "longitude": 93.9063},
  {"id": "meghalaya", "name": "Meghalaya", "administrative_type": "STATE", "state_code": "ML", "capital": "Shillong", "region": "Northeast India", "latitude": 25.4670, "longitude": 91.3662},
  {"id": "mizoram", "name": "Mizoram", "administrative_type": "STATE", "state_code": "MZ", "capital": "Aizawl", "region": "Northeast India", "latitude": 23.1645, "longitude": 92.9376},
  {"id": "nagaland", "name": "Nagaland", "administrative_type": "STATE", "state_code": "NL", "capital": "Kohima", "region": "Northeast India", "latitude": 26.1584, "longitude": 94.5624},
  {"id": "odisha", "name": "Odisha", "administrative_type": "STATE", "state_code": "OD", "capital": "Bhubaneswar", "region": "East India", "latitude": 20.9517, "longitude": 85.0985},
  {"id": "punjab", "name": "Punjab", "administrative_type": "STATE", "state_code": "PB", "capital": "Chandigarh", "region": "North India", "latitude": 31.1471, "longitude": 75.3412},
  {"id": "rajasthan", "name": "Rajasthan", "administrative_type": "STATE", "state_code": "RJ", "capital": "Jaipur", "region": "Northwest India", "latitude": 27.0238, "longitude": 74.2179},
  {"id": "sikkim", "name": "Sikkim", "administrative_type": "STATE", "state_code": "SK", "capital": "Gangtok", "region": "Northeast India", "latitude": 27.5330, "longitude": 88.5122},
  {"id": "tamil-nadu", "name": "Tamil Nadu", "administrative_type": "STATE", "state_code": "TN", "capital": "Chennai", "region": "South India", "latitude": 11.1271, "longitude": 78.6569},
  {"id": "telangana", "name": "Telangana", "administrative_type": "STATE", "state_code": "TS", "capital": "Hyderabad", "region": "South India", "latitude": 18.1124, "longitude": 79.0193},
  {"id": "tripura", "name": "Tripura", "administrative_type": "STATE", "state_code": "TR", "capital": "Agartala", "region": "Northeast India", "latitude": 23.9408, "longitude": 91.9882},
  {"id": "uttar-pradesh", "name": "Uttar Pradesh", "administrative_type": "STATE", "state_code": "UP", "capital": "Lucknow", "region": "North India", "latitude": 26.8467, "longitude": 80.9462},
  {"id": "uttarakhand", "name": "Uttarakhand", "administrative_type": "STATE", "state_code": "UK", "capital": "Dehradun", "region": "North India", "latitude": 30.0668, "longitude": 79.0193},
  {"id": "west-bengal", "name": "West Bengal", "administrative_type": "STATE", "state_code": "WB", "capital": "Kolkata", "region": "East India", "latitude": 22.9868, "longitude": 87.8550},
  {"id": "delhi", "name": "Delhi (NCT)", "administrative_type": "UNION_TERRITORY", "state_code": "DL", "capital": "New Delhi", "region": "North India", "latitude": 28.7041, "longitude": 77.1025},
  {"id": "jammu-kashmir", "name": "Jammu and Kashmir", "administrative_type": "UNION_TERRITORY", "state_code": "JK", "capital": "Srinagar / Jammu", "region": "North India", "latitude": 33.7782, "longitude": 76.5762},
  {"id": "ladakh", "name": "Ladakh", "administrative_type": "UNION_TERRITORY", "state_code": "LA", "capital": "Leh", "region": "North India", "latitude": 34.1526, "longitude": 77.5771},
  {"id": "chandigarh", "name": "Chandigarh", "administrative_type": "UNION_TERRITORY", "state_code": "CH", "capital": "Chandigarh", "region": "North India", "latitude": 30.7333, "longitude": 76.7794},
  {"id": "puducherry", "name": "Puducherry", "administrative_type": "UNION_TERRITORY", "state_code": "PY", "capital": "Pondicherry", "region": "South India", "latitude": 11.9416, "longitude": 79.8083},
  {"id": "andaman-nicobar", "name": "Andaman & Nicobar Islands", "administrative_type": "UNION_TERRITORY", "state_code": "AN", "capital": "Port Blair", "region": "Bay of Bengal", "latitude": 11.7401, "longitude": 92.6586},
  {"id": "dadra-nagar-haveli-daman-diu", "name": "Dadra & Nagar Haveli and Daman & Diu", "administrative_type": "UNION_TERRITORY", "state_code": "DN", "capital": "Daman", "region": "West India", "latitude": 20.4283, "longitude": 72.8397},
  {"id": "lakshadweep", "name": "Lakshadweep", "administrative_type": "UNION_TERRITORY", "state_code": "LD", "capital": "Kavaratti", "region": "Arabian Sea", "latitude": 10.5667, "longitude": 72.6417}
]

def auto_seed_database(db: Session):
    try:
        count = db.query(Location).count()
        if count == 0:
            logger.info("Database contains 0 locations. Auto-seeding 37 Indian States and UTs...")
            for item in INITIAL_LOCATIONS:
                loc = Location(**item)
                db.add(loc)
                db.flush()

                base_score = 75 if "assam" in loc.id else 45
                assessment = RiskAssessment(
                    location_id=loc.id,
                    disaster_type="FLOOD",
                    risk_score=base_score,
                    risk_level=classify_risk_score(base_score),
                    model_version="baseline_v1",
                    assessment_status="BASELINE"
                )
                db.add(assessment)
                db.flush()

                db.add(RiskFactor(
                    assessment_id=assessment.id,
                    factor_name="Monsoon Catchment Saturation",
                    factor_value="Nominal Seasonal Level",
                    importance="Medium",
                    unit="percentile"
                ))
            db.commit()
            logger.info("Auto-seeding complete.")
    except Exception as e:
        logger.error(f"Auto-seed error: {e}")
        db.rollback()
