---
name: design-problem-blueprint
description: Design a competitive programming problem blueprint - learning objective, difficulty calibration, prerequisites, constraints, and story direction. Supports single problem and balanced problem set generation with configurable difficulty distributions (beginner to grandmaster).
---

# Problem Architect (Agent 1)

Design the blueprint for a competitive programming problem. You do NOT write the problem statement — you produce a structured specification (`architect_spec.json`) that downstream agents consume.

## When to Use

- Designing a new problem concept from scratch
- Choosing difficulty, prerequisites, and constraints for a target audience
- Planning a balanced problem set with specific distribution ratios
- Deciding what concept a problem should teach

## Input Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `domain` | string | `dsa`, `language_learning`, or `competitive_programming` |
| `topic` | string | e.g., `graphs`, `dynamic programming`, `strings` |
| `subtopic` | string | e.g., `shortest paths`, `knapsack variants` |
| `difficulty_range` | string | e.g., `1300-1600`, `800-1200` |
| `bloom_target` | string | `remember`, `understand`, `apply`, `analyze`, `evaluate`, `create` |
| `target_audience` | string | e.g., `Div2 beginners`, `advanced contestants` |
| `mode` | string | `single` (default) or `set` |
| `level` | string | `beginner`, `specialist`, `expert`, `master`, `grandmaster` (for set mode) |
| `set_size` | integer | Number of problems in set (default: 5) |
| `distribution` | object | `{comfortable, challenging, stretch}` ratios |
| `topic_preferences` | array | Preferred topics for set mode |

## Output

Single mode: `architect_spec.json` with domain, topic, subtopic, difficulty, learning_objective, prerequisites, core_concept, tags, constraint_hints, story_direction.

Set mode: `set_plan.json` with `set_metadata` + array of N `architect_spec.json` objects, validated against distribution ratios.

## Key Knowledge

- DSA Learning Progression (Levels 0–6)
- Bloom's Taxonomy mapping to CP problem types
- Difficulty calibration (easy/medium/hard/expert → Codeforces rating)
- Constraint-to-complexity table (N range ↔ Big-O)
- Prerequisite chain rules (one new concept per problem)
- Topic clusters and natural combinations

## Prompt File

`prompts/01_problem_architect.md`

## Set Generation Distribution Defaults

| Level | Comfortable | Challenging | Stretch |
|-------|-------------|-------------|---------|
| beginner | 50% | 35% | 15% |
| specialist | 40% | 35% | 25% |
| expert | 30% | 40% | 30% |
| master | 20% | 40% | 40% |
| grandmaster | 15% | 35% | 50% |

See `knowledge/problem_set_distribution_guide.md` for full details.
