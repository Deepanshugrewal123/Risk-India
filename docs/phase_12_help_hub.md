# Phase 12 — Verified Help Hub & Help Others System Architecture

**Project**: RISK // INDIA — AI Disaster Intelligence Prototype  
**Phase**: Phase 12 (Verified Help Hub + Help Others Completion)  
**Status**: Fully Completed & Verified  
**Date**: September 2026  

---

## 1. Executive Summary

Phase 12 completes the operational civic assistance ecosystem for **RISK // INDIA**. Prior to Phase 12, assistance components contained simulated mock pledge forms and demonstration placeholders. Phase 12 eliminates all synthetic placeholders, establishes a verified directory of 17 statutory and governmental disaster response organizations, enforces strict donation and volunteer safety protocols, implements multi-parameter filtering, adds verified geographic map markers, and integrates prominent emergency disclaimers across all user flows.

Importantly, Phase 12 strictly enforces the separation between **observed physical disasters**, **probabilistic AI hazard vulnerability**, and **actionable relief assistance opportunities**.

---

## 2. Architectural Pillars

```
┌──────────────────────────────────────────────────────────────────────────┐
│                               USER CLIENT                                │
│          GetHelpPage.tsx           │         HelpOthersPage.tsx          │
│   (Multi-filter, Speed-Dial,       │    (Observed Disasters, Verified    │
│    Verified Directory, Disclaimer) │     Relief Channels, Safety Rules)  │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
                    Frontend Resource Service (src/services/resourceService.ts)
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                             FASTAPI BACKEND                              │
│                      GET /api/resources                                  │
│                      GET /api/resources/{id}                             │
│                                    │                                     │
│                     ResourceService (backend/app/services)               │
│                                    │                                     │
│            ┌───────────────────────┴───────────────────────┐             │
│            ▼                                               ▼             │
│   13 Government Agencies                          4 Statutory NGOs       │
│   (NDMA, NDRF, ASDMA, HPSDMA,                     (Indian Red Cross,     │
│    OSDMA, CWC, IMD, 112, 1078,                     Ramakrishna Mission,  │
│    108, PMNRF, CMRF, Aapda Mitra)                  Goonj, Akshaya Patra) │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Verification Rules & Standards

1. **Strict Statutory & Official Eligibility**:
   - Only entities established under Acts of Parliament (e.g. Disaster Management Act 2005, Indian Red Cross Society Act XV of 1920), State Disaster Management Authorities (SDMAs), central scientific ministries (MoES/IMD, MoWR/CWC, MHA), or registered Section 8 / 80G statutory trusts with public standing are eligible.
2. **Domain Integrity Requirement**:
   - Every external source URL must resolve strictly to official domains (`.gov.in`, `.nic.in`, `osdma.org`, `indianredcross.org`, `belurmath.org`, `goonj.org`, `akshayapatra.org`). No commercial intermediary or unverified third-party domains are permitted.
3. **No Fabricated Fallbacks**:
   - When a search query yields zero matches, the backend and frontend return an explicit empty state (`[]` / "No verified resources found"). The system never synthesizes fake relief camps, fake numbers, or demo placeholders to fill UI voids.

---

## 4. Government Sources Inventory (13 Entities)

1. **National Disaster Management Authority (NDMA HQ)**: Apex statutory body (MHA) for national policies, early warnings, and NDRF deployment. Contact: `1078`. Portal: `https://ndma.gov.in`
2. **National Disaster Response Force (NDRF HQ)**: Specialized multi-disciplinary disaster rescue force with 16 operational battalions. Contact: `011-24363260`. Portal: `https://www.ndrf.gov.in`
3. **Assam State Disaster Management Authority (ASDMA)**: Nodal authority for Assam flood operations, river monitoring, and relief camps. Contact: `1070`. Portal: `https://asdma.assam.gov.in`
4. **HP State Disaster Management Authority (HPSDMA)**: State emergency control for Himalayan cloudbursts, flash floods, and landslides. Contact: `1070`. Portal: `https://hpsdma.nic.in`
5. **Odisha State Disaster Management Authority (OSDMA)**: Premier coastal cyclone management and early warning authority. Contact: `1070`. Portal: `https://www.osdma.org`
6. **Central Water Commission (CWC Flood Forecast Division)**: National river gauge telemetry and flood bulletin authority. Contact: `011-26106523`. Portal: `https://cwc.gov.in`
7. **India Meteorological Department (IMD Cyclone Warning Division)**: Weather, monsoon radar, and cyclone track forecasting. Contact: `011-24631913`. Portal: `https://mausam.imd.gov.in`
8. **Unified National Emergency Response System (112 India)**: All-India 24/7 single emergency number under ERSS for police, fire, ambulance, and disaster distress. Contact: `112`. Portal: `https://112.gov.in`
9. **NDMA National Disaster Helpline (1078)**: Dedicated 24/7 toll-free national disaster helpline. Contact: `1078`. Portal: `https://ndma.gov.in`
10. **National Emergency Medical & Ambulance Service (108)**: 24/7 basic and advanced life support trauma transit under NHM. Contact: `108`. Portal: `https://nhm.gov.in`
11. **Prime Minister's National Relief Fund (PMNRF)**: Official statutory disaster relief buffer fund managed by PMO. Portal: `https://pmnrf.gov.in`
12. **Chief Minister's Relief Fund - Assam (CMRF Assam)**: State relief buffer for flood damage rehabilitation. Portal: `https://cm.assam.gov.in`
13. **NDMA Aapda Mitra Community Volunteer Scheme**: Official government disaster volunteer training and mobilization framework across 350 disaster-prone districts. Portal: `https://ndma.gov.in/Governance/Aapda-Mitra`

---

## 5. Statutory NGO Resources (4 Entities)

1. **Indian Red Cross Society (Disaster Management Division)**: Statutory humanitarian society under Act of Parliament XV of 1920 providing first aid, water purification, and disaster relief kits. Portal: `https://indianredcross.org`
2. **Ramakrishna Mission Relief and Rehabilitation Services**: Century-old humanitarian mission providing dry ration supply kits, community kitchen operations, and medical camps. Portal: `https://belurmath.org`
3. **Goonj (Rahat Disaster Relief Initiative)**: Standardized relief kits, clothing material logistics, and community reconstruction. Portal: `https://goonj.org`
4. **The Akshaya Patra Foundation (Disaster Relief Feeding)**: Automated industrial relief kitchens producing thousands of cooked hot meals daily during flood crises. Portal: `https://www.akshayapatra.org`

---

## 6. Donation Safety & Financial Integrity

To prevent fraud, payment leakage, and user deception:
- **No In-App Payment Links**: RISK // INDIA does not collect payments, process credit cards, or store banking credentials.
- **Direct Domain Routing**: All monetary contribution links are labeled strictly as `"Donate via official organization"` and redirect directly to official government portals (`pmnrf.gov.in`, `cm.assam.gov.in`) or registered NGO gateways (`indianredcross.org`, `goonj.org`, `akshayapatra.org`).
- **Simulated Form Elimination**: Removed previous demonstration forms that accepted user names and rupee amounts. Replaced with authentic organizational information and direct official links.

---

## 7. Semantic Separation of Signals

Users are presented with clear semantic distinctions:
1. **Observed Disaster**: Physical, ground-truth incident logged by an authorized feed (USGS Seismic network or State Disaster Management bulletin).
2. **Potential Risk (AI Baseline)**: Statistical vulnerability estimate based on regional hydrology and historical flood datasets. *Explicit notice informs users that an AI prediction does not mean donations or relief are currently requested.*
3. **Assistance Opportunity**: Verified statutory relief organization, disaster fund, or government volunteer framework.

---

## 8. Map Integration

- **Coordinate Verification**: Verified entities with physical headquarters, dispatch depots, or relief centers have exact geographic coordinates within India (Latitude: 8.0°N – 37.0°N, Longitude: 68.0°E – 97.5°E).
- **Distinct Visual Marker**: Rendered as an emerald diamond marker with white border and center point (`polygon`), visually distinct from circular baseline pins (pastels) and pulsating incident pings (red/rose).
- **Interactive Tooltip & Layer Toggle**: Dedicated "Help Centers" button in the map header toggles display on/off; hovering displays entity name, category, authority, and verification badge.

---

## 9. Limitations & Ethical Boundary

1. **Non-Replacement of Emergency Services**: The platform is an intelligence prototype. It does not replace official 112/1078 emergency call centers or local district administration instructions.
2. **Prototype Scope**: Directory focuses on national nodal bodies and key state authorities in pilot zones (Assam, Himachal Pradesh, Odisha). Pan-India scaling requires ongoing integration with state disaster management rosters.
