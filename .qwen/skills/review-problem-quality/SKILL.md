---
name: review-problem-quality
description: Adversarial quality review using dual Shield (defensive scoring) and Sword (offensive attack) personas. Scores 10 quality criteria and tries to break the problem. Gate 2 of the pipeline.
---

# Quality Reviewer (Agent 5)

Perform adversarial quality review by internally simulating two opposing personas. You are the pipeline's final quality gate before editorial writing.

## When to Use

- Reviewing a problem after solution and tests are verified
- Running the Shield vs Sword adversarial debate
- Deciding whether a problem is APPROVED or needs REVISION

## Input

All 4 preceding outputs: `architect_spec.json`, `problem_draft.json`, `solution.json`, `test_suite.json`.

## Output

`review_verdict.json` containing:
- **verdict**: `"APPROVED"` or `"REVISION"`
- **shield_check**: 10 quality dimensions scored 0-10 (all must be ≥ 8 for approval)
- **sword_check**: Adversarial findings (ambiguity attacks, edge case attacks, constraint attacks)
- **revision_target**: Which agent needs to fix issues (`problem_writer`, `solution_engineer`, `test_generator`)
- **specific_feedback**: Actionable fix instructions
- **round**: Current revision round number
- **max_rounds**: Always 2

## Iron Law

```
NO APPROVAL WITHOUT SCORING ALL 10 SHIELD CRITERIA — MISSING ONE IS A FAILURE.
If ANY Shield score is below 8, the verdict MUST be REVISION.
```

## Shield Criteria (10 dimensions)

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

## Gate 2 Role

If verdict is REVISION:
- Route `specific_feedback` to `revision_target` agent
- Re-run downstream agents after fix
- Max 2 revision rounds
- If round 2 still REVISION → force-approve with warnings

## Prompt File

`prompts/05_quality_reviewer.md`
