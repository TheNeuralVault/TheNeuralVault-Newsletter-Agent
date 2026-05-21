#!/usr/bin/env python3
"""
TheNeuralVault-Newsletter-Agent
Weekly newsletter production engine.
NEVER sends. NEVER calls email APIs.
Produces drafts for operator approval only.
Five-tier provenance on every factual claim.
"""

import os
import sys
from datetime import datetime
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"]
)

SYSTEM_PROMPT = """You are TheNeuralVault-Newsletter-Agent.
You produce weekly newsletter drafts for a human-AI collaboration
business federation. You NEVER send anything. You produce drafts only.

TheNeuralVault brand voice:
- Visionary but grounded
- Collaborative — treats AI as partner not tool
- Resourceful — achieves maximum with minimum
- Principled — transparent provenance on everything
- Empowering — gives readers tools they can use immediately

Newsletter doctrine:
- The inbox is sacred — earn your place there every week
- Value first — teach, inspire, or solve something real
- One big idea per issue — never scatter attention
- Subject lines are promises — keep them inside the issue
- Under 600 words — respect the reader's time
- One clear call to action — never more than one
- Consistency beats brilliance — show up every week

Five-tier provenance for newsletter claims:
T1 VERIFIED    — real subscriber metrics from Beehiiv API
T2 EXTRACTED   — from primary email research with citation
T3 INFERRED    — patterns from content performance over time
T4 MODELED     — projected engagement (always disclose as estimate)
T5 FOUNDATIONAL— core newsletter principle

Rules you cannot break:
- Never claim to send or publish
- Never call any email API
- Tag every factual claim T1-T5
- Flag DEFAULT for thin evidence
- Flag CONFLICT for contradicting signals
- Brand Bible voice governs every word
- Operator approves before anything goes live

Output format — follow exactly:

---
# NEWSLETTER DRAFT — [EDITION]
**Status:** PENDING OPERATOR APPROVAL
**Date:** [date]
**Agent:** TheNeuralVault-Newsletter-Agent

---
## SUBJECT LINE OPTIONS (choose one)
1. [Option 1] — [strategy: curiosity/benefit/question]
2. [Option 2] — [strategy]
3. [Option 3] — [strategy]

## PREVIEW TEXT OPTIONS (choose one)
1. [Option 1 — extends subject line naturally, under 90 chars]
2. [Option 2]
3. [Option 3]

---
## ISSUE BODY

[Complete newsletter issue — under 600 words]
[Brand Bible voice throughout]
[One big idea]
[One actionable intelligence item]
[One call to action]
[Human moment — real vision behind the system]

---
## PROVENANCE REPORT
[Every factual claim tagged T1-T5]
[DEFAULT flags disclosed]
[CONFLICT flags if any]

---
## OPERATOR CHECKLIST
- [ ] Subject line selected
- [ ] Preview text selected
- [ ] Content approved
- [ ] Brand voice confirmed
- [ ] Call to action confirmed
- [ ] Ready to copy to Beehiiv: YES / NO
---"""

def read_file_bounded(path, max_chars=1500):
    """Read file with bounded context — prevents context overflow"""
    if path and os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
        if len(content) > max_chars:
            return content[:max_chars] + "\n[Truncated — bounded context]"
        return content
    return None

def generate_issue(edition, intel, seo, brand, article):
    """Generate newsletter issue — fresh bounded context"""
    print(f"\nGenerating issue: {edition}...")

    # Build bounded context from upstream inputs
    context_parts = []

    if article:
        context_parts.append(f"LATEST WRITER ARTICLE (primary content source):\n{article}")
    if intel:
        context_parts.append(f"MARKET INTELLIGENCE (trending signals):\n{intel}")
    if seo:
        context_parts.append(f"SEO BRIEF (keyword targets and topics):\n{seo}")
    if brand:
        context_parts.append(f"BRAND BIBLE EXCERPT (voice and tone guide):\n{brand}")

    context = "\n\n---\n\n".join(context_parts) if context_parts else "No upstream context available — generate from TheNeuralVault philosophy directly."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""Produce a complete newsletter issue for TheNeuralVault.

Edition: {edition}
Date: {datetime.now().strftime('%Y-%m-%d')}

Federation context (use to inform the issue):
{context}

Requirements:
- Under 600 words in the issue body
- Three subject line options with strategy notes
- Three preview text options under 90 characters each
- One big idea clearly explained
- One actionable item the reader can use today
- One human moment connecting to the founder vision
- One clear call to action
- Brand Bible voice throughout
- Five-tier provenance tags on every factual claim
- Complete operator checklist at the end

Remember: You produce a draft only.
The operator reads, approves, and publishes manually on Beehiiv.
You never send. You never call any email API."""
        }
    ]

    result = ""
    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=messages,
        temperature=0.7,
        max_tokens=3000,
        stream=True
    )

    for chunk in completion:
        if not chunk.choices:
            continue
        if chunk.choices[0].delta.content is not None:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            result += text

    print(f"\n[✓] Issue {edition} draft complete.")
    return result

def main():
    edition = sys.argv[1] if len(sys.argv) > 1 else f"issue-{datetime.now().strftime('%Y-%m-%d')}"
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"drafts/newsletter-{edition}.md"
    intel_path = sys.argv[3] if len(sys.argv) > 3 else None
    seo_path = sys.argv[4] if len(sys.argv) > 4 else None
    brand_path = sys.argv[5] if len(sys.argv) > 5 else None
    article_path = sys.argv[6] if len(sys.argv) > 6 else None

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("=" * 60)
    print("TheNeuralVault-Newsletter-Agent")
    print(f"Edition: {edition}")
    print(f"Started: {timestamp}")
    print("SEND PERMANENTLY BLOCKED — draft only")
    print("Five-tier provenance: ACTIVE")
    print("=" * 60)

    # Load all upstream inputs with bounded context
    intel = read_file_bounded(intel_path, 1200)
    seo = read_file_bounded(seo_path, 1000)
    brand = read_file_bounded(brand_path, 800)
    article = read_file_bounded(article_path, 1500)

    print(f"Intel loaded:   {'YES' if intel else 'NO'}")
    print(f"SEO loaded:     {'YES' if seo else 'NO'}")
    print(f"Brand loaded:   {'YES' if brand else 'NO'}")
    print(f"Article loaded: {'YES' if article else 'NO'}")

    result = generate_issue(edition, intel, seo, brand, article)

    # Check for flags
    conflicts = "CONFLICT" in result.upper()
    defaults = "DEFAULT" in result.upper()

    # Write output
    os.makedirs(
        os.path.dirname(output_file) if os.path.dirname(output_file) else "drafts",
        exist_ok=True
    )

    with open(output_file, "w") as f:
        f.write(f"# TheNeuralVault Newsletter Draft\n")
        f.write(f"**Edition:** {edition}\n")
        f.write(f"**Date:** {timestamp}\n")
        f.write(f"**Agent:** TheNeuralVault-Newsletter-Agent v1.0\n")
        f.write(f"**Status:** PENDING OPERATOR APPROVAL\n")
        f.write(f"**SEND BLOCKED:** Yes — operator publishes manually\n\n")
        f.write("---\n\n")
        f.write("> OPERATOR: Read, approve, then copy to Beehiiv manually.\n")
        f.write("> This agent never sends. You always publish.\n\n")
        f.write("---\n\n")
        f.write(result)

    print("\n" + "=" * 60)
    print(f"Draft saved: {output_file}")
    print("STATUS: PENDING OPERATOR APPROVAL")
    print("NEXT: Open in Drive, approve, copy to Beehiiv manually")
    if conflicts:
        print("⚠ CONFLICTS detected — review before publishing")
    if defaults:
        print("◈ DEFAULTS flagged — thin evidence disclosed")
    print("=" * 60)

if __name__ == "__main__":
    main()
