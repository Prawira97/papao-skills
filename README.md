# Papao Skills

A collection of **288 agent skills** — the working skill library of Papao, a personal AI agent. It covers design (typography, color, layout, motion, accessibility), SEO (technical SEO, research, link building, content), bug bounty and security auditing, make.fun contests, crypto trading and wallets, and general agent workflows (planning, self-improvement, skill curation).

## Install

Clone this repo, then copy any skill folder into your agent's skills directory — for example:

```bash
git clone https://github.com/Prawira97/papao-skills.git
cp -r papao-skills/skills/<skill-name> ~/.claude/skills/
```

Each skill is a folder containing a `SKILL.md` (the instructions the agent reads) plus any reference files, scripts, or assets it needs. Pick only the skills you want; you do not need all 288.

## Contents

- **88 design skills** — curated from topinspo.design (Taste, Review, Typography, Color, Layout, Motion, Effects, Accessibility)
- **SEO** — 30 open-source skills from Illyism/seo-skills (technical SEO, Ahrefs/DataForSEO research, AI search/GEO, link building, directories, content, copywriting)
- **Security & bug bounty** — web/API attack playbooks, smart-contract auditing, bug-bounty hunting and reporting
- **make.fun** — contest entry, submission, rank watching, and verification skills
- **Trading & wallets** — memecoin trading, copy-trading, EVM/Solana wallets, WalletConnect
- **Agent skills** — SPIDER-style coordination, self-improvement, skill curation, problem solving

See [SOURCES.md](SOURCES.md) for the per-skill source and license.

## Licenses

Each skill keeps its original author's license. This collection mixes skills written by Papao with third-party open-source skills. License summary across the 288 skills:

- MIT: 132
- Apache-2.0: 5
- CC-BY-4.0: 2
- Kubai Icons License (source-available): 1
- Unknown (no license recorded): 148

Skills listed as **Unknown** in SOURCES.md have no license file or license field in the library, or their source repository declares no license. If you reuse one, check its source repository first. Skills written by Papao himself are unlicensed in this snapshot — no license has been chosen for them yet.

## Notes

- The library was scanned before publishing: it contains no API keys, private keys, seed phrases, or other credentials. Some skills describe security testing techniques — they are for authorized bug bounty, audit, and research work only.
- Some Binance skills are hardened versions: live-trading code was removed (dry-run / read-only), and the on-chain-pay skill carries a hard gate that blocks credential use until its operator is confirmed by Binance.
- `impeccable` downloads its engine binary (v0.1.27) from the author's own GitHub releases on first run, checksum-verified. `anti-slop` runs the published npm package `@gessobuild/anti-slop@0.4.3` (pinned).
