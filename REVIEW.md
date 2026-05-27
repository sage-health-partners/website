# Sage Health Website — End-to-End Review

**Date:** 2026-05-24
**Reviewer:** Expert marketing / brand / customer-messaging audit
**Scope:** 17 HTML pages, `styles.css`, `main.js` — total 6,221 lines
**Status:** Review only. No files modified.

---

## Executive Summary

The Sage Health website does a great many things very well. The writing is **operator-grade** — confident, declarative, specific, free of marketing hedge-language — and the core positioning ("Your practice, operating at its full potential" / "enterprise-grade AI + advisory, for the independent practice") is genuinely differentiated and credibly delivered. The visual system is consistent: a single design-token CSS file (`styles.css`, well-organized), shared header/footer pattern, an icon sprite reused across pages. Page-level information architecture inside `/solutions/*` is excellent. The Insights articles are substantive — these read as written by operators, not by marketing.

However, the site is **not ready to ship to prospects in its current state.** Two material problems stand in the way:

1. **The site appears mid-migration and the old structure has not been deleted.** Two pages at the repo root — `advisory.html` and `technology.html` — are orphaned from the main navigation but still actively linked from `about.html`'s CTA and from each other's footers. They use a **different set of product names** than the canonical `/solutions/ai/*` pages ("Voice Agent" vs. "Voice Scheduling Agent," "Confirmation Agent" vs. "Smart Confirmations," "Eligibility Agent" vs. "Eligibility Intelligence"). A prospect who clicks "Explore Advisory" on the About page will land inside the *old* site and read different product copy than the prospect who used the top nav. This is the single highest-risk finding in the review.

2. **The brand-voice rules are partially honored.** Several pillar rules from the stated brand voice ("no consultant language," "no negatives to define ourselves") are violated in specific, fixable places — most prominently the About page's "Operators, not consultants" value card, and a repeated "Most consulting engagements deliver a deck / end at the recommendation / get skimmed once and shelved" pattern that appears on at least three Advisory pages. The site defines itself by what it isn't in the very places it's trying hardest to differentiate.

A handful of smaller issues — a broken/duplicate Insights card, an undefined "Active Partnership tier," "Operations Assessment" used interchangeably with "Front Desk Evaluation Framework," a non-functional contact form — are easy to fix once the structural duplication above is resolved.

**Priority signal:** The Critical-tier items below should all be resolved before any prospect URL is shared. Fixing them is roughly half a day of editing once decisions are made.

---

## Page-by-Page Analysis

### Home — `index.html`

**Messaging:** Excellent. Hero ("Your practice, operating at its full potential") is the brand's strongest single line and lands at the top. Opportunity section quantifies leakage in dollar terms. Patient-journey graphic is original, visual, ownable.
**Customer Alignment:** Strong. Speaks to the practice owner directly. The $125K–250K-per-practice framing is the right magnitude to register without feeling speculative.
**Value Prop Clarity:** Clear. Two cards on dark surface (Advisory / Technology) make the two halves of the offer immediately scannable. Both cards have explicit product nesting (Evaluation Framework / SOPs / Strategic Transformation under Advisory; Practice Agentic Suite / Practice BI under Technology).
**Brand Voice:** Mostly compliant. Two soft issues:
- Hero meta tag (line 104): `Fortune-500 caliber AI`. Other pages say `Fortune 500 health systems` (no hyphen) or `the nation's largest health systems`. Pick one phrasing.
- Hero tag (line 93): `Sage Health · Enterprise AI for Independent Practices` — but everywhere else the term is `Enterprise-grade AI`. Trivial but visible.
**Content Quality:** No placeholders, no TODOs. Real copy throughout.
**Recommended Changes:**
1. Standardize on either "Fortune 500" or "the nation's largest health systems" — both work, but use one. Recommendation: lean on "the nation's largest health systems" because it's evocative and avoids the brand-association risk of the Fortune-500 trademark phrasing.
2. Change the hero tag at line 93 to read `Enterprise-grade AI for Independent Practices` for consistency with every other surface.
3. The "Active Partnership" tile in the flow (line 304) introduces a product term that's never defined elsewhere on the site except a passing reference in Contact's FAQ. Either define it (it's the engagement tier where both AI + Advisory + monthly review come together) or rename it to something self-evident like "Ongoing Partnership."

---

### Solutions Hub — `solutions/index.html`

**Messaging:** Best-articulated positioning page on the site. The "Machines do the repetition. Humans do the judgment." H2 captures the dual offering in seven words.
**Customer Alignment:** Perfect for the practice owner who is "shopping" between options.
**Value Prop Clarity:** The side-by-side panels (Advisory vs. AI) explicitly tell the reader they can pick one, both, or start with either. This addresses a real buyer hesitation — feeling forced into a bundled engagement.
**Brand Voice:** Compliant.
**Content Quality:** Clean. Real metrics on the journey graphic (color-coded categories).
**Recommended Changes:** None at the page level. This page is launch-ready.

---

### AI Solutions Overview — `solutions/ai/index.html`

**Messaging:** Strong "intelligence gap, closed" framing. The "10× more inbound coverage / 24/7 / $0 EHR replacement" trio is well-chosen.
**Customer Alignment:** Good. Some technical language ("LLM · TTS · Routing," "X12 270/271") shows up later, which is acceptable on a product page but should not be the lead.
**Value Prop Clarity:** Clear — two products, one platform.
**Brand Voice:** Mostly compliant. The Umair pull-quote (lines 156–161) is excellent and on-brand.
**Content Quality:** No issues.
**Recommended Changes:**
1. The hero-meta tag `Built for scale · Deployed for you` (line 81) is a minor inconsistency vs. the home page's `Turnkey · Fully managed`. Pick one of these meta tag formats as the canonical pattern and use it on every product hero.

---

### Practice Agentic Suite — `solutions/ai/agentic-suite.html`

**Messaging:** Best product page on the site. The "Patient → Agent → EHR. That's the whole architecture." section sells the technical credibility without forcing jargon to the surface.
**Customer Alignment:** Good. The "60% of front-desk time" problem statement (line 95) is exactly how a practice owner would frame it.
**Value Prop Clarity:** Clear. Three agents named and described in customer language.
**Brand Voice:** Largely compliant — but one repeat-offender line at 294: `"We don't do slides."` This is technically a negation-as-positioning pattern, but it's defensible because it's defining the *demo experience*, not the brand. Marginal.
**Content Quality:** Customer quote at line 282 is anonymized ("Practice Administrator · Multi-Specialty Group · Houston") — credible for a quiet launch but lower trust than a named source. Confirm the quote is accurate or replace with a published source.
**Recommended Changes:**
1. Verify the customer testimonial at line 282 is real and quote-cleared. If it isn't, it should not ship. If it is, push to add the practice name when permission is in hand.
2. Roadmap list (lines 234–239) uses status labels "Live" / "Pilot" / "Roadmap" — verify this is the actual state. "Pilot" is a commitment.

---

### Practice BI — `solutions/ai/practice-bi.html`

**Messaging:** Good. "Monday-morning operational clarity" is a great line. Sample dashboard is visually strong.
**Customer Alignment:** Strong. The "EHR has reports. The phone system has reports. The clearinghouse has reports." opening (line 93) is exactly the lived experience.
**Value Prop Clarity:** Clear.
**Brand Voice:** **One violation.** Pull quote at line 220 opens with "Most practice reports get pulled monthly, emailed to nobody, and decided by gut feel." This is the "define-ourselves-by-what-others-do-wrong" pattern.
**Content Quality:** Sample dashboard metrics look like sample data (94% answer rate, 8.2% no-show, 98% eligibility) — these are aspirational top-quartile numbers. Make sure they're labeled as illustrative, not as Sage Health customer averages. The "Lakeside Family Practice · Live" attribution suggests a real customer, which would be misleading if it's a mock.
**Recommended Changes:**
1. Rewrite the pull quote at line 220 to lead with what Practice BI *is*, not what other reports aren't. Example: `"Practice BI is the dashboard you open Monday morning — and keep open all week. Every metric that moves revenue, in one place, in real time."`
2. Label "Lakeside Family Practice" explicitly as a sample/anonymized example (e.g., `Sample dashboard · Anonymized customer data`) — or remove the practice name entirely. The current "Live" badge implies live customer data.

---

### Advisory Solutions Overview — `solutions/advisory/index.html`

**Messaging:** Strong. "Evidence before opinion. Observation before recommendation." captures the firm's discipline in eight words.
**Customer Alignment:** Excellent for the practice owner. Tahir pull-quote (line 149) is on-voice except for the negation it leads with.
**Value Prop Clarity:** The three-engagement card grid is clear; each card has its own deep-dive page.
**Brand Voice:** **Two violations.**
- Line 149 pull quote: `"Most consulting engagements deliver a deck. We deliver a document you can act on Tuesday morning..."` This is the most prominent place the brand defines itself by what consultants do wrong. It's also wearing the founder's name, which makes it land harder.
- The repeated word "consulting" inside the advisory site implicitly invites the reader to categorize Sage Health as consulting — the very thing the brand voice rule says to avoid.
**Content Quality:** Clean.
**Recommended Changes:**
1. Rewrite the Tahir pull quote without the "Most consulting engagements" frame. Example: `"We deliver a document you can act on Tuesday morning — with the dollars sized, the priorities ranked, and the next step named."` The point lands harder without the contrast scaffolding.
2. Audit the use of the word "consulting" globally — replace where the context invites Sage Health to be seen as a consultancy.

---

### Front Desk Evaluation Framework — `solutions/advisory/evaluation-framework.html`

**Messaging:** Very strong methodology page. Five-pillar table is concrete and ownable.
**Customer Alignment:** The "half-day on-site, 10-business-day report" specificity is exactly what a practice owner wants to know.
**Value Prop Clarity:** Excellent. The sample-report visual (table of contents with page numbers) is a great way to show the deliverable without producing the actual PDF.
**Brand Voice:** **One violation.** Line 170: `"Most consulting reports get skimmed once and shelved. Ours are structured..."` — same pattern as the advisory hub page.
**Content Quality:** "Lakeside Family Practice · Q2 2026" sample-report label is good — explicitly marked "Sample Report."
**Recommended Changes:**
1. Rewrite line 170 to lead with the structure choice instead of the contrast. Example: `"Our reports are structured the way an operator wants to read them: executive summary up front, prioritized actions in the middle, supporting data at the back. Roughly 30 pages of substance."`

---

### Operational SOPs — `solutions/advisory/operational-sops.html`

**Messaging:** Strong. "Processes that scale beyond any single employee" is a clean reframing of a tribal-knowledge problem most practice owners feel.
**Customer Alignment:** The "$17–18/hour vs $22 retail" pay-benchmark detail (line 87) is exactly the operational language that signals credibility.
**Value Prop Clarity:** Clear. The "4–6 weeks → 3–5 days" onboarding comparison bar (lines 122–131) is one of the strongest single visualizations on the site.
**Brand Voice:** Compliant. No negation violations on this page.
**Content Quality:** The footnote at line 132 ("Based on Sage Health engagements with multi-physician independent practices") implies a track record. Verify this is substantiated — if Sage Health was founded in 2024 and this is the first prospect-facing deployment of the site, the customer base may not yet support the claim.
**Recommended Changes:**
1. Verify the "Based on Sage Health engagements" attribution at line 132 — if there isn't a substantiated track record yet, weaken to "Based on industry benchmarks and Sage Health pilot deployments" or similar.

---

### Strategic Transformation — `solutions/advisory/strategic-transformation.html`

**Messaging:** Strong. The "Assess. Implement. Optimize." three-card structure is clear.
**Customer Alignment:** The "We're a force multiplier, not a substitute for leadership" candor (line 182) is well-judged — it disqualifies the wrong-fit buyer rather than overpromising.
**Value Prop Clarity:** The "Who It's For / Not for everyone" two-card structure (lines 186–195) is exemplary buyer-honesty.
**Brand Voice:** **One violation.** Line 170 pull quote: `"Most consulting engagements end at the recommendation. Ours start there."` Same pattern again.
**Content Quality:** Clean.
**Recommended Changes:**
1. Rewrite the line 170 pull quote without the negation. Example: `"The 90 days are about getting the work done — with monthly check-ins, named owners, and KPIs that have to move. Recommendations are where this engagement starts, not where it ends."`

---

### About — `about.html`

**Messaging:** Founder-led, clear, on-voice. The "real Tuesday" line (line 97) is memorable.
**Customer Alignment:** Good. Founder bios speak to operator credibility.
**Value Prop Clarity:** The "Four principles. Non-negotiable." section is the brand's strongest statement of what it stands for.
**Brand Voice:** **Multiple violations.**
- **Line 119:** `Operators, not consultants.` — the most direct violation on the site. This is the rule literally cited in the brand voice guide ("No 'consultant' language"). The card title needs to be reframed.
- **Line 96:** `"previously required a six-figure consulting engagement and an IT department"` — adjacent to the same pattern.
- **Line 130:** `"We don't serve hospital systems. We don't serve private-equity-rolled-up MSOs."` — technically a negation, but here it's defining the customer focus, which is a different and arguably acceptable use of the pattern. Less critical than line 119 but worth softening.
**Content Quality:** Avatars use initials ("UK," "TA") rather than photos. This is consistent with the design but reduces credibility for a high-trust B2B sale. Optional improvement: add real photos.
**Recommended Changes:**
1. Rewrite the "Operators, not consultants." card title to lead with what Sage Health *is*. Example: `Operator-led, always.` (then body: "The Sage Health partnership includes operating the technology we deploy. Our incentives stay aligned with your outcomes, every month.") The body of the card is already strong; only the title needs editing.
2. Soften "previously required a six-figure consulting engagement" at line 96. Example: `"We bring the assessment frameworks, the SOPs, and the agentic technology that previously lived only inside the budgets of the largest health systems."` Loses nothing, drops the "consulting" framing.
3. **CRITICAL — link target fix at line 202:** The CTA `<a href="advisory.html">Explore Advisory</a>` links to the **orphaned root-level advisory.html**, not the canonical `solutions/advisory/index.html`. This will send the prospect into the old site with the old product names. Update to `solutions/advisory/index.html`.
4. Add real founder photos when available — initials-only avatars work for a beta site but should be the first thing replaced before a real launch.

---

### Contact — `contact.html`

**Messaging:** Strong. "Three steps. Under three weeks." sets clear expectations.
**Customer Alignment:** Form is well-designed; the optional-context text area asks for the right thing.
**Value Prop Clarity:** Clear.
**Brand Voice:** Compliant.
**Content Quality:** **The contact form is non-functional.**
- Line 117: `onsubmit="event.preventDefault();this.querySelector('.form-success').hidden=false;..."` — the form prevents the submit and just toggles a success message. There is no backend, no email, no Formspree, no Resend, no Vercel function. Any prospect who fills this out and trusts the "we'll respond within one business day" message will get zero response. This is the most reputationally damaging single line of code on the site if shipped as-is.
**Recommended Changes:**
1. **CRITICAL — wire the form to a real submission target before showing to anyone.** Options: a serverless function (Vercel/Netlify), a hosted form service (Formspree, Tally, Basin), or a simple mailto fallback. Whatever it is, test it end-to-end.
2. Line 271 FAQ references an `Active Partnership tier` — this term is used here for the first time. Either link to the homepage flow (`index.html#partnership` if you add an anchor) or define it inline.

---

### Technology — `technology.html` ⚠️ ORPHANED

**Messaging:** Inconsistent with the rest of the site. This page was clearly written *before* the `/solutions/*` rewrite and was not deleted or updated.
**Customer Alignment:** Same content quality as elsewhere, but the page is reachable from `about.html` footer/CTA and from each other root-level page.
**Value Prop Clarity:** **The product names are different:**
- This page: `Voice Agent`, `Confirmation Agent`, `Eligibility Agent`
- Canonical `/solutions/ai/agentic-suite.html`: `Voice Scheduling Agent`, `Smart Confirmations`, `Eligibility Intelligence`
A prospect who reads the home page, clicks into `/solutions/ai/`, then clicks an Advisory CTA from About and lands here will read **three different product names for the same agent.**
**Brand Voice:** Hero: `The intelligence powering Fortune 500 health systems` — same Fortune-500 inconsistency.
**Content Quality:** No issues *within the page*. The problem is the page itself.
**Recommended Changes:**
1. **CRITICAL — delete this page.** Add a server-side or HTML meta-refresh redirect to `/solutions/ai/index.html` so any external link, bookmark, or footer reference that still points here lands on the canonical page.

---

### Advisory — `advisory.html` ⚠️ ORPHANED

Same issue as `technology.html`. This page also lives at the root, also isn't in main nav, also is linked from `about.html` and from `technology.html`. Content overlaps with `/solutions/advisory/*` but with the older product framing.

**Recommended Changes:**
1. **CRITICAL — delete this page**, redirect to `/solutions/advisory/index.html`.
2. Update About page CTA (`about.html:202`) and any other internal links pointing to root-level `advisory.html`.

---

### Insights Index — `insights/index.html`

**Messaging:** Clear positioning ("Field notes from the front desk").
**Customer Alignment:** Strong.
**Value Prop Clarity:** N/A — this is a content hub.
**Brand Voice:** Compliant.
**Content Quality:** **Broken card.** Four article cards on the grid:
1. "Why Your Front Desk Is Your Biggest Revenue Lever" → correct file
2. "AI Agents for Independent Practices: A Practical Guide" → correct file
3. "Reducing No-Shows: Why Reminders Aren't Enough" → correct file
4. **"The Voicemail Era is Over"** → links to `why-front-desk-is-your-biggest-revenue-lever.html` — **wrong target.** The article does not exist as a file. A prospect who clicks this card lands on a duplicate of card #1.
**Recommended Changes:**
1. **CRITICAL — either write the "Voicemail Era is Over" article or remove the card.** Until the article exists, the card is a broken promise.

---

### Insights — `ai-agents-independent-practice-guide.html`

**Messaging:** Genuinely substantive. The "what is an AI agent, really" definition is the best plain-English explanation of agents-vs-RPA-vs-chatbots I've read in a vendor context.
**Customer Alignment:** Excellent for a technical-curious practice owner.
**Value Prop Clarity:** Article-level rather than product-level, appropriate for the format.
**Brand Voice:** Compliant. Line 77 uses "AI-enable" inside a quoted vendor pitch (negative framing of *vendors*, not *us*) — acceptable.
**Content Quality:** Substantive, not a thinly veiled sales pitch. The "What to ask when a vendor pitches you" section gives genuinely useful diligence questions.
**Recommended Changes:** None.

---

### Insights — `reducing-no-shows-beyond-reminders.html`

**Messaging:** Strong. "The structural ceiling on no-show rates" reframes the problem in a way most practices haven't heard.
**Customer Alignment:** Excellent.
**Value Prop Clarity:** N/A — content article.
**Brand Voice:** Compliant.
**Content Quality:** The "roughly 65% of no-shows were preventable" stat is a specific claim — should be footnoted to a source or labeled as Sage Health's observation across assessments.
**Recommended Changes:**
1. Add provenance to the no-show breakdown stat at line 85. Either footnote the industry source or attribute to Sage Health field observation.

---

### Insights — `why-front-desk-is-your-biggest-revenue-lever.html`

**Messaging:** This is the article most directly tied to the homepage opportunity stat. Math is laid out clearly.
**Customer Alignment:** Excellent.
**Value Prop Clarity:** N/A.
**Brand Voice:** Compliant.
**Content Quality:** The dollar numbers (e.g., "$95K average annual lifetime-value loss") are specific — verify the methodology if challenged.
**Recommended Changes:** None.

---

## Cross-Site Issues

### 1. Two parallel page hierarchies coexist (Critical)
- **Canonical (in main nav):** `/solutions/{ai,advisory}/*` — 7 pages
- **Orphaned (at root):** `/advisory.html`, `/technology.html` — 2 pages
- **Cross-linking:** About page CTA → orphaned `advisory.html`. Orphaned `advisory.html` CTA → orphaned `technology.html`. Orphaned `technology.html` CTA → orphaned `advisory.html`. They form a parallel sub-site.
- **Risk:** Prospects reading anything outside the top nav can land on outdated copy with different product names.

### 2. Inconsistent product naming
The same three agents are named three different ways across the site:

| Surface | Voice agent | Confirmation agent | Eligibility agent |
|---|---|---|---|
| `solutions/ai/agentic-suite.html` (canonical) | Voice Scheduling Agent | Smart Confirmations | Eligibility Intelligence |
| `solutions/ai/index.html` | Voice Scheduling Agent | Smart Confirmations | Eligibility Intelligence |
| `solutions/ai/practice-bi.html` | Voice Scheduling Agent | Smart Confirmations | Eligibility Intelligence |
| `solutions/index.html` (journey graphic) | Voice Agent | Smart Confirmations | Eligibility Intelligence |
| `index.html` (footer card) | "Voice, Confirmation, and Eligibility agents" | (same) | (same) |
| `technology.html` (orphaned) | Voice Agent | Confirmation Agent | Eligibility Agent |

**Action:** Standardize on the canonical names (Voice Scheduling Agent / Smart Confirmations / Eligibility Intelligence). Allow short-form ("Voice agent," lowercase, when in flowing copy) but never with capitalized inconsistent variants.

### 3. "Operations Assessment" vs "Front Desk Evaluation Framework"
The Advisory engagement is named "Front Desk Evaluation Framework" on the product page. But six other places call its deliverable "Operations Assessment" (homepage flow tile, About page values card, Contact form select option, three Contact FAQ answers). The terms describe related but distinct concepts: the *engagement* is the Evaluation Framework; the *deliverable* is the written report. The site currently uses them interchangeably, which is confusing.

**Action:** Pick one of two patterns:
- (A) The engagement and the deliverable share a name. Call both "Front Desk Evaluation" — drop "Framework" and "Operations Assessment" entirely.
- (B) The engagement is "Front Desk Evaluation Framework"; the deliverable is "the assessment report." Never use "Operations Assessment."

### 4. "Active Partnership" is undefined
- Used as flow-step #4 on homepage with no definition beyond "We deploy the Practice Agentic Suite, refine SOPs..."
- Used in `contact.html` FAQ as "the Active Partnership tier" (line 271) — first time the word "tier" appears anywhere.
- Not mentioned on any solutions page.

**Action:** Either define "Active Partnership" as a real product term (which would warrant its own page or section on the Solutions hub) or rename to something self-describing like "Ongoing Partnership" and stop using "tier."

### 5. "Fortune 500" / "Fortune-500" / "the nation's largest health systems"
Same idea, three phrasings:
- `index.html:104` — `Fortune-500 caliber AI`
- `technology.html:75` — `Fortune 500 health systems`
- `solutions/ai/index.html:92,159` — both `Fortune 500` and `the nation's largest health systems`
- `solutions/ai/agentic-suite.html:7,77` — `the nation's largest health systems`
- `about.html:151` — `the nation's largest health systems`

**Action:** Standardize on `the nation's largest health systems`. It's evocative, avoids any trademark risk, and feels less corporate.

### 6. Header theme inconsistency
- Most pages use `<header class="site-header dark">` (dark background, white logo, etc.).
- Advisory pages (`solutions/advisory/*` and `evaluation-framework.html`) use `<header class="site-header">` (light theme) — they sit on a light radial-gradient hero rather than a dark hero.

This is **intentional** and reads as polished — the Advisory side of the brand is the "light" side, the AI side is the "dark" side. The choice is fine. Worth confirming this was intentional and not accidental drift.

### 7. Footer taglines differ slightly between pages
- Home/About/Contact footer tagline: `"Intelligent operations for the independent practice. Built by operators. Delivered with accountability."`
- Most solutions/insights footer tagline: `"Enterprise-grade AI and operational systematization for the independent practice."`

Two reasonable taglines, but it should be one. The first is warmer and stronger. Recommend that one everywhere.

### 8. Footer "Connect" column variations
- Home/About/Contact: 3 links (Schedule a Call, two email addresses).
- Solutions/Insights: "Company" column instead, with About/Insights/Contact/email.

Mostly fine — they serve different navigation needs at different depths — but the inconsistency is visible if you flip between pages.

---

## Brand Voice Violations (with line references)

### "Consultant" language (rule: avoid)
- `about.html:119` — Card title: **"Operators, not consultants."** (most prominent violation)
- `about.html:96` — `"previously required a six-figure consulting engagement and an IT department"`
- `solutions/advisory/index.html:149` — `"Most consulting engagements deliver a deck. We deliver a document you can act on Tuesday morning"`
- `solutions/advisory/strategic-transformation.html:170` — `"Most consulting engagements end at the recommendation. Ours start there."`
- `solutions/advisory/evaluation-framework.html:170` — `"Most consulting reports get skimmed once and shelved. Ours are structured..."`

### Negative-framing / define-by-contrast (rule: forward-pulling positive framing)
- `solutions/ai/practice-bi.html:220` — `"Most practice reports get pulled monthly, emailed to nobody, and decided by gut feel..."`
- `technology.html:136` — `"Most practice owners have no real-time visibility..."` (in orphaned page, will be moot if deleted)
- `advisory.html:200` — `"Most independent practices run on tribal knowledge..."` (in orphaned page, will be moot if deleted)
- `about.html:130` — `"We don't serve hospital systems. We don't serve private-equity-rolled-up MSOs..."` (acceptable framing — defines customer focus rather than competitor, but still uses negation)
- `solutions/ai/agentic-suite.html:294` — `"We don't do slides."` (marginal; defines demo experience)

### "Enterprise-grade" usage
- Used 30+ times across the site, mostly in the dropdown subhead `"Enterprise-grade AI for your practice"` and footer taglines. This phrase **isn't** on the brand voice's prohibition list per the review brief — but the brief asks me to flag it for awareness. The phrase reads as B2B-software boilerplate and is the least distinctive part of the brand language. Consider replacing on the most prominent surfaces (hero/dropdown subhead/footer tagline) with something more ownable like `Health-system-grade AI for your practice` or `The intelligence of the largest systems, for the practice on the corner`.

### "AI-powered" usage
- Zero occurrences. ✓ Rule honored throughout.

---

## Information Architecture

### Navigation: structurally sound but mixed-state
- Top nav consistent on all pages (Home / Solutions ▾ / About / Insights / Contact / Schedule a Call CTA).
- Mega-menu dropdown has correct two-column structure (AI Solutions / Advisory Solutions) on every page.
- **Two pages live outside the nav:** `advisory.html` and `technology.html`. Not linked from nav. But linked from About and from each other. This is the root of issue #1 above.

### Internal links: mostly correct
- Footer-grid links generally point to correct canonical pages.
- **Exception:** `about.html:202` — CTA `"Explore Advisory"` → root-level `advisory.html` (the orphaned page).
- **Exception:** `insights/index.html:140` — 4th article card → wrong article file.

### URL depth: appropriate
- `/solutions/ai/agentic-suite.html` is the deepest URL path. Acceptable. Two clicks from home.

### 2-click rule: passes for canonical content
A visitor can reach any canonical product page in two clicks (Home → Solutions dropdown → product). The orphaned pages are technically also two clicks (Home → About → CTA → advisory.html), which is why deleting/redirecting them matters.

---

## SEO & Meta

### Strong baseline
- **Every page has `<title>` and `<meta name="description">`.** ✓
- Titles include "Sage Health" branding consistently.
- Descriptions are substantive (often 100–180 chars, well-tuned for SERPs).
- Open Graph tags on home (`og:title`, `og:description`) — but **not on most other pages.** Add `og:*` tags to every page that might be shared (especially insights articles) for proper social previews.

### Heading hierarchy
- Generally clean: each page has one `h1`, nested `h2`/`h3` thereafter.
- Insights articles use `h1` for title, `h2` for section breaks, `h3` for sub-points. Correct.

### Images / alt-text
- The site uses inline SVG icons exclusively (no `<img>` tags). All SVGs have `aria-hidden="true"` on the sprite container — correct.
- No actual photographic content on the site. When founder photos are added, ensure `alt="Umair Khalid, Co-Founder, Sage Health"` style attribution.

### Sitemap / robots.txt
- Not present in the repo. Worth adding for production.

### Canonical tags
- Not present. With two parallel page hierarchies, a `<link rel="canonical">` on `advisory.html` and `technology.html` pointing to the canonical `/solutions/*` pages is the *minimum* fix if those pages can't be deleted immediately.

---

## Specific Red Flags Found in Grep Sweep

| Pattern | Hits | Severity |
|---|---|---|
| `consultant` | 1 (`about.html:119` — value-card title) | Critical |
| `consulting` | 4 (negative comparison framing on 3 Advisory pages + About) | High |
| `AI-powered` | 0 | ✓ OK |
| `we're not` / `we don't` / `we aren't` | ~9 (most acceptable; one card title is a violation; "we don't do slides" is marginal) | Mixed |
| `TODO` / `FIXME` / `lorem` / `coming soon` | 0 in copy (only HTML form `placeholder=` attributes — correct usage) | ✓ OK |
| `Enterprise-grade` | 30+ | Awareness item |
| `Fortune-500` / `Fortune 500` | 4 (inconsistent hyphenation) | Medium |
| `Active Partnership` | 2 (one undefined "tier" usage) | Medium |
| `Operations Assessment` vs `Front Desk Evaluation Framework` | 6 vs 5 | Medium |

---

## Priority Matrix

### Critical (fix before showing this site to anyone)
1. **Delete or redirect `/advisory.html` and `/technology.html`.** They are orphaned, contain outdated product names, and are still linked from About. Until they're gone, the brand has three different sets of product names live on the same domain.
2. **Fix the `about.html:202` CTA link** to point to `solutions/advisory/index.html`, not the orphaned `advisory.html`.
3. **Fix the broken Insights card** at `insights/index.html:140` ("The Voicemail Era is Over") — either write the article or remove the card.
4. **Wire the Contact form to a real submission endpoint.** Right now it shows a success message but does nothing. Any prospect who submits gets ghosted.
5. **Rename or rewrite "Operators, not consultants."** card on `about.html:119` to remove the brand-by-negation pattern.

### Important (fix before launch)
6. **Standardize product names across the site** (Voice Scheduling Agent / Smart Confirmations / Eligibility Intelligence) — already canonical on `/solutions/ai/*`, just needs to be enforced everywhere the names appear.
7. **Rewrite the four "Most consulting…" pull quotes** on the Advisory section to lead with what Sage Health is, not what consultants aren't. Specific rewrites suggested above per page.
8. **Resolve "Operations Assessment" vs "Front Desk Evaluation Framework"** ambiguity. Pick one term for the engagement, one term for the deliverable.
9. **Define or rename "Active Partnership"** — either it's a real product term that deserves a section on the Solutions hub, or it's a description that should be reframed in plain language.
10. **Standardize "the nation's largest health systems"** as the canonical phrasing; remove "Fortune 500" variants.
11. **Verify or remove customer testimonials and sample-data labels.** Specifically: the Houston practice administrator quote on `agentic-suite.html:282`, the "Lakeside Family Practice · Live" attribution on `practice-bi.html`, and the "Based on Sage Health engagements" footnote on `operational-sops.html:132`.
12. **Add Open Graph tags** to every page (especially insights articles) for shareable previews.

### Nice-to-have (polish)
13. Standardize hero-meta pill format across product pages (`Turnkey · Fully managed · Always on` style).
14. Consider replacing the most prominent "Enterprise-grade AI" surfaces (hero/dropdown subhead/footer tagline) with more ownable language.
15. Add real founder photos when available (replaces the "UK" / "TA" initials).
16. Add a `robots.txt`, `sitemap.xml`, and `link rel="canonical"` tags for production deployment.
17. Audit the footer tagline ("Intelligent operations…" vs. "Enterprise-grade AI and operational systematization…") and pick one.
18. Verify or footnote specific industry stats (e.g., the no-show breakdown percentages on `reducing-no-shows-beyond-reminders.html:85`).

---

## Recommended Next Steps

1. **First half-day of edits** — handle every Critical item above. This unblocks the site to be shared with prospects.
2. **Second half-day** — work the Important list. Most are find-and-replace level edits; the pull-quote rewrites need a few minutes of thought each.
3. **Before the first live prospect demo** — verify or remove every social-proof element (customer quotes, sample dashboards labeled "Live," "Based on Sage Health engagements" footnotes). The brand voice is so strong that any single unsubstantiated claim will land disproportionately hard.
4. **Pre-launch** — wire OG tags, sitemap, canonical tags. Add real founder photos. Consider replacing "Enterprise-grade" on top surfaces.
5. **Ongoing** — the Insights articles are the strongest single asset on the site. Publishing one a month at the quality bar of the existing three is probably worth more than another full sweep of homepage copy.

---

**Overall:** The bones are excellent. The brand voice, the technical positioning, the differentiation, the customer focus, the design system — all unusually strong for a pre-launch site. The two structural issues (orphaned pages + a few brand-voice slips) are the kind of thing a careful half-day pass will resolve. After that, this is a credible enterprise-grade-vibes site that earns the room of any practice owner who reads it.
