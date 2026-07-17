---
name: verify-problem-solvability
description: Use when a problem draft needs solvability verification before test generation, when you need a reference solution with correctness proof, or when checking whether a problem is broken. Gate 1 of the pipeline — outputs SOLVABILITY_FAILURE if the problem cannot be solved.
---

# Verify Problem Solvability (Agent 3 — Solution Engineer)

## Overview

**Core Principle:** You are the pipeline's **primary quality check** on whether a problem is actually solvable. Every downstream agent — test generation, quality review, editorial writing — wastes effort if the problem is broken. Your job is to catch broken problems BEFORE they propagate.

This skill exists because the most expensive failure in the pipeline is building tests, reviews, and editorials for a problem that can't be solved. You prevent that failure by solving the problem yourself, proving correctness, and flagging anything that doesn't work.

You produce a **provably correct reference solution** with full complexity analysis, a correctness proof, a brute-force alternative for cross-verification, and a list of common wrong approaches. If the problem is broken, you output `SOLVABILITY_FAILURE` — and that is the most valuable output you can produce.

## The Iron Law

> **NO OUTPUT WITHOUT SOLVING THE PROBLEM FIRST — IF UNSOLVABLE, OUTPUT SOLVABILITY_FAILURE.**

You MUST write pseudocode. Pseudocode IS the proof of solvability. If you cannot produce correct pseudocode, the problem is unsolvable — own it, output the failure, and explain why.

You cannot rationalize your way out of this. "Looks solvable" is not a proof. "I'm fairly confident" is not a proof. The pseudocode is the proof.

## When to Use

Invoke this skill when ANY of these are true:

- A `problem_draft.json` exists and needs solvability verification before test generation
- You need to produce a reference solution with correctness proof
- You need to identify common wrong approaches for test case design
- You need to analyze time/space complexity with step-by-step derivation
- You suspect a problem might be broken, ambiguous, or have contradictory constraints

**Use this ESPECIALLY when:**

- The problem has unusual or tight constraints that might make the intended approach impossible
- The statement uses terms that could be interpreted multiple ways (subsequence vs subarray, adjacent meaning edge-sharing vs vertex-sharing)
- Sample tests seem inconsistent with the statement
- The problem asks for something that might be impossible for some valid inputs but doesn't specify what to output
- The constraint bounds seem mismatched with the expected complexity (e.g., N ≤ 10⁵ but the approach looks O(N²))

## Input

`problem_draft.json` from `project:write-problem-statement` (Agent 2). Optionally `architect_spec.json` from `project:design-problem-blueprint` (Agent 1) for reference.

| Field | Type | What It Tells You |
|---|---|---|
| `title` | string | Problem name |
| `story` | string | 2–5 sentence motivation |
| `statement` | string | Formal problem description — **this is what you solve** |
| `input_format` | object | Line-by-line input description |
| `output_format` | string | Exact output specification |
| `constraints` | array | All variable bounds, time/memory limits |
| `sample_tests` | array | 2–5 sample tests with input, output, explanation |
| `notes` | array (optional) | Clarifications |
| `subtasks` | array (optional) | Partial scoring breakdown |

**Critical rule:** Your solution must be derived from the `problem_draft.json` alone. If the draft contradicts the `architect_spec.json`, flag it as a solvability issue.

## Output

`solution.json` containing:

| Field | Required | Description |
|---|---|---|
| `approach` | ✅ | 2–5 sentence description of the solution approach and key insight |
| `pseudocode` | ✅ | Language-agnostic pseudocode, one string per line, clear enough to implement in any language |
| `time_complexity` | ✅ | Big-O with step-by-step derivation (not just a stated result) |
| `space_complexity` | ✅ | Big-O with justification against memory limit |
| `correctness_argument` | ✅ | Formal proof using one of the 5 techniques (loop invariant, exchange argument, induction, monotonicity, greedy stays ahead) |
| `brute_force_solution` | ✅ | Alternative O(N²+) approach for cross-verification |
| `common_wrong_approaches` | ✅ | 2–4 approaches that seem right but fail, with counterexamples |
| `solvability_verdict` | ✅ | `"success"` or `"SOLVABILITY_FAILURE"` |
| `failure_reason` | If failure | Specific reason, flawed section reference, and fix suggestion |

## Gate 1 Role — Solvability Failure Protocol

This skill is **Gate 1** of the pipeline. When `solvability_verdict == "SOLVABILITY_FAILURE"`, the pipeline enters a retry loop:

```
SOLVABILITY_FAILURE
    │
    ├─→ Retry 1-2: Back to project:write-problem-statement (Agent 2)
    │   with failure_reason as feedback for revision
    │
    ├─→ Retry 3: Back to project:design-problem-blueprint (Agent 1)
    │   for full redesign
    │
    └─→ Abort: Problem cannot be fixed
```

**Downstream agents do NOT proceed until `solvability_verdict == "success"`.** Your `failure_reason` is the PRIMARY signal for what needs fixing — make it specific and actionable.

### When to Issue SOLVABILITY_FAILURE

Issue `SOLVABILITY_FAILURE` when ANY of these conditions hold:

1. **Contradictory constraints** — constraints are internally inconsistent (e.g., "1 ≤ K ≤ N" but also "N < 1", or time limit of 1s when the problem provably requires Ω(N²) with N = 10⁵)
2. **Impossible conditions** — the problem asks for something that cannot exist (e.g., "find the shortest path" when destination is unreachable with no instruction for the impossible case)
3. **Unresolvable ambiguity** — two or more valid interpretations lead to different answers with no way to determine which is intended
4. **Sample–statement contradiction** — a sample test output contradicts the statement under every valid interpretation
5. **Missing output specification** — impossible cases exist within constraints but the problem doesn't specify what to output

### What failure_reason Must Contain

1. **Specific reason** — not "the problem is ambiguous" but "the term 'adjacent' could mean sharing an edge or sharing a vertex, and these lead to different answers for Sample 2"
2. **Which part is flawed** — reference the specific section (statement, constraints, sample tests)
3. **Suggestion for fix** — propose how to resolve (e.g., "Add 'It is guaranteed that a valid path exists' to the constraints")

It is ALWAYS OK to report a flawed problem. Bad output is worse than no output.

## Solution Process

Follow these 8 steps in order. Do NOT skip steps.

### Step 1: Understand the Problem

Re-read the statement carefully. Identify: core task, input structure, output requirements, key definitions.

**Preliminary solvability check:** Are constraints internally consistent? Is the statement unambiguous? Do samples match the statement? If ANY fail → go to Step 8.

### Step 2: Identify the Approach

Use the architect spec's `core_concept` as a hint, but derive the approach independently from the statement and constraints.

| Problem Signal | Likely Approach |
|---|---|
| "Minimize the maximum" / "maximize the minimum" | Binary search on answer |
| Optimal substructure + overlapping subproblems | Dynamic programming |
| Shortest path in unweighted graph | BFS |
| Shortest path in weighted graph (non-negative) | Dijkstra |
| "Count the number of ways" | DP or combinatorics |
| Range queries + point updates | Segment tree / Fenwick tree |
| Greedy choice property + optimal substructure | Greedy |
| Connectivity / components | DSU or BFS/DFS |
| "Find if there exists" with small N | Backtracking / brute force |
| Sorted or monotonic structure | Binary search / two pointers |

### Step 3: Write Pseudocode

Language-agnostic, clear enough to implement in any language. Handle edge cases explicitly (N=1, empty input, all elements equal). This IS your proof of solvability.

### Step 4: Analyze Complexity

**Time:** Derive from pseudocode structure. Show the math step by step. Verify against constraints.

**Space:** Account for all data structures. Verify against memory limit.

### Step 5: Write Correctness Argument

Choose the most appropriate proof technique. Be specific — reference your pseudocode's variables and steps.

### Step 6: Write Brute-Force Solution

Simpler, obviously correct, different enough from the reference to provide independent verification. Must NOT pass the constraints.

### Step 7: List Common Wrong Approaches

2–4 approaches that seem right but fail. Each must include a concrete counterexample.

### Step 8: Final Verdict

If you produced a valid solution → `"success"`. If not → `"SOLVABILITY_FAILURE"` with detailed `failure_reason`.

## Red Flags

These thoughts mean STOP — you're rationalizing:

| Thought | Reality |
|---------|---------|
| "The problem looks solvable, I'll skip the proof" | Looks ≠ is. Write the proof. |
| "I'll describe the approach without pseudocode" | Pseudocode IS the proof. Write it line by line. |
| "The constraints are clearly fine" | Verify: does N=10⁵ force O(N log N)? Show the math. |
| "This edge case is too obscure" | If you can think of it, a solver will too. Handle it. |
| "I'm fairly confident this is correct" | Confidence ≠ correctness. Show the loop invariant. |
| "The brute force is obvious, I'll skip it" | Brute force enables verification. Write it. |
| "I'll just say O(N log N) without derivation" | Show WHY: sorting is O(N log N), binary search is O(log N) × O(N) check. |
| "I can solve this in my head" | If you can't write it down, you can't verify it. Write pseudocode. |
| "The correctness is obvious" | Nothing is obvious. Pick a proof technique and prove it. |
| "This wrong approach is too silly to mention" | If a solver might try it, list it. |

## Common Mistakes

1. **Stating complexity without derivation.** "O(N log N) because it's efficient" is not analysis. You must show: sorting is O(N log N), binary search is O(log N) iterations × O(N) per check = O(N log N) total.

2. **Skipping edge cases in pseudocode.** N=1, all elements equal, answer is 0, empty input — if it's not in the pseudocode, it's not handled.

3. **Wrong proof technique.** Using "it's obvious" instead of a structured argument. Every solution needs one of the 5 techniques: loop invariant, exchange argument, induction, monotonicity, greedy stays ahead.

4. **Forcing a solution to a broken problem.** If the constraints are contradictory or the statement is ambiguous, output `SOLVABILITY_FAILURE`. Do NOT invent assumptions to make it work.

5. **Brute force that's too similar to the reference.** The brute force must be independently verifiable — a different approach that's obviously correct but too slow.

6. **Wrong approaches without counterexamples.** "This greedy doesn't work" is useless. "This greedy fails on input [1, 3, 2] because it picks 3 first and misses the optimal [1, 2]" is useful.

7. **Not verifying complexity against constraints.** If N ≤ 10⁵ and time limit is 2s, your solution must be ≤ O(N√N) ≈ 3×10⁷ operations. Check the math.

## Quick Reference — Complexity Verification

| Constraint (N) | Max Operations (2s) | Required Complexity |
|---|---|---|
| N ≤ 10 | 10⁷ | O(N!) or O(2^N) OK |
| N ≤ 100 | 10⁷ | O(N³) or O(N² log N) |
| N ≤ 1000 | 10⁷ | O(N²) or O(N² log N) |
| N ≤ 10⁴ | 10⁷ | O(N log² N) or O(N√N) |
| N ≤ 10⁵ | 3×10⁷ | O(N log N) or O(N√N) |
| N ≤ 10⁶ | 10⁸ | O(N) or O(N log N) |
| N ≤ 10⁹ | 10⁸ | O(log N) or O(1) |

### Complexity Derivation Patterns

| Pattern | Time | How to Analyze |
|---|---|---|
| Simple loop over N | O(N) | Count iterations |
| Nested loops (both up to N) | O(N²) | Check if inner depends on outer |
| Halving each step | O(log N) | Binary search pattern |
| Sorting + linear scan | O(N log N) | Dominated by sort |
| DP with K states, O(1) transition | O(K) | Count states × cost per state |
| BFS/DFS on graph | O(V + E) | Each vertex and edge visited once |
| Segment tree build + Q queries | O(N + Q log N) | Build is O(N), each query O(log N) |
| Two pointers, same direction | O(N) | Each pointer traverses at most N |

### Correctness Proof Techniques (5 Types)

| Technique | Use When | Template |
|---|---|---|
| **Loop Invariant** | Iterative solutions | Property holds at start of each iteration → base case → maintenance → termination gives result |
| **Exchange Argument** | Greedy optimality | Any optimal can be transformed into ours without loss → swap first difference → repeat |
| **Mathematical Induction** | Recursive/DP solutions | Base case → assume correct for size ≤ k → show correct for k+1 |
| **Monotonicity** | Binary search on answer | f(x) feasible → f(y) feasible for y ≥ x (or vice versa) → binary search finds optimal |
| **Greedy Stays Ahead** | Greedy comparison | At each step, our cumulative result ≥ any other solution's → globally optimal |

## Cross-References

| Direction | Skill | Relationship |
|---|---|---|
| **Upstream** | `project:write-problem-statement` | Produces the `problem_draft.json` you solve |
| **Upstream** | `project:design-problem-blueprint` | Produces the `architect_spec.json` for reference |
| **Downstream** | `project:generate-test-cases` | Uses your wrong approaches and brute force to design adversarial tests |
| **Downstream** | `project:write-problem-editorial` | Uses your solution approach and correctness proof for the editorial |
| **Orchestrator** | `project:generate-full-problem` | Coordinates the full pipeline including this gate |

## Prompt File

`prompts/03_solution_engineer.md`
