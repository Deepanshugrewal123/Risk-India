# FUTURE RISK UX SPECIFICATION
## Design System, Information Architecture & Accessibility Standards

**Document Version**: 2.0.0  
**Status**: APPROVED  
**Date**: September 2026  
**Scope**: Primary Homepage & Geospatial Future Risk UI  
**Target Accessibility**: WCAG 2.1 Level AA Compliance  

---

### 1. Information Architecture & Progressive Disclosure

The citizen-facing future risk interface is engineered for rapid comprehension during both calm preparedness and imminent crisis situations. It follows a 3-tier progressive disclosure model:

1. **Level 1: Immediate Gist (0–3 seconds)**
   - Horizon selector pills (`NOW`, `0-6h`, `6-24h`, `1-3d`, `3-7d`).
   - Macro status badge (e.g., `ELEVATED // WATCH`, `CRITICAL // WARNING`).
   - Directional trend icon and label (`INCREASING`, `STABLE`, `DECREASING`).
   - Recommended advance action callout.

2. **Level 2: Contextual Breakdown (3–10 seconds)**
   - Qualitative Confidence level (`LOW`, `MODERATE`, `HIGH`).
   - Qualitative Uncertainty level with lead-time explanation.
   - Primary driving environmental factors (e.g., *Sustained upstream catchment discharge + heavy rainfall forecast*).
   - Authoritative source badges (IMD Mausam, CWC FFS, USGS).

3. **Level 3: Deep Technical Audit (10+ seconds)**
   - Specific gauge hydrograph / telemetry levels vs danger marks.
   - Verification of zero synthetic records (`synthetic_records = 0`).
   - Model localization boundary (Assam Brahmaputra gauges vs nationwide baseline climatology).
   - Direct link to official district disaster management advisories.

---

### 2. The 5 Standard Forecast Horizons

Future risk projections are strictly organized across five standardized operational horizons:

| Horizon Code | Horizon Label | Operational Temporal Window | Scientific Lead Time Nature | Maximum Qualitative Uncertainty |
|---|---|---|---|---|
| `now` | **NOW / CURRENT** | Past 0 to 60 minutes | Real-time gauge & radar observations | `VERY_LOW` |
| `0-6h` | **NEXT 6 HOURS** | +1 to +6 hours | Nowcasting (Doppler radar + telemetry extrapolation) | `LOW` |
| `6-24h` | **NEXT 24 HOURS** | +6 to +24 hours | High-resolution numerical weather prediction (NWP) | `MODERATE` |
| `1-3d` | **DAYS 1 TO 3** | +24 to +72 hours | Regional ensemble meteorological models | `HIGH` |
| `3-7d` | **DAYS 3 TO 7** | +72 to +168 hours | Global medium-range synoptic circulation outlook | `VERY_HIGH` |

#### Monotonic Uncertainty Invariant
The user interface mathematically enforces monotonic uncertainty expansion:
$$\text{Uncertainty}(\text{NOW}) \le \text{Uncertainty}(0\text{--}6\text{h}) \le \text{Uncertainty}(6\text{--}24\text{h}) \le \text{Uncertainty}(1\text{--}3\text{d}) \le \text{Uncertainty}(3\text{--}7\text{d})$$
Visual badges communicate this progression clearly using a 5-step uncertainty bar, ensuring citizens understand that distant forecasts carry wider variability margins than immediate nowcasts.

---

### 3. Qualitative Confidence Guidelines (Strict Ban on Numeric Pseudo-Probabilities)

To avoid misleading citizens with false mathematical precision, **all numeric percentages ("87% probability of flood") are strictly prohibited**. Risk confidence is expressed exclusively via three qualitative tiers:

1. **HIGH Confidence**:
   - Multiple corroborating sensor feeds (IMD AWS + CWC gauge + Satellite soil moisture).
   - Short lead time (NOW or 0–6h).
   - High data freshness ($< 2$ hours old).
   - Clear historical precedent.

2. **MODERATE Confidence**:
   - Single authoritative telemetry stream or standard numerical model consensus.
   - Intermediate lead time (6–24h or 1–3d).
   - Standard data freshness ($2$ to $6$ hours old).

3. **LOW Confidence**:
   - Long-range outlook (3–7d) or sparse remote sensing coverage.
   - Divergent meteorological ensemble members.
   - Complex terrain interaction or unmonitored tributary catchments.

---

### 4. Color Palette & Visual Accessibility (WCAG 2.1 AA)

All visual elements conform to WCAG 2.1 Level AA color contrast requirements ($\ge 4.5:1$ for normal text, $\ge 3.0:1$ for large text and UI controls). High-contrast mode (Crisis Mode) achieves $\ge 7:1$.

#### Colorblind-Safe Severity Indicators
Colors are never used as the sole conveyor of information. Every severity state combines color, icon, and explicit text:

| Severity Level | Background Color | Text Color | Border Color | Accompanying Icon | Text Descriptor |
|---|---|---|---|---|---|
| **LOW** | `bg-emerald-50` (`#ECFDF5`) | `text-emerald-900` (`#064E3B`) | `border-emerald-300` | `ShieldCheck` | `LOW // STABLE` |
| **MODERATE** | `bg-amber-50` (`#FFFBEB`) | `text-amber-950` (`#451A03`) | `border-amber-300` | `Clock` | `MODERATE // ELEVATED` |
| **HIGH** | `bg-orange-50` (`#FFF7ED`) | `text-orange-950` (`#431407`) | `border-orange-300` | `AlertTriangle` | `HIGH // WATCH` |
| **CRITICAL** | `bg-rose-50` (`#FFF1F2`) | `text-rose-950` (`#4C0519`) | `border-rose-400` | `ShieldAlert` | `CRITICAL // WARNING` |

---

### 5. Touch Target & Ergonomics Specification

To support users on budget mobile smartphones with cracked screens or wet fingers during adverse weather:
- **Minimum Interactive Touch Target**: Every button, pill selector, accordion trigger, and link has a minimum bounding box of $44 \times 44\text{px}$ (`min-h-[44px] min-w-[44px]`).
- **Pill & Button Spacing**: Minimum $8\text{px}$ gap between adjacent touch targets to eliminate mis-taps.
- **Focus Indicators**: Visible keyboard focus ring (`focus-visible:ring-2 focus-visible:ring-charcoal-900`) on all interactive controls.
- **Form Controls**: Large native select dropdowns ($48\text{px}$ height) with readable system typography.

---

### 6. Preparation Guidance vs Evacuation Directive Demarcation

The UX enforces a strict visual boundary between community preparedness and mandatory civil directives:
- **Green / Neutral Border Panels**: Preparedness guidance (e.g., *"Charge mobile phones and power banks"*, *"Boil drinking water"*, *"Clear rooftop drains"*).
- **Red / Amber Flashing Banner Panels**: Civil Evacuation Directives. Accompanied by the legal statement:  
  > *"Evacuation orders are issued exclusively by District Magistrates / SDMA / NDRF under the Disaster Management Act, 2005. Do not delay evacuation if ordered by civil authorities."*

---

### 7. Performance & Bandwidth Budget

- **First Contentful Paint (FCP)**: $< 1.2$ seconds on 4G connections.
- **Total Initial Bundle Size**: Gzipped assets $< 200\text{ kB}$.
- **Zero Heavy Geospatial Bloat on Homepage**: Homepage renders lightweight SVG map vectors and cached telemetry; heavy WebGL and tile layers load asynchronously only upon clicking `"Open Risk Map"`.
