---
name: generate-full-problem
description: Use when running the full end-to-end competitive programming problem generation pipeline, generating a balanced problem set, or coordinating multiple agents with gate checks and retry loops.
dependencies:
  - project:design-problem-blueprint
  - project:write-problem-statement
  - project:verify-problem-solvability
  - project:generate-test-cases
  - project:review-problem-quality
  - project:write-problem-editorial
---

# Pipeline Orchestrator

Coordinate 6 specialized agents to generate a complete, high-quality competitive programming problem. You manage data flow, enforce validation gates, handle retry logic, and assemble the final output.

## Overview

```
You are the conductor — the agents are the musicians.
You do NOT generate problem content yourself.
You route inputs and outputs, check gates with evidence, and make go/no-go decisions.
```

Every step depends on the output of the previous step. Gates allow feedback loops when validation fails. Your job is to ensure no defective output passes downstream.

## When to Use

- Running the full end-to-end problem generation pipeline
- Generating a balanced problem set with distribution validation
- Coordinating multiple agents with gate checks and retry loops
- Assembling final output from all agent stages

### Mode Decision Tree

```
User request
  ├─ "Generate a problem about X" → Single Problem Mode (default)
  └─ "Generate a problem set / contest / training set" → Set Mode (mode: "set")
       ├─ User specifies level? → Use level-specific distribution
       ├─ User specifies set_size? → Use that count (default: 5)
       └─ User specifies topics? → Pass as topic_preferences
```

**Single Problem Mode:** One problem through the full pipeline. Output: `final_problem.json`.

**Set Generation Mode:** Agent 1 produces N architect specs with distribution validation. Each problem runs the full pipeline independently. Output: `final_problem_set.json` with set metadata and per-problem results. Set is valid if ≥80% of problems succeed.

## Iron Law

```
NO PROCEEDING PAST A GATE WITHOUT EXPLICIT VERIFICATION.
Every gate must be checked with evidence. "Looks fine" is not verification.
```

This is non-negotiable. Gates are the pipeline's quality control. Skipping a gate or proceeding without explicit verification defeats the purpose of the entire pipeline. Every gate check must be documented with evidence from the actual output.

## Pipeline Flow

```
User Parameters
      │
      ▼
┌─────────────────────────┐
│ Step 1: Agent 1         │
│ Problem Architect       │──→ architect_spec.json
│ (project:design-problem- │
│  blueprint)             │
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ Step 2: Agent 2         │
│ Problem Writer          │──→ problem_draft.json
│ (project:write-problem- │
│  statement)             │
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ Step 3: Agent 3         │
│ Solution Engineer       │──→ solution.json
│ (project:verify-problem-│
│  solvability)           │
└─────────────────────────┘
      │
      ▼
┌═════════════════════════════════════════┐
║ GATE 1: Solvability                     ║
║ Check: solution.solvability_verdict     ║
║   ├─ "success" → continue              ║
║   └─ "SOLVABILITY_FAILURE"             ║
║       → retry Agent 2 (max 2)          ║
║       → then Agent 1 (max 1)           ║
║       → then ABORT                     ║
└═════════════════════════════════════════┘
      │ (success)
      ▼
┌─────────────────────────┐
│ Step 4: Agent 4         │
│ Test Case Generator     │──→ test_suite.json
│ (project:generate-test- │
│  cases)                 │
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ Step 5: Agent 5         │
│ Quality Reviewer        │──→ review_verdict.json
│ (project:review-problem-│
│  quality)               │
└─────────────────────────┘
      │
      ▼
┌═════════════════════════════════════════┐
║ GATE 2: Quality                         ║
║ Check: review_verdict.verdict           ║
║   ├─ "APPROVED" → continue             ║
║   └─ "REVISION"                        ║
║       → route to revision_target agent  ║
║       → max 2 rounds                   ║
║       → then force-approve w/ warnings ║
└═════════════════════════════════════════┘
      │ (APPROVED)
      ▼
┌─────────────────────────┐
│ Step 6: Agent 6         │
│ Editorial Writer        │──→ editorial.json
│ (project:write-problem- │
│  editorial)             │
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│ Step 7: Assembly        │
│ Combine all outputs     │──→ final_problem.json
└─────────────────────────┘
```

### Set Generation Flow

```
User Parameters (mode=set, level, set_size, distribution)
      │
      ▼
┌─────────────────────────────────────────┐
│ Step 0: Agent 1 (Set Mode)              │
│ Generates set_metadata + N architect    │──→ set_plan.json
│ specs with distribution validation      │    (N × architect_spec.json)
└─────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────┐
│ For each problem in set (parallel-safe):│
│                                         │
│   architect_spec → Agent 2 → Agent 3    │
│     → Gate 1 → Agent 4 → Agent 5       │
│     → Gate 2 → Agent 6 → Assembly       │
│                                         │
│   Each problem is a full pipeline run.  │
│   Problems are independent.             │
└─────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────┐
│ Set Assembly                            │
│ Combine all final_problem.json files    │──→ final_problem_set.json
│ Validate set-level distribution         │
│ Set valid if ≥80% problems succeeded    │
└─────────────────────────────────────────┘
```

## Quick Reference

| Step | Agent | Skill Dependency | Input | Output | Gate After? |
|------|-------|-----------------|-------|--------|-------------|
| 1 | Problem Architect | `project:design-problem-blueprint` | User params | `architect_spec.json` | No |
| 2 | Problem Writer | `project:write-problem-statement` | `architect_spec.json` | `problem_draft.json` | No |
| 3 | Solution Engineer | `project:verify-problem-solvability` | `problem_draft.json` | `solution.json` | **Gate 1** |
| 4 | Test Case Generator | `project:generate-test-cases` | `problem_draft.json` + `solution.json` | `test_suite.json` | No |
| 5 | Quality Reviewer | `project:review-problem-quality` | All 4 outputs | `review_verdict.json` | **Gate 2** |
| 6 | Editorial Writer | `project:write-problem-editorial` | All 5 outputs | `editorial.json` | No |
| 7 | Assembly | — | All 6 outputs | `final_problem.json` | — |

### Gate Conditions

| Gate | Condition to PASS | Fail Action | Max Retries |
|------|-------------------|-------------|-------------|
| Gate 1 | `solution.solvability_verdict == "success"` | Retry Agent 2 (×2), then Agent 1 (×1), then abort | 3 total attempts |
| Gate 2 | `review_verdict.verdict == "APPROVED"` | Route to `revision_target` agent, re-run downstream | 2 rounds total |

### Gate 1 Verification Checklist

Before proceeding past Gate 1, confirm:
- [ ] `solution.json` is valid JSON (parseable, no syntax errors)
- [ ] `solution.solvability_verdict` field exists and equals `"success"`
- [ ] `solution.pseudocode` is present (not empty, not placeholder)
- [ ] `solution.correctness_argument` is present with actual proof technique
- [ ] Show the actual field values as evidence

### Gate 2 Verification Checklist

Before proceeding past Gate 2, confirm:
- [ ] `review_verdict.json` is valid JSON
- [ ] `review_verdict.verdict` field exists and equals `"APPROVED"`
- [ ] All 10 Shield scores are present and each ≥ 8
- [ ] `review_verdict.sword_check` contains actual adversarial findings
- [ ] Show the actual scores as evidence

## Retry Logic

### Gate 1: Solvability Retry Loop

When `solvability_verdict == "SOLVABILITY_FAILURE"`:

```
gate1_retries = 0
gate1_agent1_retries = 0

while solvability_verdict == "SOLVABILITY_FAILURE":
    if gate1_retries < 2:
        # Retry Agent 2 (Problem Writer) with failure feedback
        gate1_retries += 1
        input_to_agent2 = problem_draft.json + solution.json.failure_reason
        problem_draft.json = run Agent 2 with input_to_agent2
        solution.json = run Agent 3 with problem_draft.json

    elif gate1_agent1_retries < 1:
        # Escalate to Agent 1 (Problem Architect) for full redesign
        gate1_agent1_retries += 1
        architect_spec.json = run Agent 1 with original_params + failure_context
        problem_draft.json = run Agent 2 with architect_spec.json
        solution.json = run Agent 3 with problem_draft.json

    else:
        # Max retries exceeded — abort with partial output
        output partial_result with error flags
        stop pipeline
```

**Key rules:**
- Max 2 retries to Agent 2. Each retry includes `failure_reason` from Agent 3.
- After 2 failed Agent 2 retries, escalate to Agent 1 for full redesign.
- Max 1 retry to Agent 1. If the redesigned problem also fails, abort.
- Total max attempts: 4 (initial + 2 Agent 2 retries + 1 Agent 1 redesign).

### Gate 2: Quality Revision Loop

When `review_verdict.verdict == "REVISION"`:

```
revision_round = review_verdict.round  # starts at 1
max_rounds = 2

while verdict == "REVISION" and revision_round < max_rounds:
    revision_round += 1
    target = review_verdict.revision_target

    if target == "problem_writer":
        problem_draft.json = run Agent 2 with specific_feedback + previous_outputs
        solution.json = run Agent 3 with problem_draft.json       # re-run downstream
        test_suite.json = run Agent 4 with problem_draft.json + solution.json

    elif target == "solution_engineer":
        solution.json = run Agent 3 with problem_draft.json + specific_feedback
        test_suite.json = run Agent 4 with problem_draft.json + solution.json

    elif target == "test_generator":
        test_suite.json = run Agent 4 with problem_draft.json + solution.json + specific_feedback

    review_verdict.json = run Agent 5 with all outputs + round=revision_round

if verdict == "REVISION" and revision_round >= max_rounds:
    # Force approve with warnings
    review_verdict.verdict = "APPROVED"
    review_verdict.warnings = review_verdict.specific_feedback
```

**Key rules:**
- Max 2 revision rounds total.
- Route feedback to the specific `revision_target` agent identified by Agent 5.
- After fixing, re-run ALL downstream agents (e.g., if problem_writer revises, re-run Agent 3 and Agent 4).
- If round 2 still produces REVISION, force-approve with warnings.

## Confidence-Based Routing

| Confidence | Action | Description |
|------------|--------|-------------|
| < 0.5 | **Escalate** | Route back or flag for human review. Do not proceed without intervention. |
| 0.5–0.8 | **Flag for scrutiny** | Proceed but note for Agent 5 to pay special attention. |
| ≥ 0.8 | **Proceed** | Continue pipeline normally. |

**Confidence is not a free pass.** Even high-confidence outputs must pass through Gate 1 and Gate 2. Confidence supplements, but does not replace, gate checks.

## Red Flags

If you catch yourself thinking any of these, stop and verify:

- **"The pipeline is running fine"** → Check each gate explicitly. Don't assume.
- **"The reviewer approved it"** → Verify: are all 10 Shield scores ≥ 8?
- **"I'll trust the agent's confidence score"** → Confidence ≠ correctness. Check the actual output.
- **"This retry is taking too long"** → Bounded retries exist for a reason. Use them.
- **"The solution looks correct"** → "Looks" is not verification. Check `solvability_verdict`.
- **"I'll skip Gate 1 to save time"** → Gate 1 catches unsolvable problems. Skipping wastes more time downstream.
- **"One revision round is enough"** → If scores are still < 8, another round is needed.

## Common Mistakes

1. **Skipping Gate 1** — The most dangerous mistake. An unsolvable problem wastes all downstream effort (test generation, quality review, editorial). Gate 1 exists for a reason.

2. **Trusting confidence scores instead of checking gates** — An agent may report 0.9 confidence but still have a broken solution. Confidence is a signal, not a substitute for the solvability verdict.

3. **Proceeding past a gate without showing evidence** — "Gate 1 passed" is not enough. You must show: `solvability_verdict = "success"`, pseudocode present, correctness argument present.

4. **Not re-running downstream agents after revision** — If Agent 2 revises the problem statement, Agent 3's solution may no longer match. Always re-run all downstream agents after any revision.

5. **Force-approving too early** — Force-approve is the LAST resort after 2 full revision rounds. Never force-approve after just 1 round.

6. **Discarding partial outputs on failure** — Always preserve intermediate outputs for debugging. Even failed pipelines produce diagnostic value.

7. **Ignoring set distribution validation** — In set mode, if too many problems fail in one category, the distribution skews. Flag the warning even if ≥80% succeeded.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "The solution looks correct" | "Looks" is not verification. Check the `solvability_verdict` field. |
| "One revision round is enough" | If scores are still < 8, another round is needed. |
| "I'll skip Gate 1 to save time" | Gate 1 catches unsolvable problems. Skipping wastes more time downstream. |
| "The agent said it's done" | Check the output format. Is it valid JSON? Does it match the schema? |
| "The quality report looks good" | Read the actual scores. Are all 10 Shield scores ≥ 8? |
| "This problem is obviously solvable" | Obviously ≠ provably. Check the pseudocode and correctness argument. |
| "I'll trust the confidence score" | Confidence ≠ correctness. The gate verdict is the only authority. |
| "The revision was minor, no need to re-run downstream" | Any change to the problem statement can invalidate the solution and tests. Re-run. |

## Error Handling

### Invalid JSON

If any agent produces output that is not valid JSON:
1. **First occurrence:** Retry the same agent with a format reminder: *"Your previous output was not valid JSON. Ensure you output ONLY a JSON object — no markdown fences, no explanation text. Re-read the output contract and try again."*
2. **Second occurrence:** Attempt to extract JSON (look for content between `{` and `}`). If extraction fails, treat as max retries exceeded.

### Escalation Protocol

If the pipeline fails after max retries, output a partial result:

```json
{
  "status": "PARTIAL_FAILURE",
  "failed_stage": "gate_1 | gate_2 | agent_N",
  "failure_reason": "Clear explanation of what failed and why",
  "partial_outputs": {
    "architect_spec": "<output or null>",
    "problem_draft": "<output or null>",
    "solution": "<output or null>",
    "test_suite": "<output or null>",
    "review_verdict": "<output or null>",
    "editorial": "<output or null>"
  },
  "warnings": [
    "Pipeline failed at [stage] after [N] retries",
    "Reason: [specific failure reason]",
    "Recommendation: [what to fix or try differently]"
  ]
}
```

Do NOT fabricate outputs to complete the pipeline. Report the failure honestly.

## Assembly Process

After all 6 agents produce approved outputs, assemble `final_problem.json`:

```json
{
  "metadata": {
    "id": "prob_<domain>_<topic>_<timestamp>",
    "domain": "<from architect_spec.domain>",
    "topic": "<from architect_spec.topic>",
    "subtopic": "<from architect_spec.subtopic>",
    "difficulty": {
      "codeforces_rating": "<from architect_spec>",
      "tier": "<from architect_spec>"
    },
    "tags": "<from architect_spec.tags>",
    "bloom_level": "<from architect_spec>",
    "prerequisites": "<from architect_spec>",
    "generated_at": "<ISO 8601 timestamp>",
    "pipeline_rounds": "<total Gate 2 revision rounds executed>"
  },
  "problem": "<problem_draft.json in full>",
  "solution": "<solution.json in full>",
  "test_suite": "<test_suite.json in full>",
  "editorial": "<editorial.json in full>",
  "quality_report": {
    "shield_scores": "<review_verdict.shield_check — all 10 dimension scores>",
    "sword_findings": "<review_verdict.sword_check — all findings>",
    "pipeline_rounds": "<same as metadata.pipeline_rounds>",
    "warnings": "<review_verdict.warnings — remaining issues if force-approved>"
  }
}
```

**Assembly rules:**
1. Metadata is derived from Agent 1's output — the architect spec defines the problem's identity.
2. `problem`, `solution`, `test_suite`, `editorial` are the full, unmodified agent outputs.
3. `quality_report` is extracted from Agent 5's Shield scores, Sword findings, and warnings.
4. `pipeline_rounds` = 0 if approved first round, 1 if one revision, 2 if force-approved.
5. `id` format: `prob_<domain>_<topic>_<ISO timestamp>` (e.g., `prob_dsa_arrays_20250117T120000Z`).

## Mandatory Completion Checklist

Before outputting the final result, verify ALL steps:

- [ ] Step 1: Agent 1 executed, `architect_spec.json` validated against schema
- [ ] Step 2: Agent 2 executed, `problem_draft.json` validated against schema
- [ ] Step 3: Agent 3 executed, `solution.json` validated against schema
- [ ] **Gate 1: `solvability_verdict == "success"` verified with evidence shown**
- [ ] Step 4: Agent 4 executed, `test_suite.json` validated (≥ 10 test cases)
- [ ] Step 5: Agent 5 executed, `review_verdict.json` validated against schema
- [ ] **Gate 2: `verdict == "APPROVED"` verified with all 10 Shield scores ≥ 8 shown**
- [ ] Step 6: Agent 6 executed, `editorial.json` validated against schema
- [ ] Step 7: Assembly complete — all fields present in `final_problem.json`

If any checkbox is unchecked, go back and complete it.

## Evidence-Before-Claims

Every claim must be backed by evidence shown in your output:
- If you claim a gate passes, show the actual field values.
- If you claim an output is valid JSON, show the parse result or schema validation.
- If you claim a retry is needed, show the specific failure condition.
- If you claim the pipeline is complete, show all 6 agent outputs with validation status.

DO NOT state conclusions without showing the work that leads to them.
