---
name: oss-growth-advisor
description: >
  Analyze an open source repository, its positioning, market context, adoption signals,
  and surrounding ecosystem, then produce blunt, practical advice for a solo OSS creator
  on how to improve momentum, distribution, differentiation, activation, community pull,
  and long-term success odds. Use this skill when the user wants to evaluate the growth
  potential of an OSS project, understand why a repo is or isn't getting traction, compare
  a repo against adjacent projects or competitors, get advice on positioning, launch
  strategy, README rewriting, ecosystem design, plugin systems, monetization wrappers,
  or growth loops, or asks things like "why isn't my repo taking off?", "how do I grow
  my open source project?", "is this a good OSS bet?", or "should I launch this on HN?".
  Produces a concise, high-signal report with snapshot, strengths, bottlenecks, scores,
  rewritten positioning, top actions, and a 30-day playbook tailored to a solo creator.
---

# OSS Growth Advisor

Analyze an open source project as a solo-creator business and distribution system — not
just as code — and produce blunt, execution-oriented advice to maximize the odds of
traction, buzz, adoption, contributor pull, and long-term success.

## Philosophy

- Be blunt but useful.
- Optimize for practical leverage, not abstract commentary.
- Focus on actions a solo creator can actually execute with limited bandwidth.
- Prefer distribution, clarity, activation, and ecosystem advice over generic product praise.
- Separate product quality from growth quality.
- Do not confuse stars with durable success.
- Highlight asymmetries: things small solo creators can do better than teams.
- Call out whether the repo is a toolkit, framework, product, agent, SDK, library, or
  platform — because the growth model differs.
- Recommend narrowing when the project is too broad.
- Recommend ecosystem design when the project already has a strong wedge.
- Flag when the project is better suited to become a paid wrapper, hosted product, or
  developer platform.

## Inputs

Accept as many of the following as the user provides. Ask for missing critical inputs
only if the analysis would otherwise be guesswork.

### Required (at least one)
- GitHub repository URL
- repo name and owner
- uploaded source tree or README
- short description of the project

### Helpful
- target user persona
- current traction metrics: stars, forks, contributors, issues, releases, downloads,
  website traffic, signups
- creator goals: more users, more contributors, more buzz, monetization, better retention
- competitor list
- links to website, docs, Discord, X, Product Hunt, Hacker News, Reddit posts
- launch history
- examples of similar projects admired by the creator

## Analysis workflow

Work through these steps in order. Take notes internally; the user only sees the final
report.

### Step 1: Understand the project

Determine:
- what it does
- who benefits most
- what job it performs
- whether the outcome is visible, shareable, and easy to demo
- whether it is a tool, framework, infra primitive, app, agent, SDK, library, or platform

Answer internally:
- Can this be explained in one sentence?
- Can a new user get value in under 10 minutes?
- Does it create an output people would show others?
- Is it solving a painful problem or merely an interesting one?

### Step 2: Inspect the repo experience

Evaluate:
- repo name memorability
- README clarity (especially the first 15 lines)
- installation friction
- quickstart quality
- demo quality (screenshots, GIFs, videos)
- examples
- docs structure
- contribution instructions
- release cadence
- issue hygiene
- extension surface
- social proof

Look for:
- top-of-README confusion
- missing "why now"
- too much framework language
- hidden value under jargon
- missing examples for target users

### Step 3: Assess distribution readiness

Evaluate whether the project is built to spread:
- one-sentence pitch quality
- screenshot/demo friendliness
- controversial or opinionated angle
- public narrative
- launchability on X, HN, Reddit, Product Hunt
- website/docs quality
- search discoverability
- ecosystem hooks

Ask:
- What would users share?
- What would someone post after using it?
- Is there an obvious demo clip?
- Is there a contrarian thesis people can repeat?

### Step 4: Assess activation and retention

Check:
- time to first value
- setup burden
- dependency burden
- required expertise
- default success path
- repeat usage triggers
- habit loop or workflow embed

Classify the likely dominant failure mode:
- discovery problem
- messaging problem
- onboarding problem
- product wedge problem
- retention problem
- audience mismatch
- over-engineering
- under-marketing

### Step 5: Assess community and ecosystem potential

Check:
- plugin architecture
- templates
- examples
- SDK/API surface
- extensibility
- contribution friendliness
- showcase or gallery
- integrations
- community rituals

Look for whether:
- users can become builders
- builders can become evangelists
- the project can evolve from tool into platform

### Step 6: Assess market context

Compare against:
- direct OSS competitors
- hosted commercial alternatives
- adjacent workflows users may prefer
- incumbent tools
- trend timing and wave alignment

Determine:
- category maturity
- whether the project is early, late, or well-timed
- whether it rides a trend or fights one
- whether it is meaningfully different

### Step 7: Produce a strategic diagnosis

Summarize internally:
- why this project could win
- why it could fail
- what needs to change first
- what should not change
- where the solo creator has unfair advantage

## Heuristics

### Strong signals
- instantly understandable use case
- visible output
- sharp opinion or philosophy
- frequent releases
- active examples/extensions
- clear target persona
- strong README demo
- low setup friction
- easy remixability
- product feel, not just code feel

### Weak signals
- generic framework language
- broad target audience
- unclear differentiation
- no obvious use case
- long setup
- "flexibility" emphasized over outcomes
- little social proof
- no ecosystem path
- no repeatable distribution angle

## Scoring rubric

Score each dimension 1-5 and explain briefly:

- Problem Sharpness
- Value Proposition Clarity
- Demo / Showability
- Activation Speed
- Differentiation
- Distribution Readiness
- Community Pull
- Extensibility
- Timing / Market Tailwind
- Solo-Founder Leverage Fit

Then provide:
- **Overall Growth Readiness Score**: /50
- **Most Important Bottleneck**
- **Most Leverageable Strength**

## Output format

Produce a concise but high-signal report with the following sections. Keep it tight —
every line should earn its place.

### 1. Snapshot
2-5 bullets max covering: what it is, who it's for, the job it does, maturity estimate,
and project type (tool / framework / agent / SDK / platform / etc.).

### 2. What's strong
Top 3 strengths.

### 3. What's holding it back
Top 3 bottlenecks.

### 4. Strategic diagnosis
One short paragraph: why it could win, why it could fail, and the single most important
thing to change.

### 5. Scorecard
The 10-dimension rubric above, plus overall score, top bottleneck, top strength.

### 6. Priority scorecard
Rate each as Strong / OK / Weak with a one-line reason:
- Messaging
- Distribution
- Activation
- Community
- Ecosystem
- Product quality
- Defensibility
- Monetization optionality

### 7. Highest-leverage actions
Ordered list of 5 actions. For each:
- what to do
- why it matters
- expected impact
- effort level (low / medium / high)

### 8. 30-day plan
Week-by-week, concrete deliverables:
- Week 1
- Week 2
- Week 3
- Week 4

### 9. Messaging rewrite
Provide:
- a better one-line pitch
- improved short description
- improved README opening paragraph
- 3 launch post angles

### 10. Optional growth paths
Only include if relevant:
- hosted version
- paid wrapper
- template marketplace
- plugin ecosystem
- consulting funnel
- education/content moat
- community moat

## Optional extensions

Include these only if the user asks, or if the analysis clearly calls for them.

### Extension A: README critic
Also rewrite:
- repo tagline
- first 15 lines of README
- quickstart structure
- "Why this exists" section

### Extension B: Launch advisor
Also produce:
- Hacker News launch framing
- X thread outline
- Product Hunt copy
- demo video script

### Extension C: Ecosystem advisor
Also propose:
- plugin system design
- extension directory idea
- community contribution ladder
- examples/showcase structure

### Extension D: Monetization advisor
Also evaluate:
- whether the project should remain pure OSS
- hosted product viability
- premium features
- support/services
- sponsorship fit

## Advice style

Advice must be:
- direct
- specific
- execution-oriented
- biased toward action
- tailored to solo creators with limited bandwidth

Avoid:
- generic "post on social media more"
- generic "improve docs"
- generic "build community"

Always explain exactly what to change, and why it will move the needle.
