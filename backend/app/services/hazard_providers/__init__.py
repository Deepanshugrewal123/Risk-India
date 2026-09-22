"""
RISK // INDIA — Multi-Hazard Provider Package
============================================
Exports base classes and modular hazard provider implementations:
- BaseHazardProvider
- USGSSeismicProvider (Earthquake)
- CWCFloodProvider (Flood)
- IMDWeatherProvider (Severe Weather)
- IMDCycloneProvider (Cyclone)
- IMDHeatwaveProvider (Heatwave)
- GSILandslideProvider (Landslide)
"""

from app.services.hazard_providers.base import BaseHazardProvider
from app.services.hazard_providers.usgs_provider import USGSSeismicProvider
from app.services.hazard_providers.cwc_provider import CWCFloodProvider
from app.services.hazard_providers.imd_provider import IMDWeatherProvider
from app.services.hazard_providers.cyclone_provider import IMDCycloneProvider
from app.services.hazard_providers.heatwave_provider import IMDHeatwaveProvider
from app.services.hazard_providers.landslide_provider import GSILandslideProvider

__all__ = [
    "BaseHazardProvider",
    "USGSSeismicProvider",
    "CWCFloodProvider",
    "IMDWeatherProvider",
    "IMDCycloneProvider",
    "IMDHeatwaveProvider",
    "GSILandslideProvider"
]
