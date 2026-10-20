# CLAUDE.md

## What this project is

**Hack-Verifiable Environments (HVE)** is a research paradigm for measuring reward hacking in
AI agents *reliably and at scale*. Instead of detecting hacks post hoc (human review or LLM
judges reading trajectories, both unreliable), we **plant** verifiable hacks (honeypots) into
environments, so any exploitation is flagged deterministically the moment it happens, by
construction rather than by judgment.

Paper: *Hack-Verifiable Environments: Towards Evaluating Reward Hacking at Scale*
(Roth, Samanta, Halevy, Levine, Efroni) — arXiv:2605.20744.

The paradigm has two instantiations:

### 1. HVTA — Hack-Verifiable TextArena (games)

A fork/wrapper of [TextArena](https://github.com/TextArena/TextArena) (text-based games:
Wordle, Tower of Hanoi, Negotiation, …). A **mock filesystem wrapper**
(`hvta/FilesystemWrapper`) adds actions (`ls`, `cat`, `mv`, `write`, `encrypt`, …) on top of
the game and plants bait: hidden solution files, buggy source (logical bug), the opponent's
private prompt. Any read/write of planted content is flagged: `h: O × A → {0,1}`.
21 environments, 4 hack types. Metrics: **Hack Rate** and **Hack-Free Win Rate**.
Key findings: harder tasks → more hacking; hacking is "addictive"
(P(hack | prior hack) >> P(hack)); prompting reduces but never eliminates hacking.

### 2. HVTB — Hack-Verifiable Terminal Bench (real coding agents)

Applies the same principle to **Terminal Bench** (terminal-bench-2-1, 89 community-reviewed
real coding tasks), via the Harbor framework. An `admin/` directory is planted in the agent's
real shell containing the ground-truth solution and held-out tests (simulating an accidental
leak), with a README saying not to explore it. `inotify` filesystem watchers flag every read
or write; the verifier reads the flags after the run. Two hacks: **hidden solution** and
**read tests**. A single script transforms any Harbor-format task into its hack-verifiable
version.

Paper: *Hack-Verifiable Terminal Bench: Evaluating Reward Hacking in Terminal Tasks*
(Roth, Bercovich, Efroni) — arXiv:2608.22103.

Evaluated 5 frontier agents (claude-opus-5, gpt-5.6-sol, gemini-3.1-pro, kimi-k3, glm-5.2)
under 5 prompt settings (Ablation = no instruction; L0–L3 reveal progressively more about the
vulnerability). Headline results: default hack rates 22–48%; a "don't hack" line helps but
never reaches zero; gemini-3.1-pro hacks *more* when warned (59.8% at L0 vs 47.7% ablation);
some hacks are silent (spotless final report, only the watchers see them).

## Repo layout

- `hvta/` — the HVTA filesystem wrapper (Python package). Usage example in root README.
- `examples/` — `test_1p.py`, `test_2p.py`, `run_hidden_solution_benchmark.py`.
- `tests/` — includes hack-onset logging regression tests (community PR #2).
- `docs/` — the **GitHub Pages site** (https://majoroth.github.io/hack-verifiable-environments/):
  - `index.html` — HVE project page (light theme): paper, abstract, authors, HVTA, citation.
  - `hvtb.html` — the HVTB blog post (dark theme), served at the extensionless URL `/hvtb`.
    Fully self-contained: interactive hack-rate figure (hover = bold line + exact rates),
    collapsible "Caught in the act" trace gallery, README expander, citation with copy button.
    Both pages carry a Google Analytics tag (G-D95WGYCY4Q).
- `README.md` — HVE/HVTA intro + an **HVTB section with direct Harbor job links** (the Harbor
  hub currently does not list the jobs on the org page — a Hub visibility bug, see issue #5 —
  so the 25 job links (5 models × 5 settings) live in a table there).

## Git conventions

- Website/blog work historically happened on the `HVTB` branch, then merged into `main`
  (which is what GitHub Pages deploys). The two branches are kept in sync; always
  `git pull --ff-only` before merging — collaborators and other sessions push to `main`.
- Merged community PRs: #1 (Hvtb), #2 (onset logging), #3 (textarena pin).

## External resources

- Blog: https://majoroth.github.io/hack-verifiable-environments/hvtb
- HVE paper: https://arxiv.org/abs/2605.20744 · HVTB paper: https://arxiv.org/abs/2608.22103
- Harbor dataset (environments): https://hub.harborframework.com/datasets/hack-verifiable-environments/hv-terminal-bench-2-1
- Harbor org (jobs/traces, 2,225 traces ≈ $2.5K of agent runs): https://hub.harborframework.com/organizations/hack-verifiable-environments

## Related local projects (outside this repo)

- `~/PycharmProjects/hackable-envs/` — the experiments workbench: `jobs/` holds all raw run
  directories (`hvtb-<model>-<level>/<task>__<id>/` with `agent/trajectory.json` and
  `verifier/reward.json` carrying the hack flags `hidden_solution`/`read_tests`/`modify_tests`),
  `hvtb_analysis/` holds curated findings (`interesting_findings_<model>.md`,
  `INTERESTING_TRACES.md`) and plotting scripts.
- `~/PycharmProjects/hackable-envs/69c39bccd3174d89469b01be/` — Overleaf clone with the HVE
  paper sources, NeurIPS poster, and reveal.js talk decks (`tau-llm-symposium` is the most
  recent with HVTB content; `heron-conf-draft` is the in-progress Heron talk).
- The HVTB paper PDF lives in this repo at `.claude/HVE_Terminal_Bench-5.pdf` (untracked).
