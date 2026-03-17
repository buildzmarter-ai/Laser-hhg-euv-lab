"""Citation rendering system for the Laser-HHG-EUV Lab platform.

Provides:
  - CSS for citation footnotes, tooltips, and the references panel
  - JavaScript for interactive citation hover/click behavior
  - Python helpers to inject citations into page HTML
  - A references footer section generator
"""

import re
from backend.references import REFERENCES, CLAIMS


# ── CSS for citations ─────────────────────────────────────────────────

CITATION_CSS = """
/* Citation superscript links */
.cite-ref {
    color: #3b82f6;
    cursor: pointer;
    font-size: 11px;
    vertical-align: super;
    line-height: 0;
    padding: 0 1px;
    font-weight: 600;
    text-decoration: none;
    border-bottom: 1px dotted #3b82f6;
    transition: color 0.15s;
    position: relative;
}
.cite-ref:hover {
    color: #1d4ed8;
    border-bottom-color: #1d4ed8;
}

/* Tooltip on hover */
.cite-tooltip {
    display: none;
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: #1e293b;
    color: #e2e8f0;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 400;
    line-height: 1.4;
    white-space: normal;
    width: 320px;
    max-width: 90vw;
    z-index: 1000;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    pointer-events: none;
}
.cite-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: #1e293b;
}
.cite-ref:hover .cite-tooltip {
    display: block;
}
.cite-tooltip .cite-type {
    display: inline-block;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 1px 5px;
    border-radius: 3px;
    margin-bottom: 4px;
    font-weight: 700;
}
.cite-type-patent { background: #7c3aed22; color: #a78bfa; }
.cite-type-article { background: #3b82f622; color: #60a5fa; }
.cite-type-book { background: #10b98122; color: #34d399; }
.cite-type-technology { background: #f59e0b22; color: #fbbf24; }

/* References panel at bottom of page */
.references-panel {
    background: #f1f5f9;
    border-top: 2px solid #e2e8f0;
    padding: 24px 32px;
    margin-top: 32px;
}
.references-panel h3 {
    font-size: 14px;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
}
.references-panel .ref-list {
    columns: 1;
    column-gap: 32px;
}
@media (min-width: 900px) {
    .references-panel .ref-list { columns: 2; }
}
.references-panel .ref-entry {
    font-size: 12px;
    color: #64748b;
    line-height: 1.5;
    margin-bottom: 6px;
    break-inside: avoid;
    padding-left: 28px;
    text-indent: -28px;
}
.references-panel .ref-entry .ref-num {
    color: #3b82f6;
    font-weight: 700;
    min-width: 24px;
    display: inline-block;
}
.references-panel .ref-entry a {
    color: #3b82f6;
    text-decoration: none;
}
.references-panel .ref-entry a:hover {
    text-decoration: underline;
}

/* Claim badge styling */
.claim-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    background: #1e3a5f;
    color: #93c5fd;
    cursor: help;
    position: relative;
    letter-spacing: 0.3px;
}
.claim-badge:hover .claim-tooltip {
    display: block;
}
.claim-tooltip {
    display: none;
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: #1e293b;
    color: #e2e8f0;
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 400;
    white-space: nowrap;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    pointer-events: none;
    margin-bottom: 4px;
}
.claim-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 5px solid transparent;
    border-top-color: #1e293b;
}
"""


def render_citation(num: int) -> str:
    """Render a single citation as an interactive superscript with tooltip."""
    ref = REFERENCES.get(num)
    if not ref:
        return f'<sup class="cite-ref">[{num}]</sup>'

    type_class = f"cite-type-{ref['type']}"
    tooltip_html = (
        f'<span class="cite-tooltip">'
        f'<span class="cite-type {type_class}">{ref["type"]}</span><br>'
        f'{ref["full"]}'
        f'</span>'
    )
    return (
        f'<a class="cite-ref" href="#ref-{num}" title="{ref["short"]}">'
        f'[{num}]'
        f'{tooltip_html}'
        f'</a>'
    )


def render_claim_badge(claim_num: int) -> str:
    """Render a Claim reference as a styled badge with tooltip."""
    desc = CLAIMS.get(claim_num, "")
    tooltip = ""
    if desc:
        tooltip = f'<span class="claim-tooltip">Claim {claim_num}: {desc}</span>'
    return (
        f'<span class="claim-badge">'
        f'Claim {claim_num}'
        f'{tooltip}'
        f'</span>'
    )


def process_citations(html: str) -> str:
    """Replace all [cite: ##] patterns in HTML with interactive citation footnotes."""
    def _replace(m):
        num = int(m.group(1))
        return render_citation(num)
    return re.sub(r'\[cite:\s*(\d+)\]', _replace, html)


def process_claim_refs(html: str) -> str:
    """Replace 'Claim N' text references with styled badges (only in prose, not headings)."""
    def _replace(m):
        num = int(m.group(1))
        if num in CLAIMS:
            return render_claim_badge(num)
        return m.group(0)
    # Only match "Claim N" not inside HTML tags or headings
    return re.sub(r'(?<![<\w/])Claim (\d+)(?![^<]*>)', _replace, html)


def build_references_footer(used_refs: list[int] | None = None) -> str:
    """Build the references panel HTML for the bottom of a page.

    Args:
        used_refs: List of citation numbers to include. If None, includes all.
    """
    if used_refs is None:
        refs_to_show = sorted(REFERENCES.keys())
    else:
        refs_to_show = sorted(set(used_refs))

    if not refs_to_show:
        return ""

    entries = []
    for num in refs_to_show:
        ref = REFERENCES.get(num)
        if not ref:
            continue
        text = ref["full"]
        url = ref.get("url")
        if url:
            text += f' <a href="{url}" target="_blank" rel="noopener">[link]</a>'
        entries.append(
            f'<div class="ref-entry" id="ref-{num}">'
            f'<span class="ref-num">[{num}]</span> {text}'
            f'</div>'
        )

    return (
        f'<div class="references-panel">'
        f'<h3>References</h3>'
        f'<div class="ref-list">{"".join(entries)}</div>'
        f'</div>'
    )


def extract_citation_numbers(html: str) -> list[int]:
    """Extract all citation numbers used in an HTML string."""
    return [int(m) for m in re.findall(r'\[cite:\s*(\d+)\]', html)]


def inject_citations(html: str, extra_refs: list[int] | None = None) -> str:
    """Full pipeline: process [cite: ##] references, add CSS and references footer.

    This is the main entry point. Call it on the final HTML before returning
    from a route handler.

    Args:
        html: Complete HTML page string
        extra_refs: Additional reference numbers to include in the footer
                    beyond those found in [cite: ##] patterns
    """
    # Extract which refs are used
    used = extract_citation_numbers(html)
    if extra_refs:
        used.extend(extra_refs)

    # Process citation markers
    html = process_citations(html)

    # Inject CSS into <head>
    css_block = f"<style>{CITATION_CSS}</style>"
    if "<head>" in html:
        html = html.replace("<head>", f"<head>\n{css_block}", 1)
    elif "</head>" in html:
        html = html.replace("</head>", f"{css_block}\n</head>", 1)
    else:
        # No head tag — prepend
        html = css_block + html

    # Inject references footer before </body>
    if used:
        footer = build_references_footer(used)
        if "</body>" in html:
            html = html.replace("</body>", f"{footer}\n</body>", 1)
        else:
            html += footer

    return html
