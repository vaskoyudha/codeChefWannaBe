# Problem Set Distribution Guide

> Defines how to generate balanced problem sets at each skill level, with ideal difficulty distributions, topic coverage rules, and set templates.

---

## Skill Levels & Rating Bands

Each level maps to a Codeforces rating band and a competitive programming stage.

| Level | Name | Codeforces Rating | Typical Solver |
|-------|------|-------------------|----------------|
| **Beginner** | Newbie → Pupil | 800–1200 | Learning basic data structures, control flow, simple algorithms |
| **Specialist** | Pupil → Specialist | 1300–1600 | Comfortable with standard algorithms, learning to combine techniques |
| **Expert** | Specialist → Expert | 1700–2100 | Strong algorithmic toolkit, solving requires analysis and insight |
| **Master** | Expert → Master | 2200–2600 | Advanced techniques, creative problem-solving, novel combinations |
| **Grandmaster** | Master → GM | 2600+ | Research-level insight, ad-hoc brilliance, technique fusion |

---

## Difficulty Distribution Model

Each problem set contains problems at three relative difficulty levels:

| Category | Meaning | Description |
|----------|---------|-------------|
| **Comfortable** | Solver should be able to solve this | Tests known techniques at the solver's level. Approach is clear or requires minor insight. Builds confidence and reinforces fundamentals. |
| **Challenging** | Solver needs to think but can solve it | Requires combining 2+ techniques, recognizing a non-obvious pattern, or applying a known technique in an unfamiliar context. The growth zone. |
| **Stretch** | Solver should struggle but learn from attempting | Pushes beyond current level. May require a technique from the next level up, or a creative insight. Even failing to solve teaches valuable lessons. |

### Ideal Distribution Ratios by Level

| Level | Comfortable | Challenging | Stretch | Rationale |
|-------|-------------|-------------|---------|-----------|
| **Beginner** (800–1200) | 50% | 35% | 15% | Beginners need confidence. Heavy comfortable ratio reinforces fundamentals. Small stretch exposure builds aspiration. |
| **Specialist** (1300–1600) | 40% | 35% | 25% | Balanced. Comfortable maintains speed, challenging drives growth, stretch introduces next-level thinking. |
| **Expert** (1700–2100) | 30% | 40% | 30% | Challenging-heavy. Expert solvers need problems that require analysis, not just implementation. Comfortable problems are warm-ups. |
| **Master** (2200–2600) | 20% | 40% | 40% | Stretch-heavy. At this level, growth comes from solving problems that require creative insight. Comfortable problems are rare. |
| **Grandmaster** (2600+) | 15% | 35% | 50% | Almost all problems are challenging or stretch. Comfortable problems only as openers. |

### Visual Distribution

```
Beginner:    ████████████░░░░░░░░████░░░░  (50/35/15)
Specialist:  ██████████░░░░░░░░████████░░  (40/35/25)
Expert:      ███████░░░░░░░████████░░░░░░  (30/40/30)
Master:      █████░░░░░░░░░██████████████  (20/40/40)
Grandmaster: ███░░░░░░░░░░███████████████  (15/35/50)
             ├─ Comfortable ─┤├─ Challenging ─┤├─ Stretch ─┤
```

---

## Topic Coverage Rules

### Topic Diversity

A well-balanced problem set should cover **multiple DSA topics**, not just one. The exact mix depends on the level:

| Level | Topic Focus | Rule |
|-------|-------------|------|
| **Beginner** | 1–2 core topics per set | Focus on fundamentals. A set can be themed around one topic (e.g., "arrays + strings") with slight variation. |
| **Specialist** | 2–3 topics per set | Mix familiar topics with one new area. E.g., "binary search + greedy + basic DP." |
| **Expert** | 3–4 topics per set | Broad coverage. Include at least one cross-topic problem that combines techniques. |
| **Master** | 3–5 topics per set | Wide range with deep problems. Expect technique fusion across domains. |
| **Grandmaster** | 4+ topics per set | Full spectrum. Problems often combine 2+ advanced topics in novel ways. |

### Topic Rotation

When generating multiple sets at the same level, rotate topics to ensure coverage over time:

**Core topic groups** (ensure each set touches at least 2 different groups):

1. **Foundations:** arrays, strings, sorting, searching, implementation
2. **Data Structures:** stacks, queues, heaps, hash maps, trees, DSU
3. **Algorithms:** greedy, binary search, divide & conquer, backtracking
4. **Dynamic Programming:** 1D DP, 2D DP, knapsack, LIS, bitmask DP
5. **Graphs:** BFS, DFS, shortest paths, MST, topological sort
6. **Advanced:** segment trees, Fenwick trees, string algorithms, number theory, geometry, flows

### Bloom's Level Distribution

| Level | Remember/Understand | Apply | Analyze | Evaluate/Create |
|-------|---------------------|-------|---------|-----------------|
| Beginner | 10% | 60% | 25% | 5% |
| Specialist | 0% | 40% | 50% | 10% |
| Expert | 0% | 20% | 55% | 25% |
| Master | 0% | 10% | 40% | 50% |
| Grandmaster | 0% | 5% | 30% | 65% |

---

## Set Size Templates

### Contest-Style Sets

| Set Name | Problems | Duration | Use Case |
|----------|----------|----------|----------|
| **Mini Contest** | 3–4 | 1.5–2 hours | Quick practice, speed training |
| **Standard Contest** | 5–7 | 2–2.5 hours | Full contest simulation |
| **Extended Contest** | 8–10 | 3–4 hours | Marathon practice |
| **Training Camp Session** | 10–15 | 4–5 hours | Deep practice with review |

### Themed Sets

| Set Name | Problems | Focus | Use Case |
|----------|----------|-------|----------|
| **Topic Deep-Dive** | 4–6 | Single topic, escalating difficulty | Master one concept |
| **Technique Fusion** | 3–5 | Cross-topic combinations | Learn to combine techniques |
| **Speed Round** | 5–8 | All comfortable/challenging | Build solving speed |
| **Gauntlet** | 5–7 | All challenging/stretch | Push limits |

---

## Problem Ordering Within a Set

Problems within a set should follow a **difficulty ramp**:

1. **Opener** (Comfortable): Easy entry point. Builds confidence. Tests one core concept.
2. **Early problems** (Comfortable → Challenging): Gradual step-up. Introduce the set's themes.
3. **Mid problems** (Challenging): The core of the set. Require insight, technique combination.
4. **Late problems** (Challenging → Stretch): Hardest problems. Require deep analysis or creative insight.
5. **Closer** (Stretch): The final boss. Often the most creative or technically demanding.

**Ordering rules:**
- Never place two stretch problems consecutively (solver fatigue).
- Alternate topics when possible (don't put 3 graph problems in a row).
- The first problem should be solvable in ≤15 minutes by the target solver.
- The last problem should take 45–90 minutes for the target solver (even if they don't solve it).

---

## Distribution Validation Checklist

After generating a problem set, verify:

- [ ] The comfortable/challenging/stretch ratio matches the target level's distribution (±5% tolerance)
- [ ] At least 2 different topic groups are represented
- [ ] Problems are ordered by difficulty (opener → closer)
- [ ] No two consecutive problems share the same primary technique
- [ ] Bloom's level distribution matches the level's profile
- [ ] Prerequisites form a logical progression (earlier problems' concepts help with later ones)
- [ ] At least one problem requires cross-topic thinking
- [ ] The set has a clear narrative arc (easy start → challenging middle → hard finish)

---

## Example: Specialist Set (1300–1600), 5 Problems

**Target distribution:** 40% comfortable (2), 35% challenging (2), 25% stretch (1)

| # | Category | Rating | Topic | Bloom | Description |
|---|----------|--------|-------|-------|-------------|
| A | Comfortable | 1300 | arrays, implementation | Apply | Direct application of prefix sums |
| B | Comfortable | 1350 | strings, hashing | Apply | String comparison with rolling hash |
| C | Challenging | 1450 | binary search, greedy | Analyze | Binary search on answer with feasibility check |
| D | Challenging | 1550 | graphs, BFS | Analyze | BFS with state augmentation |
| E | Stretch | 1700 | DP, graphs | Evaluate | DP on DAG with optimization insight |

**Distribution check:** 2/5 comfortable (40%), 2/5 challenging (40%), 1/5 stretch (20%) — within ±5% tolerance.

**Topic coverage:** Foundations (arrays, strings), Algorithms (binary search, greedy), Graphs (BFS), DP — 4 different groups.

---

## How to Use This Guide

### Input Format for Set Generation

When requesting a problem set, specify:

```json
{
  "mode": "set",
  "level": "specialist",
  "set_size": 5,
  "distribution": {
    "comfortable": 0.40,
    "challenging": 0.35,
    "stretch": 0.25
  },
  "topic_preferences": ["graphs", "binary search"],
  "topic_groups_required": 3,
  "ordering": "difficulty_ramp"
}
```

### Defaults

If no distribution is specified, use the level's ideal ratio from the table above.
If no set_size is specified, default to 5 (standard mini-contest).
If no topic_preferences are specified, ensure coverage across at least 3 topic groups.
