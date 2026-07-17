# Usage Guide

How to use the Agent Skills Problem Gen prompts to generate competitive programming problems with any LLM.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Using with OpenAI (GPT-4)](#using-with-openai-gpt-4)
- [Using with Anthropic (Claude)](#using-with-anthropic-claude)
- [Using with Google (Gemini)](#using-with-google-gemini)
- [Running the Pipeline Manually](#running-the-pipeline-manually)
- [Customizing Parameters](#customizing-parameters)
- [Interpreting the Output](#interpreting-the-output)
- [Tips for Best Results](#tips-for-best-results)

---

## Prerequisites

- An LLM API key (OpenAI, Anthropic, or Google)
- A way to send prompts and receive JSON responses (CLI tool, API client, or playground)
- Familiarity with competitive programming concepts (helpful but not required)

---

## Using with OpenAI (GPT-4)

### Recommended Models
- **GPT-4** (best quality, slower)
- **GPT-4 Turbo** (good balance)
- **GPT-4o** (fastest, good for iteration)

### Setup

```bash
export OPENAI_API_KEY="your-api-key"
```

### Example: Python with OpenAI API

```python
import openai
import json

client = openai.OpenAI()

def run_agent(prompt_file: str, context: dict = None) -> dict:
    """Run a single agent with optional context from previous agents."""
    
    with open(prompt_file) as f:
        system_prompt = f.read()
    
    messages = [{"role": "system", "content": system_prompt}]
    
    if context:
        messages.append({
            "role": "user",
            "content": f"Here is the input from the previous agent:\n{json.dumps(context, indent=2)}"
        })
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,  # See tips section
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

# Run the pipeline
architect_spec = run_agent("prompts/01_problem_architect.md")
problem_draft = run_agent("prompts/02_problem_writer.md", architect_spec)
solution = run_agent("prompts/03_solution_engineer.md", problem_draft)
test_suite = run_agent("prompts/04_test_case_generator.md", {
    "problem_draft": problem_draft,
    "solution": solution
})
review = run_agent("prompts/05_quality_reviewer.md", {
    "architect_spec": architect_spec,
    "problem_draft": problem_draft,
    "solution": solution,
    "test_suite": test_suite
})

if review["verdict"] == "APPROVED":
    editorial = run_agent("prompts/06_editorial_writer.md", {
        "architect_spec": architect_spec,
        "problem_draft": problem_draft,
        "solution": solution,
        "test_suite": test_suite,
        "review": review
    })
else:
    print(f"Quality review failed: {review['specific_feedback']}")
```

### Example: OpenAI CLI

```bash
# Agent 1
cat prompts/01_problem_architect.md | openai chat --model gpt-4 --temperature 0.7 > architect_spec.json

# Agent 2 (pass Agent 1's output as context)
cat prompts/02_problem_writer.md | openai chat --model gpt-4 --temperature 0.7 --system "$(cat architect_spec.json)" > problem_draft.json

# Continue for all agents...
```

---

## Using with Anthropic (Claude)

### Recommended Models
- **Claude 3.5 Sonnet** (best balance)
- **Claude 3 Opus** (highest quality, slower)
- **Claude 3 Haiku** (fastest, good for iteration)

### Setup

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### Example: Python with Anthropic API

```python
import anthropic
import json

client = anthropic.Anthropic()

def run_agent(prompt_file: str, context: dict = None) -> dict:
    """Run a single agent with optional context."""
    
    with open(prompt_file) as f:
        system_prompt = f.read()
    
    user_message = "Generate the output according to your instructions."
    if context:
        user_message = f"Here is the input from the previous agent:\n{json.dumps(context, indent=2)}"
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        temperature=0.7,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    # Extract JSON from response
    content = response.content[0].text
    return json.loads(content)

# Run the pipeline (same sequence as OpenAI example)
architect_spec = run_agent("prompts/01_problem_architect.md")
problem_draft = run_agent("prompts/02_problem_writer.md", architect_spec)
# ... continue through all agents
```

### Notes for Claude
- Claude excels at following complex instructions and maintaining consistency across long contexts
- Use `max_tokens=4096` or higher to ensure complete JSON output
- Claude's JSON output is typically well-formatted and schema-compliant

---

## Using with Google (Gemini)

### Recommended Models
- **Gemini 1.5 Pro** (best quality)
- **Gemini 1.5 Flash** (fastest, good for iteration)

### Setup

```bash
export GOOGLE_API_KEY="your-api-key"
```

### Example: Python with Google Generative AI

```python
import google.generativeai as genai
import json

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def run_agent(prompt_file: str, context: dict = None) -> dict:
    """Run a single agent with optional context."""
    
    with open(prompt_file) as f:
        system_prompt = f.read()
    
    user_message = "Generate the output according to your instructions."
    if context:
        user_message = f"Here is the input from the previous agent:\n{json.dumps(context, indent=2)}"
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_prompt
    )
    
    response = model.generate_content(
        user_message,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            response_mime_type="application/json"
        )
    )
    
    return json.loads(response.text)

# Run the pipeline (same sequence as other providers)
architect_spec = run_agent("prompts/01_problem_architect.md")
problem_draft = run_agent("prompts/02_problem_writer.md", architect_spec)
# ... continue through all agents
```

### Notes for Gemini
- Gemini 1.5 Pro has a large context window, making it suitable for the full pipeline
- Use `response_mime_type="application/json"` to enforce JSON output
- Gemini may occasionally add markdown code fences around JSON — strip them before parsing

---

## Running the Pipeline Manually

If you prefer to run each agent step-by-step (e.g., in a playground or chat interface):

### Step 1: Problem Architect

1. Open `prompts/01_problem_architect.md`
2. Paste it as the **system prompt**
3. Send a user message with your parameters:

```
Generate a problem blueprint with these parameters:
- domain: dsa
- topic: binary_search
- subtopic: binary_search_on_answer
- difficulty_range: 1200-1600
- bloom_target: apply
- target_audience: "competitive programmers preparing for Div. 2 C/D"
```

4. Save the JSON output as `architect_spec.json`

### Step 2: Problem Writer

1. Open `prompts/02_problem_writer.md`
2. Paste it as the **system prompt**
3. Send the `architect_spec.json` as the user message
4. Save the output as `problem_draft.json`

### Step 3: Solution Engineer

1. Open `prompts/03_solution_engineer.md`
2. Paste it as the **system prompt**
3. Send the `problem_draft.json` as the user message
4. Save the output as `solution.json`
5. **Check the solvability gate**: if `solvability_verdict` is `SOLVABILITY_FAILURE`, go back to Step 2 with feedback

### Step 4: Test Case Generator

1. Open `prompts/04_test_case_generator.md`
2. Paste it as the **system prompt**
3. Send both `problem_draft.json` and `solution.json` as the user message
4. Save the output as `test_suite.json`

### Step 5: Quality Reviewer

1. Open `prompts/05_quality_reviewer.md`
2. Paste it as the **system prompt**
3. Send all four JSON files as the user message
4. Save the output as `review_verdict.json`
5. **Check the verdict**: if `REVISION`, route feedback to the appropriate agent and re-run from that point

### Step 6: Editorial Writer

1. Open `prompts/06_editorial_writer.md`
2. Paste it as the **system prompt**
3. Send all five JSON files as the user message
4. Save the output as `editorial.json`

### Step 7: Assembly

Combine all outputs into `final_problem.json` according to the schema in `schemas/final_problem.json`.

---

## Customizing Parameters

### Changing Difficulty

Adjust the `difficulty_range` parameter for Agent 1:

- **Easy (800–1200)**: Direct implementation, single concept
- **Medium (1200–1600)**: Combine 2 concepts, some insight required
- **Hard (1600–2100)**: Multiple concepts, non-obvious approach
- **Very Hard (2100–2600)**: Advanced techniques, significant insight
- **Expert (2600–3500)**: Novel combinations, research-level

### Changing Topic

Update `topic` and `subtopic` to target specific DSA areas:

```
topic: dynamic_programming
subtopic: knapsack_variants
```

See `knowledge/dsa_learning_progression.md` for the full topic hierarchy.

### Changing Domain

The prompts currently focus on DSA/competitive programming. To target a different domain:

1. Update the `domain` enum in `schemas/architect_spec.json`
2. Modify Agent 1's prompt to include domain-specific guidance
3. Add domain-specific knowledge to `knowledge/`

See [docs/extending.md](extending.md) for details.

### Adjusting Bloom's Taxonomy Level

Target different cognitive levels:

- **Remember**: MCQ, syntax questions
- **Understand**: Code tracing, explanation
- **Apply**: Direct implementation (most CP problems)
- **Analyze**: Decompose and choose the right approach
- **Evaluate**: Prove correctness, justify choices
- **Create**: Design novel algorithms

See `knowledge/blooms_taxonomy_mapping.md` for examples.

---

## Interpreting the Output

### `final_problem.json` Structure

#### `metadata`
- `id`: Unique identifier for the problem
- `domain`: Problem domain (dsa, language_learning, etc.)
- `topic`, `subtopic`: DSA topic hierarchy
- `difficulty`: Codeforces rating, tier, Bloom level
- `tags`: CP tags (binary search, dp, graph, etc.)
- `prerequisites`: Required knowledge
- `generated_at`: Timestamp
- `pipeline_rounds`: Number of quality review rounds

#### `problem`
- `title`: Problem name (≤6 words)
- `story`: Context/narrative (2–5 sentences)
- `statement`: Formal problem statement
- `input_format`: Line-by-line input description
- `output_format`: Output description
- `constraints`: Array of constraint strings
- `sample_tests`: 2–5 sample test cases with explanations
- `subtasks` (optional): Subtask definitions with points and constraints

#### `solution`
- `approach`: High-level description
- `pseudocode`: Language-agnostic algorithm
- `time_complexity`, `space_complexity`: Big-O notation
- `correctness_argument`: Formal proof sketch
- `brute_force_solution`: Alternative for cross-verification
- `common_wrong_approaches`: 2–4 incorrect approaches with explanations
- `solvability_verdict`: `success` or `SOLVABILITY_FAILURE`

#### `test_suite`
- `test_cases`: 10+ test cases across 4 categories:
  - `basic`: Sample tests + simple verification
  - `edge_case`: From the edge case taxonomy
  - `adversarial`: Designed to break wrong approaches
  - `boundary`: At constraint extremes
- `stress_test_config`: Random test generation parameters
- `coverage_report`: Edge cases covered, wrong approaches tested

#### `editorial`
- `hints`: 3 progressive hints (direction → approach → key insight)
- `brute_force_explanation`: Why brute force is too slow
- `optimal_solution_walkthrough`: Step-by-step on Sample 1
- `complexity_analysis`: Time/space with constraint verification
- `alternative_approaches`: 0–3 alternatives with trade-offs
- `common_mistakes`: 2–3 mistakes with counterexamples

#### `quality_report`
- `shield_scores`: 10 quality dimensions (0–10 each)
- `sword_findings`: Attack vector results
- `pipeline_rounds`: Number of revision rounds
- `warnings`: Any warnings from forced approval

---

## Tips for Best Results

### Temperature Settings

- **0.5–0.7**: Best for most agents (balance of creativity and consistency)
- **0.3–0.5**: Use for Solution Engineer and Test Case Generator (more deterministic)
- **0.7–0.9**: Use for Problem Architect and Editorial Writer (more creative)

### Model Recommendations

| Agent | Best Model | Good Alternative | Fast Iteration |
|-------|-----------|------------------|----------------|
| Problem Architect | GPT-4 / Claude 3 Opus | Gemini 1.5 Pro | GPT-4o / Haiku |
| Problem Writer | Claude 3.5 Sonnet | GPT-4 | Gemini 1.5 Flash |
| Solution Engineer | GPT-4 / Claude 3 Opus | Gemini 1.5 Pro | GPT-4o |
| Test Case Generator | GPT-4 | Claude 3.5 Sonnet | Gemini 1.5 Flash |
| Quality Reviewer | Claude 3 Opus | GPT-4 | Claude 3.5 Sonnet |
| Editorial Writer | Claude 3.5 Sonnet | GPT-4 | Gemini 1.5 Pro |

### Handling Quality Review Failures

If Agent 5 returns `REVISION`:

1. Read the `specific_feedback` carefully
2. Identify the `revision_target` (problem_writer, solution_engineer, or test_generator)
3. Re-run that agent with the feedback appended to the prompt
4. Continue the pipeline from that point

Example:
```
The quality reviewer found issues with the test coverage. Please regenerate the test suite with this feedback:
"Add more adversarial tests targeting the greedy approach that sorts by value/weight ratio."
```

### Ensuring JSON Compliance

- Use `response_format={"type": "json_object"}` (OpenAI) or equivalent
- Set `max_tokens` high enough (4096+) to avoid truncation
- Validate output against schemas in `schemas/` before passing to the next agent
- If JSON parsing fails, retry with a lower temperature

### Debugging Pipeline Issues

- **Agent produces invalid JSON**: Lower temperature, add explicit JSON instructions
- **Solvability failure**: The problem may be too hard or ill-defined; adjust parameters
- **Quality review fails repeatedly**: Check if the topic is too niche or the difficulty is misaligned
- **Schema violations**: Validate intermediate outputs against `schemas/*.json`

---

## Next Steps

- See [docs/extending.md](extending.md) to add new agents, domains, or examples
- Browse [examples/](../examples/) for complete pipeline traces
- Review [knowledge/](../knowledge/) for DSA pedagogy reference material
