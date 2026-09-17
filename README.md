# Hack-Verifiable Environments: Towards Evaluating Reward Hacking at Scale

<p align="center">
  <a href="https://arxiv.org/abs/2605.20744"><img src="https://img.shields.io/badge/arXiv-2605.20744-b31b1b?style=for-the-badge&logo=arxiv&logoColor=white" height="40"/></a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://majoroth.github.io/hack-verifiable-environments/"><img src="https://img.shields.io/badge/Webpage-Online-blue?style=for-the-badge&logo=githubpages&logoColor=white" height="40"/></a>
</p>

---

## Introduction

Hack-Verifiable Environments is a new paradigm for evaluating reward hacking.
This repository contains the original code for the paper, including experiment scripts needed to reproduce the results.
We also release Hack-Verifiable TextArena, a fork of TextArena with a filesystem wrapper for evaluating reward hacking on TextArena environments.

![Demo](docs/video.gif)

---

## Installation

```bash
uv sync
```

Set your API keys in a `.env` file in the project root:

```
OPENAI_API_KEY=...
OPENROUTER_API_KEY=...
```

---

## Hack-Verifiable TextArena

We release [Hack-Verifiable TextArena](https://github.com/MajoRoth/hack-verifiable-environments/tree/main/hvta).
We implemented the filesystem wrapper on top of [TextArena](https://github.com/TextArena/TextArena), which allows us to evaluate reward hacking in a wide range of text-based environments.
We implemented hidden-solution and logical-bug for single-player environments, and read-and-write prompt for two-player environments.


```python
import textarena as ta
from hvta.FilesystemWrapper import FilesystemWrapper

agents = {
    0: ta.agents.HumanAgent(), # ta.agents.OpenRouterAgent(model_name="openai/gpt-5-mini")
}

# initialize the environment
env = ta.make(env_id="Wordle-v0")
env = FilesystemWrapper(env=env, hidden_solution=True, logical_bug=True)
env.reset(num_players=len(agents))

# main game loop
done = False
while not done:
  player_id, observation = env.get_observation()
  action = agents[player_id](observation)
  print(action)
  done, step_info = env.step(action=action)
  if step_info.get("reward_hack"):
    print("[HACK DETECTED 🚨🚨🚨]")

rewards, game_info = env.close()
```

You can use the examples prvovided in `hvta/test_1p.py`, `hvta/test_2p.py` and `hvta/run_hidden_solution_benchmark.py` to get started.

---

## Hack-Verifiable Terminal Bench

We release [Hack-Verifiable Terminal Bench (HVTB)](https://majoroth.github.io/hack-verifiable-environments/hvtb), a benchmark of 89 hack-verifiable terminal tasks for reliably measuring reward hacking of terminal agents.

> ⚠️ **Note:** The Harbor hub view currently does not expose the jobs, so they need to be accessed directly:

| Model | Ablation | L0 | L1 | L2 | L3 |
|---|---|---|---|---|---|
| gpt-5.6-sol | [link](https://hub.harborframework.com/jobs/5a83bf48-30f2-495a-8725-83e85a4d2bf7) | [link](https://hub.harborframework.com/jobs/59ff1d1e-5f6f-431d-92e2-7e4a7429a130) | [link](https://hub.harborframework.com/jobs/8e3ab605-9cc8-40d9-a37f-36cd19d18904) | [link](https://hub.harborframework.com/jobs/688853ba-5104-4acf-b4c2-a6efab9eae7b) | [link](https://hub.harborframework.com/jobs/67263c53-e84c-4a03-a4e6-c9ef737288a4) |
| glm-5.2 | [link](https://hub.harborframework.com/jobs/41999802-e81d-475e-82c3-531c27d7cc87) | [link](https://hub.harborframework.com/jobs/2b1ce716-6154-4b44-a68f-32e209f13dcd) | [link](https://hub.harborframework.com/jobs/ec056ef2-40f7-4b72-8329-07d6941f3777) | [link](https://hub.harborframework.com/jobs/a9e8711c-8585-452f-a552-539fa5c938b9) | [link](https://hub.harborframework.com/jobs/c6be9f38-127d-450b-8c75-e3e6778c5384) |
| kimi-k3 | [link](https://hub.harborframework.com/jobs/52d27bfa-7d52-4654-b3f9-f87dc091dff4) | [link](https://hub.harborframework.com/jobs/45617deb-c410-4aeb-9e0b-ec0628525a0e) | [link](https://hub.harborframework.com/jobs/94d4b319-f979-4540-b30e-3057ab4f2df8) | [link](https://hub.harborframework.com/jobs/dd71ad9f-314c-4806-8665-d97cc944bcf7) | [link](https://hub.harborframework.com/jobs/db407c5f-68ad-468c-922a-b342ad03289c) |
| claude-opus-5 | [link](https://hub.harborframework.com/jobs/19161777-df3f-4232-9906-0f77520e1e98) | [link](https://hub.harborframework.com/jobs/70f69025-3d04-4289-aa62-9eba0eb24c08) | [link](https://hub.harborframework.com/jobs/31690d34-bc55-4e10-9a2e-f0ea3dcfaa52) | [link](https://hub.harborframework.com/jobs/267e792b-1ecf-4ac6-a0c6-ab0ff72352db) | [link](https://hub.harborframework.com/jobs/564c4628-9264-4575-90a4-043e89473d78) |
| gemini-3.1-pro | [link](https://hub.harborframework.com/jobs/5ed558d7-ee40-456f-9697-a791b61648e7) | [link](https://hub.harborframework.com/jobs/6d831c9e-d45a-4a6d-b4b1-38242338103b) | [link](https://hub.harborframework.com/jobs/8d54ad79-c435-4c8f-accd-6ef178e2cd9c) | [link](https://hub.harborframework.com/jobs/9afa629c-8d5b-4230-8b1f-b6c550fa2742) | [link](https://hub.harborframework.com/jobs/b989030e-0e79-4593-be8f-a773d3c58f76) |

---

## Citation

```bibtex
@article{roth2026hack,
  title={Hack-Verifiable Environments: Towards Evaluating Reward Hacking at Scale},
  author={Roth, Amit and Samanta, Ankur and Halevy, Matan and Levine, Yoav and Efroni, Yonathan},
  journal={arXiv preprint arXiv:2605.20744},
  year={2026}
}
```
