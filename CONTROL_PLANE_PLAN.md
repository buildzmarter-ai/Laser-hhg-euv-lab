# Control-Plane Surface — PLAN

**Matter:** Laser-HHG-EUV Lab ↔ vdw-polaritonics-lab — programmable optical-transfer-function control-plane.
**As of:** 2026-04-16 (session close).
**Purpose:** prioritize next-session work and surface candidate new lanes for confirmation.

---

## 1. Active lane — Patent-positioning / drafting

**Status:** counsel-ready base draft complete and pushed. Next actions are external (prior-art landscape, counsel intake) or internal edit passes driven by counsel feedback.

**Open tasks in this lane:**

| Priority | Task | Owner | Notes |
| --- | --- | --- | --- |
| P0 | Commission targeted prior-art landscape pull on the four clusters (CE-HHG; pulse-shaping-for-HHG; vdW intracavity optical control; simulation/provenance reporting) | User | Vendor selection pending; budget unconfirmed |
| P0 | Intake-handoff to drafting counsel with `patent_draft_2026-04-16.md` as primary document and the other four as depth record | User | Draft counsel-intake cover note if requested |
| P1 | On receipt of landscape results, amend spec with cluster-specific disclaimers before claims freeze | Claude + Counsel | Hold for landscape output |
| P1 | Decide whether to file provisional or full utility; decision driven by landscape output and priority-date pressure | User + Counsel | — |
| P2 | Review whether `.venv/` should be added to `.gitignore` to clean working-tree noise | User | Separate follow-up commit, not part of patent package |
| P2 | Consider drafting Figure 2 (controller architecture schematic) and Figure 3 (three-part flux-budget reporting construct) as formal patent drawings when drafting counsel advises | Claude + Counsel | Figure list already locked in the handoff packet |

## 2. Candidate new lanes (need user confirmation before opening)

The following lanes are proposed but not opened. Each would be a distinct work track with its own repo or subfolder if opened.

### Candidate lane A — vdw-polaritonics-lab companion patent track

**Premise:** the vdW cavity side has its own defensible invention surface at the DUV intracavity stage, independent of the HHG driver-front-end conditioning claim. A companion application directed at intracavity DUV programmable modulation (without the HHG coupling) could be filed in parallel.

**Open decision:** file together as one application with multiple claim tracks, or file as a companion application under the same priority date? Benefits and risks depend on landscape output.

### Candidate lane B — Counsel-intake cover note drafting

**Premise:** the handoff packet is the technical document; counsel intake typically also wants a one-page cover letter that frames the matter in prosecution-oriented language for the drafting attorney.

**Open decision:** do you want Claude to draft this cover note now, or does counsel have a preferred intake format?

### Candidate lane C — Provisional-application-text preparation

**Premise:** if the decision is to file provisional first, `patent_draft_2026-04-16.md` can be lightly reformatted into USPTO provisional-application structure (spec + drawings + optional claims) and delivered as a ready-to-file packet.

**Open decision:** file timing and counsel preference.

### Candidate lane D — Foreign-filing strategy (EPO emphasis)

**Premise:** the tier-labeled reporting track has §101 exposure in the US but a technical-effect path in the EPO. A foreign-filing strategy memo would lock the EPO-friendly framing before Paris Convention deadlines.

**Open decision:** is foreign filing in scope? If yes, which jurisdictions (EPO, JPO, CNIPA)?

### Candidate lane E — Hardening vdw-polaritonics-lab repo to match Laser-hhg-euv-lab posture

**Premise:** the patent package assumes both repos are on the same epistemic-tiered posture. If the vdW-polaritonics-lab repo is not yet hardened to the same standard, its posture could undermine the patent narrative during counsel diligence.

**Open decision:** does vdw-polaritonics-lab need a parallel hardening pass before counsel sees the package?

## 3. Dormant lanes (closed for now; can be reopened)

- Industrial-EUV-source claim track — permanently excluded per locked premises; do not reopen.
- HVM-lithography applicability claim track — permanently excluded per locked premises; do not reopen.
- PSF / resist numerical-performance claim track — permanently excluded per locked premises; do not reopen.
- Multihead writer-array packaging as a claim surface — closed; retained as background only.
- Fleet economics as claim subject matter — closed; retained as background in the repo, not in the patent application.

## 4. Pre-filing checklist (carried across sessions)

- [ ] Prior-art landscape output received and integrated.
- [ ] Counsel identified and engaged.
- [ ] Provisional-vs-utility decision locked.
- [ ] Foreign-filing strategy locked.
- [ ] Figure 2 and Figure 3 drafted as formal drawings.
- [ ] Non-enablement closing sentences reviewed on every embodiment and caption.
- [ ] Abstract reviewed for 150-word ceiling.
- [ ] Cross-reference-to-related-applications section populated.
- [ ] Inventorship and assignment resolved.

## 5. Session-boot instruction for next session

On boot, read, in order:
1. `CONTROL_PLANE_STATE.md` — what exists.
2. `CONTROL_PLANE_GUARDRAILS.md` — what cannot drift.
3. `CONTROL_PLANE_PLAN.md` — what to do next.
4. Most recent `DELTA_LOG_YYYY-MM-DD.md` — what changed last session.
5. `patent_draft_2026-04-16.md` — counsel deliverable anchor.

Do not broaden the claim structure without an explicit user directive; drift protection is enforced by `CONTROL_PLANE_GUARDRAILS.md`.

---

*End of PLAN surface.*
