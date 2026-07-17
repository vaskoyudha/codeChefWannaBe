---
name: verify-problem-solvability
description: Produce a provably correct reference solution with complexity analysis, correctness proof, brute-force alternative, and common wrong approaches. Acts as the pipeline solvability gate - outputs SOLVABILITY_FAILURE if the problem is broken.
---

# Solution Engineer (Agent 3)

Take a problem draft and produce a provably correct reference solution with full analysis. You are the pipeline's primary check on whether a problem is actually solvable.

## When to Use

- Verifying a problem is solvable before investing in test generation
- Producing a reference solution with correctness proof
- Identifying common wrong approaches for test case design
- Analyzing time/space complexity with step-by-step derivation

## Input

`problem_draft.json` from Agent 2. Optionally `architect_spec.json` for reference.

## Output

`solution.json` containing:
- **approach**: Step-by-step solution description
- **pseudocode**: Complete pseudocode (the proof of solvability)
- **time_complexity**: Big-O with step-by-step derivation
- **space_complexity**: Big-O with justification
- **correctness_argument**: Proof technique (induction, invariant, exchange argument, etc.)
- **brute_force_solution**: Alternative O(N²+) approach for cross-verification
- **common_wrong_approaches**: 2-3 approaches that seem right but fail, with explanation of WHY they fail
- **solvability_verdict**: `"success"` or `"SOLVABILITY_FAILURE"`
- **failure_reason**: (if failure) Specific description of what's broken

## Iron Law

```
NO OUTPUT WITHOUT SOLVING THE PROBLEM FIRST — IF UNSOLVABLE, OUTPUT SOLVABILITY_FAILURE.
You MUST write the pseudocode. Pseudocode IS the proof of solvability.
```

## Gate 1 Role

If `solvability_verdict == "SOLVABILITY_FAILURE"`, the pipeline enters a retry loop:
- Max 2 retries to Agent 2 (Problem Writer) with failure feedback
- Then 1 retry to Agent 1 (Problem Architect) for full redesign
- Then abort

## Prompt File

`prompts/03_solution_engineer.md`
