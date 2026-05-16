# Hack-Verifiable Environments: Towards Evaluating Reward Hacking at Scale


[![Paper](https://img.shields.io/badge/Paper-PDF-red)](https://arxiv.org/)
[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b)](https://arxiv.org/)
[![Webpage](https://img.shields.io/badge/Webpage-Online-blue)](https://majoroth.github.io/hack-verifiable-environments/)
[![Hack-Verifiable TextArena](https://img.shields.io/badge/Hack--Verifiable%20TextArena-Code-green)](https://github.com/)

---

## Introduction

Hack-Verifiable Environments is a new paradigm for evaluating reward hacking.
This repository contains the original code for the paper, including all experiment scripts needed to reproduce the results.
We also release Hack-Verifiable TextArena, a fork of TextArena with a filesystem wrapper for evaluating reward hacking on TextArena environments.

![Main Figure](docs/main_figure_no_border.png)

---

## Hack-Verifiable TextArena

We release [Hack-Verifiable TextArena](https://github.com/MajoRoth/hack-verifiable-environments/hvta).
We implemented the filesystem wrapper on top of [TextArena](https://github.com/TextArena/TextArena), which allows us to evaluate reward hacking in a wide range of text-based environments.
We implemented hidden-solution and logical-bug for single-player environments, and read-and-write prompt for two-player environments.

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
