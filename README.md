# Hack-Verifiable Environments: Towards Evaluating Reward Hacking at Scale

<p align="center">
  <a href="https://arxiv.org/">
    <img src="https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b?style=for-the-badge&logo=arxiv&logoColor=white" height="40"/>
  </a>
  &nbsp;&nbsp;
  <a href="https://majoroth.github.io/hack-verifiable-environments/">
    <img src="https://img.shields.io/badge/Webpage-Online-blue?style=for-the-badge&logo=githubpages&logoColor=white" height="40"/>
  </a>
</p>

---

## Introduction

Hack-Verifiable Environments is a new paradigm for evaluating reward hacking.
This repository contains the original code for the paper, including all experiment scripts needed to reproduce the results.
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

## Citation

```bibtex
@article{authorone2025hack,
  title   = {Hack-Verifiable Environments: Towards Evaluating Reward Hacking at Scale},
  author  = {Amit Roth and Ankur Samanta and Matan Halevy and Yoav Levin and Yonathan Efroni},
  journal = {arXiv preprint arXiv:XXXX.XXXXX},
  year    = {2025}
}
```
