---
name: write-statement
description: Use when converting an architect_spec.json into a polished competitive programming problem statement, writing story/input-output format/constraints/sample tests, or running the anti-ambiguity checklist on a problem draft.
---

# Problem Writer (Agent 2)

## Overview

Transform an architectural blueprint into a polished problem statement that feels like it belongs in a real contest. Your job is NOT to design the algorithm — that is already done. Your job is to **bring the problem to life**: write a compelling story, state the problem with surgical precision, design constraints that guide solvers toward the intended approach, and create sample tests that teach the solver how the problem works.

**Core principle:** A boring, clear problem is better than an exciting, ambiguous one. Every term must be defined. Every assumption must be stated. Every edge case must be covered. Precision and clarity are non-negotiable.

## When to Use

- Converting an `architect_spec.json` from Agent 1 into a readable problem statement
- Writing the story, input/output format, constraints, and sample tests
- Running the anti-ambiguity checklist on a problem draft
- Refining a draft that has ambiguous language or missing edge case coverage

**Upstream dependency:** `project:design-blueprint` — the architect spec is the contract. Every field informs your output. Do not deviate from the core concept, difficulty tier, or constraint hints without strong justification.

## Iron Law

```
NO PROBLEM STATEMENT WITHOUT RUNNING THE ANTI-AMBIGUITY CHECKLIST.
Every indexing convention, every edge case, every output format detail must be explicit.
All 8 checks must pass before output. No exceptions.
```

## Input

`architect_spec.json` from Agent 1 (Problem Architect) containing:

| Field | Type | What It Tells You |
|---|---|---|
| `domain` | string | Problem domain (`dsa`, `language_learning`, `competitive_programming`) |
| `topic` | string | High-level topic area (e.g., `"arrays"`, `"graphs"`) |
| `subtopic` | string | Specific subtopic (e.g., `"prefix sums with frequency counting"`) |
| `difficulty` | object | `codeforces_rating` (int), `tier` (easy/medium/hard/expert), `bloom_level` |
| `learning_objective` | string | What the solver will learn or demonstrate |
| `prerequisites` | array | Concepts the solver already knows |
| `core_concept` | string | The single new concept being taught/tested |
| `tags` | array | Standard CP tags for the problem |
| `constraint_hints` | object | `n_range` [min, max], `expected_complexity`, `time_limit_seconds` |
| `story_direction` | string | 1–3 sentence suggestion for the thematic wrapper |

## Output

`problem_draft.json` containing:

| Field | Required | Description |
|---|---|---|
| `title` | Yes | Short, memorable problem name. Max 6 words. No jargon. |
| `story` | Yes | 2–5 sentence thematic wrapper. Neutral, motivating, non-distracting. |
| `statement` | Yes | Full problem statement with precise language. Every term defined. |
| `input_format` | Yes | Line-by-line specification of every input token. |
| `output_format` | Yes | Exact output specification (modulo, precision, separators). |
| `constraints` | Yes | Array of constraint strings. Every variable bounded. |
| `sample_tests` | Yes | 2–5 samples, each with input, output, and explanation. |
| `subtasks` | No | Partial scoring breakdowns with own constraints and points. |
| `notes` | No | Clarifications and edge case hints. |

## Quick Reference — Anti-Ambiguity Checklist (8 Items)

Before finalizing ANY problem statement, verify ALL of the following:

| # | Check | What Goes Wrong If You Skip |
|---|---|---|
| 1 | **Every term is defined on first use** | Solvers guess whether "subsequence" means contiguous or not |
| 2 | **Indexing is specified** (1-based or 0-based) | Off-by-one errors on correct solutions |
| 3 | **Edge cases are mentioned** ("If no answer exists, print -1") | Solvers don't know what to output for impossible cases |
| 4 | **Output format is exact** (modulo? precision? newline? spaces?) | "Print the answer" — modulo what? How many decimal places? |
| 5 | **Constraints are complete** (every variable has bounds) | Solvers don't know if elements can be negative, zero, etc. |
| 6 | **Single interpretation** — the statement cannot be read two ways | Post-contest clarification requests and rejudging |
| 7 | **No gotchas** — no hidden tricks beyond the core concept | Solvers feel cheated, not challenged |
| 8 | **No hidden assumptions** — everything needed is stated | Assumptions buried in examples rather than in the statement |

**Self-test:** Read your statement WITHOUT looking at the examples. Can you implement directly? If not, something is missing.

**Hard gate:** You MUST include at least 2 sample tests. You MUST specify indexing. You MUST define every term used. You MUST include constraints for every variable.

## Red Flags

If any of these thoughts cross your mind, you are about to produce a defective problem:

- **"Statement is clear enough"** → You wrote it. Re-read as a stranger. Is every term defined?
- **"I'll skip the edge case sample"** → Every problem needs an N=1 or boundary test. Add it.
- **"The story is just flavor"** → Story motivates the algorithm. If it doesn't connect, rewrite it.
- **"Constraints are the architect's job"** → You set the final numbers. Verify they force the intended complexity.
- **"This ambiguity is minor"** → Minor ambiguity = wrong interpretation = frustrated solver. Fix it.
- **"Sample tests give away the approach"** → Samples illustrate mechanics, not approach. Rewrite them if they reveal the technique.
- **"I'll skip the notes section"** → Notes clarify edge cases. Add them.
- **"The input format is obvious"** → Obvious to you ≠ obvious to solver. Specify line by line.
- **"This is just a formatting detail"** → Formatting details cause Wrong Answer. Specify exactly.

## Rationalization Table

| Excuse | Reality |
|---|---|
| "The statement is clear to me" | You wrote it. Read it as a stranger. Is indexing specified? |
| "I'll skip the edge case sample" | Every problem needs an N=1 or boundary test. Add it. |
| "The story is just flavor" | Story motivates the algorithm. If it doesn't connect, rewrite it. |
| "Constraints are the architect's job" | You set the final numbers. Verify they force the intended complexity. |
| "This ambiguity is minor" | Minor ambiguity = wrong interpretation = frustrated solver. Fix it. |
| "Sample tests give away the approach" | Samples illustrate mechanics, not approach. If they reveal the technique, rewrite them. |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Ambiguous constraint wording | Add "It is guaranteed that..." for implicit constraints |
| Undefined terms ("subsequence", "subarray") | Define on first use: "A subarray is a contiguous portion of the array" |
| Missing indexing convention | State explicitly: "The array is 1-indexed: elements are A₁, A₂, ..., Aₙ" |
| Vague output format | Specify exactly: modulo, precision, separators, impossible-case output |
| Incomplete variable bounds | Every input variable must have explicit bounds in constraints |
| All samples are trivial | Each sample needs a purpose: basic mechanics, non-obvious behavior, edge case |
| Story misleads about algorithm | A "shortest path" story should not have a DP solution |
| Notes used to fix bad statement | If the statement needs notes to be understandable, rewrite the statement |

## Sample Test Design Rules

Every sample test must serve a specific purpose. Never include a "filler" test.

| Test # | Purpose | Design Guidelines |
|---|---|---|
| **Sample 1** | Basic mechanics | Smallest non-trivial input. Demonstrates I/O format. Traceable by hand. |
| **Sample 2** | Non-obvious behavior | Demonstrates something NOT immediately obvious from the statement. |
| **Sample 3** | Edge case | Minimum input size (N=1), or answer is 0/-1/empty. |
| **Sample 4** (optional) | Scale / constraint boundary | Moderately large input showing the format scales. |
| **Sample 5** (optional) | Multiple valid answers | If problem accepts any valid answer, show different acceptable outputs. |

**Rules:**
- All sample inputs must be small enough to trace by hand (N ≤ 10 typically)
- Every sample must have an explanation walking through WHY the output is correct
- Samples must be consistent with the statement — no contradictions
- If the problem has subtasks, at least one sample should satisfy the smallest subtask's constraints

## Constraint Design Rules

Constraints are a communication channel with the solver. The right constraints say "you need O(N log N)" without saying it.

**Constraint–Complexity Table:**

| Intended Complexity | Set N to at most |
|---|---|
| O(N!) | 10–12 |
| O(2^N) | 20–22 |
| O(N³) | 300–500 |
| O(N² log N) | 1,000–2,000 |
| O(N²) | 2,000–5,000 |
| O(N log N) | 10⁵ – 5 × 10⁵ |
| O(N √N) | 10⁵ |
| O(N) | 10⁶ – 10⁷ |
| O(√N) | 10⁹ – 10¹² |
| O(log N) | 10⁹ – 10¹⁸ |

**Key rules:**
1. **Reverse-engineer from complexity** — start with intended solution's Big-O, then set N
2. **Exclude simpler solutions** — the next-slower complexity class must NOT pass
3. **Use natural values** — powers of 10 (10⁵, 10⁶) or common values (2000, 5000)
4. **Account for test cases** — use "sum of N over all test cases does not exceed X"
5. **Check memory** — 2D int array of N×N viable only up to N ≈ 5000 (100 MB)
6. **State all constraints explicitly** — variable ranges, array sizes, sum constraints, special guarantees
7. **Include time limit** (standard: 1–2 seconds) and **memory limit** (standard: 256 MB)

## Story-to-Algorithm Mapping

The story should MOTIVATE the algorithm, not obscure it. Good stories make the solver think "of course you'd need [algorithm] for this!"

| Algorithm / Concept | Good Story | Why It Works |
|---|---|---|
| Binary search on answer | "Minimum daily rainfall to ensure all fields watered within D days" | "Minimum maximum" framing suggests binary search |
| Prefix sums + frequency | "How many books of genre G between positions L and R?" | Range queries over categories → prefix frequency arrays |
| BFS / shortest path | "Minimum steps from start to exit in a grid warehouse" | Grid + minimum steps = BFS |
| Sliding window | "For every contiguous block of K readings, find the maximum" | "Every contiguous block of K" → sliding window |
| DP (knapsack) | "Maximize total value carried in a bag with weight capacity W" | Physical constraint + optimization = knapsack |

**Story rules:** 2–5 sentences. Neutral and inclusive. Explainable in one sentence. No added complexity. No misleading framing.

## Writing Process

Follow these 8 steps in order. Do NOT skip steps.

1. **Read the architect spec** — identify the one thing the solver must learn (`core_concept`), what they already know (`prerequisites`), target difficulty, and story direction. Can you state the intended solution in one sentence? If not, re-read.

2. **Design the story** — expand `story_direction` into 2–5 sentences. Must not reveal the algorithm. Must not add complexity beyond the core concept.

3. **Write the problem statement** — complete, unambiguous, precise, self-contained. Define custom terms on first use. State indexing explicitly. Use "It is guaranteed that..." for implicit constraints. Use "If there are multiple valid answers, print any of them" or "If it is impossible, print -1" as appropriate.

4. **Define input/output format line by line** — describe every line and every token. Name variables consistently. Specify separators. State precision requirements.

5. **Set constraints** — use `constraint_hints` from architect spec. Every variable must have bounds. Verify against the constraint–complexity table. Include time and memory limits.

6. **Create sample tests (3–5)** — each with a specific purpose (basic mechanics, non-obvious behavior, edge case). Small enough to trace by hand. Each has input, output, and explanation.

7. **Run the anti-ambiguity checklist** — all 8 items must pass. Read the statement without looking at examples. Can you implement directly?

8. **Add notes/clarifications** — only for edge cases that don't fit in the main statement. Do NOT use notes to fix a badly written statement.

## Escalation Protocol

If the architect spec is incomplete, contradictory, or missing critical information, do NOT guess. Output:

```json
{
  "NEEDS_CONTEXT": "Description of what is missing or contradictory in the architect spec."
}
```

A partial draft with guessed constraints or a fabricated story is worse than no draft at all.

## Anti-Patterns to Avoid

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| Ambiguous statement | Terms undefined, multiple interpretations | Define every term. State all assumptions. Use "It is guaranteed that..." |
| Weak samples | All trivial, no edge cases | Each sample needs a purpose. Include explanations. |
| Constraint–solution mismatch | Brute force passes or intended solution barely fits | Use constraint–complexity table. Verify intended passes, next-slower fails. |
| Implementation-heavy | 300+ lines with no algorithmic insight | Insight should matter more than code length. |
| "Guess the output" | Only approach is careful simulation | Add constraints that force finding a pattern. |
| Insufficient edge cases | No N=1, all-same, extreme values, or answer=0 | Include edge case samples. State edge case behavior. |
| Obscure algorithm required | Solution needs research-paper technique | Ensure technique is standard for target difficulty. |
| Story misleads | Story suggests wrong algorithm | Story should motivate, not obscure. |

## Prompt File

`prompts/02_problem_writer.md`
