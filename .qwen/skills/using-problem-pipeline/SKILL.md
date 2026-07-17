---
name: using-problem-pipeline
description: You MUST use this before any problem generation work - explores user intent, selects the right pipeline skills, and enforces the Iron Law of skill-first workflow
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
NO PROBLEM GENERATION WITHOUT CHECKING RELEVANT SKILLS FIRST.

If you think there is even a 1% chance a pipeline skill applies to what you are doing, you ABSOLUTELY MUST invoke it.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## Overview

**Core Principle:** Every problem generation task flows through the right pipeline skills in the right order — no exceptions, no shortcuts, no "I'll just write it directly."

This skill is the **entry point** for all competitive programming problem work. It exists to prevent the most common failure mode: jumping straight into writing a problem without using the structured pipeline that produces contest-quality output.

## The Iron Law

> **NO PROBLEM GENERATION WITHOUT CHECKING RELEVANT SKILLS FIRST.**

Before writing a single line of problem text, before designing a single test case, before sketching a solution — you MUST:

1. **Identify** which pipeline skill(s) apply to the task
2. **Invoke** them using the decision tree below
3. **Follow** each skill's workflow exactly as written

Announce: *"Using `project:skill-name` to [purpose]"* — then follow the skill.

## When to Use

Invoke this skill whenever ANY of these are true:

- The user asks to create, generate, or design a competitive programming problem
- The user mentions "problem set," "contest problem," "practice problem," or "CP problem"
- The user asks to write test cases, editorials, or problem statements
- The user wants to review or improve an existing problem
- The user mentions difficulty levels (Div1, Div2, Div3, Div4, beginner, grandmaster)
- Any request that will produce output consumed by competitive programmers

## Decision Tree

### Step 1: What is the scope?

```
User Request
│
├─ "Generate a full problem (everything)"
│   └─→ project:generate-full-problem
│       (Orchestrator — runs all 6 agents in sequence)
│
├─ "I need just [specific piece]"
│   └─→ Go to Step 2
│
└─ Unclear?
    └─→ Ask the user what they need BEFORE proceeding
```

### Step 2: Which piece?

| User Needs | Invoke Skill | Agent # | Output |
|---|---|---|---|
| Problem design / blueprint / spec | `project:design-problem-blueprint` | 1 — Problem Architect | `architect_spec.json` |
| Polished problem statement | `project:write-problem-statement` | 2 — Problem Writer | `problem_draft.json` |
| Reference solution + solvability check | `project:verify-problem-solvability` | 3 — Solution Engineer | `solution.json` |
| Test suite (15-30 adversarial cases) | `project:generate-test-cases` | 4 — Test Case Generator | `test_suite.json` |
| Quality review / adversarial scoring | `project:review-problem-quality` | 5 — Quality Reviewer | `review_verdict.json` |
| Pedagogical editorial | `project:write-problem-editorial` | 6 — Editorial Writer | `editorial.json` |

### Step 3: Single problem or problem set?

| Scope | Behavior |
|---|---|
| **Single problem** | Each skill runs once, produces one output |
| **Problem set** | `project:design-problem-blueprint` handles set-level config (difficulty distribution, topic balance); downstream skills run per-problem |

### Pipeline Order (when running pieces individually)

```
1. project:design-problem-blueprint     → architect_spec.json
                    ↓
2. project:write-problem-statement      → problem_draft.json
                    ↓
3. project:verify-problem-solvability   → solution.json        ◄── GATE 1
                    ↓
4. project:generate-test-cases          → test_suite.json
                    ↓
5. project:review-problem-quality       → review_verdict.json  ◄── GATE 2
                    ↓
6. project:write-problem-editorial      → editorial.json
```

**Gates cannot be skipped.** If Gate 1 (solvability) fails, fix the problem before continuing. If Gate 2 (quality) fails, iterate before writing the editorial.

## Cross-References

All pipeline skills (invoke by name using `project:skill-name` syntax):

- `project:design-problem-blueprint` — Agent 1: Problem Architect. Designs the blueprint (learning objective, difficulty, prerequisites, constraints, story direction).
- `project:write-problem-statement` — Agent 2: Problem Writer. Transforms architect spec into a polished, contest-ready problem statement.
- `project:verify-problem-solvability` — Agent 3: Solution Engineer. Produces provably correct reference solution with complexity analysis and correctness proof. **Gate 1.**
- `project:generate-test-cases` — Agent 4: Test Case Generator. Creates 15-30 adversarial test cases covering basic, edge, boundary, and stress scenarios.
- `project:review-problem-quality` — Agent 5: Quality Reviewer. Dual-persona adversarial review (Shield + Sword) scoring 10 quality criteria. **Gate 2.**
- `project:write-problem-editorial` — Agent 6: Editorial Writer. Writes pedagogical editorial with progressive hints and brute-force-to-optimal progression.
- `project:generate-full-problem` — Pipeline Orchestrator. Coordinates all 6 agents, manages data flow, validation gates, retry logic, and final assembly.

## Red Flags

These thoughts mean STOP — you're rationalizing:

| Thought | Reality |
|---------|---------|
| "I'll just write the problem directly" | Direct writing bypasses quality gates. Use the pipeline. |
| "This is a simple problem, doesn't need the full pipeline" | Simple problems still need solvability verification. |
| "I can skip the blueprint and go straight to writing" | The blueprint is the contract between agents. Skipping it breaks downstream. |
| "I'll write the statement and tests together" | Each skill has a specific role. Run them in order. |
| "The solvability check is overkill for this" | Gate 1 exists because unsolvable problems waste all downstream work. |
| "I don't need a quality review, I know it's good" | Gate 2 catches what you miss. Run it. |
| "Let me just generate test cases for this existing problem" | Existing problems still need `project:verify-problem-solvability` before testing. |
| "I remember how the pipeline works" | Skills evolve. Read the current version of each skill before invoking. |
| "The user just wants a quick problem" | Quick ≠ sloppy. Use `project:generate-full-problem` for the full ride. |
| "I'll handle the editorial myself" | The editorial skill has specific pedagogical structure. Use it. |

## Common Mistakes

1. **Skipping the blueprint.** The architect spec (`architect_spec.json`) is the foundation. Every downstream agent depends on it. Always start with `project:design-problem-blueprint` unless using the orchestrator.

2. **Running skills out of order.** The pipeline has dependencies. The Problem Writer needs the architect spec. The Solution Engineer needs the problem draft. Tests need the solution. Reviews need everything. Editorials come last.

3. **Ignoring gate failures.** When `project:verify-problem-solvability` returns `SOLVABILITY_FAILURE`, do NOT continue. Fix the problem at the blueprint or statement level, then re-verify.

4. **Using the orchestrator for single pieces.** If the user only needs test cases, don't run `project:generate-full-problem`. Use `project:generate-test-cases` directly (after ensuring prerequisites exist).

5. **Not reading skill instructions before invoking.** Each skill has detailed workflows, output schemas, and constraints. Read the skill — don't guess what it does.

6. **Mixing manual work with pipeline output.** If you're in the pipeline, let the pipeline produce the artifacts. Don't hand-edit `architect_spec.json` and then pass it downstream — regenerate it through the skill.

7. **Forgetting problem set mode.** When generating multiple problems, `project:design-problem-blueprint` handles set-level configuration. Don't manually design each problem independently — that breaks balance guarantees.

## User Instructions

User instructions (QWEN.md, direct requests) take precedence over skills. If the user explicitly says "just write a problem without the pipeline," respect that — but warn them that quality gates will be skipped.
