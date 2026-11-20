---
name: binance
description: Use binance-cli for Binance Spot, Futures (USD-S), and Convert. Requires auth.
metadata:
  version: 2.1.0
  author: Binance
  openclaw:
    requires:
      bins:
        - binance-cli
    # MODIFIKASI KEAMANAN (Papao, 2026-11-19): blok `install:` (curl | sh
    # remote installer) DIHAPUS dari frontmatter ini. Jangan kembalikan.
    # Instalasi binance-cli HANYA manual: unduh installer release dengan versi
    # yang di-pin (bukan `latest`), BACA seluruh isinya, baru jalankan — atau
    # install `@binance/binance-cli` via npm dengan versi di-pin. Lihat
    # "binance-cli setup" di bawah.
license: MIT
---

## MODIFIKASI KEAMANAN (Papao, 2026-11-19)

**Yang diubah:**
- Dihapus: instruksi installer `curl …/binance-cli-installer.sh | sh` dari frontmatter `openclaw.install` dan dari langkah setup. Diganti: unduh installer release dengan versi yang di-pin (bukan `latest`), BACA seluruh isinya sampai paham, baru jalankan; atau install `@binance/binance-cli` via npm dengan versi di-pin.
- Dihapus/dilarang: escape hatch `binance-cli request <url> [--signed]` untuk endpoint arbitrer. Hanya endpoint yang tercantum di skill ini yang boleh dipakai.
- Dipertahankan: aturan CONFIRM (user mengetik `CONFIRM`) untuk semua transaksi produksi.

**Kenapa:** installer `curl | sh` mengeksekusi kode jarak jauh yang tidak ada di repo ini dan tidak teraudit; escape hatch memungkinkan request terautentikasi ke endpoint mana saja.

**Risiko sisa:** `binance-cli` itu sendiri (binary + installer release) tidak teraudit di sini — kepercayaannya bergantung pada rilis resmi Binance dan pada pemeriksaan manual isi installer sebelum dijalankan. Skill ini tetap bisa memindahkan dana (spot/futures/margin/pay/dll) — selalu minta konfirmasi eksplisit sebelum eksekusi.

# Binance

## binance-cli setup

Before using `binance-cli`:

1. If global npm package `@binance/binance-cli` exists and `binance-cli --version` is `< 2.0.0`, uninstall it:

```sh
npm uninstall -g @binance/binance-cli
```

2. Install a PINNED release — never `latest`, and never pipe a remote script to `sh` unseen:

```sh
# 1. Pick an exact version from the releases page and verify it exists:
#    https://github.com/binance/binance-cli/releases
#    (ganti v2.0.0 di bawah dengan versi yang sudah kamu verifikasi)
# 2. Download the installer for that exact version:
curl --proto '=https' --tlsv1.2 -LsSf -o /tmp/binance-cli-installer.sh \
  https://github.com/binance/binance-cli/releases/download/v2.0.0/binance-cli-installer.sh
# 3. READ the whole script and understand what it does before running it:
less /tmp/binance-cli-installer.sh
# 4. Only then run it:
sh /tmp/binance-cli-installer.sh
```

Or install the npm package at a pinned version instead:

```sh
npm install -g @binance/binance-cli@2.0.0
```

3. Verify:

```sh
binance-cli --version
```


> **PREREQUISITE:** Read [`auth.md`](./references/auth.md) for auth, global flags, and security rules.

## Helper Commands

| Command | Description |
|---------|-------------|
| [`algo`](./references/algo.md) | Algo Trading |
| [`alpha`](./references/alpha.md) | Alpha |
| [`c2c`](./references/c2c.md) | C2C |
| [`cms`](./references/cms-streams.md) | CMS Streams |
| [`convert`](./references/convert.md) | Convert |
| [`copy-trading`](./references/copy-trading.md) | Copy Trading |
| [`crypto-loan`](./references/crypto-loan.md) | Crypto Loan |
| [`derivatives-options`](./references/derivatives-options.md) | Derivatives Trading (Options) |
| [`derivatives-portfolio-margin`](./references/derivatives-portfolio-margin.md) | Derivatives Trading (Portfolio Margin) |
| [`derivatives-portfolio-margin-streams`](./references/derivatives-portfolio-margin-streams.md) | Derivatives Trading Streams (Portfolio Margin) |
| [`derivatives-portfolio-margin-pro`](./references/derivatives-portfolio-margin-pro.md) | Derivatives Trading (Portfolio Margin Pro) |
| [`derivatives-portfolio-margin-pro-streams`](./references/derivatives-portfolio-margin-pro-streams.md) | Derivatives Trading Streams (Portfolio Margin Pro) |
| [`dual-investment`](./references/dual-investment.md) | Dual Investment |
| [`fiat`](./references/fiat.md) | Fiat |
| [`futures-coin`](./references/futures-coin.md) | Derivatives Trading (COIN-M Futures) |
| [`futures-coin-streams`](./references/futures-coin-streams.md) | Derivatives Trading Streams (COIN-M Futures) |
| [`futures-usds`](./references/futures-usds.md) | Derivatives Trading (USDS-M Futures) |
| [`futures-usds-streams`](./references/futures-usds-streams.md) | Derivatives Trading Streams (USDS-M Futures) |
| [`gift-card`](./references/gift-card.md) | Gift Card |
| [`margin-trading`](./references/margin-trading.md) | Margin Trading |
| [`margin-trading-streams`](./references/margin-trading-streams.md) | Margin Trading Streams |
| [`mining`](./references/mining.md) | Mining |
| [`pay`](./references/pay.md) | Pay |
| [`rebate`](./references/rebate.md) | Rebate |
| [`simple-earn`](./references/simple-earn.md) | Simple Earn |
| [`spot`](./references/spot.md) | Spot Trading |
| [`spot-streams`](./references/spot-streams.md) | Spot Trading Streams |
| [`staking`](./references/staking.md) | Staking |
| [`stocks`](./references/stocks.md) | Stocks |
| [`stocks-streams`](./references/stocks-streams.md) | Stocks Streams |
| [`sub-account`](./references/sub-account.md) | Sub Account |
| [`vip-loan`](./references/vip-loan.md) | VIP Loan |
| [`wallet`](./references/wallet.md) | Wallet |

## Notes

- ⚠️ **Prod transactions** — always ask user to type `CONFIRM` before executing.
- Use `--help` to get the list of commands and parameters.
- Use the output from both stdout and stderr.
- Append `--profile <name>` to any command to use a non-active profile.
- All authenticated endpoints accept optional `--recvWindow <ms>` (max 60 000).
- Timestamps (`startTime`, `endTime`) are Unix ms.
- Only endpoints listed in this skill may be used. The generic `binance-cli request <url> [--signed]` escape hatch is DISABLED by this modification — never call arbitrary endpoints, signed or not.