# AI Company OS

> Three AI executives in your terminal. From business idea to executable plan.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-blueviolet)](https://claude.com/claude-code)
[![Plugins: 6](https://img.shields.io/badge/Plugins-6-green)]()

**English** | [中文](./README.zh-CN.md)

---

You run `/init-company`. The AI CEO starts asking questions like a real investor would. What's your product? Who's the customer? What stage are you at? What's blocking you?

Ten minutes later you have `company.md` — your startup's DNA in a structured file that every AI agent can read and reason over.

Then you run `/ceo-plan`. Your vague goal "hit $20k MRR this quarter" becomes 30+ tasks decomposed across 4 dimensions (product, growth, tech, ops), each with a priority, owner, deadline, and success criteria. The agent scores its own plan across 7 dimensions and flags: "You allocated zero people to KOL outreach but expect 5 partnerships. This plan won't survive contact with reality."

You run `/teardown`. It reverse-engineers each competitor through 6 layers: problem space → data model → user journey → pricing mapping → retention mechanics → feature catalog + design decisions. Each competitor gets a ~500-line structured dossier. Cross-competitor patterns emerge automatically.

You run `/cpo-plan`. It builds on that intelligence to write a real PRD with user stories and acceptance criteria, and designs a 3-month version plan: V1.0 MVP → V1.1 Validation → V1.2 Growth.

You run `/cmo-plan`. It scores every growth channel by 6 metrics, builds keyword matrices, designs SEM campaigns with budget allocation, and maps your AI writing tools as growth weapons.

Finally, `/ceo-plan --mode roadmap` synthesizes everything into a unified timeline. Dependencies are explicit. Resource conflicts are flagged. Risk mitigation plans are included.

All of it version-controlled in Git. You can `git diff` your strategy from 3 months ago.

```
/init-company "My Startup"
      ↓
/ceo-plan        → Diagnose stage → Decompose goals → 4 dimensions × P0/P1/P2
      ↓
/teardown        → 6-layer competitor reverse-engineering → structured dossiers
      ↓
/cpo-plan        → PRD with user stories → Version plan
      ↓
/cmo-plan        → Score channels → SEO/SEM/Social/KOL → Budget + calendar
      ↓
/ceo-plan --mode roadmap   → Synthesize all → Timeline + dependencies
```

## Quick Start

```bash
# Add the marketplace
/plugin marketplace add La-fe/ai-company

# Install all plugins
/plugin install init-company@ai-company
/plugin install ai-ceo@ai-company
/plugin install ai-cpo@ai-company
/plugin install ai-cmo@ai-company
/plugin install competitor-teardown@ai-company
/plugin install company-pipeline@ai-company
```

Or run the full pipeline in one command:

```bash
/company-pipeline "My Startup"
```

## See It In Action

### 1. Initialization: The CEO Interview

You run `/init-company`. The agent conducts a structured interview:

```
Round 1: Identity + Product
→ What's your core product? What problem does it solve?
→ What stage are you at? (users? revenue? still building?)
→ Who's your target customer? (be specific: industry, size, role)

Round 2: Positioning + Competition
→ How do your customers solve this problem today?
→ What's your advantage? (mechanisms, not adjectives)
→ What do you explicitly NOT do?

Round 3: Principles + Goals
→ What's your decision-making principle? ("speed > perfection"?)
→ What are the 1-3 most important things this quarter?
→ What does success look like for each? (measurable)
```

Output: `company.md` + `goals.md` + `arsenal.md` — your company's structured genome.

### 2. CEO Diagnosis: Vague Goals → Executable Tasks

You say: "We need to hit $20k MRR this quarter."

The CEO agent diagnoses your stage, identifies the main contradiction, and decomposes:

```
Goal G1: Hit $20k MRR

Product (CPO)
  G1-P-01  Complete payment redesign      P0  2 weeks  blocks G1-G-01
  G1-P-02  Customer analytics dashboard   P1  1.5 weeks

Growth (CMO)
  G1-G-01  Launch SEO strategy            P0  ongoing  depends on G1-P-02
  G1-G-02  Test 2 paid channels           P0  3 weeks

Tech (CTO)
  G1-T-01  Data tracking pipeline         P0  2 weeks  blocks G1-P-02, G1-G-01

Ops (COO)
  G1-O-01  Customer onboarding SOP        P1  1 week
```

Then it **self-evaluates** across 7 dimensions:

```
Main contradiction accuracy    9/10   Correctly identified growth channel bottleneck
Goal achievability             7/10   $20k in 3 weeks is tight. Consider external risks.
Task completeness              8/10   4 dimensions covered. Missing risk mitigation task.
Resource feasibility           6/10   3-person team + 0 marketing. Growth tasks are at risk.

Verdict: Adjust. Add contingency plan for marketing capacity.
```

Plans that score too low get **rejected with reasons**. No wishful thinking allowed.

### 3. Competitor Teardown: 6-Layer Reverse Engineering

You run `/teardown whop.com stan.store durable.co`. The agent crawls each competitor and produces a structured dossier through 6 analytical layers:

```
Layer 1: Problem Space
  → Target user persona, core JTBD, trigger scenarios, alternatives
  → Key metrics: users, revenue, ARPU, market share

Layer 2: Data Model (core layer)
  → Entity extraction: Core / Supporting / Value / Transactional
  → Entity relationship diagram with standardized notation
  → Field-level definitions for top 3-5 core entities

Layer 3: User Journey
  → Step × Page × Entity × CRUD operation table
  → Critical flow diagrams (forks, loops)
  → TTFV analysis (Time To First Value)

Layer 4: Pricing-Entity Mapping
  → Pricing model classification (subscription / transaction / credits / freemium / hybrid)
  → Tier comparison: Free / Basic / Pro / Enterprise
  → Entity ↔ pricing boundary table (what's gated at each tier)

Layer 5: Retention Mechanics
  → 7 retention strategies scored: data lock-in, social binding, habit formation,
    switching cost, network effects, content accumulation, revenue dependency

Layer 6: Feature Catalog + Design Decisions
  → Complete feature inventory (category × entity × pricing tier)
  → AI capability audit (when applicable)
  → Design decision reasoning with inference chains
```

Each competitor outputs a ~500-line `{name}.md` dossier. After all competitors are analyzed, a cross-competitor `landscape.md` emerges:

```
Landscape synthesis:
  → Entity commonality matrix (core / majority / minority / whitespace)
  → Architecture patterns (flat / hierarchical / polymorphic / event-driven)
  → Pricing panorama comparison
  → TTFV comparison across competitors
  → Retention strategy comparison matrix
  → Whitespace opportunities with impact assessment
```

### 4. CPO: PRD → Version Plan

Building on the teardown intelligence, the CPO agent generates:

**Competitive Matrix:**

```
           Us          Competitor A     Competitor B
ICP        SMB ecomm   All ecommerce    Enterprise only
Pricing    $99-299     $49-199          $499-999
Strength   AI-driven   Feature-rich     Enterprise trust
Weakness   No i18n     Over-complex     Expensive + steep curve

Opportunity: Nobody does AI-driven content localization.
```

**PRD with real user stories:**

```
As a cross-border ecommerce operator uploading 15+ SKUs daily,
I want to generate 3-language product descriptions from a photo,
so I can reduce per-SKU time from 30 minutes to 5 minutes.

Acceptance criteria:
- [ ] 60-second generation from image + basic info
- [ ] Output includes headline, features, use cases
- [ ] One-click sync to Amazon/Shopify
- [ ] Batch import via CSV (100+ SKUs)
```

**3-month version plan:**

```
V1.0 MVP (Weeks 1-4)     Core value validation
V1.1 Data (Weeks 5-8)    User behavior analytics, iterate
V1.2 Growth (Weeks 9-12) Multi-platform integrations, batch ops
```

### 5. CMO: Channel Scoring → Growth Strategy

The CMO agent scores channels by 6 dimensions:

```
Channel    Cost  Speed  Ceiling  Compound  AI-friendly  Product-fit  Score
SEO        Low   Slow   High     High      High         High         8.5 ← Top 1
SEM        Med   Fast   Med      None      High         Med          7.0 ← Top 2
Social     Low   Fast   Med      Med       Med          Low          6.5
KOL        High  Fast   Low      Low       None         High         6.0
```

Then builds detailed strategies per channel: keyword matrices, campaign structures, budget allocation, ROI projections, 30-60-90 day action plans.

And maps your AI writing tools as execution weapons:

```
/find-topic         → Keyword discovery
/article-pipeline   → End-to-end content production
/publish            → LinkedIn, X, Substack, WeChat
```

### 6. Unified Roadmap: Everything In Sync

```
       March               April                May
Prod   V1.0 MVP dev        V1.0 polish          V1.1 dev
Growth SEO content (10x)   SEM launch           KOL partnerships
Tech   Analytics setup     Payment integration  Dashboard
Ops    CS playbook         Fundraise prep       Fundraise

Dependencies:
  SEM launch ← V1.0 + landing page complete
  KOL start ← 10+ customer success stories
  V1.1 dev  ← V1.0 analytics data collected
```

### 7. Your Git Log Is Your Company History

```
$ git log --oneline
abc123 retro: 2026-03 completed
def456 review: week 2026-W12
ghi789 adjust: G1 target 100 → 150 based on traction
jkl012 roadmap: 2026-04 final
mno345 cmo: growth plan 2026-03
pqr678 cpo: PRD + version plan 2026-03
stu901 ceo: goals + tasks 2026-03
vwx234 init: company context
```

Every decision tracked. Every pivot documented. `git diff` your strategy evolution.

## What Makes This Different

**It's not a prompt wrapper. It's a methodology engine.**

- **70+ reference documents**: Task decomposition frameworks, PRD writing standards, channel scoring matrices, industry KPI benchmarks, product type templates
- **RLHF quality loops**: Every output evaluated across 7 role-specific dimensions. Dynamic weights adjust by company stage. Veto rules reject low-quality plans
- **Dependency management**: Tasks aren't isolated. The system tracks what blocks what. Change a deadline and it flags downstream impacts
- **Git-native**: All company knowledge in version-controlled markdown. Your startup gets smarter the longer you run it

## Plugins

| Plugin                                          | Trigger             | What It Does                                          |
| ----------------------------------------------- | ------------------- | ----------------------------------------------------- |
| [init-company](./init-company/)                 | `/init-company`     | Guided interview → company.md + goals.md + arsenal.md |
| [ai-ceo](./ai-ceo/)                             | `/ceo-plan`         | Diagnose → decompose → roadmap → review (3 modes)     |
| [ai-cpo](./ai-cpo/)                             | `/cpo-plan`         | PRD → version plan → feature design                   |
| [ai-cmo](./ai-cmo/)                             | `/cmo-plan`         | Channel scoring → SEO/SEM/Social/KOL → growth plan    |
| [competitor-teardown](./competitor-teardown/)     | `/teardown`         | 6-layer competitor reverse engineering → dossiers     |
| [company-pipeline](./company-pipeline/)           | `/company-pipeline` | Full pipeline + daily dashboard + retrospectives      |

## Output Structure

```
{company_dir}/
├── context/
│   ├── company.md            # Company DNA
│   ├── arsenal.md            # Skills, APIs, tools inventory
│   └── competitors/          # Deep teardowns per competitor
├── plans/{cycle}/
│   ├── goals.md              # OKR-format objectives
│   ├── prd.md                # Product requirements (CPO)
│   ├── version-plan.md       # 3-month roadmap (CPO)
│   ├── growth-plan.md        # Channel strategy (CMO)
│   └── roadmap.md            # Unified timeline (CEO)
├── reviews/                  # Weekly & monthly retrospectives
└── tasks.jsonl               # Central task repository with dependencies
```

## Architecture

```
ai-company/
├── init-company/              # Company initialization
├── ai-ceo/                    # CEO: goals, tasks, roadmap, review
│   └── references/            # Task decomposition, eval dimensions, review framework
├── ai-cpo/                    # CPO: PRD, versions, feature design
│   └── references/            # PRD framework, product eval, data model extraction
├── ai-cmo/                    # CMO: channels, SEO, SEM, social, KOL
│   ├── channels/              # Channel leader profiles (SEO/SEM/Social/KOL)
│   └── references/            # Channel matrix, growth playbook, eval dimensions
├── competitor-teardown/       # 6-layer competitor reverse engineering
│   └── references/            # Extraction methods, AI audit, synthesis patterns
├── company-pipeline/          # Orchestrator + dashboard
└── shared/                    # RLHF loop, task schema, dashboard scripts
```

## Contributing

Contributions welcome.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[MIT](LICENSE)
