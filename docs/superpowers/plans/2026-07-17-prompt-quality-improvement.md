# System Prompt Quality Improvement Plan

> **Goal:** Upgrade all 7 system prompts with battle-tested patterns from the Superpowers framework to make them more robust, reliable, and resistant to agent rationalization.

**Target Quality:** 9.0+/10 (currently 7.4/10)

---

## Priority Improvements (by impact)

### 🔴 Critical (Must Fix)

#### 1. Add Iron Laws to Each Agent
**Problem:** No single non-negotiable rule anchors each agent's behavior.
**Fix:** Add one Iron Law per agent — a code-block rule that cannot be violated.

| Agent | Iron Law |
|-------|----------|
| Architect | `NO PROBLEM DESIGN WITHOUT A CLEAR LEARNING OBJECTIVE` |
| Writer | `NO PROBLEM STATEMENT WITHOUT RUNNING THE ANTI-AMBIGUITY CHECKLIST` |
| Solution Engineer | `NO OUTPUT WITHOUT SOLVING THE PROBLEM FIRST — IF UNSOLVABLE, OUTPUT SOLVABILITY_FAILURE` |
| Test Generator | `NO TEST SUITE WITHOUT COVERING ALL WRONG APPROACHES FROM THE SOLUTION` |
| Quality Reviewer | `NO APPROVAL WITHOUT SCORING ALL 10 SHIELD CRITERIA — MISSING ONE IS A FAILURE` |
| Editorial Writer | `NO EDITORIAL WITHOUT A BRUTE-FORCE → OPTIMAL PROGRESSION` |
| Orchestrator | `NO PROCEEDING PAST A GATE WITHOUT EXPLICIT VERIFICATION` |

#### 2. Add Anti-Rationalization Tables
**Problem:** Agents can negotiate their way out of rules under pressure.
**Fix:** Add excuse→reality tables to each agent.

**Example for Solution Engineer:**
```markdown
## Common Rationalizations
| Excuse | Reality |
|--------|---------|
| "The problem looks solvable, I'll skip the proof" | Looks ≠ is. Write the proof. |
| "I'll describe the approach without pseudocode" | Pseudocode is the proof. Write it. |
| "The constraints are clearly fine" | Verify: does N=10^5 force O(N log N)? Check. |
| "This edge case is too obscure" | If you can think of it, a solver will too. Test it. |
| "I'm fairly confident this is correct" | Confidence ≠ correctness. Prove it. |
```

#### 3. Add Hard Gates with XML Tags
**Problem:** Rules are suggestions, not mandates.
**Fix:** Use `<HARD-GATE>` tags for unbreakable rules.

**Example for Quality Reviewer:**
```markdown
<HARD-GATE>
You MUST score ALL 10 Shield criteria. Missing even one is a failure.
You MUST output the verdict as valid JSON. No exceptions.
If ANY Shield score is below 8, the verdict MUST be REVISION.
You CANNOT approve a problem you haven't tried to break.
</HARD-GATE>
```

---

### 🟡 Important (Should Fix)

#### 4. Add Red Flags Self-Check Lists
**Problem:** Agents don't know when to STOP and reconsider.
**Fix:** Add "Red Flags" lists that trigger self-correction.

**Example for Problem Writer:**
```markdown
## Red Flags — STOP if you catch yourself thinking:
- "The statement is clear enough" → Re-read it. Is indexing specified?
- "I'll skip the edge case sample" → Add it. Every problem needs N=1 test.
- "The constraints look fine" → Verify: does N force the intended complexity?
- "This is just a small ambiguity" → Ambiguity is a bug. Fix it.
- "The story is optional" → Story motivates the algorithm. Write it.
```

#### 5. Add Good/Bad Example Pairs
**Problem:** Only showing what TO do, not what NOT to do.
**Fix:** Add `<Good>` / `<Bad>` tagged examples.

**Example for Test Generator:**
```markdown
<Bad>
{"id": "tc_1", "category": "basic", "input": "5 3\n1 2 3 4 5", "expected_output": "3"}
// No explanation of what this tests
</Bad>

<Good>
{"id": "tc_1", "category": "basic", "input": "5 3\n1 2 3 4 5", "expected_output": "3",
 "purpose": "Sample test — verifies basic binary search on answer mechanics"}
// Clear purpose, explains what is being verified
</Good>
```

#### 6. Add Escalation Protocols
**Problem:** Agents can't say "I'm stuck" without penalty.
**Fix:** Add explicit escalation paths.

```markdown
## Escalation Protocol
If you are unsure or stuck, output:
{
  "status": "NEEDS_CONTEXT",
  "what_i_need": "Specific description of missing information",
  "confidence": 0.3
}

It is ALWAYS OK to ask for help. Bad output is worse than no output.
```

---

### 🟢 Nice to Have

#### 7. Add Evidence-Before-Claims Enforcement
**Problem:** Agents claim things without verification.
**Fix:** Force agents to show their work.

**Example for Solution Engineer:**
```markdown
<EXTREMELY-IMPORTANT>
You MUST show your complexity derivation step-by-step.
DO NOT just state "O(N log N)" — show WHY:
- Sorting: O(N log N)
- Binary search: O(log N) iterations
- Each iteration: O(N) feasibility check
- Total: O(N log N) + O(N log N) = O(N log N)
</EXTREMELY-IMPORTANT>
```

#### 8. Add Phase-Gated Checklists
**Problem:** Agents can skip steps in multi-step processes.
**Fix:** Add mandatory checklists with checkboxes.

**Example for Problem Writer:**
```markdown
## Mandatory Checklist (complete in order)
- [ ] Read architect_spec completely
- [ ] Identify the core concept to teach
- [ ] Design story/scenario that motivates the algorithm
- [ ] Write problem statement with precise language
- [ ] Define input format (line by line)
- [ ] Define output format (exact specification)
- [ ] Set constraints (from architect's constraint_hints)
- [ ] Create sample tests (3-5, each with specific purpose)
- [ ] Run anti-ambiguity checklist (all 8 items)
- [ ] Add notes/clarifications
- [ ] Verify output matches problem_draft.json schema
```

#### 9. Add Model Selection Guidance
**Problem:** No guidance on which LLM tier to use.
**Fix:** Add recommendations.

```markdown
## Model Recommendations
- **Best results:** GPT-4, Claude 3.5 Sonnet, Gemini 1.5 Pro
- **Acceptable:** GPT-3.5-turbo, Claude 3 Haiku (may need more retries)
- **Not recommended:** Smaller models (< 7B parameters) — insufficient reasoning
```

---

## Implementation Plan

### Phase 1: Critical Fixes (Tasks 1-7)
Add Iron Laws, anti-rationalization tables, and hard gates to all 7 prompts.

| Task | Agent | Changes |
|------|-------|---------|
| 1 | Problem Architect | Add Iron Law + rationalization table + hard gate |
| 2 | Problem Writer | Add Iron Law + rationalization table + hard gate |
| 3 | Solution Engineer | Add Iron Law + rationalization table + hard gate |
| 4 | Test Generator | Add Iron Law + rationalization table + hard gate |
| 5 | Quality Reviewer | Add Iron Law + rationalization table + hard gate |
| 6 | Editorial Writer | Add Iron Law + rationalization table + hard gate |
| 7 | Orchestrator | Add Iron Law + rationalization table + hard gate |

### Phase 2: Important Fixes (Tasks 8-14)
Add red flags, good/bad examples, and escalation protocols.

| Task | Agent | Changes |
|------|-------|---------|
| 8 | Problem Architect | Add red flags + escalation protocol |
| 9 | Problem Writer | Add red flags + good/bad examples + escalation |
| 10 | Solution Engineer | Add red flags + good/bad examples + escalation |
| 11 | Test Generator | Add red flags + good/bad examples + escalation |
| 12 | Quality Reviewer | Add red flags + good/bad examples + escalation |
| 13 | Editorial Writer | Add red flags + good/bad examples + escalation |
| 14 | Orchestrator | Add red flags + escalation protocol |

### Phase 3: Polish (Tasks 15-16)
Add evidence enforcement, phase-gated checklists, model guidance.

| Task | Scope | Changes |
|------|-------|---------|
| 15 | All agents | Add evidence-before-claims enforcement |
| 16 | All agents | Add phase-gated checklists + model recommendations |

---

## Expected Quality Improvement

| Dimension | Before | After |
|-----------|--------|-------|
| Anti-rationalization | 3/10 | 9/10 |
| Hard gates | 4/10 | 9/10 |
| Error handling | 6/10 | 9/10 |
| Few-shot examples | 7/10 | 9/10 |
| **Overall** | **7.4/10** | **9.0+/10** |

---

## Success Criteria

After implementation, each prompt must have:
- [ ] One Iron Law (code block, non-negotiable)
- [ ] Anti-rationalization table (5+ excuse→reality pairs)
- [ ] At least one `<HARD-GATE>` tag
- [ ] Red flags list (5+ stop triggers)
- [ ] At least one `<Good>` / `<Bad>` example pair
- [ ] Escalation protocol (NEEDS_CONTEXT output format)
- [ ] Evidence-before-claims enforcement
- [ ] Phase-gated checklist with checkboxes
