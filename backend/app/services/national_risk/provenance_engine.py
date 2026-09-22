"""
RISK // INDIA — National Provenance Engine
=========================================
Tracks verifiable official source attribution, URLs, observation timestamps,
and fallback statuses for every disaster intelligence datum.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timezone


@dataclass
class ProvenanceRecord:
    provider: str
    source_type: str
    source_record_id: Optional[str]
    observation_timestamp: Optional[str]
    retrieval_timestamp: str
    freshness: str
    fallback_status: str
    source_url: Optional[str] = None
    data_license: str = "Government Open Data / Public Disaster Bulletin"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ProvenanceEngine:
    """Builds and validates provenance chains for official alerts, baselines, and models."""

    PROVIDER_URLS = {
        "CWC": "https://ffs.india-water.gov.in",
        "IMD": "https://mausam.imd.gov.in",
        "USGS": "https://earthquake.usgs.gov",
        "GSI": "https://bhukosh.gsi.gov.in",
        "NDMA": "https://ndma.gov.in",
        "NRSC": "https://bhuvan.nrsc.gov.in",
        "ASDMA": "https://asdma.assam.gov.in"
    }

    def build_provenance(
        self,
        provider: str,
        source_type: str,
        source_record_id: Optional[str],
        observation_timestamp: Optional[str],
        freshness: str,
        fallback_status: str = "OFFICIAL_PRIMARY",
        source_url: Optional[str] = None
    ) -> ProvenanceRecord:
        """Constructs a verifiable provenance record."""
        now_str = datetime.now(timezone.utc).isoformat()
        resolved_url = source_url or self.PROVIDER_URLS.get(provider.upper(), "https://ndma.gov.in")

        return ProvenanceRecord(
            provider=provider,
            source_type=source_type,
            source_record_id=source_record_id,
            observation_timestamp=observation_timestamp,
            retrieval_timestamp=now_str,
            freshness=freshness,
            fallback_status=fallback_status,
            source_url=resolved_url
        )


provenance_engine = ProvenanceEngine()
