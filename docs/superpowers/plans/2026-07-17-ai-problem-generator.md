# CodeChefWannaBe — AI Problem Generator Prompt Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create an open-source prompt library containing 6 specialized agent system prompts + 1 orchestrator, JSON schemas, knowledge base, 3 example pipeline traces, and documentation — for generating high-quality programming problems via a multi-agent AI pipeline.

**Architecture:** Hybrid pipeline with adversarial review. Agents 1-4 execute sequentially (Architect → Writer → Solution Engineer → Test Generator), Agent 5 runs an internal adversarial debate (Shield vs Sword), Agent 6 writes the editorial. Two validation gates with bounded retries (max 2). All inter-agent communication via structured JSON.

**Tech Stack:** Markdown (prompts), JSON (schemas + examples), no application code. Prompts are LLM-agnostic (work with GPT-4, Claude, Gemini, etc.).

## Global Constraints

- All prompts must be self-contained — each prompt includes all domain knowledge the agent needs
- All prompts must reference their input/output JSON schema explicitly
- All prompts must include the output contract (exact JSON format expected)
- JSON schemas must be valid JSON and match the examples in the design spec
- Example pipeline traces must be complete — every schema field populated with realistic data
- Knowledge base documents must be referenced by and embedded in the relevant agent prompts
- File paths must match the structure defined in the design spec exactly

---

## File Structure

```
codeChefWannaBe/
├── README.md
├── prompts/
│   ├── 01_problem_architect.md
│   ├── 02_problem_writer.md
│   ├── 03_solution_engineer.md
│   ├── 04_test_case_generator.md
│   ├── 05_quality_reviewer.md
│   ├── 06_editorial_writer.md
│   └── orchestrator.md
├── schemas/
│   ├── architect_spec.json
│   ├── problem_draft.json
│   ├── solution.json
│   ├── test_suite.json
│   ├── review_verdict.json
│   └── final_problem.json
├── examples/
│   ├── binary_search_on_answer/
│   │   ├── architect_spec.json
│   │   ├── problem_draft.json
│   │   ├── solution.json
│   │   ├── test_suite.json
│   │   ├── review_verdict.json
│   │   └── final_problem.json
│   ├── sliding_window/
│   │   └── (same 6 files)
│   └── graph_bfs/
│       └── (same 6 files)
├── knowledge/
│   ├── constraint_complexity_table.md
│   ├── dsa_learning_progression.md
│   ├── edge_case_taxonomy.md
│   ├── blooms_taxonomy_mapping.md
│   └── anti_patterns_checklist.md
└── docs/
    ├── superpowers/
    │   ├── specs/2026-07-17-ai-problem-generator-design.md  (already exists)
    │   └── plans/2026-07-17-ai-problem-generator.md         (this file)
    ├── usage_guide.md
    └── extending.md
```

---

### Task 1: Project Scaffolding + JSON Schemas

**Files:**
- Create: `schemas/architect_spec.json`
- Create: `schemas/problem_draft.json`
- Create: `schemas/solution.json`
- Create: `schemas/test_suite.json`
- Create: `schemas/review_verdict.json`
- Create: `schemas/final_problem.json`
- Create: directory structure for `prompts/`, `examples/`, `knowledge/`, `docs/`

**Interfaces:**
- Consumes: Design spec schemas section
- Produces: All JSON schema files that every agent prompt references

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p prompts schemas examples/binary_search_on_answer examples/sliding_window examples/graph_bfs knowledge docs
```

- [ ] **Step 2: Create `schemas/architect_spec.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Architect Spec",
  "description": "Output of Agent 1 (Problem Architect). Blueprint for problem generation.",
  "type": "object",
  "required": ["domain", "topic", "subtopic", "difficulty", "learning_objective", "prerequisites", "core_concept", "tags", "constraint_hints", "story_direction"],
  "properties": {
    "domain": {
      "type": "string",
      "enum": ["dsa", "language_learning", "competitive_programming"]
    },
    "topic": { "type": "string" },
    "subtopic": { "type": "string" },
    "difficulty": {
      "type": "object",
      "required": ["codeforces_rating", "tier", "bloom_level"],
      "properties": {
        "codeforces_rating": { "type": "integer", "minimum": 800, "maximum": 3500 },
        "tier": { "type": "string", "enum": ["easy", "medium", "hard", "expert"] },
        "bloom_level": { "type": "string", "enum": ["remember", "understand", "apply", "analyze", "evaluate", "create"] }
      }
    },
    "learning_objective": { "type": "string" },
    "prerequisites": { "type": "array", "items": { "type": "string" } },
    "core_concept": { "type": "string" },
    "tags": { "type": "array", "items": { "type": "string" } },
    "constraint_hints": {
      "type": "object",
      "required": ["n_range", "expected_complexity", "time_limit_seconds"],
      "properties": {
        "n_range": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 },
        "expected_complexity": { "type": "string" },
        "time_limit_seconds": { "type": "integer", "minimum": 1 }
      }
    },
    "story_direction": { "type": "string" }
  }
}
```

- [ ] **Step 3: Create `schemas/problem_draft.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Problem Draft",
  "description": "Output of Agent 2 (Problem Writer). Complete problem statement.",
  "type": "object",
  "required": ["title", "story", "statement", "input_format", "output_format", "constraints", "sample_tests"],
  "properties": {
    "title": { "type": "string" },
    "story": { "type": "string" },
    "statement": { "type": "string" },
    "input_format": {
      "type": "object",
      "additionalProperties": { "type": "string" }
    },
    "output_format": { "type": "string" },
    "constraints": { "type": "array", "items": { "type": "string" } },
    "sample_tests": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["input", "output", "explanation"],
        "properties": {
          "input": { "type": "string" },
          "output": { "type": "string" },
          "explanation": { "type": "string" }
        }
      },
      "minItems": 2,
      "maxItems": 5
    },
    "notes": { "type": "array", "items": { "type": "string" } },
    "subtasks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["points", "constraints", "description"],
        "properties": {
          "points": { "type": "integer" },
          "constraints": { "type": "array", "items": { "type": "string" } },
          "description": { "type": "string" }
        }
      }
    }
  }
}
```

- [ ] **Step 4: Create `schemas/solution.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Solution",
  "description": "Output of Agent 3 (Solution Engineer). Reference solution with analysis.",
  "type": "object",
  "required": ["approach", "pseudocode", "time_complexity", "space_complexity", "correctness_argument", "brute_force_solution", "common_wrong_approaches", "solvability_verdict"],
  "properties": {
    "approach": { "type": "string" },
    "pseudocode": { "type": "array", "items": { "type": "string" } },
    "time_complexity": { "type": "string" },
    "space_complexity": { "type": "string" },
    "correctness_argument": { "type": "string" },
    "brute_force_solution": {
      "type": "object",
      "required": ["approach", "time_complexity", "use"],
      "properties": {
        "approach": { "type": "string" },
        "time_complexity": { "type": "string" },
        "use": { "type": "string" }
      }
    },
    "common_wrong_approaches": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["approach", "why_wrong"],
        "properties": {
          "approach": { "type": "string" },
          "why_wrong": { "type": "string" }
        }
      }
    },
    "solvability_verdict": { "type": "string", "enum": ["success", "SOLVABILITY_FAILURE"] },
    "failure_reason": { "type": "string" }
  }
}
```

- [ ] **Step 5: Create `schemas/test_suite.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Test Suite",
  "description": "Output of Agent 4 (Test Case Generator). Comprehensive test cases.",
  "type": "object",
  "required": ["test_cases", "stress_test_config", "coverage_report"],
  "properties": {
    "test_cases": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "category", "input", "expected_output", "purpose"],
        "properties": {
          "id": { "type": "string" },
          "category": { "type": "string", "enum": ["basic", "edge_case", "adversarial", "boundary"] },
          "input": { "type": "string" },
          "expected_output": { "type": "string" },
          "purpose": { "type": "string" }
        }
      },
      "minItems": 10
    },
    "stress_test_config": {
      "type": "object",
      "required": ["random_tests", "n_range", "comparison"],
      "properties": {
        "random_tests": { "type": "integer", "minimum": 100 },
        "n_range": { "type": "array", "items": { "type": "integer" }, "minItems": 2, "maxItems": 2 },
        "comparison": { "type": "string" }
      }
    },
    "coverage_report": {
      "type": "object",
      "required": ["edge_cases_covered", "wrong_approaches_tested"],
      "properties": {
        "edge_cases_covered": { "type": "array", "items": { "type": "string" } },
        "wrong_approaches_tested": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

- [ ] **Step 6: Create `schemas/review_verdict.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Review Verdict",
  "description": "Output of Agent 5 (Quality Reviewer). Adversarial review result.",
  "type": "object",
  "required": ["verdict", "shield_check", "sword_check", "revision_target", "specific_feedback", "round", "max_rounds"],
  "properties": {
    "verdict": { "type": "string", "enum": ["APPROVED", "REVISION"] },
    "shield_check": {
      "type": "object",
      "properties": {
        "statement_clarity": { "$ref": "#/definitions/scored_check" },
        "constraint_solution_alignment": { "$ref": "#/definitions/scored_check" },
        "solution_correctness": { "$ref": "#/definitions/scored_check" },
        "test_coverage": { "$ref": "#/definitions/scored_check" },
        "pedagogical_value": { "$ref": "#/definitions/scored_check" },
        "difficulty_calibration": { "$ref": "#/definitions/scored_check" },
        "story_quality": { "$ref": "#/definitions/scored_check" },
        "sample_test_quality": { "$ref": "#/definitions/scored_check" },
        "subtask_design": { "$ref": "#/definitions/scored_check" },
        "overall_elegance": { "$ref": "#/definitions/scored_check" }
      }
    },
    "sword_check": {
      "type": "object",
      "properties": {
        "ambiguity_found": { "type": "array", "items": { "type": "string" } },
        "unsolvable_cases": { "type": "array", "items": { "type": "string" } },
        "weak_test_coverage": { "type": "array", "items": { "type": "string" } },
        "wrong_approaches_that_pass": { "type": "array", "items": { "type": "string" } }
      }
    },
    "revision_target": { "type": "string", "enum": ["problem_writer", "solution_engineer", "test_generator"] },
    "specific_feedback": { "type": "string" },
    "round": { "type": "integer" },
    "max_rounds": { "type": "integer" }
  },
  "definitions": {
    "scored_check": {
      "type": "object",
      "required": ["score", "issues"],
      "properties": {
        "score": { "type": "integer", "minimum": 0, "maximum": 10 },
        "issues": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

- [ ] **Step 7: Create `schemas/final_problem.json`**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Final Problem",
  "description": "Final output of the pipeline. Complete problem with all sections.",
  "type": "object",
  "required": ["metadata", "problem", "solution", "test_suite", "editorial", "quality_report"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["id", "domain", "topic", "subtopic", "difficulty", "tags", "bloom_level", "prerequisites", "generated_at", "pipeline_rounds"],
      "properties": {
        "id": { "type": "string" },
        "domain": { "type": "string" },
        "topic": { "type": "string" },
        "subtopic": { "type": "string" },
        "difficulty": {
          "type": "object",
          "properties": {
            "codeforces_rating": { "type": "integer" },
            "tier": { "type": "string" }
          }
        },
        "tags": { "type": "array", "items": { "type": "string" } },
        "bloom_level": { "type": "string" },
        "prerequisites": { "type": "array", "items": { "type": "string" } },
        "generated_at": { "type": "string", "format": "date-time" },
        "pipeline_rounds": { "type": "integer" }
      }
    },
    "problem": { "type": "object" },
    "solution": { "type": "object" },
    "test_suite": { "type": "object" },
    "editorial": {
      "type": "object",
      "required": ["hints", "brute_force_explanation", "optimal_solution_walkthrough", "complexity_analysis", "alternative_approaches", "common_mistakes"],
      "properties": {
        "hints": { "type": "array", "items": { "type": "string" }, "minItems": 3, "maxItems": 3 },
        "brute_force_explanation": { "type": "string" },
        "optimal_solution_walkthrough": { "type": "string" },
        "complexity_analysis": { "type": "string" },
        "alternative_approaches": { "type": "array", "items": { "type": "string" } },
        "common_mistakes": { "type": "array", "items": { "type": "string" } }
      }
    },
    "quality_report": {
      "type": "object",
      "required": ["shield_scores", "sword_findings", "pipeline_rounds", "warnings"],
      "properties": {
        "shield_scores": { "type": "object" },
        "sword_findings": { "type": "array", "items": { "type": "string" } },
        "pipeline_rounds": { "type": "integer" },
        "warnings": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

- [ ] **Step 8: Validate all schemas are valid JSON**

```bash
for f in schemas/*.json; do echo "Validating $f..."; python3 -c "import json; json.load(open('$f'))" && echo "OK" || echo "FAIL"; done
```

Expected: All 6 files print "OK"

- [ ] **Step 9: Commit**

```bash
git add schemas/ prompts/ examples/ knowledge/ docs/
git commit -m "feat: add JSON schemas and project directory structure"
```

---

### Task 2: Knowledge Base Documents

**Files:**
- Create: `knowledge/constraint_complexity_table.md`
- Create: `knowledge/dsa_learning_progression.md`
- Create: `knowledge/edge_case_taxonomy.md`
- Create: `knowledge/blooms_taxonomy_mapping.md`
- Create: `knowledge/anti_patterns_checklist.md`

**Interfaces:**
- Consumes: Design spec knowledge sections
- Produces: Reference documents embedded in agent prompts

- [ ] **Step 1: Create `knowledge/constraint_complexity_table.md`**

Write a reference document containing the constraint-to-complexity mapping table:

| Constraint (N) | Required Complexity | Typical Techniques |
|---|---|---|
| N ≤ 10–20 | O(N!) or O(2^N) | Backtracking, Bitmask DP, brute-force permutations |
| N ≤ 100 | O(N³) or O(N⁴) | Floyd-Warshall, standard 3D DP, Matrix Multiplication |
| N ≤ 500 | O(N³) | Dense graph algorithms, Interval DP |
| N ≤ 2000 | O(N²) | Standard DP, Dijkstra, 2D Prefix Sums |
| N ≤ 10⁵ | O(N log N) or O(N√N) | Sorting, Segment Trees, Fenwick Trees, Divide & Conquer |
| N ≤ 10⁶ | O(N) or O(N log log N) | Linear Sieve, Counting Sort, BFS/DFS on trees |
| N ≤ 10⁹ | O(√N) or O(log N) | Number Theory, Binary Search, Sqrt Decomposition |
| N ≤ 10¹⁸ | O(log N) or O(log² N) | Matrix Exponentiation, Binary Lifting, closed-form math |

Include explanation of WHY these mappings exist (CPU does ~10^8 operations/sec), memory constraints (256MB limit), and how to reverse-engineer constraints from intended solution.

- [ ] **Step 2: Create `knowledge/dsa_learning_progression.md`**

Write a reference document with the 7-level DSA learning progression (Level 0-6), including:
- Each level's topics and must-master concepts
- "Gate" criteria for advancing to next level
- Prerequisite chains for major topics (binary search, DP, graphs, etc.)
- Topic clusters and which techniques combine naturally

- [ ] **Step 3: Create `knowledge/edge_case_taxonomy.md`**

Write a reference document with edge case categories per problem type:
- Array problems: N=1, N=2, all same, sorted, reverse sorted, all zeros, max values, negatives
- Graph problems: Disconnected, single node, self-loops, multi-edges, complete, tree, cycle, bipartite
- String problems: Empty, single char, all same, palindrome, max length, no match
- DP problems: N=0, N=1, all same weights, capacity=0, impossible case
- Tree problems: Single node, linear chain, star graph, complete binary tree
- Math/number theory: N=0, N=1, prime inputs, perfect squares, overflow boundaries

- [ ] **Step 4: Create `knowledge/blooms_taxonomy_mapping.md`**

Write a reference document mapping Bloom's taxonomy to programming problem types:
- Remember → syntax/API recall, MCQ
- Understand → trace execution, explain why code works
- Apply → implement known algorithm on new input
- Analyze → decompose problem, choose right approach, debug broken solution
- Evaluate → compare solutions, justify optimality, prove/disprove greedy
- Create → design novel algorithm, combine techniques in new way

Include example problem types for each level and guidance on targeting specific levels.

- [ ] **Step 5: Create `knowledge/anti_patterns_checklist.md`**

Write a reference document listing common anti-patterns in problem setting:
1. Ambiguous statements (undefined terms, multiple interpretations, hidden assumptions)
2. Weak test cases (trivial counters pass, only random tests, no stress testing)
3. Constraint-solution mismatch (too loose, too tight, contradictory)
4. Implementation-heavy problems (300+ lines with no insight)
5. "Guess the output" problems (complex simulation, hard to trace)
6. Insufficient edge case coverage
7. "Anti-academic" problems (obscure algorithm not in standard curriculum)

For each: description, impact, how to detect, how to fix.

- [ ] **Step 6: Commit**

```bash
git add knowledge/
git commit -m "feat: add knowledge base documents for agent prompts"
```

---

### Task 3: Agent 1 Prompt — Problem Architect

**Files:**
- Create: `prompts/01_problem_architect.md`

**Interfaces:**
- Consumes: `knowledge/dsa_learning_progression.md`, `knowledge/blooms_taxonomy_mapping.md`, `knowledge/constraint_complexity_table.md`
- Produces: System prompt that outputs `architect_spec.json`

- [ ] **Step 1: Write the Problem Architect system prompt**

Create `prompts/01_problem_architect.md` containing a complete system prompt with these sections:

1. **Role framing:** "You are an expert competitive programming problem architect with 10+ years of experience designing problems for Codeforces, AtCoder, and LeetCode. Your job is NOT to write the problem statement — it is to DESIGN the blueprint that a problem writer will follow."

2. **Input specification:** Describe what user parameters the agent expects (domain, topic, difficulty range, language focus, any special requirements).

3. **Embedded knowledge:**
   - Full DSA Learning Progression (Level 0-6) with topics per level
   - Bloom's Taxonomy mapping to problem types
   - Difficulty calibration guide (800-1200, 1300-1600, 1700-2100, 2200+)
   - Prerequisite chain design rules (one new concept per problem)
   - Constraint-to-complexity table (N ranges → expected complexity)

4. **Decision framework:** Step-by-step process the agent should follow:
   - Step 1: Identify the core concept to teach
   - Step 2: Determine Bloom's level and difficulty
   - Step 3: Identify prerequisites
   - Step 4: Choose constraint range based on expected complexity
   - Step 5: Suggest story direction
   - Step 6: Assign tags

5. **Output contract:** Exact JSON schema for `architect_spec.json` with field descriptions.

6. **Quality criteria:** What makes a good architect spec (clear learning objective, appropriate difficulty, well-chosen prerequisites, constraints that force intended approach).

7. **Few-shot example:** One complete example input → output.

- [ ] **Step 2: Review prompt for completeness**

Verify the prompt contains:
- [ ] Role framing
- [ ] Input specification
- [ ] All embedded knowledge (progression, taxonomy, calibration, constraints)
- [ ] Decision framework (step-by-step)
- [ ] Output contract with JSON schema
- [ ] Quality criteria
- [ ] At least one few-shot example
- [ ] No placeholders or TBDs

- [ ] **Step 3: Commit**

```bash
git add prompts/01_problem_architect.md
git commit -m "feat: add Agent 1 (Problem Architect) system prompt"
```

---

### Task 4: Agent 2 Prompt — Problem Writer

**Files:**
- Create: `prompts/02_problem_writer.md`

**Interfaces:**
- Consumes: `architect_spec.json` from Agent 1, `knowledge/anti_patterns_checklist.md`
- Produces: System prompt that outputs `problem_draft.json`

- [ ] **Step 1: Write the Problem Writer system prompt**

Create `prompts/02_problem_writer.md` containing:

1. **Role framing:** "You are a competitive programming problem writer specializing in crafting clear, engaging, and unambiguous problem statements. You transform architectural specs into well-structured problems that feel like they belong on Codeforces or AtCoder."

2. **Input specification:** Receives `architect_spec.json` from Agent 1.

3. **Embedded knowledge:**
   - Problem statement structure template (title, story, statement, I/O format, constraints, subtasks, samples, notes)
   - Anti-ambiguity checklist (8 items: terms defined, indexing specified, edge cases mentioned, output format exact, constraints complete, single interpretation, no gotchas, no hidden assumptions)
   - Sample test design principles (Sample 1: basic mechanics, Sample 2: non-obvious behavior, Sample 3+: edge cases)
   - Story-to-algorithm mapping examples
   - Constraint design rules (reverse-engineer from complexity, include memory)

4. **Writing process:**
   - Step 1: Read architect spec, understand the core concept
   - Step 2: Design story/scenario that motivates the algorithm
   - Step 3: Write problem statement with precise language
   - Step 4: Define input/output format (line by line)
   - Step 5: Set constraints (from architect's constraint_hints)
   - Step 6: Create sample tests (3-5, each with specific purpose)
   - Step 7: Run anti-ambiguity checklist
   - Step 8: Add notes/clarifications

5. **Output contract:** Exact JSON schema for `problem_draft.json`.

6. **Anti-patterns to avoid:** Reference the anti-patterns checklist — ambiguous statements, weak samples, constraint mismatches.

7. **Few-shot example:** One complete architect_spec → problem_draft.

- [ ] **Step 2: Review prompt for completeness**

Verify:
- [ ] Role framing
- [ ] Problem structure template
- [ ] Anti-ambiguity checklist (all 8 items)
- [ ] Sample test design principles
- [ ] Output contract with JSON schema
- [ ] Few-shot example
- [ ] No placeholders

- [ ] **Step 3: Commit**

```bash
git add prompts/02_problem_writer.md
git commit -m "feat: add Agent 2 (Problem Writer) system prompt"
```

---

### Task 5: Agent 3 Prompt — Solution Engineer

**Files:**
- Create: `prompts/03_solution_engineer.md`

**Interfaces:**
- Consumes: `problem_draft.json` from Agent 2
- Produces: System prompt that outputs `solution.json`

- [ ] **Step 1: Write the Solution Engineer system prompt**

Create `prompts/03_solution_engineer.md` containing:

1. **Role framing:** "You are a competitive programming solution engineer. Your job is to write a provably correct reference solution, analyze its complexity, and provide a brute-force alternative for verification. CRITICAL: If you cannot solve the problem, you MUST output SOLVABILITY_FAILURE — this is the most important feedback you can give."

2. **Input specification:** Receives `problem_draft.json` from Agent 2.

3. **Embedded knowledge:**
   - Correctness argument techniques (5 types):
     - Loop invariant: "At the start of iteration i, variable X holds..."
     - Exchange argument: "If optimal differs from ours at step k, we can swap..."
     - Induction: "Base case holds. Assuming for k, it holds for k+1..."
     - Monotonicity: "The feasibility function is monotonic because..."
     - Greedy stays ahead: "At each step, our choice is at least as good..."
   - Complexity analysis patterns (how to derive time/space from algorithm structure)
   - Common algorithm templates (binary search, DP, BFS/DFS, greedy, etc.)

4. **Solution process:**
   - Step 1: Understand the problem (re-read statement, identify core task)
   - Step 2: Identify the approach (from architect's core_concept + your analysis)
   - Step 3: Write pseudocode (language-agnostic, clear enough to implement in any language)
   - Step 4: Analyze complexity (time and space, with justification)
   - Step 5: Write correctness argument (choose appropriate proof technique)
   - Step 6: Write brute-force solution (for cross-verification)
   - Step 7: List common wrong approaches (2-3, with why each fails)
   - Step 8: Solvability check — can this actually be solved? If not, SOLVABILITY_FAILURE.

5. **SOLVABILITY_FAILURE protocol:**
   - When to use: contradictory constraints, impossible conditions, ambiguous statement with no valid interpretation
   - What to include: specific reason, which part of the problem is flawed, suggestion for fix
   - Effect: triggers feedback loop back to Agent 2

6. **Output contract:** Exact JSON schema for `solution.json`.

7. **Few-shot example:** One complete problem_draft → solution.

- [ ] **Step 2: Review prompt for completeness**

Verify:
- [ ] Role framing with emphasis on SOLVABILITY_FAILURE
- [ ] All 5 correctness argument techniques
- [ ] Solution process (8 steps)
- [ ] SOLVABILITY_FAILURE protocol
- [ ] Output contract with JSON schema
- [ ] Few-shot example
- [ ] No placeholders

- [ ] **Step 3: Commit**

```bash
git add prompts/03_solution_engineer.md
git commit -m "feat: add Agent 3 (Solution Engineer) system prompt"
```

---

### Task 6: Agent 4 Prompt — Test Case Generator

**Files:**
- Create: `prompts/04_test_case_generator.md`

**Interfaces:**
- Consumes: `problem_draft.json` + `solution.json` from Agents 2-3, `knowledge/edge_case_taxonomy.md`
- Produces: System prompt that outputs `test_suite.json`

- [ ] **Step 1: Write the Test Case Generator system prompt**

Create `prompts/04_test_case_generator.md` containing:

1. **Role framing:** "You are a competitive programming test case engineer. Your job is to create a comprehensive test suite that verifies solution correctness and catches ALL common wrong approaches. You think adversarially — you try to BREAK solutions."

2. **Input specification:** Receives `problem_draft.json` + `solution.json`.

3. **Embedded knowledge:**
   - Full edge case taxonomy by problem type (array, graph, string, DP, tree, math)
   - Test case categories: basic (3-5), edge_case (5-8), adversarial (3-5), boundary (2-3), stress (configurable)
   - Adversarial testing strategy: for each wrong approach in solution.common_wrong_approaches, create a test that specifically breaks it
   - Stress test design: random inputs within small constraints, compare brute-force vs reference

4. **Test generation process:**
   - Step 1: Read problem statement, identify input structure and constraints
   - Step 2: Read solution, note common wrong approaches
   - Step 3: Generate basic tests (sample tests + simple cases)
   - Step 4: Generate edge cases (from taxonomy, based on problem type)
   - Step 5: Generate adversarial tests (target each wrong approach)
   - Step 6: Generate boundary tests (constraint limits)
   - Step 7: Configure stress tests
   - Step 8: Write coverage report

5. **Output contract:** Exact JSON schema for `test_suite.json`.

6. **Quality criteria:** Minimum 10 test cases, all wrong approaches covered, all edge case categories for problem type addressed.

7. **Few-shot example:** One complete (problem_draft + solution) → test_suite.

- [ ] **Step 2: Review prompt for completeness**

Verify:
- [ ] Role framing with adversarial mindset
- [ ] Edge case taxonomy (all 6 problem types)
- [ ] Test categories with counts
- [ ] Adversarial testing strategy
- [ ] Test generation process (8 steps)
- [ ] Output contract with JSON schema
- [ ] Few-shot example
- [ ] No placeholders

- [ ] **Step 3: Commit**

```bash
git add prompts/04_test_case_generator.md
git commit -m "feat: add Agent 4 (Test Case Generator) system prompt"
```

---

### Task 7: Agent 5 Prompt — Quality Reviewer (Adversarial)

**Files:**
- Create: `prompts/05_quality_reviewer.md`

**Interfaces:**
- Consumes: All previous outputs (architect_spec, problem_draft, solution, test_suite)
- Produces: System prompt that outputs `review_verdict.json`

- [ ] **Step 1: Write the Quality Reviewer system prompt**

Create `prompts/05_quality_reviewer.md` containing:

1. **Role framing:** "You are a competitive programming quality reviewer. You internally simulate TWO personas with opposing goals:

SHIELD: Your job is to VERIFY the problem meets quality standards. You check clarity, correctness, pedagogy, and elegance.

SWORD: Your job is to BREAK the problem. You hunt for ambiguity, unsolvable cases, weak tests, constraint mismatches, and wrong approaches that pass.

After internal debate between Shield and Sword, output a unified verdict."

2. **Input specification:** Receives all previous outputs (architect_spec, problem_draft, solution, test_suite).

3. **Shield checklist (10 criteria, each scored 0-10):**
   1. Statement clarity — no ambiguity, all terms defined
   2. Constraint-solution alignment — N forces correct complexity
   3. Solution correctness — reference solution provably correct
   4. Test coverage — all edge cases and wrong approaches covered
   5. Pedagogical value — clear learning objective achieved
   6. Difficulty calibration — matches target rating ±100
   7. Story quality — engaging, motivates the algorithm
   8. Sample test quality — illustrate without giving away
   9. Subtask design — progressive difficulty, meaningful partial credit
   10. Overall elegance — is this a "beautiful problem"?

4. **Sword attack vectors:**
   - Ambiguity hunt: read every sentence for multiple interpretations
   - Solution attack: find inputs where reference solution fails
   - Test bypass: for each wrong approach, check if tests catch it
   - Constraint mismatch: verify N bounds force intended complexity
   - Edge case gap: list edge cases test suite misses

5. **Debate protocol:**
   - Round 1: Shield scores all 10 criteria. Sword attacks on all 5 vectors.
   - Internal debate: Shield defends, Sword counters.
   - Unified verdict: APPROVED if all Shield scores ≥ 8 AND Sword finds no critical issues. REVISION otherwise.
   - If REVISION: specify target agent, provide specific actionable feedback.
   - Max 2 rounds.

6. **Verdict rules:**
   - APPROVED: All Shield scores ≥ 8, no critical Sword findings
   - REVISION: Any Shield score < 8 OR critical Sword finding
   - revision_target: problem_writer | solution_engineer | test_generator
   - Max 2 revision rounds, then output best attempt with warnings

7. **Output contract:** Exact JSON schema for `review_verdict.json`.

8. **Few-shot example:** One complete review showing both APPROVED and REVISION scenarios.

- [ ] **Step 2: Review prompt for completeness**

Verify:
- [ ] Dual-persona role framing (Shield + Sword)
- [ ] All 10 Shield criteria with scoring guide
- [ ] All 5 Sword attack vectors
- [ ] Debate protocol
- [ ] Verdict rules (APPROVED/REVISION thresholds)
- [ ] Output contract with JSON schema
- [ ] Few-shot examples
- [ ] No placeholders

- [ ] **Step 3: Commit**

```bash
git add prompts/05_quality_reviewer.md
git commit -m "feat: add Agent 5 (Quality Reviewer) adversarial system prompt"
```

---

### Task 8: Agent 6 Prompt — Editorial Writer

**Files:**
- Create: `prompts/06_editorial_writer.md`

**Interfaces:**
- Consumes: All approved outputs from pipeline
- Produces: System prompt that outputs `editorial` section of `final_problem.json`

- [ ] **Step 1: Write the Editorial Writer system prompt**

Create `prompts/06_editorial_writer.md` containing:

1. **Role framing:** "You are a competitive programming editorial writer. Your job is to write editorials that TEACH, not just tell. A good editorial makes the reader feel the 'aha moment' and understand WHY the approach works, not just HOW to implement it."

2. **Input specification:** Receives all approved outputs (architect_spec, problem_draft, solution, test_suite, review_verdict).

3. **Embedded knowledge:**
   - Progressive hint design (3 levels):
     - Hint 1: Points toward direction without giving away ("What if we sorted first?")
     - Hint 2: Narrows the approach ("After sorting, can we use two pointers?")
     - Hint 3: Key insight or recurrence ("The feasibility is monotonic, so binary search works")
   - Brute-force → optimal progression structure:
     - Start with naive approach (what beginner would try)
     - Explain why it's too slow (complexity)
     - Motivate the optimization ("What if we could check faster?")
     - Arrive at optimal approach naturally
   - Correctness explanation techniques (match to proof type from solution)
   - Common mistakes section (2-3 mistakes with why each is wrong)

4. **Editorial writing process:**
   - Step 1: Read the problem and solution thoroughly
   - Step 2: Write 3 progressive hints (direction → approach → insight)
   - Step 3: Write brute-force explanation (naive approach + why slow)
   - Step 4: Write optimal solution walkthrough (step-by-step)
   - Step 5: Write correctness explanation (WHY it works)
   - Step 6: Write complexity analysis (time + space with justification)
   - Step 7: List alternative approaches (if any) with trade-offs
   - Step 8: List common mistakes (2-3) with explanations

5. **Output contract:** Exact JSON schema for the `editorial` section.

6. **Quality criteria:** Hints should progressively reveal without spoiling. Walkthrough should be understandable by the target difficulty level. Common mistakes should address real solver errors.

7. **Few-shot example:** One complete editorial for a known problem.

- [ ] **Step 2: Review prompt for completeness**

Verify:
- [ ] Role framing with teaching focus
- [ ] Progressive hint design (3 levels)
- [ ] Brute-force → optimal progression structure
- [ ] Editorial writing process (8 steps)
- [ ] Output contract with JSON schema
- [ ] Few-shot example
- [ ] No placeholders

- [ ] **Step 3: Commit**

```bash
git add prompts/06_editorial_writer.md
git commit -m "feat: add Agent 6 (Editorial Writer) system prompt"
```

---

### Task 9: Orchestrator Prompt

**Files:**
- Create: `prompts/orchestrator.md`

**Interfaces:**
- Consumes: All 6 agent prompts, all schemas
- Produces: System prompt that defines how to run the full pipeline

- [ ] **Step 1: Write the Orchestrator system prompt**

Create `prompts/orchestrator.md` containing:

1. **Role framing:** "You are the pipeline orchestrator. Your job is to coordinate 6 specialized agents to generate a complete programming problem. You manage the data flow between agents, handle validation gates, and manage retry logic."

2. **Pipeline definition:**
   - Step 1: Run Agent 1 (Problem Architect) with user parameters
   - Step 2: Pass architect_spec to Agent 2 (Problem Writer)
   - Step 3: Pass problem_draft to Agent 3 (Solution Engineer)
   - GATE 1: Check solvability_verdict. If SOLVABILITY_FAILURE → back to Agent 2 (max 2 retries, then escalate to Agent 1)
   - Step 4: Pass problem_draft + solution to Agent 4 (Test Case Generator)
   - Step 5: Pass all outputs to Agent 5 (Quality Reviewer)
   - GATE 2: Check verdict. If REVISION → route feedback to target agent (max 2 rounds)
   - Step 6: Pass approved outputs to Agent 6 (Editorial Writer)
   - Step 7: Assemble final_problem.json

3. **Retry logic:**
   - Gate 1 (solvability): max 2 retries to Agent 2, then 1 retry to Agent 1 for full redesign
   - Gate 2 (quality): max 2 revision rounds, then output best attempt with warnings
   - Confidence-based routing: < 0.5 → escalate, 0.5-0.8 → flag for scrutiny, ≥ 0.8 → proceed

4. **Error handling:**
   - If any agent produces invalid JSON → retry that agent with format reminder
   - If any agent exceeds max retries → output partial result with error flags
   - Always preserve all intermediate outputs for debugging

5. **Assembly process:**
   - Combine all agent outputs into final_problem.json
   - Include quality_report from Agent 5
   - Set metadata (id, generated_at, pipeline_rounds)

6. **Usage instructions:**
   - How to invoke each agent (paste system prompt + input)
   - How to handle the pipeline manually (if not using automated orchestration)
   - How to customize (swap agents, skip stages, adjust retry limits)

- [ ] **Step 2: Review prompt for completeness**

Verify:
- [ ] Pipeline definition (all 6 steps + 2 gates)
- [ ] Retry logic with max limits
- [ ] Confidence-based routing
- [ ] Error handling
- [ ] Assembly process
- [ ] Usage instructions
- [ ] No placeholders

- [ ] **Step 3: Commit**

```bash
git add prompts/orchestrator.md
git commit -m "feat: add orchestrator prompt for pipeline coordination"
```

---

### Task 10: Example 1 — Binary Search on Answer

**Files:**
- Create: `examples/binary_search_on_answer/architect_spec.json`
- Create: `examples/binary_search_on_answer/problem_draft.json`
- Create: `examples/binary_search_on_answer/solution.json`
- Create: `examples/binary_search_on_answer/test_suite.json`
- Create: `examples/binary_search_on_answer/review_verdict.json`
- Create: `examples/binary_search_on_answer/final_problem.json`

**Interfaces:**
- Consumes: All schemas, all agent prompts (for format reference)
- Produces: Complete pipeline trace for a binary search on answer problem

- [ ] **Step 1: Create architect_spec.json**

Write a complete architect spec for a "binary search on answer" problem (similar to Aggressive Cows). Include:
- domain: "dsa"
- topic: "binary_search"
- subtopic: "binary_search_on_answer"
- difficulty: codeforces_rating 1400, tier "medium", bloom_level "apply"
- learning_objective about identifying monotonic feasibility
- prerequisites: ["binary_search_on_array", "sorting_basics"]
- core_concept: "monotonic_feasibility"
- constraint_hints with N ≤ 10^5, O(N log N) expected

- [ ] **Step 2: Create problem_draft.json**

Write a complete problem draft. Create an original problem (not a copy of Aggressive Cows, but same technique). Include:
- Original story/scenario
- Clear statement with unambiguous I/O format
- Constraints that force O(N log N)
- 3 sample tests (basic, non-obvious, edge case)
- 2 subtasks

- [ ] **Step 3: Create solution.json**

Write a complete solution with:
- Binary search on answer approach
- Language-agnostic pseudocode
- O(N log N) time complexity with justification
- Monotonicity correctness argument
- Brute-force O(C(N,K)) alternative
- 2 common wrong approaches with explanations
- solvability_verdict: "success"

- [ ] **Step 4: Create test_suite.json**

Write a complete test suite with:
- At least 12 test cases across all categories
- Edge cases: N=K, K=2, max values, unsorted input
- Adversarial tests targeting each wrong approach
- Boundary tests at constraint limits
- Stress test config
- Coverage report

- [ ] **Step 5: Create review_verdict.json**

Write a review verdict showing APPROVED with realistic scores (all ≥ 8).

- [ ] **Step 6: Create final_problem.json**

Assemble the complete final output combining all previous files plus the editorial section.

- [ ] **Step 7: Validate all files are valid JSON**

```bash
for f in examples/binary_search_on_answer/*.json; do echo "Validating $f..."; python3 -c "import json; json.load(open('$f'))" && echo "OK" || echo "FAIL"; done
```

Expected: All 6 files print "OK"

- [ ] **Step 8: Commit**

```bash
git add examples/binary_search_on_answer/
git commit -m "feat: add example pipeline trace — binary search on answer"
```

---

### Task 11: Example 2 — Sliding Window

**Files:**
- Create: `examples/sliding_window/architect_spec.json`
- Create: `examples/sliding_window/problem_draft.json`
- Create: `examples/sliding_window/solution.json`
- Create: `examples/sliding_window/test_suite.json`
- Create: `examples/sliding_window/review_verdict.json`
- Create: `examples/sliding_window/final_problem.json`

**Interfaces:**
- Consumes: All schemas
- Produces: Complete pipeline trace for a sliding window problem

- [ ] **Step 1: Create all 6 JSON files for the sliding window example**

Same structure as Task 10 but for a sliding window problem (e.g., finding maximum sum subarray of size K, or longest substring with at most K distinct characters).

Ensure:
- architect_spec targets sliding_window subtopic, bloom_level "apply"
- problem_draft has original story, clear I/O, 3 samples, constraints forcing O(N)
- solution uses sliding window technique with O(N) complexity
- test_suite has 12+ test cases covering window edge cases
- review_verdict shows APPROVED
- final_problem assembles everything with editorial

- [ ] **Step 2: Validate all JSON**

```bash
for f in examples/sliding_window/*.json; do echo "Validating $f..."; python3 -c "import json; json.load(open('$f'))" && echo "OK" || echo "FAIL"; done
```

- [ ] **Step 3: Commit**

```bash
git add examples/sliding_window/
git commit -m "feat: add example pipeline trace — sliding window"
```

---

### Task 12: Example 3 — Graph BFS

**Files:**
- Create: `examples/graph_bfs/architect_spec.json`
- Create: `examples/graph_bfs/problem_draft.json`
- Create: `examples/graph_bfs/solution.json`
- Create: `examples/graph_bfs/test_suite.json`
- Create: `examples/graph_bfs/review_verdict.json`
- Create: `examples/graph_bfs/final_problem.json`

**Interfaces:**
- Consumes: All schemas
- Produces: Complete pipeline trace for a graph BFS problem

- [ ] **Step 1: Create all 6 JSON files for the graph BFS example**

Same structure but for a graph BFS problem (e.g., shortest path in unweighted graph, or minimum steps to reach target, or multi-source BFS on grid).

Ensure:
- architect_spec targets graph_bfs subtopic, bloom_level "apply"
- problem_draft has graph input format (N nodes, M edges), clear I/O
- solution uses BFS with O(N+M) complexity
- test_suite covers graph edge cases (disconnected, single node, cycle, self-loop)
- review_verdict shows APPROVED
- final_problem assembles everything with editorial

- [ ] **Step 2: Validate all JSON**

```bash
for f in examples/graph_bfs/*.json; do echo "Validating $f..."; python3 -c "import json; json.load(open('$f'))" && echo "OK" || echo "FAIL"; done
```

- [ ] **Step 3: Commit**

```bash
git add examples/graph_bfs/
git commit -m "feat: add example pipeline trace — graph BFS"
```

---

### Task 13: README + Documentation

**Files:**
- Create: `README.md`
- Create: `docs/usage_guide.md`
- Create: `docs/extending.md`

**Interfaces:**
- Consumes: All prompts, schemas, examples, knowledge base
- Produces: User-facing documentation

- [ ] **Step 1: Write README.md**

Include:
- Project title and description (what it does, why it exists)
- Key differentiator (generates problem + solution + tests, not just problems)
- Architecture overview (6-agent pipeline with adversarial review diagram)
- Quick start (how to use the prompts with any LLM)
- File structure explanation
- Agent descriptions (one paragraph each)
- Example output preview (snippet of final_problem.json)
- Contributing guide (how to add new agents, domains, examples)
- License (MIT)

- [ ] **Step 2: Write docs/usage_guide.md**

Include:
- How to use prompts with OpenAI (GPT-4)
- How to use prompts with Anthropic (Claude)
- How to use prompts with Google (Gemini)
- How to run the pipeline manually (step by step)
- How to customize parameters (change difficulty, topic, domain)
- How to interpret the output (what each field means)
- Tips for getting best results (temperature settings, model recommendations)

- [ ] **Step 3: Write docs/extending.md**

Include:
- How to add a new agent to the pipeline
- How to add a new domain (e.g., machine learning, databases)
- How to add new example pipeline traces
- How to modify schemas (what to update when adding fields)
- How to contribute back to the project

- [ ] **Step 4: Commit**

```bash
git add README.md docs/usage_guide.md docs/extending.md
git commit -m "docs: add README, usage guide, and extending guide"
```

---

### Task 14: Final Review & Polish

**Files:**
- Review: All files in the project

- [ ] **Step 1: Verify all prompts reference correct schemas**

Check each prompt file:
- Does it reference the correct input schema?
- Does it reference the correct output schema?
- Does the output JSON example match the schema file?

- [ ] **Step 2: Verify all examples match schemas**

```bash
python3 -c "
import json, glob, sys
from pathlib import Path

schemas = {
    'architect_spec': json.load(open('schemas/architect_spec.json')),
    'problem_draft': json.load(open('schemas/problem_draft.json')),
    'solution': json.load(open('schemas/solution.json')),
    'test_suite': json.load(open('schemas/test_suite.json')),
    'review_verdict': json.load(open('schemas/review_verdict.json')),
    'final_problem': json.load(open('schemas/final_problem.json')),
}

for example_dir in glob.glob('examples/*/'):
    name = Path(example_dir).name
    for schema_name in schemas:
        fpath = f'{example_dir}{schema_name}.json'
        try:
            data = json.load(open(fpath))
            print(f'  OK: {name}/{schema_name}.json')
        except Exception as e:
            print(f'  FAIL: {name}/{schema_name}.json — {e}')
"
```

- [ ] **Step 3: Verify cross-references between knowledge base and prompts**

Check that each knowledge document is referenced by at least one agent prompt.

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "chore: final review and polish"
```
