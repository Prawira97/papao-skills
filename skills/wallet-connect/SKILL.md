# wallet-connect

Cara Papao (agent) menghubungkan wallet agent ke situs yang membutuhkan
"Connect Wallet" — tanpa ekstensi browser, tanpa aplikasi HP, lewat
WalletConnect v2 (paste URI `wc:`) atau lewat signing langsung.

## Wallet yang ada

| Wallet | Alamat | Keypair | Saldo |
|---|---|---|---|
| EVM agent | `0xfEa9E003594eCd4afE26bA2FC03B73eaE892f010` | `~/workspace/agent-wallet/agent-evm-keypair.json` (0600) | 0 (belum didanai) |
| Solana agent | `BupM4zgsie9upSt94UdVAEHaKr1KRWpPMDgvXZGm46qf` | `~/workspace/agent-wallet/agent-keypair.json` (0600) | berisi dana trading |

Recovery phrase EVM (12 kata) dikirim ke yudieprawira97@gmail.com
(Gmail `1a1e983f3cadbf76`) — TIDAK PERNAH di chat, MEMORY.md, atau file lain.

## Cara situs connect wallet (ringkasan riset)

### 1. Injected provider — EIP-1193 (`window.ethereum`)
- Situs mengecek `window.ethereum`, lalu `provider.request({ method: 'eth_requestAccounts' })`.
- Login: `personal_sign` atas pesan teks (challenge/nonce dari server), server
  memverifikasi dengan `ecrecover` — ini SIWE (EIP-4361) bila format pesannya
  standar: `domain wants you to sign in with your Ethereum account:` +
  address + `URI:` + `Version: 1` + `Chain ID:` + `Nonce:` + `Issued At:`.
- **Browser cloud TIDAK punya ini**: `window.ethereum` = `undefined` →
  MetaMask gagal "Error Provider not found". Tidak ada cara meng-inject
  provider ke browser cloud dari sini. Jalan keluarnya: WalletConnect.
- `eth_sign` (raw bytes) berbahaya — jangan pernah pakai. `personal_sign`
  memakai prefix ERC-191 (`\x19Ethereum Signed Message:\n<len>`) sehingga
  pesan tidak bisa disalahartikan sebagai transaksi.

### 2. EIP-6963 — discovery multi-provider
- Event `eip6963:announceProvider` / `eip6963:requestProvider`; detail berisi
  `info { uuid, name, icon, rdns }` + `provider` (EIP-1193).
- Hanya relevan bila ada ekstensi terpasang. Di browser cloud: tidak ada
  provider yang announce → daftar wallet injected kosong.

### 3. WalletConnect v2 — SATU-SATUNYA jalan di browser cloud
- Situs (wagmi / RainbowKit / Reown AppKit) menampilkan modal QR + tombol
  **"Copy link"** yang menyalin URI pairing `wc:<topic>@2?relay-protocol=...&symKey=...`.
- Wallet (HP atau script agent) melakukan `pair({ uri })`, menerima
  `session_proposal`, lalu `approve` dengan namespaces yang didukung.
- Setelah session aktif, situs mengirim `session_request` (mis. `personal_sign`)
  lewat relay `wss://relay.walletconnect.com`; wallet menandatangani dan
  membalas lewat `client.respond({ topic, response: { id, result, jsonrpc: '2.0' } })`.
- SDK resmi saat ini: **Reown WalletKit (`@reown/walletkit`)** — penerus
  `@walletconnect/web3wallet`; di bawahnya memakai `@walletconnect/sign-client`.
  API (terverifikasi dari type definitions paket 1.6.0/2.26.0):
  `Core({ projectId })` → `WalletKit.init({ core, metadata })` →
  `kit.pair({ uri })` → event `session_proposal` →
  `buildApprovedNamespaces({ proposal, supportedNamespaces })` →
  `kit.approveSession({ id, namespaces })` → event `session_request` →
  `kit.respondSessionRequest({ topic, response: { id, jsonrpc: '2.0', result } })`.
  Event lain: `session_delete`, `proposal_expire`, `session_authenticate`
  (SIWE — `kit.formatAuthMessage` + `approveSessionAuthenticate`).
- **Butuh `projectId` gratis dari https://dashboard.reown.com** (Reown Cloud,
  paket Starter gratis: 1 project, 2,5 jt RPC call, 500 MAU).
  Tanpa projectId yang valid, SignClient/WalletKit tidak bisa connect ke relay.
  ProjectId BUKAN rahasia seperti private key, tapi simpan di env
  (`WC_PROJECT_ID`), jangan hardcode di repo.
  **Tidak ada projectId demo/test publik** — jangan pakai / mengarang ID
  orang lain; buat project Starter sendiri.
- **dApp test resmi untuk uji live pertama:** https://react-app.walletconnect.com
  (disebut di docs WalletConnect) — pair dari sana sebelum mencoba situs
  sungguhan seperti Immunefi.

### 4. Solana — Wallet Adapter + WalletConnect
- Injected: `window.phantom?.solana` / `window.solana`, `connect()`,
  `signMessage(bytes)` (off-chain, tanpa fee).
- Verifikasi: ed25519 `nacl.sign.detached.verify(msg, sig, pubkeyBytes)`.
- WalletConnect: namespace `solana`, chainId `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`
  (mainnet beta), method `solana_signMessage` (+ `solana_signTransaction`,
  `solana_signAllTransactions` — JANGAN approve tanpa perintah eksplisit).
- Paket baru: `@walletconnect/solana-adapter` (ganti
  `@solana/wallet-adapter-walletconnect` yang lama). Juga butuh `projectId`.
- SIWS (`solana:signIn`): varian sign-in Solana dengan field domain/statement/
  nonce/issuedAt; verifikasi via `verifySignIn`.

## Script — `~/workspace/agent-wallet/wc-connect/`

```
wc-connect/
  package.json          # ethers 6, @reown/walletkit, @walletconnect/utils, tweetnacl, bs58
  test-local.mjs        # tes lokal EVM: derivasi alamat + sign/verify (tanpa jaringan)
  solana-test-local.mjs # tes lokal Solana: ed25519 sign/verify, keypair THROWAWAY
  wc-connect.mjs        # pairing wc: URI + approve session EVM + layani personal_sign
  wc-solana.mjs         # rencana/skrip Solana: namespace solana + solana_signMessage
  README.md             # cara pakai singkat
```

### Tes lokal (sudah terbukti, 2026-11-17)
- `node test-local.mjs` — PASS: alamat derivasi cocok
  `0xfEa9E003594eCd4afE26bA2FC03B73eaE892f010`; sign + `verifyMessage`
  round-trip OK.
- `node solana-test-local.mjs` — PASS (keypair throwaway, in-memory saja):
  ed25519 sign + verify OK; format secret-key 64-byte Solana
  (`fromSecretKey` → alamat sama) OK. Keypair Solana agent TIDAK disentuh.
- `node wc-connect.mjs --dry-run '<wc-uri>'` — PASS (URI test yang valid
  formatnya): validasi URI, load keypair, init WalletKit semua OK; tanpa
  projectId / URI rusak / URI kedaluwarsa semua gagal bersih dengan instruksi.
- `node wc-solana.mjs --dry-run '<wc-uri>'` — PASS dengan keypair file
  throwaway (file di-shred sesudahnya).
- Versi terpasang (terverifikasi): `@reown/walletkit` 1.6.0,
  `@walletconnect/sign-client` 2.26.0, `@walletconnect/utils` 2.26.0,
  `@walletconnect/core` 2.26.0, `ethers` 6.17.0, `tweetnacl`, `bs58`,
  `@solana/web3.js` 3.2.1 (catatan: web3.js v3 mengubah API `Keypair` —
  tes Solana memakai `tweetnacl` langsung, bukan `Keypair.generate()`).
- QUIRK (terbukti): `@walletconnect/utils` v2 `parseUri` mengembalikan
  `protocol: ""` untuk URI `wc:` yang valid — validasi URI harus memakai
  `uri.startsWith('wc:')` + `version === 2` + `topic` + `symKey`, bukan
  `parsed.protocol`. Script sudah memperbaikinya (bug ini sempat membuat
  semua URI test ditolak sebelum diperbaiki).

### Belum teruji live (butuh browser + projectId asli)
- Pairing sungguhan ke dApp live: relay menolak projectId dummy — butuh
  projectId asli dari Reown Cloud (gratis, daftar pakai email Prawira) +
  URI `wc:` segar yang di-copy di browser. Uji live pertama sebaiknya di
  dApp test resmi https://react-app.walletconnect.com sebelum situs sungguhan.
  Sampai itu dilakukan, alur pair → proposal → approve → session_request
  belum terbukti end-to-end.
- Aturan namespace (dari spec): approve SEMUA method/event yang REQUIRED
  proposal, tidak boleh kurang; optional boleh sebagian / tidak sama sekali.
  Script sudah mengikuti ini — bila proposal MEWAJIBKAN method transaksi
  (`eth_sendTransaction` dkk.), `buildApprovedNamespaces` gagal dan script
  menolak session (bukan meng-approve sebagian). Itu perilaku yang benar
  menurut spec (proposal invalid → reject).
- Encoding param `solana_signMessage` di dApp nyata (script menerima
  base58 / hex / UTF-8; jawaban berupa signature base58) — asumsi ini
  perlu verifikasi live pertama.

### Pakai wc-connect.mjs (butuh uji live pertama via browser)
1. Di browser, di modal connect wallet situs, klik **Copy link** (bukan scan QR).
2. Paste URI `wc:...` ke Papao (chat) — URI pairing kedaluwarsa dalam
   hitungan menit, jadi lakukan segera.
3. Jalankan: `WC_PROJECT_ID=<id> node wc-connect.mjs '<wc-uri>'`
   (URI juga bisa via stdin agar tidak masuk shell history).
4. Script: load keypair EVM (cek perms 0600) → init WalletKit → `pair` →
   tunggu `session_proposal` → `approve` namespace eip155
   (chains `eip155:1`, methods `personal_sign` + `eth_sign` DITOLAK di
   handler, events `accountsChanged`/`chainChanged`, account
   `eip155:1:0xfEa9...`) → layani `session_request`:
   - `personal_sign`: tampilkan pesan, sign HANYA bila pesannya human-readable
     (teks login/verifikasi, SIWE) → balas signature.
   - `eth_sign`, `eth_sendTransaction`, `eth_signTransaction`,
     `eth_signTypedData*`: TOLAK otomatis, kecuali Prawira memerintahkan
     eksplisit untuk request spesifik itu.
5. Script tetap jalan (foreground) sampai session dihapus (`session_delete`)
   atau Ctrl+C → `disconnect`.

## YANG BISA dan yang TIDAK BISA

BISA:
- Pair WalletConnect via URI yang di-copy (tanpa scan QR, tanpa ekstensi).
- Approve session EVM + sign pesan login/verifikasi (`personal_sign`, SIWE).
- Solana: approve session namespace `solana` + `solana_signMessage`
  (ed25519, off-chain, tanpa fee).
- Verifikasi signature secara lokal sebelum membalas.

TIDAK BISA / TIDAK BOLEH:
- MetaMask / injected provider di browser cloud — tidak ada ekstensinya.
- Scan QR — wallet agent tidak punya aplikasi HP.
- Human Passport dengan wallet FRESH: skor 0 (butuh aktivitas on-chain /
  stamps). Wallet EVM agent yang baru dibuat TIDAK lolos verifikasi identitas
  Immunefi — tetap butuh wallet Prawira sendiri (0xD64d...) yang punya
  riwayat, di-scan lewat MetaMask HP.
- Sign transaksi / transfer dana tanpa perintah eksplisit Prawira.
- Memakai keypair Solana agent untuk test — hanya teori + keypair throwaway.

## ATURAN KEAMANAN (keras)
1. Private key / mnemonic TIDAK PERNAH dicetak ke log, chat, atau file lain.
   Keypair hanya dibaca script langsung dari file 0600.
2. Hanya sign pesan login/verifikasi yang HUMAN-READABLE (teks biasa / SIWE).
   Tolak `eth_sign` (raw bytes), tolak blind hash.
3. JANGAN PERNAH sign transaksi (`eth_sendTransaction`,
   `eth_signTransaction`, `solana_signTransaction`, dsb.) tanpa perintah
   eksplisit Prawira untuk transaksi spesifik itu — sebutkan tujuan, jumlah,
   dan alamat tujuan dulu.
4. Cek isi pesan sebelum sign: domain harus cocok dengan situs yang diminta,
   nonce harus baru, dan pesan tidak boleh berisi persetujuan transfer /
   approval token / perubahan kepemilikan.
5. WC_PROJECT_ID simpan di env, jangan hardcode.
6. Session WalletConnect yang sudah tidak dipakai → `disconnect` + hapus
   dari daftar session. Jangan biarkan session menggantung.
7. URI `wc:` berisi symKey session — perlakukan sebagai sensitif: jangan
   disebar, jangan disimpan di file setelah dipakai.

## Sumber
- EIP-1193: https://eips.ethereum.org/EIPS/eip-1193
- EIP-6963: https://eips.ethereum.org/EIPS/eip-6963
- EIP-4361 (SIWE): https://eips.ethereum.org/EIPS/eip-4361
- Reown WalletKit: https://docs.reown.com/walletkit
- WalletConnect docs: https://docs.walletconnect.com
- Reown Solana adapter: https://docs.reown.com/advanced/providers/solana-adapter
- Solana messages & auth: https://solana.com/docs/frontend/messages-and-auth
