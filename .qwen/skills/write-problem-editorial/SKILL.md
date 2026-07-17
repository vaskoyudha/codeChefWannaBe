---
name: write-problem-editorial
description: Write a pedagogical editorial with progressive hints, brute-force to optimal progression, step-by-step walkthrough, complexity analysis, alternative approaches, and common mistakes. Makes readers feel the aha moment.
---

# Editorial Writer (Agent 6)

Write an editorial that makes readers think "of course! why didn't I see that?" — not "I could never have thought of that." Build understanding layer by layer, from naive to elegant.

## When to Use

- Writing the editorial after a problem passes quality review
- Creating progressive hints for a problem
- Explaining the brute-force → optimal solution progression
- Documenting common mistakes and alternative approaches

## Input

All 5 preceding agent outputs (all approved).

## Output

`editorial.json` containing:
- **hints**: 3 progressive hints (direction → approach → key insight)
- **brute_force_explanation**: Naive approach with complexity analysis
- **optimal_solution_walkthrough**: Step-by-step derivation of the optimal approach
- **complexity_analysis**: Time and space complexity with derivation
- **alternative_approaches**: 2-3 valid alternative solutions
- **common_mistakes**: 3-5 mistakes solvers typically make, with explanation

## Iron Law

```
NO EDITORIAL WITHOUT A BRUTE-FORCE → OPTIMAL PROGRESSION.
The reader must see WHY the naive approach fails and HOW the optimal approach naturally emerges.
```

## Core Philosophy

A good editorial builds the "aha moment" through pedagogy:
1. Start with what the reader already knows (brute force)
2. Show why it's not enough (complexity wall)
3. Guide toward the insight (what pattern emerges?)
4. Reveal the optimal approach (feels natural, not magical)
5. Prove it works (correctness + complexity)

## Hint Progression

| Hint | Level | Purpose |
|------|-------|---------|
| 1 | Direction | Points toward the right area without revealing the technique |
| 2 | Approach | Names the technique and key idea |
| 3 | Key Insight | Reveals the critical observation that makes it click |

## Prompt File

`prompts/06_editorial_writer.md`
