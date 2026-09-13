"""
RISK // INDIA — Automated Test Suite: Verified Help Hub & Help Others Completion
Rigorous verification of verified resource directory, multi-parameter filtering,
donation safety, disaster-aware scoping, map markers, and emergency disclaimers.

14 Required Test Conditions:
1. test_01_resource_listing: Resource listing returns verified resources with all required fields
2. test_02_category_filtering: Filtering by category returns matching resources
3. test_03_location_filtering: Filtering by state returns state-specific & pan-india resources
4. test_04_disaster_filtering: Filtering by disaster type returns matching hazard resources
5. test_05_verification_filtering: Filtering by verification status returns only verified entities
6. test_06_verified_source_display: All resources have non-empty source name and official source URL
7. test_07_empty_result: Non-existent query parameters return empty list cleanly
8. test_08_api_failure: get_resource_by_id returns None for non-existent resource ID
9. test_09_invalid_resource: HTTP endpoint returns 404 for invalid resource ID
10. test_10_no_fabricated_fallback: When 0 resources match, no synthetic/demo resources are injected
11. test_11_help_others_flow: Help Others flow directs to official portals, no payment collection
12. test_12_get_help_flow: Get Help hotlines are genuine official government helplines
13. test_13_resource_map_marker: All map markers have valid Indian geographic coordinates
14. test_14_emergency_disclaimer: Critical emergency disclaimers are present and unambiguous
"""

import sys
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.resource_service import resource_service, VERIFIED_RESOURCES_REGISTRY
from backend.app.schemas.resource import ResourceOut


class TestHelpHub(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_resource_listing(self):
        """1. Resource listing returns verified resources with all required fields."""
        resources = resource_service.get_resources()
        self.assertGreaterEqual(len(resources), 10, "Registry should have at least 10 verified resources")
        for res in resources:
            # Validates against Pydantic schema
            model = ResourceOut(**res)
            self.assertTrue(model.id)
            self.assertTrue(model.name)
            self.assertTrue(model.category)
            self.assertTrue(model.source)
            self.assertTrue(model.source_url)
            self.assertEqual(model.verification_status, "VERIFIED")

        # Also verify via HTTP endpoint
        resp = self.client.get("/api/resources")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(len(data), 10)

    def test_02_category_filtering(self):
        """2. Category filtering returns only matching resources."""
        medical_res = resource_service.get_resources(category="Medical Assistance")
        self.assertGreaterEqual(len(medical_res), 1)
        for r in medical_res:
            self.assertEqual(r["category"], "Medical Assistance")

        relief_res = resource_service.get_resources(category="Government Relief")
        self.assertGreaterEqual(len(relief_res), 1)
        for r in relief_res:
            self.assertEqual(r["category"], "Government Relief")

    def test_03_location_filtering(self):
        """3. Location filtering by state returns matching or Pan-India resources."""
        assam_res = resource_service.get_resources(state="Assam")
        self.assertGreaterEqual(len(assam_res), 1)
        for r in assam_res:
            self.assertTrue(r["state"] == "Assam" or r["state"] == "Pan-India" or r.get("location_id") == "assam")

        odisha_res = resource_service.get_resources(state="Odisha")
        self.assertGreaterEqual(len(odisha_res), 1)
        for r in odisha_res:
            self.assertTrue(r["state"] == "Odisha" or r["state"] == "Pan-India" or r.get("location_id") == "odisha")

    def test_04_disaster_filtering(self):
        """4. Disaster type filtering returns matching hazard resources."""
        flood_res = resource_service.get_resources(disaster_type="Flood")
        self.assertGreaterEqual(len(flood_res), 1)
        for r in flood_res:
            self.assertIn(r["disaster_type"].upper(), ["FLOOD", "ALL", "ALL HAZARDS", "CYCLONE / FLOOD", "WATERLOGGING / FLOOD"])

    def test_05_verification_filtering(self):
        """5. Verification filtering returns strictly verified entities."""
        verified_res = resource_service.get_resources(verification_status="VERIFIED")
        for r in verified_res:
            self.assertEqual(r["verification_status"], "VERIFIED")

        # If an unverified status is requested, nothing should be returned
        unverified = resource_service.get_resources(verification_status="UNVERIFIED")
        self.assertEqual(len(unverified), 0)

    def test_06_verified_source_display(self):
        """6. Verified source display: official attribution and valid domain."""
        resources = resource_service.get_resources()
        allowed_domains = [
            ".gov.in",
            ".nic.in",
            "osdma.org",
            "indianredcross.org",
            "belurmath.org",
            "goonj.org",
            "akshayapatra.org"
        ]
        for r in resources:
            self.assertTrue(r.get("source"), f"Resource {r['id']} missing source")
            self.assertTrue(r.get("source_url"), f"Resource {r['id']} missing source_url")
            has_valid_domain = any(domain in r["source_url"].lower() for domain in allowed_domains)
            self.assertTrue(has_valid_domain, f"Resource {r['id']} source_url not in authorized domains: {r['source_url']}")

    def test_07_empty_result(self):
        """7. Empty result: queries with no match return clean empty list without failure."""
        empty_res = resource_service.get_resources(state="NonExistentStateXYZ")
        self.assertEqual(empty_res, [])

        resp = self.client.get("/api/resources", params={"state": "NonExistentStateXYZ"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

    def test_08_api_failure(self):
        """8. API failure / single resource lookup: None for non-existent ID."""
        non_existent = resource_service.get_resource_by_id("fake-resource-id-999")
        self.assertIsNone(non_existent)

    def test_09_invalid_resource(self):
        """9. Invalid resource route returns 404 with structured detail message."""
        resp = self.client.get("/api/resources/invalid-resource-id-999")
        self.assertEqual(resp.status_code, 404)
        self.assertIn("detail", resp.json())
        self.assertIn("not found", resp.json()["detail"].lower())

    def test_10_no_fabricated_fallback(self):
        """10. No fabricated fallback: system must never synthesize demo or fake resources."""
        # Querying an unsupported disaster type
        res = resource_service.get_resources(disaster_type="AlienInvasion")
        self.assertEqual(len(res), 0, "Must not inject fabricated fallback resources")

        # Verify no resource in registry has is_demo = True or fake domains
        for r in VERIFIED_RESOURCES_REGISTRY:
            self.assertFalse(r.get("is_demo", False), f"Found demo flag on {r['id']}")
            self.assertNotIn("example.com", r.get("source_url", "").lower())
            self.assertNotIn("fake", r.get("name", "").lower())

    def test_11_help_others_flow(self):
        """11. Help Others flow: official direct portals only, zero payment collection."""
        donation_resources = resource_service.get_resources(category="Donations / Volunteering")
        self.assertGreaterEqual(len(donation_resources), 2)
        for r in donation_resources:
            url = r.get("website_url") or r.get("source_url") or ""
            self.assertTrue(url.startswith("https://"))
            self.assertTrue(
                "pmnrf.gov.in" in url or
                "assam.gov.in" in url or
                "indianredcross.org" in url or
                "goonj.org" in url or
                "akshayapatra.org" in url or
                "ndma.gov.in" in url
            )

    def test_12_get_help_flow(self):
        """12. Get Help flow: authentic national and state emergency hotlines."""
        helpline_resources = resource_service.get_resources(category="Emergency Services")
        self.assertGreaterEqual(len(helpline_resources), 2)
        phones = [r.get("phone") for r in helpline_resources if r.get("phone")]
        valid_hotlines = {"112", "1078", "1070", "108"}
        found_hotlines = set(phones).intersection(valid_hotlines)
        self.assertGreaterEqual(len(found_hotlines), 2, f"Expected official hotlines, found: {phones}")

    def test_13_resource_map_marker(self):
        """13. Resource map marker coordinates: valid geographic bounds within India."""
        mappable = [r for r in resource_service.get_resources() if r.get("latitude") is not None and r.get("longitude") is not None]
        self.assertGreaterEqual(len(mappable), 5, "At least 5 resources must have map coordinates")
        for r in mappable:
            lat = r["latitude"]
            lng = r["longitude"]
            # India latitude: approx 8.0 to 37.0 N
            self.assertGreaterEqual(lat, 8.0, f"Lat too low for {r['name']}: {lat}")
            self.assertLessEqual(lat, 37.0, f"Lat too high for {r['name']}: {lat}")
            # India longitude: approx 68.0 to 97.5 E
            self.assertGreaterEqual(lng, 68.0, f"Lng too low for {r['name']}: {lng}")
            self.assertLessEqual(lng, 97.5, f"Lng too high for {r['name']}: {lng}")

    def test_14_emergency_disclaimer(self):
        """14. Emergency disclaimer: check presence in frontend page files."""
        get_help_path = PROJECT_ROOT / "src" / "components" / "pages" / "GetHelpPage.tsx"
        help_others_path = PROJECT_ROOT / "src" / "components" / "pages" / "HelpOthersPage.tsx"

        self.assertTrue(get_help_path.exists(), "GetHelpPage.tsx must exist")
        self.assertTrue(help_others_path.exists(), "HelpOthersPage.tsx must exist")

        get_help_content = get_help_path.read_text(encoding="utf-8")
        help_others_content = help_others_path.read_text(encoding="utf-8")

        required_disclaimer_phrase = "For immediate emergencies, contact local emergency services and follow official government instructions"
        self.assertIn(
            required_disclaimer_phrase.lower(),
            get_help_content.lower(),
            "GetHelpPage missing mandatory emergency disclaimer phrase"
        )
        self.assertIn(
            "observed disaster",
            help_others_content.lower(),
            "HelpOthersPage missing observed disaster distinction"
        )
        self.assertIn(
            "potential risk",
            help_others_content.lower(),
            "HelpOthersPage missing potential risk distinction"
        )
        self.assertIn(
            "assistance opportunity",
            help_others_content.lower(),
            "HelpOthersPage missing assistance opportunity distinction"
        )


if __name__ == "__main__":
    unittest.main()
