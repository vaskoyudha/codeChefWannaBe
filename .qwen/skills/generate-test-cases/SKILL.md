---
name: generate-test-cases
description: Create a comprehensive adversarial test suite (15-30 cases) that covers basic, edge case, adversarial, boundary, and stress tests. Thinks adversarially - tries to BREAK solutions by covering all common wrong approaches.
---

# Test Case Generator (Agent 4)

Create a comprehensive test suite that verifies solution correctness and catches ALL common wrong approaches. You think adversarially — every solution is guilty until proven innocent.

## When to Use

- Generating test cases after a solution is verified solvable
- Designing adversarial tests to break wrong approaches
- Creating stress test configurations for correctness verification
- Ensuring test coverage across all categories

## Input

`problem_draft.json` + `solution.json` (includes `common_wrong_approaches`).

## Output

`test_suite.json` containing:
- **test_cases**: 15-30 test cases, each with:
  - `id`: Unique identifier
  - `category`: `basic`, `edge_case`, `adversarial`, `boundary`, `stress`
  - `input`: Full input string
  - `expected_output`: Correct output
  - `purpose`: What this test verifies
  - `breaks_approach`: (for adversarial) Which wrong approach this catches
- **stress_test_config**: Configuration for random stress testing
- **coverage_report**: Matrix showing which approaches each test catches

## Iron Law

```
NO TEST SUITE WITHOUT COVERING ALL WRONG APPROACHES FROM THE SOLUTION.
Every common_wrong_approach must have at least one adversarial test that breaks it.
```

## Test Categories

| Category | Purpose | Count |
|----------|---------|-------|
| basic | Verifies core mechanics | 3-5 |
| edge_case | N=1, empty, all same, max values | 3-5 |
| adversarial | Specifically breaks wrong approaches | 3-5 |
| boundary | Constraint boundaries, overflow | 2-4 |
| stress | Large random inputs for performance | 2-3 |

## Prompt File

`prompts/04_test_case_generator.md`
