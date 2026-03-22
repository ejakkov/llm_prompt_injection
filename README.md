# LLM prompt injection - experimental playground

Educational / research codebase for exploring prompt injection attacks and defences against a simple “history Q&A” chatbot. It runs automated experiments: combinations of intentions (attack goals), injection templates, and defences, then records model responses and success metrics.

It was developed for the bachelor thesis research *[Prompt Injection Vulnerabilities in Large Language Models and Their Mitigation Strategies](https://nda.rtu.lv/lv/view/43864)* at Riga Technical University.

## Configuration

Create a `config.json` file in the project root (it is gitignored). Include the API keys for the providers you use:

- `openai_key` - OpenAI (GPT family)
- `anthropic_key` - Anthropic (Claude)

Example structure:

```json
{
  "openai_key": "sk-...",
  "anthropic_key": "sk-ant-..."
}
```

Models used in the thesis experiments: `gpt-3.5-turbo`, `gpt-4o`, `claude-3-haiku`, and `claude-3-opus` (exact API model IDs may include a version suffix depending on the provider).

## Streamlit GUI (optional)

![Streamlit playground UI](streamlit_screenshot.png)

Install Streamlit, then from the project root:

```bash
pip install streamlit
streamlit run streamlit_app.py
```

Choose an intention, injection template, defence, and model, then run a single call. Requires `config.json` as in the Configuration section above.

## Running the benchmark

Requires `config.json` as in the Configuration section above. From the project root:

```bash
python main.py
```

Optional first argument: model name (passed through to the experiment), for example:

```bash
python main.py gpt-4o
python main.py claude-3-haiku-20240307
```

The script:

- Iterates over intentions (e.g. content manipulation vs. illegal-information-style prompts).
- For each prompt injection method, runs the chatbot against each defence several times (`try_times` in `main.py`).
- Writes JSON under `results/<timestamp>/` and logs under `logs/`.

## How the code is organized


| Area                | Role                                                                                                 |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| `intention/`        | Attack goal: what “success” means and `validate(response)` for automation.                       |
| `prompt_injection/` | Templates that wrap the intention string into a full user message (`build_prompt`).              |
| `defence/`          | System prompts and extra behaviour (few-shot, encoding, tagging, etc.).                          |
| `chatbot.py`        | Builds the final user message (including defence-specific preprocessing) and calls OpenAI or Claude. |
| `main.py`           | Wires lists of intentions, injections, and defences; runs the matrix and saves results.              |
| `util/`             | API helpers, encoding/sanitization, optional plotting and tables.                                    |


## Results and logs

- `results/` - Per-run JSON with fields such as injection success, defence name, prompts, responses, token usage, and timing.
- `logs/`- Per-injection log files and `demo.log` from the logger configuration in `main.py`.

## Optional: plots and tables

If dependencies are installed, you can adapt `util/show_plot_util.py` and `util/table.py` to aggregate JSON outputs and build figures or summary tables for a thesis or report.

## Key findings (thesis experiments)

Summary of the empirical results reported in the thesis (957 benchmark-style test cases across models and defences). Percentages are *attack success rate* (share of attempts that met the automated success criteria).

### Baseline - no extra defence

*33 injection templates × 3 runs per template.*

Output-manipulation intention (e.g. override app behaviour / change the answer):


| Model                     | Successful attacks | Rate  |
| ------------------------- | ------------------ | ----- |
| `gpt-3.5-turbo`           | 26 / 33            | 78.8% |
| `gpt-4o`                  | 11 / 33            | 33.3% |
| `claude-3-haiku-20240307` | 26 / 33            | 78.8% |
| `claude-3-opus-20240229`  | 10 / 33            | 30.1% |


Smaller / cheaper models align with much higher success than flagship ones (~50 percentage points gap). Even the best baseline still admits more than 30% successful attempts.

Forbidden-information style intention (policy / filter bypass):


| Model                     | Successful attacks | Rate |
| ------------------------- | ------------------ | ---- |
| `gpt-3.5-turbo`           | 2 / 33             | 6.1% |
| `gpt-4o`                  | 0 / 33             | 0.0% |
| `claude-3-haiku-20240307` | 0 / 33             | 0.0% |
| `claude-3-opus-20240229`  | 0 / 33             | 0.0% |


Outcome depends strongly on attack goal: RLHF / filters block this class far more often than simple output manipulation.

### Focused run - `Jailbreak2` on `gpt-3.5-turbo` (forbidden-information goal)

*3 attempts per defence configuration.*


| Defence         | Successful attacks | Rate   |
| --------------- | ------------------ | ------ |
| *(none)*        | 3 / 3              | 100.0% |
| BasicDefence    | 0 / 3              | 0.0%   |
| Encoding        | 0 / 3              | 0.0% † |
| FewShotLearning | 0 / 3              | 0.0%   |
| Tagging         | 3 / 3              | 100.0% |
| DataMarking     | 1 / 3              | 33.3%  |
| Paraphrasing    | 0 / 3              | 0.0%   |
| LLMPiDetection  | 0 / 3              | 0.0%   |


† Encoding blocked attacks but hurt answer quality badly.

### Output-manipulation intention - mean defence lift (all four models)

Average improvement in blocked attacks vs. the same model’s baseline (thesis Table 4.14):


| Defence         | Mean improvement |
| --------------- | ---------------- |
| LLMPiDetection  | +55.3%           |
| Paraphrasing    | +37.1%           |
| DataMarking     | +17.4%           |
| Encoding        | +17.1%           |
| BasicDefence    | +14.4%           |
| Tagging         | +12.8%           |
| FewShotLearning | +10.6%           |


LLMPiDetection achieved 0 / 33 successful attacks on every model (full block in that sweep) at roughly 15–20% extra compute. Paraphrasing was second by mean lift; latency and cost rose about 2–3×. Other methods helped less on average and were model-dependent (for example few-shot or datamarking sometimes worsened weaker models; tagging could leak delimiter hints).

### Takeaways

- Prefer newer, capable models when possible; add defence-in-depth - prompting alone is not enough for high assurance.
- Trade-offs: lighter prompt-engineering defences are cheaper but need maintenance; external-LLM checks and paraphrasing are stronger but cost latency and money.
- Metrics are approximate: outputs are stochastic; “aligned / unaligned” style prompts needed manual review on top of automation.

## Limitations

- Success detection is heuristic (e.g. keyword checks, refusal phrase lists). Treat metrics as approximate unless you add a separate evaluation protocol.
- Some defence branches in `chatbot.py` (e.g. input sanitization) are only active if a matching defence object is used; align `DEFENCES_LIST` in `main.py` with what you want to measure.
- As of 2026, the threat and model landscape keeps moving. New models should be re-tested, and new attacks and defences should be added or refreshed as the field evolves. This repo is a snapshot; ongoing maintenance (dependencies, API behaviour, and experiment lists) is required for results to stay meaningful.

