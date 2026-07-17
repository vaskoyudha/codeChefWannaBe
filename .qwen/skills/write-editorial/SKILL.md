---
name: write-editorial
description: Use when writing the editorial for an approved competitive programming problem — produces progressive hints, brute-force → optimal progression, step-by-step walkthrough, complexity analysis, alternative approaches, and common mistakes.
---

# Editorial Writer (Agent 6)

Write an editorial that makes readers think **"of course! why didn't I see that?"** — not "I could never have thought of that." You are the final content agent in the pipeline. You receive all approved outputs from Agents 1–5 and produce the `editorial` section of `final_problem.json`.

## Overview

A good editorial builds the "aha moment" through pedagogy, not revelation. The difference between a great editorial and a bad one is not the solution — it's the journey. You build understanding layer by layer, from the naive to the elegant, so the optimal approach feels like a natural destination, not a magic trick.

**Core principle:** The reader must see WHY the naive approach fails and HOW the optimal approach naturally emerges from eliminating that failure. Every editorial is a story of optimization motivated by constraint pressure.

## When to Use

- Writing the editorial after a problem passes quality review (Gate 2 APPROVED)
- Creating progressive hints that scaffold from direction to key insight
- Explaining the brute-force → optimal solution progression
- Documenting common mistakes with concrete counterexamples
- Producing alternative approaches with trade-off analysis

**Pedagogical philosophy:** Contestants who read the editorial attempted the problem. They are smart. Don't condescend. But don't assume they know the technique — that's why they're reading. The editorial must reward both those who solved it (deepening understanding) and those who didn't (teaching the technique).

## Dependencies (Upstream Agents)

| Agent | Output | What You Use It For |
|-------|--------|---------------------|
| Agent 1 — Problem Architect | `architect_spec.json` | `learning_objective`, `core_concept`, `bloom_level`, `difficulty` — calibrate editorial depth |
| Agent 2 — Problem Writer | `problem_draft.json` | `story`, `statement`, `constraints`, `sample_tests` — the problem you're explaining |
| Agent 3 — Solution Engineer | `solution.json` | `approach`, `pseudocode`, `brute_force_solution`, `correctness_argument`, `common_wrong_approaches` — the core content |
| Agent 4 — Test Case Generator | `test_suite.json` | `test_cases`, `coverage_report` — edge cases to reference in walkthrough |
| Agent 5 — Quality Reviewer | `review_verdict.json` | `verdict` (must be APPROVED), `shield_check`, `sword_findings`, `warnings` — quality context |

## Input

All 5 preceding agent outputs (all must be approved).

## Output

`editorial.json` containing:
- **hints**: Exactly 3 progressive hints (direction → approach → key insight)
- **brute_force_explanation**: Naive approach with constraint arithmetic proving it's too slow, bottleneck identified
- **optimal_solution_walkthrough**: Motivating bridge, key insight, step-by-step walkthrough traced on Sample 1, correctness explanation (adapted proof technique)
- **complexity_analysis**: Time and space complexity derived from algorithm structure, verified against constraints with arithmetic
- **alternative_approaches**: 0–3 correct alternative solutions with trade-offs
- **common_mistakes**: 2–3 plausible mistakes, each with concrete counterexample and lesson

## Iron Law

```
NO EDITORIAL WITHOUT A BRUTE-FORCE → OPTIMAL PROGRESSION.
The reader must see WHY the naive approach fails and HOW the optimal approach naturally emerges.
Skipping straight to the optimal approach is teaching failure.
```

## Red Flags

If you catch yourself thinking any of these, stop and correct:

| Red Flag | Correction |
|----------|------------|
| "The optimal solution is clear" | Did you show WHY the brute force fails? Did you bridge from bottleneck to insight? |
| "The learner should already know this" | If they knew it, they wouldn't need the editorial. Teach it. |
| "I'll just copy the solution's correctness argument" | The solution uses formal language. The editorial uses teaching language. Rewrite it accessibly. |
| "One hint is enough" | Three hints scaffold from direction to insight. Use all three. |
| "The common mistakes are too basic" | Basic mistakes are the most common. List them with counterexamples. |
| "Three hints is too many" | Each hint serves a different reader. Removing one loses a scaffolding level. |
| "The correctness proof is in the solution" | The solution is for verification. The editorial is for teaching. |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "The optimal approach is obvious" | Obvious to you ≠ obvious to learner. Show the journey. |
| "I'll skip the brute force to save space" | Without brute force, there's no motivation for the optimization. |
| "Hints should be vague to challenge the reader" | Vague hints help nobody. Each hint must be actionable at its level. |
| "The proof is too complex to simplify" | Focus on the KEY IDEA, not every detail. One accessible paragraph. |
| "Common mistakes are obvious" | If you don't list them, learners will make them. Minimum 2 with counterexamples. |
| "Alternative approaches are optional" | Alternatives teach trade-offs. Include at least one if it exists. |
| "The reader can trace the sample themselves" | Trace it explicitly. Show the algorithm working step by step. |

## Quick Reference: Hint Progression

| Hint | Level | Purpose | Reader State After |
|------|-------|---------|-------------------|
| 1 | **Direction** | Points toward the right area without naming the technique | "I know WHERE to think" |
| 2 | **Approach** | Names the technique and WHY it applies | "I know WHAT to use" |
| 3 | **Key Insight** | Reveals the critical observation or recurrence | "I know HOW to make it work" |

**Calibration by difficulty:**

| Difficulty | Hint 1 | Hint 2 | Hint 3 |
|------------|--------|--------|--------|
| Easy (800–1200) | Almost an observation | Names the technique | Nearly complete approach |
| Medium (1300–1700) | Structural hint | Technique + why it applies | Key insight or formula |
| Hard (1800–2200) | Subtle observation | Technique hint (may be vague) | Key insight with brief justification |
| Expert (2300+) | Very subtle hint | High-level direction | The critical observation |

## Brute-Force → Optimal Progression (4 Stages)

This is the single most important pedagogical structure in editorial writing.

### Stage 1: The Naive Approach
Describe the most obvious solution. Validate the reader's first instinct. State its complexity. Explain why it's correct.

### Stage 2: Why It's Too Slow (The Constraint Signal)
Compute worst-case operations from constraints. Compare against ~10⁸ ops/sec. **Identify the BOTTLENECK** — the specific expensive operation. State clearly: "This is too slow."

### Stage 3: Motivating the Optimization (The Bridge)
Ask a motivating question that targets the bottleneck:
- **Precomputation:** "What if we could preprocess so each query takes O(1)?"
- **Sorting/reordering:** "What if we sorted queries to reuse work between consecutive ones?"
- **Eliminating redundancy:** "What if we stored results of subproblems we recompute?"
- **Monotonicity:** "What if we could check feasibility and search faster?"

### Stage 4: The Optimal Approach (The Destination)
Present the optimal as the natural conclusion. State the key insight. Walk through the algorithm. Show how it resolves the bottleneck. Verify the new complexity passes.

## Correctness Explanation Techniques

Match the proof technique from `solution.correctness_argument`:

| Proof Type | Editorial Adaptation |
|------------|---------------------|
| **Loop invariant** | "At each step, [variable] maintains [property]. True initially because [base]. Each iteration preserves it because [maintenance]. At loop end, [termination] gives the correct answer." |
| **Exchange argument** | "Suppose an optimal solution disagrees with ours. We can swap to our choice without making things worse, because [reason]. So our solution IS optimal." |
| **Mathematical induction** | "Base case is trivial. Assume smaller subproblems are correct. Our answer combines them correctly because [reason]." |
| **Monotonicity** | "[Condition] is monotonic: if it holds for X, it holds for all [larger/smaller]. Binary search exploits this." |
| **Greedy stays ahead** | "At every step, our greedy choice is at least as good as any other strategy's cumulative result, because [reason]." |

**Rules:** One paragraph. Concrete language. Reference the problem's variables. The reader should be convinced, not overwhelmed.

## Common Mistakes Section

Each mistake follows this structure:
1. **Describe the approach** — what the contestant tries
2. **Explain why it seems right** — validate the instinct
3. **Show why it fails** — concrete counterexample with specific input and wrong output
4. **State the lesson** — what to watch out for

**Categories:** Greedy that fails subtly, off-by-one in ranges, missing edge cases, integer overflow, wrong binary search bounds, incorrect DP transition.

**Rules:** 2–3 mistakes. Each must be plausible and include a concrete counterexample. Prioritize by likelihood. No trivial mistakes (syntax, I/O errors).

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Fix |
|--------------|-------------|-----|
| Hint spoilage | Hint 1 gives away the technique — no room for progression | Start with structural observation, not algorithm name |
| Magic insight | Optimal appears from nowhere with no motivation | Always bridge from brute force through the bottleneck |
| Proof dump | Formal proof overwhelms the reader | Accessible language, one paragraph |
| Assertion without derivation | "O(N log N)" with no justification | Show where each factor comes from |
| Generic mistakes | "Forgetting edge cases" — not specific to this problem | Concrete counterexample for THIS problem |
| Wrong approach as alternative | Incorrect method in `alternative_approaches` | Alternatives must be CORRECT even if suboptimal |
| Redundant hints | All three hints say the same thing differently | Each hint reveals strictly new information |
| Missing bottleneck | "Too slow" without explaining WHY | Compute operations, identify the specific bottleneck |
| Story disconnect | Editorial ignores the problem's story | Reference the story when it builds intuition |

## Quality Criteria (Pre-Output Checklist)

| Criterion | Standard |
|-----------|----------|
| Hint progression | Each hint reveals strictly more. Reader stopping at any level gains value. |
| Brute-force motivation | Arithmetic from constraints shown. Bottleneck named. |
| Motivating bridge | Optimal feels like natural evolution from brute force, not a leap. |
| Walkthrough clarity | Every step follows from the previous. No unexplained jumps. |
| Correctness accessibility | Convincing without being a formal proof. Matches solution's proof technique. |
| Complexity verification | Constraint values plugged in. Comparison to time budget explicit. |
| Common mistake quality | Each mistake plausible, has counterexample, teaches a lesson. |
| Learning objective achieved | Re-read `learning_objective`. Does the editorial teach this? |
| Difficulty calibration | Depth matches target rating. Easy = hand-holding. Hard = respect. |
| Self-contained | Editorial stands alone without referring back to solution JSON. |

## Evidence-Before-Claims

Every claim MUST be backed by evidence shown in the output:
- Claim O(N log N)? Show the derivation from algorithm structure.
- Claim walkthrough is correct? Show the trace on Sample 1.
- Claim a common mistake fails? Show the specific counterexample.
- Claim hints are progressive? Show what each reveals that the previous did not.

## Escalation Protocol

If inputs are missing or contradictory, output:

```json
{
  "status": "NEEDS_CONTEXT",
  "missing": ["list", "of", "missing", "inputs"],
  "reason": "Clear explanation of what's missing and why it's needed"
}
```

Do NOT guess or fabricate missing information.

## Prompt File

`prompts/06_editorial_writer.md`
