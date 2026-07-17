---
name: write-problem-statement
description: Transform an architect spec into a polished competitive programming problem statement with compelling story, surgical precision, anti-ambiguity checked, with constraints and sample tests that teach the solver how the problem works.
---

# Problem Writer (Agent 2)

Transform an architectural blueprint into a polished problem statement that feels like it belongs in a real contest.

## When to Use

- Converting an `architect_spec.json` into a readable problem statement
- Writing the story, input/output format, constraints, and sample tests
- Running the anti-ambiguity checklist on a problem draft

## Input

`architect_spec.json` from Agent 1 (Problem Architect).

## Output

`problem_draft.json` containing:
- **title**: Contest-style problem name
- **story**: 2-4 sentence thematic wrapper (neutral, motivating, simple)
- **statement**: The full problem statement with precise language
- **input_format**: Line-by-line specification of every input element
- **output_format**: Exact output specification
- **constraints**: Array of constraint strings
- **sample_tests**: 3-5 samples, each with input, output, and explanation
- **subtasks**: Optional partial scoring breakdowns
- **notes**: Clarifications and edge case hints

## Iron Law

```
NO PROBLEM STATEMENT WITHOUT RUNNING THE ANTI-AMBIGUITY CHECKLIST.
Every indexing convention, every edge case, every output format detail must be explicit.
```

## Anti-Ambiguity Checklist (8 items)

1. Is 1-indexed vs 0-indexed explicitly stated?
2. Are all variable names defined on first use?
3. Is the output format exact (newlines, spaces, case)?
4. Are edge cases (N=1, empty input, all same) mentioned or sample-tested?
5. Are constraints complete (no implicit bounds)?
6. Is the story free of cultural specificity?
7. Can the solver determine the answer for every sample without guessing?
8. Is there exactly one valid interpretation of every sentence?

## Prompt File

`prompts/02_problem_writer.md`
