---
name: generate-full-problem
description: Coordinate the full 6-agent pipeline to generate a complete competitive programming problem. Manages data flow, validation gates (solvability + quality), retry logic, and final assembly. Supports single problem and problem set generation modes.
---

# Pipeline Orchestrator

Coordinate 6 specialized agents to generate a complete, high-quality competitive programming problem. You manage data flow, enforce validation gates, handle retry logic, and assemble the final output.

## When to Use

- Running the full end-to-end problem generation pipeline
- Generating a balanced problem set with distribution validation
- Coordinating multiple agents with gate checks and retry loops
- Assembling final output from all agent stages

## Pipeline Flow

```
User Parameters
  → [1] Problem Architect → architect_spec.json
  → [2] Problem Writer → problem_draft.json
  → [3] Solution Engineer → solution.json
  → [GATE 1: Solvable?]
      ├─ success → continue
      └─ SOLVABILITY_FAILURE → retry Agent 2 (×2), then Agent 1 (×1), then abort
  → [4] Test Case Generator → test_suite.json
  → [5] Quality Reviewer → review_verdict.json
  → [GATE 2: Quality?]
      ├─ APPROVED → continue
      └─ REVISION → route feedback to target agent (×2 rounds), then force-approve
  → [6] Editorial Writer → editorial.json
  → [7] Assembly → final_problem.json
```

## Modes

### Single Problem (default)
One problem through the full pipeline. Output: `final_problem.json`.

### Problem Set (`mode: "set"`)
Step 0: Agent 1 produces N architect specs with distribution validation.
Each problem runs the full pipeline independently.
Output: `final_problem_set.json` with set metadata and per-problem results.
Set is valid if ≥80% of problems succeed.

## Iron Law

```
NO PROCEEDING PAST A GATE WITHOUT EXPLICIT VERIFICATION.
Every gate must be checked with evidence. "Looks fine" is not verification.
```

## Retry Limits

| Gate | Condition | Fail Action | Max Retries |
|------|-----------|-------------|-------------|
| Gate 1 | `solvability_verdict == "success"` | Retry Agent 2 (×2), then Agent 1 (×1) | 3 total attempts |
| Gate 2 | `verdict == "APPROVED"` | Route to `revision_target` agent | 2 rounds total |

## Confidence-Based Routing

| Confidence | Action |
|------------|--------|
| < 0.5 | Escalate — route back or flag for human review |
| 0.5–0.8 | Flag for Quality Reviewer scrutiny |
| ≥ 0.8 | Proceed normally |

## Prompt File

`prompts/orchestrator.md`
