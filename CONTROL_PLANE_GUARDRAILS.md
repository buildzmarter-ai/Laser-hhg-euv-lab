# Control-Plane Surface — GUARDRAILS

**Matter:** Laser-HHG-EUV Lab ↔ vdw-polaritonics-lab — programmable optical-transfer-function control-plane.
**As of:** 2026-04-16 (session close).
**Purpose:** invariants and do-not-drift rules. Any new session must read this before producing claim language, spec paragraphs, or external communications.

---

## 1. Five locked premises

1. The `Laser-hhg-euv-lab` repository is an epistemically tiered architectural modeling lab. Not a device demonstration. Not an industrial EUV source claim.
2. The strongest defensible bridge between the two repos is front-end driver conditioning — not any claim that the vdW cavity itself operates at EUV.
3. Generated, transmitted, and delivered photon flux are three separately reportable planes. No plane is ever reported without the other two and their respective tier labels.
4. The two repos are complementary architectural layers coupled through a shared control plane. They are not a single demonstrated integrated device.
5. The tier-labeled reporting track is a machine-governed control / export constraint. It is not presentation of information.

Any session that proposes to violate one of the five premises must stop and ask the user explicitly before proceeding.

## 2. Load-bearing claim surface (do not drift)

Programmable optical-transfer-function control plane operating across two physically distinct optical stages:
- a DUV intracavity modulation stage at 193/248 nm;
- a driver-front-end conditioning stage at 800/1030/1800–3000 nm, upstream of an HHG gas target;

coupled only through shared parameter space and controller logic, not through a shared optical path;

plus controller-enforced tier-labeled three-part flux export (source-side estimate / transmission-product estimate / delivered-side estimate) with emission-inhibit gating when one or more of the three components or their tier labels is absent.

## 3. Hard exclusions — never in any claim or dependent

- Photon-flux magnitudes, brightness, dose, or throughput values.
- Extreme-ultraviolet-source apparatus naming in any form.
- Lithography applicability, including wafer, HVM, or patterning language.
- Integrated-device phrasing ("integrated into a single optical assembly", "single cavity containing both stages", "co-located stages").
- Cavity-enhanced function for the DUV intracavity modulation stage.
- Operation of a two-dimensional-material modulation element beyond a native absorption edge.
- Numerical resolution, line-edge-roughness, dose-latitude, or throughput values derived from point-spread-function or resist modules.
- Single-atom λ^−(5…6.5) efficiency-exponent range as a numerical claim element.
- Any standalone statement of `E_cut = 3.17·U_p + I_p` as a claim element; the relation appears only inside a constraint-computation step.

## 4. Prohibited verbs and phrases for tier labels

**Never:** display, show, present, render, visualize, flag, annotate, indicate to a user, user interface.
**Always:** emit, transmit, store, associate, inhibit emission of, gate on, refuse to emit.

## 5. Prohibited competitive-positioning phrases

**Never, whenever placed near** laser-produced-plasma, ASML, extreme-ultraviolet source, lithography, high-volume manufacturing, or intermediate focus: replaces, alternative to, comparable to, equivalent to, on par with.

## 6. Six language traps (with safe substitutes)

1. **EUV-source overclaim.** Trap: "an EUV source comprising…". Safe: "a harmonic-generation stage configured to produce harmonic orders within one or more of the VUV, EUV, and soft-X-ray bands".

2. **Integrated-device implication.** Trap: shared cavity / mirror / optical path. Safe: "the first stage and the second stage are coupled through the selection logic and are not in optical series".

3. **Flux / brightness implication from analytical models.** Trap: scalar delivered-flux language. Safe: "the controller reports an estimated delivered photon count as a product of a literature-anchored source-side estimate and an analytically computed transmission-product estimate, each labeled with its epistemic tier drawn from the predetermined tier set".

4. **CE-HHG / vdW-cavity conflation.** Trap: language equating the DUV intracavity element with a femtosecond enhancement cavity at the driver wavelength. Safe: "the DUV intracavity modulation stage is not configured to enhance, build up, or recirculate a driver pulse of the high-harmonic-generation gas target and is not in optical series with a driver path of the gas target".

5. **PSF / resist numerical-performance implication.** Trap: resolution / LER / dose / throughput from parameterized modules. Safe: omit from claims; include only as background.

6. **§101 presentation-of-information framing for tier labels.** Trap: describing tier labels as displayed, shown, or user-facing. Safe: controller-enforced export-interface gate with emission inhibit on the absence of source-side estimate, transmission-product estimate, or their tier labels.

## 7. Per-paragraph and per-caption drafting rule

Every embodiment paragraph in the specification ends with one sentence naming what the embodiment does not demonstrate. Every drawing description ends with one sentence naming what the drawing does not represent. This is the prose analog of the repo's epistemic-tier banners and is the single most effective written-description defense.

## 8. Terminology normalization (do not drift)

**Use exactly:**
- "source-side estimate"
- "transmission-product estimate"
- "delivered-side estimate"
- "not in optical series"
- "predetermined tier set"

**Minimize or avoid:**
- "application-facing tier"
- Any synonym-drift for the three estimates (e.g., "generated flux estimate", "throughput estimate", "final flux number").

## 9. Cleanup-pass discipline (applies to every session)

- No broadening of claim scope without explicit user directive.
- No new embodiments without explicit user directive.
- No new modalities promoted to independent-claim status.
- No new use-case endpoints beyond the four locked endpoints (CDI; ptychography; actinic EUV mask inspection; ARPES).
- No edits to the five locked premises without explicit user directive.

## 10. Session-boot compliance check

Before producing any claim language, spec paragraph, or external communication in a new session, verify:

- [ ] Five locked premises read and acknowledged.
- [ ] Load-bearing claim surface read and acknowledged.
- [ ] Hard exclusions read.
- [ ] Prohibited-verb list read.
- [ ] Six language traps read.
- [ ] Per-paragraph drafting rule will be applied.
- [ ] Terminology normalization will be respected.

---

*End of GUARDRAILS surface.*
