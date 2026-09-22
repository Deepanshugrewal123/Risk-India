# RISK // INDIA — UI & UX Forensic Gap Analysis
## Visual Hierarchy, Discoverability, Accessibility & Human Factors

**Document:** `ui_gap_analysis.md`  
**Classification:** Forensic System Re-Analysis  
**Authoritative Workspace:** `C:\Users\HP\Desktop\Risk Analyser`  

---

### 1. The Citizen Experience Audit

During a developing disaster (e.g. rising floodwaters or an approaching cyclone), an ordinary citizen opens RISK // INDIA on their phone with high urgency, limited bandwidth, and emotional stress.

We audited the existing frontend against this exact scenario:

| Citizen Need | Current UI Behavior | Forensic Evaluation | Required Betterment |
| :--- | :--- | :---: | :--- |
| **1. See immediate future risk** | Buried inside a secondary tab on `RiskMapPage.tsx`. Homepage only shows live snapshot. | **FAIL** | Move **Future Risk Hero ("WHAT COULD HAPPEN NEXT?")** directly to the homepage. |
| **2. Check my district/city** | `AnalyzeAreaSection.tsx` has state dropdown, but loads a demo Assam flood object. | **FAIL** | Convert into **Live Location Risk Checker** connecting to live APIs with zero demo flags. |
| **3. Know how serious it could become** | Score shown as a number without clear citizen consequence benchmarks. | **MEDIOCRE** | Provide plain-language consequence benchmarks (Low, Moderate, High, Severe). |
| **4. Understand WHY risk may increase** | Why factors were technical model weights rather than physical causes. | **MEDIOCRE** | Present physical drivers: *"Heavy rainfall forecast (65mm) + Brahmaputra approaching danger mark"*. |
| **5. Know what to do right now** | Hidden behind multiple scroll levels or separate "Preparedness" tab. | **FAIL** | Put **"WHAT SHOULD I DO?"** (Do Now, Prepare Before, During, After) right on homepage. |
| **6. Distinguish Prepare vs Evacuate** | Preparation checklists and evacuation advisories were visually similar. | **FAIL** | High-contrast **Evacuation Directive** shown ONLY when statutory evacuation is active. |
| **7. Access emergency helplines** | Small SOS button in bottom right; easy to miss. | **MEDIOCRE** | Permanent, prominent speed-dial row on homepage and emergency access hub. |
| **8. Multi-hazard future trends** | Only one hazard displayed at a time; hard to compare threats. | **FAIL** | Provide **6-Hazard Future Risk Cards** comparing all hazards over the next 24 hours. |

---

### 2. Nomenclature & Language Inconsistencies

1. **"Dedicated Risk Map"**: 
   - Confusing internal phrasing. 
   - **Fix**: Replaced by clear, action-oriented **"Open Risk Map"**.
2. **"Model Version v1.4.0-demo"**:
   - Exposed technical prototype jargon.
   - **Fix**: Replaced by **"Official Data Fusion"** with provenance citations (IMD, CWC, NDMA).
3. **Color-Only Warning Indicators**:
   - Some badges relied solely on green/yellow/orange/red backgrounds without text icons or labels, failing WCAG AA for colorblind citizens.
   - **Fix**: Every warning and risk state is paired with a distinct icon, text state badge, and font-mono code.

---

### 3. Mobile Viewport & Touch Target Deficiencies

1. **Dashboard Overload**: Some desktop components attempted to display 4-column metrics on mobile, causing horizontal scrolling or microscopic text.
2. **Touch Target Size**: Several dropdown triggers and link pills were under $36 \times 36$ pixels.
3. **Fix**: Standardize all touch targets to $\ge 44 \times 44$ px, adopt single-column responsive stacking for mobile, and make the emergency speed-dial bar sticky at the bottom of the mobile viewport.
