# Clean Integrated Patent Draft

**Matter:** Laser-HHG-EUV Lab / vdw-polaritonics-lab — programmable optical-transfer-function control-plane.
**Date:** 2026-04-16.
**Status:** counsel-ready base draft. Cleanup-to-handoff pass. Invention scope unchanged from prior working documents.
**Prior working documents (depth record, same repository):** `patent_positioning_2026-04-16.md`; `patent_claim_priority_brief_2026-04-16.md`; `patent_counsel_handoff_packet_2026-04-16.md`; `hhg-euv-lab-complete.pdf`.

---

## TITLE

Controller and Method for a Programmable Optical-Transfer-Function Control Plane Across Physically Decoupled Optical Stages, With Controller-Enforced Tier-Labeled Reporting.

---

## CROSS-REFERENCE TO RELATED APPLICATIONS

*[Placeholder for counsel.]*

---

## FIELD OF THE INVENTION

The invention relates to controllers and methods for coordinated operation of physically distinct optical stages of a laser photon-source architecture, and more particularly to a controller that applies a programmable optical transfer function jointly across a deep-ultraviolet (DUV) intracavity modulation stage and a driver-front-end conditioning stage upstream of a high-harmonic-generation (HHG) gas target, and to a controller-enforced reporting construct in which computed photon-estimate outputs carry tier labels drawn from a predetermined tier set and in which emission of a delivered-side estimate is gated on the presence of a source-side estimate and a transmission-product estimate and their respective tier labels.

---

## BACKGROUND

High-harmonic generation in a gas target produces harmonic orders of a driver laser pulse and populates spectral regions including the vacuum-ultraviolet, extreme-ultraviolet, and soft-X-ray bands. The harmonic output of such an HHG stage is sensitive to driver-pulse temporal and spectral structure and to a phase-matching condition of the gas target.

Separately, intracavity modulation of a DUV laser (for example at 193 nanometers or 248 nanometers) is known in the art for shaping the DUV output of a resonator.

Controllers operating across physically distinct optical stages in a coordinated manner, with shared parameter spaces and with rigorous separation of generated, transmitted, and delivered photon-estimate planes in their export outputs, are not known in the art. Reporting constructs in which a controller's export interface inhibits emission of a delivered-side estimate in the absence of a corresponding source-side estimate and a corresponding transmission-product estimate (and their respective tier labels) are also not known in the art.

There is a need for controller apparatus and methods that provide such coordinated operation and such controller-enforced reporting, without implying device operation beyond what the controller's stored data and computation logic enable.

---

## SUMMARY OF THE INVENTION

In one aspect, a controller for a two-stage laser photon-source architecture comprises a memory storing a shared parameter space and a predetermined tier set; a first-stage interface configured to transmit a DUV-stage parameter set to a DUV intracavity modulation stage; a second-stage interface configured to transmit a driver-stage parameter set to a driver-front-end conditioning stage upstream of an HHG gas target; selection logic configured to compute the two parameter sets jointly from the shared parameter space subject to at least one cutoff-target constraint derived from an analytical cutoff relation and at least one phase-matching-proxy constraint on an estimated ionization fraction of the gas target; and an export interface configured to emit, for a selected operating point, an output tuple comprising a source-side estimate, a transmission-product estimate, and a delivered-side estimate, each carrying a respective tier label drawn from the predetermined tier set. The export interface is configured to inhibit emission of the delivered-side estimate in the absence of either the source-side estimate or the transmission-product estimate, or the tier label associated therewith. The DUV intracavity modulation stage and the driver-front-end conditioning stage are not in optical series.

In another aspect, a method performed by such a controller comprises the corresponding steps of receiving a specification in the shared parameter space, computing the two parameter sets jointly under the two constraints, transmitting each parameter set to its respective stage, computing the source-side estimate, the transmission-product estimate, and the delivered-side estimate, associating each with a respective tier label drawn from the predetermined tier set, and emitting an output tuple via the export interface with the same emission-inhibit gating.

In a backup aspect, the controller and the method are reduced to the driver-stage subset, operating on a driver-stage parameter set alone under the same two constraints, with the same tier-labeled output tuple and the same emission-inhibit gating.

In a further aspect, an apparatus for reporting photon-flux estimates of a laser photon-source comprises the tier-labeled reporting construct and the emission-inhibit gate as an independent element, independent of the two-stage or driver-stage coordination features.

The invention does not establish a delivered extreme-ultraviolet lithography-source flux, does not assert substitution for laser-produced-plasma sources in high-volume extreme-ultraviolet lithography, and does not assert or enable operation of any two-dimensional-material modulation element beyond its native absorption edge.

---

## BRIEF DESCRIPTION OF THE DRAWINGS

**FIG. 1** is a wavelength-bridge representation placing a DUV intracavity modulation stage and a driver-conditioned high-harmonic-generation stage on a common wavelength axis, together with a harmonic-cascade representation of the HHG stage. FIG. 1 is a control-plane representation; FIG. 1 does not represent a physical optical path between the stages and does not assert operation of a two-dimensional-material modulation element beyond its native absorption edge.

**FIG. 2** is a schematic of a controller apparatus, showing a memory storing a shared parameter space and a predetermined tier set, a first-stage interface, a second-stage interface, selection logic, and an export interface with an emission-inhibit gate. FIG. 2 is a data-flow representation; FIG. 2 does not represent any physical optical coupling between the stages.

**FIG. 3** is a data-object representation of an output tuple comprising a source-side estimate, a transmission-product estimate, and a delivered-side estimate, each associated with a respective tier label drawn from the predetermined tier set, together with the emission-inhibit gate of an export interface. FIG. 3 does not assert any specific photon-flux value.

**FIG. 4** is an illustrative representation of a cutoff-energy surface of the form E_cut = 3.17 · U_p + I_p as a function of driver intensity and an ionization-fraction ceiling η_c as a function of an estimated ionization fraction, the two surfaces being usable by the selection logic as constraint surfaces. FIG. 4 does not assert any device-level photon-flux value.

---

## DETAILED DESCRIPTION OF EMBODIMENTS

### System architecture

In one embodiment, a programmable optical-transfer-function controller comprises a memory, a first-stage interface, a second-stage interface, selection logic, and an export interface. The memory stores a shared parameter space and a predetermined tier set. The first-stage interface is configured to transmit a DUV-stage parameter set to a DUV intracavity modulation stage operating at a DUV wavelength. The second-stage interface is configured to transmit a driver-stage parameter set to a driver-front-end conditioning stage upstream of an HHG gas target. The DUV intracavity modulation stage and the driver-front-end conditioning stage are not in optical series. The two stages are coupled through the controller and are not required to be physically co-located. This embodiment does not establish a delivered extreme-ultraviolet lithography-source flux.

### Selection logic and constraints

The selection logic is configured to compute the DUV-stage parameter set and the driver-stage parameter set jointly from the shared parameter space, subject to at least one cutoff-target constraint derived from an analytical cutoff relation and at least one phase-matching-proxy constraint on an estimated ionization fraction of the HHG gas target. In one embodiment, the analytical cutoff relation is of the form E_cut = 3.17 · U_p + I_p, where U_p is a ponderomotive energy of a driver pulse applied by the driver-front-end conditioning stage and I_p is an ionization potential of a gas medium of the HHG gas target. In one embodiment, the phase-matching-proxy constraint comprises a ceiling η_c on the estimated ionization fraction. This embodiment does not establish a measured phase-matching window of any particular gas medium.

### Driver-front-end conditioning stage

The driver-front-end conditioning stage is configured to apply a programmable spectral and temporal transfer function to a driver pulse prior to entry of the driver pulse into the HHG gas target. Conditioning operations include, in various embodiments, spectral-phase shaping, pulse-duration control, two-color synthesis, carrier-envelope-phase stabilization, and chirped-pulse-envelope adjustment. The driver-front-end conditioning stage operates at a driver wavelength in a near-infrared or mid-infrared band, for example at approximately 800 nanometers, approximately 1030 nanometers, or a wavelength between approximately 1800 nanometers and approximately 3000 nanometers. This embodiment does not establish a device-level delivered photon-flux achievement attributable to any single conditioning operation.

### DUV intracavity modulation stage

The DUV intracavity modulation stage operates at a DUV wavelength, for example at approximately 193 nanometers or at approximately 248 nanometers. In one embodiment, the DUV intracavity modulation stage comprises a two-dimensional-material heterostructure operating below a native absorption edge of the two-dimensional material. The DUV intracavity modulation stage is not configured to enhance, build up, or recirculate a driver pulse of the HHG gas target and is not in optical series with a driver path of the HHG gas target. This embodiment does not assert or enable operation of the two-dimensional-material heterostructure at extreme-ultraviolet wavelengths.

### Wavelength-bridge representation

In one embodiment, the controller or an associated representation places, on a common wavelength axis, an operating region of the DUV intracavity modulation stage and an operating region of the driver-front-end conditioning stage together with a harmonic-cascade representation of the HHG gas target. This wavelength-bridge representation is a control-plane representation; it does not represent a physical optical path between the stages. This embodiment does not establish operation of the DUV intracavity modulation stage at extreme-ultraviolet wavelengths.

### Export interface and tier-labeled reporting construct

The export interface is configured to emit, for a selected operating point computed by the selection logic, an output tuple comprising a source-side estimate, a transmission-product estimate, and a delivered-side estimate. The source-side estimate is derived from a literature-anchored value stored in the memory. The transmission-product estimate is computed as a product of stated optical-element reflectivities and transmissions, for example as R^N · T^M where N is a count of multilayer-mirror elements of stated reflectivity R and M is a count of foil-filter elements of stated transmission T. The delivered-side estimate is formed as a product of the source-side estimate and the transmission-product estimate. Each of the source-side estimate, the transmission-product estimate, and the delivered-side estimate is associated with a respective tier label drawn from the predetermined tier set stored in the memory. In one embodiment, the predetermined tier set comprises at least an analytical tier, a parameterized tier, an architectural tier, and a literature-quoted tier. In one embodiment, the source-side estimate carries a literature-quoted tier label, the transmission-product estimate carries an analytical tier label, and the delivered-side estimate carries a parameterized tier label. This embodiment does not assert any specific photon-flux value.

### Emission-inhibit gating

The export interface is configured to inhibit emission of the delivered-side estimate in the absence of either the source-side estimate or the transmission-product estimate, or the tier label associated therewith. In one embodiment, the controller is further configured to refuse to emit the output tuple in response to a non-compliant specification input. The emission-inhibit gating and the refusal behavior are operational states of the controller and are not presentations of information to a user. This embodiment does not assert any specific photon-flux value.

### Backup driver-only embodiment

In a backup embodiment, the controller is reduced to the driver-stage subset, operating on a driver-stage parameter set alone under the same cutoff-target constraint and the same phase-matching-proxy constraint, with the same tier-labeled output tuple and the same emission-inhibit gating. In this embodiment, the DUV intracavity modulation stage is not required. This embodiment does not establish a delivered extreme-ultraviolet lithography-source flux.

### Defensible use-case endpoints

In one embodiment, the controller is configured for use in at least one of coherent diffractive imaging, ptychography, actinic extreme-ultraviolet mask inspection, and angle-resolved photoemission. This embodiment does not assert applicability to high-volume extreme-ultraviolet lithography.

### Non-enablement statement for the embodiments as a whole

None of the embodiments described herein establishes a delivered extreme-ultraviolet lithography-source flux, demonstrates operation of a two-dimensional-material modulation element beyond its native absorption edge, or demonstrates substitution for a laser-produced-plasma source in high-volume extreme-ultraviolet lithography. The controller, the selection logic, and the export interface are the claimed subject matter; the photon-source device is downstream of the controller and is not within the claimed subject matter except as recited in the claims.

---

## CLAIMS

What is claimed is:

**1.** A controller for a two-stage laser photon-source architecture, the controller comprising:

a memory storing a shared parameter space and a predetermined tier set;

a first-stage interface configured to transmit a DUV-stage parameter set to a DUV intracavity modulation stage operating at a DUV wavelength;

a second-stage interface configured to transmit a driver-stage parameter set to a driver-front-end conditioning stage upstream of a high-harmonic-generation gas target;

selection logic configured to compute the DUV-stage parameter set and the driver-stage parameter set jointly from the shared parameter space subject to at least one cutoff-target constraint derived from an analytical cutoff relation and at least one phase-matching-proxy constraint on an estimated ionization fraction of the high-harmonic-generation gas target; and

an export interface configured to emit, for a selected operating point, an output tuple comprising a source-side estimate, a transmission-product estimate, and a delivered-side estimate, each of the source-side estimate, the transmission-product estimate, and the delivered-side estimate carrying a respective tier label drawn from the predetermined tier set,

wherein the export interface is further configured to inhibit emission of the delivered-side estimate when one or more of the source-side estimate, the transmission-product estimate, and the respective tier labels associated therewith is absent, and

wherein the DUV intracavity modulation stage and the driver-front-end conditioning stage are not in optical series.

**2.** The controller of claim 1, wherein the analytical cutoff relation is of the form E_cut = 3.17 · U_p + I_p, where U_p is a ponderomotive energy of a driver pulse applied by the driver-front-end conditioning stage and I_p is an ionization potential of a gas medium of the high-harmonic-generation gas target.

**3.** The controller of claim 1, wherein the phase-matching-proxy constraint comprises a ceiling η_c on the estimated ionization fraction of the high-harmonic-generation gas target.

**4.** The controller of claim 1, wherein the DUV wavelength is approximately 193 nanometers or approximately 248 nanometers.

**5.** The controller of claim 1, wherein the driver-front-end conditioning stage is configured to condition a driver pulse at a wavelength of approximately 800 nanometers, approximately 1030 nanometers, or a wavelength between approximately 1800 nanometers and approximately 3000 nanometers.

**6.** The controller of claim 1, wherein the predetermined tier set comprises at least an analytical tier, a parameterized tier, an architectural tier, and a literature-quoted tier, and wherein the source-side estimate carries a literature-quoted tier label, the transmission-product estimate carries an analytical tier label, and the delivered-side estimate carries a parameterized tier label.

**7.** The controller of claim 1, wherein the transmission-product estimate is computed as a product of stated optical-element reflectivities and transmissions of a form R^N · T^M, where N is a count of multilayer-mirror elements of stated reflectivity R and M is a count of foil-filter elements of stated transmission T.

**8.** The controller of claim 1, wherein the DUV intracavity modulation stage comprises a two-dimensional-material heterostructure operating below a native absorption edge of the two-dimensional material, and wherein the DUV intracavity modulation stage is not configured to enhance, build up, or recirculate a driver pulse of the high-harmonic-generation gas target.

**9.** The controller of claim 1, wherein the driver-front-end conditioning stage is configured to apply at least one of spectral-phase shaping, pulse-duration control, two-color synthesis, carrier-envelope-phase stabilization, and chirped-pulse-envelope adjustment to a driver pulse prior to entry of the driver pulse into the high-harmonic-generation gas target.

**10.** The controller of claim 1, wherein the export interface is further configured to refuse to emit the output tuple in response to a non-compliant specification input.

**11.** The controller of claim 1, wherein the controller is configured for use in at least one of coherent diffractive imaging, ptychography, actinic extreme-ultraviolet mask inspection, and angle-resolved photoemission.

**12.** A controller for a laser photon-source driver stage, the controller comprising:

a memory storing a parameter space and a predetermined tier set;

a driver-stage interface configured to transmit a driver-stage parameter set to a driver-front-end conditioning stage upstream of a high-harmonic-generation gas target;

selection logic configured to compute the driver-stage parameter set from the parameter space subject to at least one cutoff-target constraint derived from an analytical cutoff relation and at least one phase-matching-proxy constraint on an estimated ionization fraction of the high-harmonic-generation gas target; and

an export interface configured to emit an output tuple comprising a source-side estimate, a transmission-product estimate, and a delivered-side estimate, each of the source-side estimate, the transmission-product estimate, and the delivered-side estimate carrying a respective tier label drawn from the predetermined tier set,

wherein the export interface is further configured to inhibit emission of the delivered-side estimate when one or more of the source-side estimate, the transmission-product estimate, and the respective tier labels associated therewith is absent.

**13.** The controller of claim 12, wherein the analytical cutoff relation is of the form E_cut = 3.17 · U_p + I_p and the phase-matching-proxy constraint comprises a ceiling η_c on the estimated ionization fraction of the high-harmonic-generation gas target.

**14.** A method performed by a controller of a two-stage laser photon-source architecture, the method comprising:

receiving, at the controller, a specification expressed in a shared parameter space stored in a memory of the controller;

computing, by selection logic of the controller, a DUV-stage parameter set and a driver-stage parameter set jointly from the specification subject to at least one analytical-cutoff constraint and at least one phase-matching-proxy constraint on a high-harmonic-generation gas target;

transmitting, via a first-stage interface of the controller, the DUV-stage parameter set to a DUV intracavity modulation stage operating at a DUV wavelength;

transmitting, via a second-stage interface of the controller, the driver-stage parameter set to a driver-front-end conditioning stage upstream of the high-harmonic-generation gas target, wherein the DUV intracavity modulation stage and the driver-front-end conditioning stage are not in optical series;

computing a source-side estimate, a transmission-product estimate, and a delivered-side estimate associated with an operating point of the two-stage laser photon-source architecture;

associating each of the source-side estimate, the transmission-product estimate, and the delivered-side estimate with a respective tier label drawn from a predetermined tier set stored in the memory; and

emitting, via an export interface of the controller, an output tuple comprising the source-side estimate, the transmission-product estimate, and the delivered-side estimate with the respective tier labels,

wherein emission of the delivered-side estimate via the export interface is inhibited when one or more of the source-side estimate, the transmission-product estimate, and the respective tier labels associated therewith is absent.

**15.** The method of claim 14, wherein the analytical-cutoff constraint is derived from a cutoff relation of the form E_cut = 3.17 · U_p + I_p.

**16.** The method of claim 14, wherein the phase-matching-proxy constraint comprises a ceiling η_c on an estimated ionization fraction of the high-harmonic-generation gas target.

**17.** The method of claim 14, wherein the DUV wavelength is approximately 193 nanometers or approximately 248 nanometers, and wherein the driver-front-end conditioning stage is configured to condition a driver pulse at a wavelength of approximately 800 nanometers, approximately 1030 nanometers, or a wavelength between approximately 1800 nanometers and approximately 3000 nanometers.

**18.** The method of claim 14, wherein the transmission-product estimate is computed as a product of stated optical-element reflectivities and transmissions of a form R^N · T^M, where N is a count of multilayer-mirror elements of stated reflectivity R and M is a count of foil-filter elements of stated transmission T.

**19.** The method of claim 14, wherein the predetermined tier set comprises at least an analytical tier, a parameterized tier, an architectural tier, and a literature-quoted tier, and wherein the source-side estimate carries a literature-quoted tier label, the transmission-product estimate carries an analytical tier label, and the delivered-side estimate carries a parameterized tier label.

**20.** The method of claim 14, further comprising refusing to emit the output tuple in response to a non-compliant specification input.

**21.** A method performed by a controller for a laser photon-source driver stage, the method comprising:

selecting, by selection logic of the controller, a driver-stage parameter set from a parameter space stored in a memory of the controller subject to at least one analytical-cutoff constraint and at least one phase-matching-proxy constraint on a high-harmonic-generation gas target;

transmitting, via a driver-stage interface of the controller, the driver-stage parameter set to a driver-front-end conditioning stage upstream of the high-harmonic-generation gas target;

computing a source-side estimate, a transmission-product estimate, and a delivered-side estimate associated with an operating point of the high-harmonic-generation gas target;

associating each of the source-side estimate, the transmission-product estimate, and the delivered-side estimate with a respective tier label drawn from a predetermined tier set stored in the memory; and

emitting, via an export interface of the controller, an output tuple comprising the source-side estimate, the transmission-product estimate, and the delivered-side estimate with the respective tier labels,

wherein emission of the delivered-side estimate via the export interface is inhibited when one or more of the source-side estimate, the transmission-product estimate, and the respective tier labels associated therewith is absent.

**22.** The method of claim 21, wherein the analytical-cutoff constraint is derived from a cutoff relation of the form E_cut = 3.17 · U_p + I_p and the phase-matching-proxy constraint comprises a ceiling η_c on an estimated ionization fraction of the high-harmonic-generation gas target.

### Alternative Independent Claims

The following alternative independent claim is retained as a narrower independent track directed to the tier-labeled reporting construct and the emission-inhibit gate independent of the two-stage or driver-stage coordination features.

**23.** An apparatus for reporting photon-flux estimates of a laser photon-source, the apparatus comprising:

a memory storing a predetermined tier set;

computation logic configured to compute a source-side estimate derived from a literature-anchored value stored in the memory, a transmission-product estimate computed as a product of stated optical-element reflectivities and transmissions, and a delivered-side estimate formed as a product of the source-side estimate and the transmission-product estimate; and

an export interface configured to emit an output tuple comprising the source-side estimate, the transmission-product estimate, and the delivered-side estimate, each of the source-side estimate, the transmission-product estimate, and the delivered-side estimate carrying a respective tier label drawn from the predetermined tier set,

wherein the export interface is further configured to inhibit emission of the delivered-side estimate when one or more of the source-side estimate, the transmission-product estimate, and the respective tier labels associated therewith is absent.

**24.** The apparatus of claim 23, wherein the predetermined tier set comprises at least an analytical tier, a parameterized tier, an architectural tier, and a literature-quoted tier, and wherein the source-side estimate carries a literature-quoted tier label, the transmission-product estimate carries an analytical tier label, and the delivered-side estimate carries a parameterized tier label.

**25.** The apparatus of claim 23, wherein the export interface is further configured to refuse to emit the output tuple in response to a non-compliant input.

---

## ABSTRACT

A controller and method for a programmable optical-transfer-function control plane across physically distinct optical stages of a laser photon-source architecture. The controller includes a memory storing a shared parameter space and a predetermined tier set, a first-stage interface to a DUV intracavity modulation stage, a second-stage interface to a driver-front-end conditioning stage upstream of a high-harmonic-generation gas target, selection logic that computes the two parameter sets jointly subject to a cutoff-target constraint and a phase-matching-proxy constraint, and an export interface that emits a three-part tier-labeled output tuple comprising a source-side estimate, a transmission-product estimate, and a delivered-side estimate. The export interface inhibits emission of the delivered-side estimate in the absence of the source-side estimate, the transmission-product estimate, or their tier labels. The DUV intracavity modulation stage and the driver-front-end conditioning stage are not in optical series. Backup and alternative independent claims cover driver-stage-only and reporting-only embodiments.

---

## APPENDIX — EXCLUSIONS AND DO-NOT-DRIFT DISCIPLINE (CARRIED FROM PRIOR WORKING DOCUMENTS)

### Exclusions (never in any claim)

- Photon-flux magnitudes, brightness, dose, or throughput values.
- Extreme-ultraviolet-source apparatus naming in any form.
- Lithography applicability, including wafer, high-volume manufacturing, or patterning language.
- Integrated-device phrasing such as "integrated into a single optical assembly", "single cavity containing both stages", or "co-located stages".
- Cavity-enhanced function for the DUV intracavity modulation stage.
- Operation of a two-dimensional-material modulation element beyond a native absorption edge.
- Numerical resolution, line-edge-roughness, dose-latitude, or throughput values derived from point-spread-function or resist modules.
- Single-atom efficiency exponent range as a numerical claim element.
- Any standalone statement of E_cut = 3.17 · U_p + I_p as a claim element; the relation appears only inside a constraint-computation step.

### Prohibited verbs and phrases for tier labels

Never: display, show, present, render, visualize, flag, annotate, indicate to a user, user interface.
Always: emit, transmit, store, associate, inhibit emission of, gate on, refuse to emit.

### Prohibited competitive-positioning phrases

Never, whenever placed near laser-produced-plasma, ASML, extreme-ultraviolet source, lithography, high-volume manufacturing, or intermediate focus: replaces, alternative to, comparable to, equivalent to, on par with.

### Language traps and safe substitutes

1. Extreme-ultraviolet-source overclaim: avoid apparatus-level naming as an extreme-ultraviolet source. Safe: a harmonic-generation stage configured to produce harmonic orders within one or more of the vacuum-ultraviolet, extreme-ultraviolet, and soft-X-ray bands.

2. Integrated-device implication: avoid shared-cavity, shared-mirror, or shared-optical-path phrasing. Safe: the first stage and the second stage are coupled through the selection logic and are not in optical series.

3. Flux or brightness implication from analytical models: avoid scalar delivered-flux language. Safe: the controller reports an estimated delivered photon count as a product of a literature-anchored source-side estimate and an analytically computed transmission-product estimate, each labeled with its epistemic tier drawn from the predetermined tier set.

4. Cavity-enhanced HHG conflation: avoid language that could be read as equating the DUV intracavity stage with a femtosecond enhancement cavity at the driver wavelength. Safe: the DUV intracavity modulation stage is not configured to enhance, build up, or recirculate a driver pulse of the high-harmonic-generation gas target and is not in optical series with a driver path of the gas target.

5. Point-spread-function and resist numerical-performance implication: omit from the claim set; include only as background.

6. §101 presentation-of-information framing: avoid describing tier labels as displayed, shown, or user-facing. Safe: frame as a controller-enforced export-interface gate with emission inhibit on the absence of the source-side estimate, the transmission-product estimate, or their tier labels.

### Per-paragraph and per-caption drafting rule (carried into this draft)

Every embodiment paragraph in this specification ends with one sentence naming what the embodiment does not demonstrate. Every drawing description ends with one sentence naming what the drawing does not represent. These closing sentences are the single most effective written-description defense against overclaim attacks.

---

*End of clean integrated patent draft.*
