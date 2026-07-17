# Agent Skills Problem Gen

**Generate contest-quality competitive programming problems — complete with verified solutions, comprehensive test suites, and pedagogical editorials — using a 6-agent AI pipeline.**

Agent Skills Problem Gen is a prompt library that turns a single idea ("binary search on answer, rating 1400") into a complete, ready-to-publish problem package. Every output is structured JSON, reviewed by an adversarial quality gate, and grounded in DSA pedagogy.

---

## Why This Exists

Most AI-generated programming problems stop at the statement. Agent Skills Problem Gen goes further:

- **Problem statement** — contest-ready, anti-ambiguity checked
- **Verified solution** — with formal correctness proof and complexity analysis
- **Test suite** — 10+ hand-crafted cases across basic, edge, adversarial, and boundary categories, plus stress-test configuration
- **Editorial** — progressive hints, brute-force-to-optimal bridge, common mistakes

Every artifact is produced by a specialized agent and validated by an adversarial reviewer before assembly.

---

## Architecture

```
                        ┌──────────────────────┐
                        │   User Parameters    │
                        │  domain, topic,      │
                        │  difficulty, bloom   │
                        └──────────┬───────────┘
                                   │
                                   ▼
                  ┌────────────────────────────────┐
                  │  Agent 1: Problem Architect    │
                  │  Blueprint: concept, level,    │
                  │  constraints, prerequisites    │
                  └────────────────┬───────────────┘
                                   │ architect_spec.json
                                   ▼
                  ┌────────────────────────────────┐
                  │  Agent 2: Problem Writer       │
                  │  Statement, story, samples,    │
                  │  input/output format           │
                  └────────────────┬───────────────┘
                                   │ problem_draft.json
                                   ▼
                  ┌────────────────────────────────┐
                  │  Agent 3: Solution Engineer    │
                  │  Pseudocode, proof, complexity │
                  └────────────────┬───────────────┘
                                   │ solution.json
                                   ▼
                        ╔═══════════════════╗
                        ║  GATE 1: Solvable? ║
                        ╚════════╤══════════╝
                          fail ──┤── success
                          │      │
                   retry A2/A1   ▼
                  ┌────────────────────────────────┐
                  │  Agent 4: Test Case Generator  │
                  │  10+ tests, stress config,     │
                  │  coverage report               │
                  └────────────────┬───────────────┘
                                   │ test_suite.json
                                   ▼
                  ┌────────────────────────────────┐
                  │  Agent 5: Quality Reviewer     │
                  │  Shield (10 dimensions) vs     │
                  │  Sword (5 attack vectors)      │
                  └────────────────┬───────────────┘
                                   │ review_verdict.json
                                   ▼
                        ╔═══════════════════╗
                        ║  GATE 2: Quality?  ║
                        ╚════════╤══════════╝
                          fail ──┤── APPROVED
                          │      │
                   route back    ▼
                  ┌────────────────────────────────┐
                  │  Agent 6: Editorial Writer     │
                  │  Hints, walkthrough, mistakes  │
                  └────────────────┬───────────────┘
                                   │ editorial
                                   ▼
                  ┌────────────────────────────────┐
                  │  Assembly → final_problem.json │
                  └────────────────────────────────┘
```

---

## Quick Start

### 1. Pick your LLM

The prompts work with **any LLM that handles structured JSON output**: GPT-4, Claude, Gemini, Llama, etc.

### 2. Set your parameters

Decide what you want to generate:

```
domain: dsa
topic: binary_search
subtopic: binary_search_on_answer
difficulty_range: 1200-1600
bloom_target: apply
target_audience: "competitive programmers preparing for Div. 2 C/D"
```

### 3. Run the pipeline

Feed each agent's prompt (in `prompts/`) to your LLM in sequence, passing the previous agent's JSON output as context. The orchestrator prompt (`prompts/orchestrator.md`) describes the full routing logic.

```bash
# Example with OpenAI CLI (conceptual)
cat prompts/01_problem_architect.md | llm --model gpt-4 --system "..." > architect_spec.json
cat prompts/02_problem_writer.md | llm --model gpt-4 --system "$(cat architect_spec.json)" > problem_draft.json
# ... continue through all 6 agents
```

See [docs/usage_guide.md](docs/usage_guide.md) for detailed instructions per provider.

### 4. Inspect the output

The final `final_problem.json` contains everything: problem statement, solution, test suite, editorial, and quality report.

---

## File Structure

```
.
├── README.md
├── prompts/                        # The 7 agent prompts (the core library)
│   ├── 01_problem_architect.md     # Agent 1: creates the problem blueprint
│   ├── 02_problem_writer.md        # Agent 2: writes the problem statement
│   ├── 03_solution_engineer.md     # Agent 3: builds the reference solution
│   ├── 04_test_case_generator.md   # Agent 4: generates test suite
│   ├── 05_quality_reviewer.md      # Agent 5: adversarial review (Shield + Sword)
│   ├── 06_editorial_writer.md      # Agent 6: writes the pedagogical editorial
│   └── orchestrator.md             # Pipeline coordinator (routing, gates, assembly)
├── schemas/                        # JSON schemas for inter-agent contracts
│   ├── architect_spec.json
│   ├── problem_draft.json
│   ├── solution.json
│   ├── test_suite.json
│   ├── review_verdict.json
│   └── final_problem.json
├── examples/                       # Complete pipeline traces (3 problems)
│   ├── binary_search_on_answer/    # "Lab Assignment" — partition into K groups
│   ├── sliding_window/             # Festival lanterns — variable-size window
│   └── graph_bfs/                  # Network hops — BFS shortest path
├── knowledge/                      # Embedded DSA pedagogy reference
│   ├── anti_patterns_checklist.md  # 7 anti-patterns with detection + fix
│   ├── blooms_taxonomy_mapping.md  # Bloom's levels → CP problem types
│   ├── constraint_complexity_table.md  # N range → required complexity
│   ├── dsa_learning_progression.md # 7-level DSA mastery progression
│   └── edge_case_taxonomy.md       # Edge cases by data structure type
└── docs/
    ├── usage_guide.md              # How to use with OpenAI / Anthropic / Gemini
    └── extending.md                # How to add agents, domains, examples
```

---

## The Agents

### Agent 1: Problem Architect
Designs the **blueprint** — not the problem itself. Identifies the core concept to teach, maps it to the DSA learning progression (Levels 0–6), assigns a Bloom's taxonomy level, sets Codeforces rating and constraints, and lists prerequisites. Grounded in the constraint-complexity table and DSA progression knowledge base.

### Agent 2: Problem Writer
Transforms the blueprint into a **polished, contest-ready problem statement**. Writes the title, story, formal statement, input/output format, constraints, and 2–5 sample tests — each with a specific pedagogical purpose. Runs an 8-item anti-ambiguity checklist before outputting.

### Agent 3: Solution Engineer
Produces a **provably correct reference solution** with language-agnostic pseudocode, time/space complexity analysis, and a formal correctness argument (using one of five proof techniques: loop invariant, exchange argument, induction, monotonicity, greedy stays ahead). Includes a brute-force alternative for cross-verification and a **solvability gate** that halts the pipeline if the problem is unsolvable.

### Agent 4: Test Case Generator
An **adversarial test engineer** that creates 10+ hand-crafted tests across four categories: basic (3–5), edge case (5–8), adversarial (3–5, designed to break common wrong approaches), and boundary (2–3, at constraint extremes). Also configures stress testing (100+ random tests with brute-force oracle) and writes a coverage report.

### Agent 5: Quality Reviewer
The **adversarial gatekeeper** using two internal personas. **Shield** scores 10 quality dimensions (0–10): statement clarity, constraint alignment, solution correctness, test coverage, pedagogical value, difficulty calibration, story quality, sample test quality, subtask design, and overall elegance. **Sword** attacks from 5 vectors: ambiguity hunt, solution attack, test bypass, constraint mismatch, and edge case gap. Outputs `APPROVED` or `REVISION` with feedback routed to the appropriate agent.

### Agent 6: Editorial Writer
Produces a **pedagogical editorial** designed to create the "aha moment." Writes 3 progressive hints (direction → approach → key insight), explains the brute-force approach and why it's too slow, bridges to the optimal solution, walks through it step-by-step on Sample 1, and lists common mistakes with counterexamples.

### Orchestrator
The **pipeline coordinator** that routes data between agents, enforces the two quality gates (solvability and quality), handles retries with bounded loops (max 2 rounds at each gate), manages confidence-based routing, and assembles the final `final_problem.json`.

---

## Example Output Preview

Here's a snippet of what `final_problem.json` looks like (from the binary search on answer example):

```json
{
  "metadata": {
    "id": "binary_search_on_answer_001",
    "domain": "dsa",
    "topic": "binary_search",
    "subtopic": "binary_search_on_answer",
    "difficulty": {
      "codeforces_rating": 1400,
      "tier": "medium"
    },
    "bloom_level": "apply",
    "tags": ["binary search", "greedy", "math"],
    "prerequisites": ["binary search basics", "greedy algorithms", "prefix sums"]
  },
  "problem": {
    "title": "Lab Assignment",
    "story": "A computer science professor needs to partition N experiments into K contiguous groups...",
    "statement": "Given N experiments with durations D₁, D₂, ..., Dₙ, partition them into exactly K contiguous groups such that the maximum sum of any group is minimized.",
    "constraints": ["1 ≤ K ≤ N ≤ 10⁵", "1 ≤ Dᵢ ≤ 10⁹"],
    "sample_tests": [
      { "input": "5 2\n3 5 2 7 4", "output": "12", "explanation": "..." }
    ]
  },
  "solution": {
    "approach": "Binary search on the answer with greedy feasibility check",
    "time_complexity": "O(N × log(sum(D)))",
    "correctness_argument": "Monotonicity: if we can partition with max sum S, we can also do it with S+1..."
  },
  "test_suite": {
    "test_cases": [
      { "id": 1, "category": "basic", "purpose": "Verify basic mechanics" },
      { "id": 8, "category": "adversarial", "purpose": "Break linear scan approaches" }
    ],
    "stress_test_config": { "random_tests": 500, "comparison": "brute_force" }
  },
  "editorial": {
    "hints": [
      "Think about what happens if we fix the maximum group sum...",
      "Can you check if a given maximum sum is feasible?",
      "The feasibility function is monotonic — binary search!"
    ]
  },
  "quality_report": {
    "shield_scores": { "statement_clarity": 9, "solution_correctness": 9, "..." : "..." },
    "pipeline_rounds": 1
  }
}
```

See the full examples in [`examples/`](examples/).

---

## Contributing

Contributions are welcome! Here's how to get started:

### Adding a New Agent
1. Create a new prompt file in `prompts/` following the naming convention (`NN_agent_name.md`)
2. Define the agent's input/output schema in `schemas/`
3. Update the orchestrator prompt to include the new agent in the pipeline
4. Add an example trace in `examples/`

See [docs/extending.md](docs/extending.md) for detailed instructions.

### Adding a New Domain
The current prompts focus on DSA/competitive programming. To add a new domain (e.g., machine learning, databases):
1. Update the `domain` enum in `schemas/architect_spec.json`
2. Add domain-specific knowledge to `knowledge/`
3. Update the Problem Architect prompt with domain-specific guidance

### Adding Examples
1. Run the pipeline with your parameters
2. Save all intermediate JSON outputs in a new directory under `examples/`
3. Include a brief `README.md` in your example directory

### Code of Conduct
- Be respectful and constructive in reviews
- Follow the existing prompt structure and schema conventions
- Test your changes with at least one full pipeline run
- Update documentation when changing interfaces

---

## License

MIT License — see [LICENSE](LICENSE) for details.

Copyright (c) 2026 Agent Skills Problem Gen Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
