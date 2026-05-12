# Hack-Verifiable Environments: Towards Evaluating Reward Hacking at Scale

**Official repository for the paper.**

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](https://arxiv.org/)
[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b)](https://arxiv.org/)
[![Webpage](https://img.shields.io/badge/Webpage-Online-blue)](https://majorroth.github.io/hack-verifiable-environments/)
[![TextArena](https://img.shields.io/badge/TextArena-Code-green)](https://github.com/)

---

## Abstract

Aligning autonomous agents with human intent remains a central challenge in modern AI. A key manifestation of this challenge is reward hacking, whereby agents appear successful under the evaluation signal while violating the intended objective. Reward hacking has been observed across a wide range of settings, yet methods for reliably measuring it at scale remain lacking. In this work, we introduce a new evaluation paradigm for measuring reward hacking. Whereas prior studies have primarily analyzed it post hoc by inspecting agent trajectories, we instead embed detectable reward hacking opportunities directly into environments. This makes their exploitation verifiable by design, enabling deterministic and automated measurement of whether and how agents exploit such vulnerabilities. We instantiate this approach in TextArena and release Hack-Verifiable TextArena, a testbed in which reward hacking can be measured reliably. Using this benchmark, we analyze reward hacking behavior across language models in diverse environments and settings.

---

![Main Figure](docs/main_figure_no_border.png)

---

## Hack-Verifiable TextArena

We release **Hack-Verifiable TextArena**, a set of reward hacking environments built on top of [TextArena](https://github.com/). The forked code with all hack-verifiable environments is available here:

👉 **[Hack-Verifiable TextArena Code](https://github.com/)**

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
