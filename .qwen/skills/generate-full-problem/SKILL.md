---
name: generate-full-problem
description: Use when generating a complete competitive programming problem end-to-end - dispatches specialized subagents for each pipeline stage with review checkpoints between stages
---

# Generate Full Problem (Pipeline Orchestrator)

Execute the 6-agent problem generation pipeline by dispatching a fresh subagent per stage, a quality gate after each, and assembly at the end.

**Why subagents:** Each pipeline stage requires specialized expertise. By dispatching fresh subagents with precisely crafted prompts, you ensure each stage gets focused attention without context pollution from previous stages. This also preserves your own context for coordination work.

**Core principle:** Fresh subagent per stage + gate verification + retry on failure = high-quality problems

**Narration:** Between tool calls, narrate at most one short line — the ledger and tool results carry the record.

**Continuous execution:** Do not pause to check in with your human partner between stages. Execute all stages without stopping. The only reasons to stop are: SOLVABILITY_FAILURE you cannot resolve, ambiguity that genuinely prevents progress, or all stages complete.

## The Iron Law

```
NO PROCEEDING PAST A GATE WITHOUT EXPLICIT VERIFICATION.
Every gate must be checked with evidence. "Looks fine" is not verification.
```

## When to Use

**Use this skill when:**
- User asks to generate a complete problem from scratch
- User wants to run the full pipeline end-to-end
- User asks for a problem set with multiple problems

**Use this ESPECIALLY when:**
- The problem concept is complex and needs specialized attention at each stage
- You need adversarial quality review before finalizing
- The user wants a complete package (problem + solution + tests + editorial)

**Don't skip when:**
- The problem seems simple (simple problems still need verification)
- You're in a hurry (rushing guarantees low-quality output)
- The user just wants "a quick problem" (quality matters regardless of speed)

## The Process

```
User Parameters
      │
      ▼
┌─────────────────────────────────┐
│ Stage 1: Problem Architect      │
│ Subagent: design-problem-spec   │
│ Output: architect_spec.json     │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ Stage 2: Problem Writer         │
│ Subagent: write-problem-stmt    │
│ Output: problem_draft.json      │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ Stage 3: Solution Engineer      │
│ Subagent: verify-solvability    │
│ Output: solution.json           │
└─────────────────────────────────┘
      │
      ▼
═════════════════════════════════
║ GATE 1: Solvability Check       ║
║   ├─ success → continue         ║
║   └─ FAILURE → retry Stage 2    ║
║       (max 2 retries)           ║
║       → then Stage 1 (max 1)    
└═════════════════════════════════┘
      │ (success)
      ▼
┌─────────────────────────────────┐
│ Stage 4: Test Case Generator    │
│ Subagent: generate-test-cases   │
│ Output: test_suite.json         │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ Stage 5: Quality Reviewer       │
│ Subagent: review-quality        │
│ Output: review_verdict.json     │
└─────────────────────────────────┘
      │
      ▼
═════════════════════════════════
║ GATE 2: Quality Check           
║   ├─ APPROVED → continue        ║
║   └─ REVISION → retry target    ║
║       (max 2 rounds)            ║
└═════════════════════════════════┘
      │ (APPROVED)
      ▼
┌─────────────────────────────────┐
│ Stage 6: Editorial Writer       │
│ Subagent: write-editorial       │
│ Output: editorial.json          │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ Stage 7: Assembly               │
│ Combine all outputs             │
│ Output: final_problem.json      │
─────────────────────────────────┘
```

## Pre-Flight Check

Before dispatching Stage 1, verify:
- User parameters are clear (domain, topic, difficulty, etc.)
- If parameters are ambiguous, ask clarifying questions NOW, not mid-pipeline
- Check for existing ledger: `cat .superpowers/sdd/progress.md` — resume at first incomplete stage

## Model Selection

Use the least powerful model that can handle each stage:

| Stage | Complexity | Recommended Model |
|-------|------------|-------------------|
| 1. Architect | High (design decisions) | Most capable |
| 2. Writer | Medium (creative writing) | Standard |
| 3. Solution | High (correctness proof) | Most capable |
| 4. Test Gen | Medium (adversarial thinking) | Standard |
| 5. Review | High (judgment calls) | Most capable |
| 6. Editorial | Medium (pedagogical writing) | Standard |

**Always specify the model explicitly when dispatching.** An omitted model inherits your session's model — often the most expensive.

## Dispatching Subagents

### Stage 1: Problem Architect

```
Subagent (general-purpose):
  description: "Design problem blueprint"
  model: [MOST_CAPABLE]
  prompt: |
    You are designing a competitive programming problem blueprint.

    ## Your Job

    Produce a structured specification (architect_spec.json) that downstream agents will consume.

    ## Input Parameters

    [USER_PARAMETERS]

    ## Your Output

    Output ONLY a valid JSON object conforming to the architect spec schema.
    No markdown fences, no explanation text, no preamble.

    ## Iron Law

    NO PROBLEM DESIGN WITHOUT A CLEAR, SPECIFIC LEARNING OBJECTIVE.
    Every problem must teach exactly ONE concept.

    ## Quality Criteria

    - One new concept per problem
    - Constraints force the intended approach
    - Prerequisites are concrete and complete
    - Difficulty rating matches tier and Bloom level

    Write your output to: architect_spec.json
    Then report: Status (DONE/BLOCKED), file path, one-line summary.
```

### Stage 2: Problem Writer

```
Subagent (general-purpose):
  description: "Write problem statement"
  model: [STANDARD]
  prompt: |
    You are transforming an architect spec into a polished problem statement.

    ## Your Job

    Read architect_spec.json and produce problem_draft.json.

    ## Input

    Read: architect_spec.json

    ## Your Output

    Output ONLY a valid JSON object conforming to the problem draft schema.
    No markdown fences, no explanation text, no preamble.

    ## Iron Law

    NO PROBLEM STATEMENT WITHOUT RUNNING THE ANTI-AMBIGUITY CHECKLIST.
    Every indexing convention, every edge case, every output format detail must be explicit.

    ## Anti-Ambiguity Checklist

    1. Is 1-indexed vs 0-indexed explicitly stated?
    2. Are all variable names defined on first use?
    3. Is the output format exact (newlines, spaces, case)?
    4. Are edge cases (N=1, empty input, all same) mentioned or sample-tested?
    5. Are constraints complete (no implicit bounds)?
    6. Is the story free of cultural specificity?
    7. Can the solver determine the answer for every sample without guessing?
    8. Is there exactly one valid interpretation of every sentence?

    Write your output to: problem_draft.json
    Then report: Status (DONE/BLOCKED), file path, one-line summary.
```

### Stage 3: Solution Engineer

```
Subagent (general-purpose):
  description: "Verify solvability and produce solution"
  model: [MOST_CAPABLE]
  prompt: |
    You are verifying the problem is solvable and producing a reference solution.

    ## Your Job

    Read problem_draft.json and produce solution.json with a provably correct solution.

    ## Input

    Read: problem_draft.json

    ## Your Output

    Output ONLY a valid JSON object conforming to the solution schema.
    No markdown fences, no explanation text, no preamble.

    ## Iron Law

    NO OUTPUT WITHOUT SOLVING THE PROBLEM FIRST — IF UNSOLVABLE, OUTPUT SOLVABILITY_FAILURE.
    You MUST write the pseudocode. Pseudocode IS the proof of solvability.

    ## Critical Responsibility

    If the problem has contradictory constraints, impossible conditions, or is ambiguous beyond any valid interpretation, you MUST output:
    {
      "solvability_verdict": "SOLVABILITY_FAILURE",
      "failure_reason": "Specific description of what's broken"
    }

    This is the most important feedback you can give — it triggers a feedback loop back to the Problem Writer to fix the problem.

    Write your output to: solution.json
    Then report: Status (DONE/SOLVABILITY_FAILURE/BLOCKED), file path, one-line summary.
```

### Gate 1: Solvability Check

**Read solution.json and check `solvability_verdict`:**

**If `"success"`:**
- Gate 1 passes. Proceed to Stage 4.

**If `"SOLVABILITY_FAILURE"`:**
- Gate 1 fails. Enter retry loop:
  - Retry Stage 2 (Problem Writer) with failure feedback — max 2 retries
  - Then retry Stage 1 (Problem Architect) for full redesign — max 1 retry
  - Then abort with partial output

### Stage 4: Test Case Generator

```
Subagent (general-purpose):
  description: "Generate adversarial test suite"
  model: [STANDARD]
  prompt: |
    You are creating a comprehensive test suite that catches ALL common wrong approaches.

    ## Your Job

    Read problem_draft.json and solution.json, produce test_suite.json.

    ## Input

    Read: problem_draft.json, solution.json

    ## Your Output

    Output ONLY a valid JSON object conforming to the test suite schema.
    No markdown fences, no explanation text, no preamble.

    ## Iron Law

    NO TEST SUITE WITHOUT COVERING ALL WRONG APPROACHES FROM THE SOLUTION.
    Every common_wrong_approach must have at least one adversarial test that breaks it.

    ## Test Categories

    - basic (3-5): Verifies core mechanics
    - edge_case (5-8): N=1, empty, all same, max values
    - adversarial (3-5): Specifically breaks wrong approaches
    - boundary (2-3): Constraint boundaries, overflow
    - stress (configurable): Large random inputs for performance

    ## Mindset

    Every solution is guilty until proven innocent. Your tests are the interrogation.

    Write your output to: test_suite.json
    Then report: Status (DONE/BLOCKED), file path, test count, one-line summary.
```

### Stage 5: Quality Reviewer

```
Subagent (general-purpose):
  description: "Adversarial quality review"
  model: [MOST_CAPABLE]
  prompt: |
    You are performing adversarial quality review using dual Shield and Sword personas.

    ## Your Job

    Read all 4 preceding outputs and produce review_verdict.json.

    ## Input

    Read: architect_spec.json, problem_draft.json, solution.json, test_suite.json

    ## Your Output

    Output ONLY a valid JSON object conforming to the review verdict schema.
    No markdown fences, no explanation text, no preamble.

    ## Iron Law

    NO APPROVAL WITHOUT SCORING ALL 10 SHIELD CRITERIA — MISSING ONE IS A FAILURE.
    If ANY Shield score is below 8, the verdict MUST be REVISION.

    ## Shield Criteria (10 dimensions, score 0-10 each)

    1. Learning objective clarity
    2. Difficulty calibration accuracy
    3. Problem statement precision
    4. Constraint appropriateness
    5. Sample test quality
    6. Solution correctness
    7. Test suite coverage
    8. Editorial readiness
    9. Anti-pattern freedom
    10. Overall contest readiness

    ## Sword Attacks

    Try to break the problem:
    - Ambiguity attacks (find unclear wording)
    - Edge case attacks (find untested scenarios)
    - Constraint attacks (find constraint violations)
    - Solution attacks (find incorrect solutions that pass)

    Write your output to: review_verdict.json
    Then report: Status (DONE/BLOCKED), file path, verdict (APPROVED/REVISION), one-line summary.
```

### Gate 2: Quality Check

**Read review_verdict.json and check `verdict`:**

**If `"APPROVED"`:**
- Gate 2 passes. Proceed to Stage 6.

**If `"REVISION"`:**
- Gate 2 fails. Enter revision loop:
  - Read `revision_target` and `specific_feedback`
  - Re-run the target stage with feedback
  - Re-run all downstream stages
  - Max 2 revision rounds
  - If round 2 still REVISION → force-approve with warnings

### Stage 6: Editorial Writer

```
Subagent (general-purpose):
  description: "Write pedagogical editorial"
  model: [STANDARD]
  prompt: |
    You are writing an editorial that makes readers feel the "aha moment."

    ## Your Job

    Read all 5 preceding outputs and produce editorial.json.

    ## Input

    Read: architect_spec.json, problem_draft.json, solution.json, test_suite.json, review_verdict.json

    ## Your Output

    Output ONLY a valid JSON object conforming to the editorial schema.
    No markdown fences, no explanation text, no preamble.

    ## Iron Law

    NO EDITORIAL WITHOUT A BRUTE-FORCE → OPTIMAL PROGRESSION.
    The reader must see WHY the naive approach fails and HOW the optimal approach naturally emerges.

    ## Core Philosophy

    A good editorial makes the reader think "of course! why didn't I see that?" — not "I could never have thought of that."

    ## Required Sections

    - hints: 3 progressive hints (direction → approach → key insight)
    - brute_force_explanation: Naive approach with complexity analysis
    - optimal_solution_walkthrough: Step-by-step derivation
    - complexity_analysis: Time and space complexity with derivation
    - alternative_approaches: 2-3 valid alternatives
    - common_mistakes: 3-5 typical mistakes with explanations

    Write your output to: editorial.json
    Then report: Status (DONE/BLOCKED), file path, one-line summary.
```

### Stage 7: Assembly

Combine all outputs into `final_problem.json`:

```json
{
  "metadata": {
    "id": "prob_<domain>_<topic>_<timestamp>",
    "domain": "<from architect_spec>",
    "topic": "<from architect_spec>",
    "subtopic": "<from architect_spec>",
    "difficulty": {
      "codeforces_rating": "<from architect_spec>",
      "tier": "<from architect_spec>"
    },
    "tags": "<from architect_spec>",
    "bloom_level": "<from architect_spec>",
    "prerequisites": "<from architect_spec>",
    "generated_at": "<ISO 8601 timestamp>",
    "pipeline_rounds": "<Gate 2 revision rounds executed>"
  },
  "problem": "<problem_draft.json in full>",
  "solution": "<solution.json in full>",
  "test_suite": "<test_suite.json in full>",
  "editorial": "<editorial.json in full>",
  "quality_report": {
    "shield_scores": "<from review_verdict>",
    "sword_findings": "<from review_verdict>",
    "pipeline_rounds": "<same as metadata>",
    "warnings": "<from review_verdict if force-approved>"
  }
}
```

## Handling Subagent Status

Subagents report one of four statuses. Handle each appropriately:

**DONE:** Proceed to next stage or gate check.

**DONE_WITH_CONCERNS:** Read the concerns before proceeding. If concerns are about correctness or scope, address them before continuing. If they're observations, note them and proceed.

**NEEDS_CONTEXT:** The subagent needs information that wasn't provided. Provide the missing context and re-dispatch.

**BLOCKED:** The subagent cannot complete the stage. Assess the blocker:
1. If it's a context problem, provide more context and re-dispatch
2. If the stage requires more reasoning, re-dispatch with a more capable model
3. If the input is broken, escalate to the human

**Never** ignore an escalation or force the same model to retry without changes.

## Durable Progress

Track progress in a ledger file, not only in todos:

- At skill start, check for a ledger: `cat .superpowers/sdd/progress.md`
- When a stage completes, append one line: `Stage N: complete (output: <filename>)`
- The ledger is your recovery map after compaction

## Red Flags

**Never:**
- Skip gate verification ("looks fine" is not verification)
- Proceed past Gate 1 without checking `solvability_verdict`
- Proceed past Gate 2 without checking all 10 Shield scores ≥ 8
- Trust confidence scores without evidence
- Skip re-running downstream stages after a revision
- Accept "close enough" on quality review

**If a gate fails:**
- Follow the retry loop exactly
- Don't manually fix the issue (context pollution)
- Don't skip the gate to save time

## Integration

**Required skills:**
- **project:design-problem-blueprint** — Stage 1 subagent prompt
- **project:write-problem-statement** — Stage 2 subagent prompt
- **project:verify-problem-solvability** — Stage 3 subagent prompt
- **project:generate-test-cases** — Stage 4 subagent prompt
- **project:review-problem-quality** — Stage 5 subagent prompt
- **project:write-problem-editorial** — Stage 6 subagent prompt

**Alternative workflow:**
- Run stages manually for more control over each step
