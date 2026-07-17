# CodeChefWannaBe — AI Agent System Prompts for Programming Problem Generation

**Design Spec — July 17, 2026**

## Overview

CodeChefWannaBe is an open-source prompt library containing carefully engineered system prompts for a multi-agent AI pipeline that generates high-quality programming problems. The system covers three domains: language learning, data structures & algorithms (DSA), and competitive programming.

**Product:** A portable prompt library (markdown files) with JSON schemas, example pipeline traces, and an embedded knowledge base. No application code — the prompts can be plugged into any LLM (GPT-4, Claude, Gemini, etc.).

**Target Users:** Any developer, educator, or AI agent developer who wants to generate programming problems programmatically.

**Key Differentiator:** No existing open-source tool generates all three — problem statement + verified solution + comprehensive test cases — for competitive programming. This library fills that gap through a multi-agent pipeline with adversarial quality review.

## Architecture: Hybrid Pipeline with Adversarial Review

The system uses a 6-agent pipeline where agents 1-4 execute sequentially, agent 5 runs an internal adversarial debate, and agent 6 produces the final editorial. Two validation gates catch the most common failure modes: unsolvable problems and low-quality output.

```
[1] Problem Architect
        |
        v  (architect_spec.json)
[2] Problem Writer
        |
        v  (problem_draft.json)
[3] Solution Engineer
        |
        v  (solution.json)
    [GATE 1: Solvable?] --fail--> back to Agent 2 (max 2 retries)
        |
        v
[4] Test Case Generator
        |
        v  (test_suite.json)
[5] Quality Reviewer  <--- Adversarial mini-debate (2 rounds max)
        |                  |- Shield: checks correctness, clarity, pedagogy
        |                  +- Sword: tries to break the problem
        v  (review_verdict.json)
    [GATE 2: Quality?] --fail--> back to relevant agent (max 2 retries)
        |
        v  (approved_problem.json)
[6] Editorial Writer
        |
        v  (final_problem.json)
    OUTPUT
```

### Why Hybrid (Pipeline + Adversarial)?

- The **pipeline** (agents 1-4) handles creative work efficiently — each agent specializes in one phase
- The **adversarial review** (agent 5) handles the critical quality gate — this is where most AI-generated problems fail (ambiguous statements, unsolvable edge cases, weak tests)
- **Cost is controlled** — the expensive adversarial debate is scoped to one stage, not the whole pipeline
- **Maps to reality** — real CP problem setters write, solve, test, then have a separate tester try to break it

## Agent Responsibilities

### Agent 1: Problem Architect

**Role:** Expert competitive programming problem architect with 10+ years of experience designing problems for Codeforces, AtCoder, and LeetCode. Designs the blueprint, not the problem itself.

**Input:** User parameters (domain, topic, difficulty range, language focus)

**Output:** `architect_spec.json` containing:
- Domain (dsa | language_learning | competitive_programming)
- Topic and subtopic
- Difficulty (Codeforces rating 800-3500, tier, Bloom's taxonomy level)
- Learning objective (what concept/technique this problem teaches)
- Prerequisites (what problems/concepts should be mastered first)
- Core concept being tested
- Tags
- Constraint hints (N range, expected complexity, time limit)
- Story direction

**Key Knowledge Embedded:**
- DSA Learning Progression (Level 0-6):
  - Level 0: Language fundamentals (syntax, types, control flow, functions)
  - Level 1: Logic building & complexity analysis (Big-O, basic puzzles)
  - Level 2: Linear data structures (arrays, strings, stacks, queues, linked lists, hashing)
  - Level 3: Core algorithms (recursion, binary search, sorting, two pointers, sliding window, greedy, backtracking)
  - Level 4: Non-linear structures (trees, graphs, tries)
  - Level 5: Advanced algorithms (DP, advanced graph, number theory, bit manipulation)
  - Level 6: Expert topics (segment trees, network flow, advanced DP, geometry, string algorithms)
- Bloom's Taxonomy mapping to problem types (Remember through Create)
- Difficulty calibration (800-1200: single obvious technique, 1300-1600: single non-obvious, 1700-2100: multiple techniques, 2200+: advanced concepts)
- Prerequisite chain design rules (each problem introduces exactly ONE new concept)
- Constraint-to-complexity table (N<=20 -> O(2^N), N<=100 -> O(N^3), N<=2000 -> O(N^2), N<=10^5 -> O(N log N), N<=10^6 -> O(N), N<=10^9 -> O(sqrt(N) or log N), N<=10^18 -> O(log N))

### Agent 2: Problem Writer

**Role:** Competitive programming problem writer specializing in clear, engaging, unambiguous problem statements. Transforms architectural specs into well-structured problems.

**Input:** `architect_spec.json`

**Output:** `problem_draft.json` containing:
- Title (short, memorable)
- Story/flavor text
- Problem statement (core task)
- Input format (exact, line by line)
- Output format (what to print)
- Constraints (mathematical limits)
- Subtasks (optional, for partial scoring)
- Sample tests (3-5, each with explanation)
- Notes/clarifications

**Key Knowledge Embedded:**
- Problem statement structure template
- Anti-ambiguity checklist (all terms defined, indexing specified, edge cases mentioned, output format exact, constraints complete, single valid interpretation)
- Sample test design principles (basic -> non-obvious -> edge, don't give away solution)
- Story-to-algorithm mapping (story motivates algorithm, doesn't obscure it)
- Constraint design rules (reverse-engineered from intended complexity, memory constraints matter)

### Agent 3: Solution Engineer

**Role:** Solution engineer who writes provably correct reference solutions. If the problem is unsolvable, MUST report failure — this is critical feedback.

**Input:** `problem_draft.json`

**Output:** `solution.json` containing:
- Approach description
- Language-agnostic pseudocode
- Time and space complexity with justification
- Correctness argument (loop invariant, exchange argument, induction, monotonicity, or greedy-stays-ahead)
- Brute-force alternative (for cross-verification)
- Common wrong approaches (2-3, with explanation of why each fails)
- Solvability verdict (success or SOLVABILITY_FAILURE with reasons)

**Key Knowledge Embedded:**
- Correctness argument techniques (invariant, exchange argument, induction, monotonicity, greedy stays ahead)
- Solvability gate (if unsolvable, output SOLVABILITY_FAILURE -> triggers feedback to Agent 2)
- Common wrong approaches identification
- Complexity analysis patterns

### Agent 4: Test Case Generator

**Role:** Test case engineer who creates comprehensive test suites. Thinks adversarially — tries to BREAK solutions.

**Input:** `problem_draft.json` + `solution.json`

**Output:** `test_suite.json` containing:
- 15-30 test cases across categories:
  - `basic` (3-5): Sample tests + simple cases
  - `edge_case` (5-8): Boundary values, degenerate inputs
  - `adversarial` (3-5): Specifically target wrong approaches from solution
  - `stress` (configurable): Random large inputs
  - `boundary` (2-3): Constraint boundary values
- Stress test configuration (1000+ random tests, brute-force vs reference comparison)
- Coverage report (edge cases covered, wrong approaches tested, gaps identified)

**Key Knowledge Embedded:**
- Edge case taxonomy by problem type:
  - Array: N=1, N=2, all same, sorted, reverse sorted, all zeros, max values, negatives
  - Graph: Disconnected, single node, self-loops, multi-edges, complete, tree, cycle, bipartite
  - String: Empty, single char, all same, palindrome, max length, no match
  - DP: N=0, N=1, all same weights, capacity=0, impossible case
  - Tree: Single node, linear chain, star graph, complete binary tree
- Adversarial testing strategy (for each wrong approach, create a breaking test)
- Mutation testing principles

### Agent 5: Quality Reviewer (Adversarial)

**Role:** Internal dual-persona agent. Shield verifies quality, Sword tries to break the problem. After internal debate, outputs unified verdict.

**Input:** All previous outputs (architect_spec, problem_draft, solution, test_suite)

**Output:** `review_verdict.json` containing:
- Verdict (APPROVED or REVISION)
- Shield scores (10 criteria, each 0-10):
  1. Statement clarity
  2. Constraint-solution alignment
  3. Solution correctness
  4. Test coverage
  5. Pedagogical value
  6. Difficulty calibration
  7. Story quality
  8. Sample test quality
  9. Subtask design
  10. Overall elegance
- Sword findings (ambiguity, unsolvable cases, weak test coverage, wrong approaches that pass)
- Revision target (which agent should receive feedback)
- Specific, actionable feedback
- Round number and max rounds

**Adversarial Process:**
- Shield checks 10 quality criteria, scores each 0-10
- Sword attacks: ambiguity hunt, solution attack, test bypass, constraint mismatch, edge case gap
- APPROVED: All Shield scores >= 8, Sword finds no critical issues
- REVISION: Any Shield score < 8 OR Sword finds critical issues -> feedback to specific agent
- Max 2 revision rounds, then output best attempt with warnings

### Agent 6: Editorial Writer

**Role:** Editorial writer who teaches, not just tells. Makes the reader feel the "aha moment."

**Input:** All approved outputs

**Output:** `editorial` section in `final_problem.json` containing:
- 3 progressive hints:
  - Hint 1: Points toward direction ("What if we sorted first?")
  - Hint 2: Narrows approach ("After sorting, can we use greedy?")
  - Hint 3: Key insight ("The answer is monotonic, so binary search works")
- Brute-force -> optimal progression (naive approach, why it's slow, motivate optimization)
- Optimal solution walkthrough (step-by-step)
- Correctness explanation (WHY it works, with proof technique)
- Complexity analysis
- Alternative approaches (if any, with trade-offs)
- Common mistakes (2-3, with explanation)

## Inter-Agent Data Schemas

### architect_spec.json
```json
{
  "domain": "dsa | language_learning | competitive_programming",
  "topic": "string",
  "subtopic": "sliding_window",
  "difficulty": {
    "codeforces_rating": 1200,
    "tier": "easy",
    "bloom_level": "apply"
  },
  "learning_objective": "Student can identify sliding window patterns and implement fixed-size window technique",
  "prerequisites": ["array_basics", "hash_map_usage"],
  "core_concept": "fixed_size_sliding_window",
  "tags": ["strings", "sliding_window", "hash_map"],
  "constraint_hints": {
    "n_range": [1, 100000],
    "expected_complexity": "O(N)",
    "time_limit_seconds": 2
  },
  "story_direction": "real-world scenario involving contiguous subsequences"
}
```

### problem_draft.json
```json
{
  "title": "Problem Title",
  "story": "Flavor text / scenario description",
  "statement": "Core task description",
  "input_format": {
    "line_1": "Description of first line",
    "line_2_to_N": "Description of remaining lines"
  },
  "output_format": "Description of expected output",
  "constraints": [
    "1 <= N <= 10^5",
    "0 <= a_i <= 10^9"
  ],
  "sample_tests": [
    {
      "input": "5 3\nabcde\nbcdef\ncdefg",
      "output": "2",
      "explanation": "Explanation of why the answer is 2"
    }
  ],
  "notes": ["Clarification 1", "Clarification 2"],
  "subtasks": [
    {
      "points": 30,
      "constraints": ["N <= 1000"],
      "description": "Small N description"
    },
    {
      "points": 70,
      "constraints": ["N <= 10^5"],
      "description": "Full constraints"
    }
  ]
}
```

### solution.json
```json
{
  "approach": "Description of the approach",
  "pseudocode": [
    "line 1",
    "line 2"
  ],
  "time_complexity": "O(N log N) — justification",
  "space_complexity": "O(N) — justification",
  "correctness_argument": "Why this approach works (proof technique)",
  "brute_force_solution": {
    "approach": "Brute force description",
    "time_complexity": "O(2^N)",
    "use": "Used to verify correctness on small inputs"
  },
  "common_wrong_approaches": [
    {
      "approach": "Wrong approach description",
      "why_wrong": "Why it fails"
    }
  ],
  "solvability_verdict": "success | SOLVABILITY_FAILURE",
  "failure_reason": "Only if SOLVABILITY_FAILURE"
}
```

### test_suite.json
```json
{
  "test_cases": [
    {
      "id": "tc_01",
      "category": "basic | edge_case | adversarial | boundary",
      "input": "test input",
      "expected_output": "expected output",
      "purpose": "What this test verifies"
    }
  ],
  "stress_test_config": {
    "random_tests": 1000,
    "n_range": [2, 100],
    "comparison": "brute_force_vs_reference"
  },
  "coverage_report": {
    "edge_cases_covered": ["list", "of", "cases"],
    "wrong_approaches_tested": ["list", "of", "approaches"]
  }
}
```

### review_verdict.json
```json
{
  "verdict": "APPROVED | REVISION",
  "shield_check": {
    "statement_clarity": {"score": 9, "issues": []},
    "constraint_solution_alignment": {"score": 10, "issues": []},
    "solution_correctness": {"score": 10, "issues": []},
    "test_coverage": {"score": 8, "issues": ["Minor: no test for X"]},
    "pedagogical_value": {"score": 9, "issues": []},
    "difficulty_calibration": {"score": 8, "issues": []},
    "story_quality": {"score": 7, "issues": ["Could be more engaging"]},
    "sample_test_quality": {"score": 9, "issues": []},
    "subtask_design": {"score": 8, "issues": []},
    "overall_elegance": {"score": 8, "issues": []}
  },
  "sword_check": {
    "ambiguity_found": [],
    "unsolvable_cases": [],
    "weak_test_coverage": [],
    "wrong_approaches_that_pass": []
  },
  "revision_target": "problem_writer | solution_engineer | test_generator",
  "specific_feedback": "Actionable feedback",
  "round": 1,
  "max_rounds": 2
}
```

### final_problem.json
```json
{
  "metadata": {
    "id": "gen_001",
    "domain": "dsa",
    "topic": "binary_search",
    "subtopic": "binary_search_on_answer",
    "difficulty": {
      "codeforces_rating": 1400,
      "tier": "medium"
    },
    "tags": ["binary_search", "greedy", "sorting"],
    "bloom_level": "apply",
    "prerequisites": ["binary_search_on_array"],
    "generated_at": "2026-07-17T12:00:00Z",
    "pipeline_rounds": 1
  },
  "problem": { "...problem_draft fields..." },
  "solution": { "...solution fields..." },
  "test_suite": { "...test_suite fields..." },
  "editorial": {
    "hints": [
      "Hint 1: Direction pointer",
      "Hint 2: Approach narrows the direction",
      "Hint 3: Key insight"
    ],
    "brute_force_explanation": "Naive approach and why it's slow",
    "optimal_solution_walkthrough": "Step-by-step optimal solution",
    "complexity_analysis": "Time and space with justification",
    "alternative_approaches": ["Alternative 1", "Alternative 2"],
    "common_mistakes": ["Mistake 1", "Mistake 2"]
  },
  "quality_report": {
    "shield_scores": { "...scores..." },
    "sword_findings": ["...findings..."],
    "pipeline_rounds": 1,
    "warnings": []
  }
}
```

## Quality Gates & Feedback Loops

### Gate 1: Solvability Check (after Agent 3)

Agent 3 (Solution Engineer) outputs either `solution.json` (success) or `SOLVABILITY_FAILURE`.

If SOLVABILITY_FAILURE:
- Feedback routed to Agent 2 (Problem Writer) with specific reason
- Agent 2 revises the problem_draft
- Max 2 retries, then escalate to Agent 1 (Architect) for full redesign

### Gate 2: Quality Review (after Agent 4, before Agent 6)

Agent 5 (Quality Reviewer) runs adversarial debate:
- Round 1: Shield + Sword analyze all outputs
- If APPROVED -> proceed to Agent 6
- If REVISION -> feedback routed to specific agent (problem_writer, solution_engineer, or test_generator)
- Round 2 (if needed): Revised outputs re-analyzed
- If still REVISION -> output best attempt with warning flags
- Max 2 rounds total

### Confidence Scoring

Every agent includes a `confidence` field (0.0-1.0):
- >= 0.8: High confidence, proceed normally
- 0.5-0.8: Medium confidence, flag for extra scrutiny
- < 0.5: Low confidence, trigger retry or escalation

## File Structure

```
codeChefWannaBe/
├── README.md                          # Project overview, quick start
├── prompts/                           # The core prompt library
│   ├── 01_problem_architect.md        # Agent 1 system prompt
│   ├── 02_problem_writer.md           # Agent 2 system prompt
│   ├── 03_solution_engineer.md        # Agent 3 system prompt
│   ├── 04_test_case_generator.md      # Agent 4 system prompt
│   ├── 05_quality_reviewer.md         # Agent 5 system prompt (adversarial)
│   ├── 06_editorial_writer.md         # Agent 6 system prompt
│   └── orchestrator.md                # Pipeline orchestration prompt
├── schemas/                           # JSON schemas for inter-agent data
│   ├── architect_spec.json
│   ├── problem_draft.json
│   ├── solution.json
│   ├── test_suite.json
│   ├── review_verdict.json
│   └── final_problem.json
├── examples/                          # Complete pipeline traces (few-shot examples)
│   ├── binary_search_on_answer/       # Example: Aggressive Cows-style problem
│   │   ├── architect_spec.json
│   │   ├── problem_draft.json
│   │   ├── solution.json
│   │   ├── test_suite.json
│   │   ├── review_verdict.json
│   │   └── final_problem.json
│   ├── sliding_window/                # Example: Fixed-size window problem
│   │   └── ...
│   └── graph_bfs/                     # Example: BFS on grid problem
│       └── ...
├── knowledge/                         # Embedded domain knowledge (also in prompts)
│   ├── constraint_complexity_table.md
│   ├── dsa_learning_progression.md
│   ├── edge_case_taxonomy.md
│   ├── blooms_taxonomy_mapping.md
│   └── anti_patterns_checklist.md
└── docs/
    ├── architecture.md                # This design spec
    ├── usage_guide.md                 # How to use the prompts with any LLM
    └── extending.md                   # How to add new agents or domains
```

## Design Principles

1. **Every problem has a clear learning objective** — what concept or technique does it teach?
2. **Problems form prerequisite chains** — each builds on the previous, introducing one new concept
3. **Difficulty comes from the concept, not gotchas** — clear statements, reasonable constraints
4. **Editorials are more important than problems** — they explain the key insight, prove correctness
5. **Constraints signal the expected approach** — N<=10^5 means O(N log N)
6. **Adversarial review catches what single-pass misses** — the Sword persona finds flaws the Shield misses
7. **Bounded retries prevent infinite loops** — max 2 retries per gate, then escalate
8. **Language-agnostic by design** — problems described algorithmically, solutions in pseudocode
9. **Structured JSON output** — machine-readable, easy to integrate into any system
10. **Knowledge is both embedded and standalone** — prompts contain domain knowledge, but it's also available as separate reference docs

## Scope & Non-Goals

**In Scope:**
- System prompts for 6 specialized agents + 1 orchestrator
- JSON schemas for inter-agent communication
- 3 complete example pipeline traces
- Domain knowledge base (constraint tables, learning progressions, taxonomies)
- Documentation (architecture, usage guide, extending guide)

**Out of Scope (for v1):**
- Application code (CLI, web app, API) — this is a prompt library only
- Fine-tuned models — prompts work with any general-purpose LLM
- Automated execution (running solutions against test cases) — left to the user
- Difficulty estimation model — the Architect prompt uses heuristic calibration, not ML
- Multi-language support for prompts — English only for v1

## Future Extensions

- **Agent 7: Difficulty Calibrator** — uses numeric features + LightGBM for statistical difficulty estimation (research shows 86% accuracy vs 37% for LLM-as-judge)
- **Agent 8: Prerequisite Chain Builder** — given a topic, generates a sequence of problems forming a learning path
- **Agent 9: Problem Variant Generator** — takes an existing problem and creates variants (constraint shifting, concept combination)
- **Integration layer** — Python/Node wrapper that orchestrates the pipeline with actual LLM API calls
- **Automated verification** — execute reference solutions against test cases programmatically
- **Community dataset** — collect and curate few-shot examples from real CP platforms (APPS, CodeContests)
