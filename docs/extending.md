# Extending Agent Skills Problem Gen

> **Audience:** Contributors who want to add agents, support new domains, contribute example traces, or evolve the schemas.

This guide explains the extension points in the Agent Skills Problem Gen pipeline and walks through each one with concrete steps. Read the [README](../README.md) and [Usage Guide](usage_guide.md) first so you understand the baseline 6-agent pipeline.

---

## Table of Contents

- [Architecture Recap](#architecture-recap)
- [Extension Points Overview](#extension-points-overview)
- [Adding a New Agent](#adding-a-new-agent)
- [Adding a New Domain](#adding-a-new-domain)
- [Adding a New Example Pipeline Trace](#adding-a-new-example-pipeline-trace)
- [Modifying Schemas](#modifying-schemas)
- [Extending the Knowledge Base](#extending-the-knowledge-base)
- [Customizing the Orchestrator](#customizing-the-orchestrator)
- [Contributing Back](#contributing-back)

---

## Architecture Recap

The pipeline is a chain of agents, each with three artifacts:

```
prompt (prompts/NN_name.md)   →   defines the agent's behavior
schema (schemas/name.json)    →   defines the agent's output contract
example (examples/*/name.json) →   demonstrates the agent's output in practice
```

The **orchestrator** (`prompts/orchestrator.md`) wires agents together, enforces two gates (solvability + quality), and assembles `final_problem.json`. Every agent is **interchangeable** as long as it respects its input/output schema.

---

## Extension Points Overview

| What you want to do | Files to touch |
|---|---|
| Add a new agent to the pipeline | `prompts/`, `schemas/`, `prompts/orchestrator.md` |
| Support a new domain (ML, DB, etc.) | `schemas/architect_spec.json`, `knowledge/`, agent prompts |
| Contribute an example trace | `examples/<your_topic>/` (6 JSON files) |
| Add a field to an existing schema | `schemas/<name>.json`, the corresponding prompt, downstream agents |
| Add pedagogy reference material | `knowledge/` |
| Change retry/gate behavior | `prompts/orchestrator.md` |

---

## Adding a New Agent

Use this when you want to insert a new stage into the pipeline — for example, a **Difficulty Calibrator**, a **Story Editor**, a **Visualizer** (generates diagrams), or a **Translator** (produces multi-language statements).

### Step 1: Define the agent's role

Answer these questions before writing anything:

1. **Where in the pipeline does it run?** (after which agent, before which agent)
2. **What does it consume?** (which agent outputs does it read)
3. **What does it produce?** (what is the new JSON artifact)
4. **Does it need a gate?** (should the orchestrator validate its output and possibly retry)
5. **Is it optional or mandatory?** (can the pipeline skip it)

Example — adding a **Difficulty Calibrator** that runs after Agent 2 (Problem Writer) and before Agent 3 (Solution Engineer):

- Consumes: `architect_spec.json` + `problem_draft.json`
- Produces: `difficulty_calibration.json` (adjusted rating, tier, Bloom level)
- Gate: no (it's a lightweight adjustment, not a quality check)
- Mandatory: yes (every problem should be calibrated)

### Step 2: Create the schema

Create `schemas/difficulty_calibration.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Difficulty Calibration",
  "description": "Output of the Difficulty Calibrator agent.",
  "type": "object",
  "required": [
    "adjusted_rating",
    "adjusted_tier",
    "adjusted_bloom_level",
    "rationale",
    "confidence"
  ],
  "properties": {
    "adjusted_rating": { "type": "integer", "minimum": 800, "maximum": 3500 },
    "adjusted_tier": { "type": "string", "enum": ["easy", "medium", "hard", "expert"] },
    "adjusted_bloom_level": { "type": "string", "enum": ["remember", "understand", "apply", "analyze", "evaluate", "create"] },
    "rationale": { "type": "string" },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
  }
}
```

Guidelines for schemas:

- Use JSON Schema draft-07 (matches the existing schemas).
- List every field the downstream agents need in `required`.
- Use `enum` for bounded choices so the LLM can't drift.
- Add `description` at the schema level and on non-obvious fields — the prompt will reference these.

### Step 3: Write the prompt

Create `prompts/07_difficulty_calibrator.md` (or insert at the right position and renumber). Structure it like the existing prompts:

```markdown
# System Prompt — Difficulty Calibrator

You are a difficulty calibrator for competitive programming problems.
Your job is to review a problem draft and adjust its difficulty rating
based on the actual technique required, not the story complexity.

## Input
You receive:
- `architect_spec.json` (the original blueprint)
- `problem_draft.json` (the polished statement)

## Calibration Rubric
[... your rubric here ...]

## Output Contract
Output a single JSON object conforming to `schemas/difficulty_calibration.json`.
Required fields: `adjusted_rating`, `adjusted_tier`, `adjusted_bloom_level`,
`rationale`, `confidence`.

Output ONLY the JSON object. No markdown fences, no commentary.
```

Prompt-writing tips learned from the existing agents:

- **Lead with role and goal.** The LLM should know *what it is* in the first sentence.
- **Be explicit about the output contract.** List required fields, reference the schema, forbid markdown fences.
- **Include a rubric or checklist.** Agents produce higher-quality output when given a structured evaluation framework (see Agent 5's Shield/Sword, Agent 2's 8-item anti-ambiguity list).
- **Give negative examples.** "Do NOT do X" is as important as "Do Y".
- **Pin the temperature.** Recommend a temperature range at the top (e.g., `Temperature: 0.4–0.6`) so users get consistent results.

### Step 4: Update the orchestrator

Edit `prompts/orchestrator.md`:

1. Add the new agent to the **Agent Definitions** section:
   ```markdown
   ### Agent 7: Difficulty Calibrator
   - **Prompt file:** `prompts/07_difficulty_calibrator.md`
   - **Input:** `architect_spec.json` + `problem_draft.json`
   - **Output:** `difficulty_calibration.json`
   - **Role:** Adjusts difficulty rating based on actual technique required.
   ```

2. Insert it into the **pipeline diagram** at the right position.

3. Add a new **Step N** section describing:
   - What input to pass
   - How to validate the output (schema check)
   - What to do with the output (pass downstream)

4. Update the **Assembly** section to include the new artifact in `final_problem.json` (if it should be persisted).

5. Update the **Quick Reference** table at the bottom.

### Step 5: Update the final schema

If the new agent's output should appear in `final_problem.json`, add it to `schemas/final_problem.json`:

```json
{
  "properties": {
    "difficulty_calibration": { "$ref": "difficulty_calibration.json" },
    ...
  }
}
```

### Step 6: Produce an example trace

Run the pipeline with the new agent and save all intermediate JSONs in a new directory under `examples/`. See [Adding a New Example Pipeline Trace](#adding-a-new-example-pipeline-trace) below.

### Step 7: Update the README

Add a paragraph describing the new agent in the **The Agents** section of the README, and update the architecture diagram.

---

## Adding a New Domain

The current prompts are tuned for **DSA / competitive programming**. To support another domain (machine learning, databases, systems, language learning), you need to extend three places: the schema enum, the knowledge base, and the agent prompts.

### Step 1: Extend the domain enum

Edit `schemas/architect_spec.json`:

```json
"domain": {
  "type": "string",
  "enum": ["dsa", "language_learning", "competitive_programming", "machine_learning"]
}
```

Add your new domain to the enum. Keep the existing values — don't rename or remove them, or existing examples will break.

### Step 2: Add domain knowledge

Create one or more files in `knowledge/` that capture the pedagogy of your domain. For machine learning, you might create:

```
knowledge/
├── ml_concept_dependency_graph.md    # which ML concepts depend on which
├── ml_difficulty_calibration.md      # what makes an ML problem "easy" vs "hard"
├── ml_common_misconceptions.md       # mistakes learners make at each level
└── ml_problem_types.md               # classification of ML problem types
```

Model these on the existing DSA knowledge files:

- `dsa_learning_progression.md` → your domain's **level progression**
- `blooms_taxonomy_mapping.md` → how Bloom's levels map to your domain's task types
- `constraint_complexity_table.md` → your domain's analogue of "N range → required complexity"
- `anti_patterns_checklist.md` → common mistakes in your domain's problems
- `edge_case_taxonomy.md` → edge cases specific to your domain

### Step 3: Update Agent 1 (Problem Architect)

The Problem Architect is the most domain-sensitive agent — it decides *what concept to teach*. Edit `prompts/01_problem_architect.md` to:

1. Reference your new knowledge files:
   ```markdown
   When `domain` is `machine_learning`, consult:
   - `knowledge/ml_concept_dependency_graph.md` for prerequisite chains
   - `knowledge/ml_difficulty_calibration.md` for difficulty assignment
   ```

2. Add domain-specific guidance:
   ```markdown
   ### Machine Learning Domain
   - Problems should focus on conceptual understanding, not just API usage
   - Prefer problems that require choosing between models/techniques
   - Include dataset characteristics as part of the problem input
   - Target Bloom's levels: apply (choose a model), analyze (debug a pipeline), evaluate (justify a choice)
   ```

### Step 4: Update downstream agents (as needed)

Some agents are domain-agnostic and don't need changes:

- **Agent 4 (Test Case Generator)** — mostly domain-agnostic; tests are tests
- **Agent 5 (Quality Reviewer)** — mostly domain-agnostic; the Shield/Sword dimensions generalize

Others need domain-specific tweaks:

- **Agent 2 (Problem Writer)** — the story/setting vocabulary changes (e.g., ML problems might involve datasets, models, or pipelines instead of experiments and professors)
- **Agent 3 (Solution Engineer)** — the proof techniques change (ML "correctness" is often empirical, not formal)
- **Agent 6 (Editorial Writer)** — the "aha moment" is different in ML (e.g., "why does regularization help here?")

You don't have to rewrite these prompts entirely. Add a **domain-specific notes** section that the agent consults when the `domain` field is your new value.

### Step 5: Produce an example trace

Generate at least one complete pipeline trace in your new domain and add it to `examples/`. This is critical — it's the proof that your domain extension works end-to-end.

---

## Adding a New Example Pipeline Trace

Examples are the project's most valuable artifacts. They prove the pipeline works, demonstrate the expected output quality, and serve as few-shot references for the agents.

### Step 1: Choose a topic

Pick a topic that:

- **Differs from existing examples.** We already have binary search on answer, sliding window, and graph BFS. Good next choices: dynamic programming, segment trees, number theory, greedy with sorting.
- **Exercises interesting pipeline behavior.** A problem that needs a Gate 1 retry or a Gate 2 revision is more instructive than one that passes on the first round.
- **Targets a different difficulty tier.** We have a medium (1400) example. Add an easy (1000) or hard (1800) one.

### Step 2: Run the pipeline

Follow the [Usage Guide](usage_guide.md) to generate the problem. Save **every intermediate JSON**:

- `architect_spec.json`
- `problem_draft.json`
- `solution.json`
- `test_suite.json`
- `review_verdict.json`
- `editorial.json` (if generated)
- `final_problem.json` (the assembled output)

### Step 3: Create the example directory

```bash
mkdir examples/<your_topic>/
# use snake_case, matching the subtopic name
# e.g., examples/knapsack_dp/, examples/dijkstra_shortest_path/
```

Copy all 6–7 JSON files into the directory.

### Step 4: Add a README for the example

Create `examples/<your_topic>/README.md`:

```markdown
# <Problem Title>

**Topic:** <topic> / <subtopic>
**Difficulty:** Codeforces <rating> (<tier>)
**Bloom's Level:** <level>
**Pipeline Rounds:** <N>

## Problem Summary
<2–3 sentence summary of the problem>

## Key Techniques
- <technique 1>
- <technique 2>

## Pipeline Notes
<Any interesting observations about the pipeline run — did it need retries?
did the quality reviewer catch something important?>
```

### Step 5: Validate the example

Before committing:

1. **Schema-validate every JSON file** against the corresponding schema in `schemas/`. Use a JSON Schema validator (e.g., `ajv` in Node, `jsonschema` in Python).
2. **Check the final_problem.json** has all required sections: `metadata`, `problem`, `solution`, `test_suite`, `editorial`, `quality_report`.
3. **Verify test cases** — the `test_suite.json` should have ≥ 10 test cases across all 4 categories.
4. **Sanity-check the solution** — does it actually solve the problem? Run it mentally on Sample 1.

### Step 6: Commit

```bash
git add examples/<your_topic>/
git commit -m "feat: add example pipeline trace — <your_topic>"
```

---

## Modifying Schemas

Schemas are the contracts between agents. Changing them is high-leverage — every agent that produces or consumes the schema needs to be updated.

### When to modify a schema

- **Adding a field** — usually safe, as long as the field is optional or has a default
- **Removing a field** — dangerous; check all downstream consumers first
- **Changing a field's type or enum** — check all producers and consumers
- **Renaming a field** — same as remove + add; update every reference

### Step 1: Identify the blast radius

Before changing `schemas/<name>.json`, search for every file that references it:

```bash
# Find every prompt that mentions the schema
grep -r "<name>" prompts/
# Find every example that produces this artifact
find examples/ -name "<name>.json"
# Find downstream agents that consume this artifact
grep -r "<name>.json" prompts/
```

### Step 2: Make the change backward-compatible when possible

- **Adding a field:** add it as optional (don't put it in `required`) until all producers are updated.
- **Deprecating a field:** keep it in the schema but mark it with a `deprecated: true` annotation (custom, since JSON Schema doesn't have this natively) and remove it from prompts. Remove from the schema in the next major version.
- **Changing an enum:** add new values first, update producers, then remove old values.

### Step 3: Update the producer prompt

Edit the prompt of the agent that produces this schema. Update the **Output Contract** section to:

- List the new field in the required fields
- Describe what the field means
- Give an example value

### Step 4: Update consumer prompts

Edit every prompt that reads this schema. Update the **Input Specification** section so the agent knows the new field exists and how to use it.

### Step 5: Update the orchestrator

If the schema change affects validation (e.g., a new required field), update the orchestrator's validation step for that agent.

### Step 6: Update existing examples

Re-run the pipeline (or manually edit) the existing examples in `examples/` so their JSON files conform to the new schema. Don't leave broken examples in the repo.

### Step 7: Update documentation

- Update the README's **Example Output Preview** section if the shape of `final_problem.json` changed.
- Update the Usage Guide's **Interpreting the Output** section.
- Update this file if you changed a process.

### Schema change checklist

Before merging a schema change, verify:

- [ ] Producer prompt updated
- [ ] All consumer prompts updated
- [ ] Orchestrator validation updated
- [ ] All examples re-validated against the new schema
- [ ] README and usage guide updated
- [ ] Schema version bumped (if you're using versioning)

---

## Extending the Knowledge Base

The `knowledge/` directory contains domain-agnostic pedagogy reference material that agents consult during generation.

### What belongs in `knowledge/`

- **Taxonomies** — classifications of concepts, problems, edge cases, techniques
- **Progressions** — leveled skill hierarchies (like `dsa_learning_progression.md`)
- **Mapping tables** — e.g., Bloom's level → problem type, constraint range → complexity
- **Checklists** — anti-patterns, quality criteria, review rubrics
- **Reference data** — anything an agent might need to look up mid-generation

### What does NOT belong in `knowledge/`

- Agent prompts (those go in `prompts/`)
- Schema definitions (those go in `schemas/`)
- Example outputs (those go in `examples/`)
- Provider-specific instructions (those go in `docs/usage_guide.md`)

### Adding a new knowledge file

1. Create the file in `knowledge/` with a descriptive snake_case name.
2. Start with a **Purpose** block explaining what the file is for and which agents reference it.
3. Structure the content with clear headers and tables — agents parse markdown better than prose.
4. Reference the file from the relevant agent prompts:
   ```markdown
   Consult `knowledge/<your_file>.md` when:
   - <situation 1>
   - <situation 2>
   ```

### Example: adding a "common wrong approaches" knowledge file

```markdown
# Common Wrong Approaches by Topic

> **Purpose:** Catalog of incorrect approaches students commonly attempt,
> organized by DSA topic. Referenced by Agent 3 (Solution Engineer) for
> the `common_wrong_approaches` field, and Agent 4 (Test Case Generator)
> for adversarial test design.

## Binary Search

### Wrong Approach 1: Linear scan
- **Description:** Scan the entire search space linearly
- **Why it's wrong:** O(N) instead of O(log N); TLEs on large inputs
- **Test to catch it:** N = 10⁹ with tight time limit

### Wrong Approach 2: Binary search without monotonicity check
- **Description:** Apply binary search when the feasibility function isn't monotonic
- **Why it's wrong:** Returns incorrect answer when the predicate isn't monotone
- **Test to catch it:** Craft input where feasibility is non-monotonic

...
```

---

## Customizing the Orchestrator

The orchestrator (`prompts/orchestrator.md`) is itself a prompt — you can customize its behavior without touching code.

### Adjusting retry limits

The defaults are:
- **Gate 1 (solvability):** 2 retries to Agent 2, then 1 retry to Agent 1, then abort
- **Gate 2 (quality):** 2 revision rounds, then force-approve with warnings

To change, edit the **Retry Logic** section of the orchestrator prompt. Examples:

- **Higher quality, higher cost:** increase Gate 2 to 3–4 rounds
- **Faster iteration:** reduce Gate 1 to 1 retry, Gate 2 to 1 round
- **Research mode:** disable gates entirely (not recommended for production)

### Adding custom gates

You can insert additional gates between any two agents. For example, a **Story Sensitivity Gate** between Agent 2 and Agent 3 that checks the problem story for inappropriate content:

```markdown
### Gate 1.5: Story Sensitivity

After Agent 2 produces `problem_draft.json`, check:
- `story` does not contain [forbidden terms]
- `story` is culturally neutral
- `story` length is 2–5 sentences

If the check fails, route back to Agent 2 with specific feedback.
Max 1 retry.
```

Add the gate to the pipeline diagram, the step-by-step execution, and the retry logic section.

### Skipping optional agents

The orchestrator already documents which agents can be skipped. To skip an agent:

1. Declare it optional in the **Agent Definitions** section.
2. Add a conditional in the step-by-step execution:
   ```markdown
   ### Step 6 (optional): Run Agent 6 (Editorial Writer)
   If the user requested an editorial, run Agent 6. Otherwise, set `editorial` to `null` in the final assembly.
   ```
3. Update the assembly rules to handle the missing artifact.

### Adding confidence-based routing

The orchestrator already has confidence-based routing rules. To customize:

- Change the thresholds (currently 0.5 / 0.8)
- Add agent-specific thresholds (e.g., Agent 3 needs higher confidence than Agent 2)
- Add routing actions (e.g., "if Agent 4 confidence < 0.6, also run Agent 4 again with a different seed")

---

## Contributing Back

We welcome contributions! Here's the workflow:

### Before you start

1. **Open an issue** describing what you want to add and why. This avoids duplicate work and lets maintainers give guidance early.
2. **Read the existing prompts and schemas** end-to-end so you understand the contracts.
3. **Pick one extension point.** Don't try to add a new agent AND a new domain AND three examples in one PR.

### Development workflow

1. **Fork the repo** and create a feature branch:
   ```bash
   git checkout -b feat/add-difficulty-calibrator
   ```

2. **Make your changes** following the relevant section of this guide.

3. **Test your changes with a full pipeline run.** Use the [Usage Guide](usage_guide.md) to run the pipeline end-to-end with your new component. Verify:
   - All JSON outputs validate against their schemas
   - The pipeline produces a complete `final_problem.json`
   - The output quality is at least as good as the existing examples

4. **Add an example trace** demonstrating your extension in action.

5. **Update documentation** — README, usage guide, this file, and any inline comments.

### Pull request checklist

Before submitting your PR, verify:

- [ ] Every new/modified prompt ends with an explicit output contract referencing a schema
- [ ] Every new/modified schema validates with a JSON Schema validator
- [ ] Every example JSON file validates against its schema
- [ ] The pipeline runs end-to-end with your changes
- [ ] README is updated if you added/removed an agent
- [ ] Usage guide is updated if you changed how to run the pipeline
- [ ] This file (`extending.md`) is updated if you changed an extension process
- [ ] Your PR description explains the *why*, not just the *what*

### Review process

- A maintainer will review your PR within a few days.
- Expect feedback on prompt quality (clarity, specificity, output contract rigor).
- Schema changes get extra scrutiny because they affect every downstream agent.
- Example traces are reviewed for correctness (does the solution actually solve the problem?) and quality (does it meet the standard of existing examples?).

### Style guide for prompts

- **Lead with role and goal.** First sentence = who the agent is and what it does.
- **Use markdown headers** to structure the prompt (Input, Output, Rubric, Examples, Anti-examples).
- **Be explicit about the output contract.** List required fields, reference the schema, forbid markdown fences.
- **Include a rubric or checklist** when the agent needs to make judgments.
- **Give concrete examples** of good and bad output when possible.
- **Pin the temperature** at the top of the prompt (e.g., `Temperature: 0.5–0.7`).
- **Keep prompts under 3000 words.** Longer prompts dilute the LLM's attention. Split into sub-sections with clear headers.

---

## Questions?

- Open an issue on GitHub for bugs, feature requests, or design discussions.
- Check the [README](../README.md) for project overview and [Usage Guide](usage_guide.md) for how to run the pipeline.
- Browse the [existing examples](../examples/) to see what good output looks like.

Happy extending!
