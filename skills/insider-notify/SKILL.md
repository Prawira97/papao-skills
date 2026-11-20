# Skill: notifikasi insider (insider-notify)

Notifikasi real-time ke Prawira di chat WhatsApp untuk semua yang bergerak di sistem trading memecoin Solana: pembelian 12 wallet insider Tier 1, pembelian 12 wallet whale (auto-beli bila lolos gerbang sejak 2026-11-17 22:20 WITA, notify-only bila tidak lolos), SOL masuk ke dompet agent, perubahan posisi manual, dan pergerakan holding tiap 30 detik. Dibuat 2026-11-17 atas perintah Prawira ("Skill notifikasi seperti tadi dan update dari wallet insider", "jangan telat kasih sinyal"). Whale ditambah 2026-11-17 18:26 WITA atas perintahnya ("gabung dengan seluruh whales ini yang aktif membeli memetoken solana") — total 24 wallet dipantau. Pantau holding ditambah 2026-11-17 18:27 WITA atas perintahnya ("pantau naik atau turun aset holding setiap 30 detik di seluruh aset yg ada di wallet" + "jangan jual").

## Prinsip

- **Cepat:** sinyal beli insider dicek tiap **1 menit** (dipercepat dari 5 → 2 → 1 menit atas perintah Prawira 2026-11-17); sinyal beli whale dicek tiap **1 menit** (dipercepat dari 2 menit atas perintah Prawira 2026-11-17 21:47 WITA, "pantau insider bukan cuman dari wallet tapi juga dari whales"; poll wallet tiap 15 detik, 6 worker paralel — sejak 22:20 WITA whale-watch juga AUTO-BELI, lihat §4); deposit + penjaga posisi tiap 5 menit; **holding dicek tiap 30 detik, notifikasi pergerakan tiap 2 menit**.
- **Sekali saja:** setiap peristiwa dilaporkan tepat satu kali (state file mencatat yang sudah dilaporkan).
- **Diam bila tidak ada apa-apa:** output NO_NEW / BASELINE_OK / NO_ACTION / CLOSED = tidak ada pesan.
- **Alamat kontrak selalu dalam code block** agar bisa dicopy.
- **Jangan pernah jual diam-diam:** sebelum jual apa pun, tanya Prawira dulu atau minimal beri notifikasi dulu dan tunggu perintahnya (aturan keras sejak 2026-11-17 17:43 WITA, pelajaran $AI).

## Aturan penekanan (suppression) — pelajaran 2026-11-17 sore

Notifikasi yang diulang-ulang untuk hal yang sama membuat Prawira kebal terhadap sinyal — penekanan sama pentingnya dengan kecepatan.

- **Osilasi di pita yang sama = laporkan sekali, lalu diam.** RaRa osilasi $0,0000557 ↔ $0,00006653 (0,88x–1,08x entry) sejak 18:36 WITA — dilaporkan beberapa kali, lalu DITEKAN dari ~18:53 WITA. Bila token kembali ke level yang sudah dilaporkan dalam 10 menit terakhir, jangan laporkan lagi.
- **Beli debu berulang = bukan sinyal baru.** Dior beli 1B 0,021 SOL berulang (18:54, 19:00, 19:04, 19:06, 19:15, dst) — pola yang sama, ukuran yang sama, token yang sama. Setelah pola debu dikenali, tekan notifikasi berikutnya untuk token+wallet itu kecuali ukurannya membesar ≥5x atau ada wallet lain ikut beli.
- **Glitch feed harga = jangan laporkan, jangan koreksi.** 18:49 WITA mihao sempat tampil $10,0047 (+91.712%, 869x) selama satu tick — harga asli $0,01064. Glitch satu tick + koreksinya DITEKAN; laporkan hanya bila harga bertahan ≥2 siklus monitor (60 detik).
- **Pergerakan yang sama = sekali.** Aturan umum: satu peristiwa (satu level, satu ambang, satu pembelian) dilaporkan tepat satu kali. Bila ragu apakah sesuatu sudah dilaporkan, cek `~/memory/2026-11-17.md` / log harian sebelum mengirim.
- **Kualitas sinyal di pesan:** bila pembelian whale/insider adalah akumulasi nyata (berulang + ukuran membesar, tingkat A §8 memecoin-analysis), tulis begitu ("akumulasi ke-7, ukuran membesar"). Bila debu (tingkat C), tulis terus terang ("beli kecil/top-up") — jangan membesar-besarkan.

## Komponen (sudah hidup)

### 1. Notifikasi beli wallet insider — `insider-buy-notify` (tiap 1 menit)
- Script: `~/workspace/memecoin-auto-trader/copy-trader/notify-buys.py` (state: `notify-buys-state.json` di folder yang sama).
- Membaca `trades.log` bot copy-trade, mencari event `trigger_detected` baru (wallet yang dipantau membeli token).
- Per pembelian baru, cetak satu baris: `BUY <jam WITA> <nama wallet> <alamat wallet> <simbol> <mint> <jumlah token> <SOL yang dibelanjakan atau ?> <hasil bot> <detail>`.
- Hasil bot: `BOT_BELI <tx>` / `SKIP <alasan>` (misal: saldo rendah, likuiditas < $5.000, mint authority aktif, sudah ada posisi) / `SUDAH_PUNYA_POSISI`.
- **Token yang diblokir (config `blockedMints`, saat ini PUMP) tidak pernah dilaporkan.**
- Simbol token diambil dari Dexscreener (cache di state); bila gagal, simbol `?`.
- Cron agent membaca output script: baris BUY → kirim SATU pesan WhatsApp berisi semua pembelian baru; NO_NEW/BASELINE_OK → diam.
- Nama wallet (12 Tier 1): Decu, Cented, Theo, Trunoest, Dv, Casino, Nyhrox, Kadenox, Cap, Limfork, Johnson, Jijo — peta nama→alamat ada di script (`WALLETS`); bila daftar wallet bot berubah, update peta ini juga.

### 2. Notifikasi SOL masuk — `agent-wallet-deposit-watch` (tiap 5 menit)
- Script: `~/workspace/memecoin-auto-trader/check-deposit.py` (state: `wallet-watch-state.json`).
- Cek dompet agent `BupM4zgsie9upSt94UdVAEHaKr1KRWpPMDgvXZGm46qf` via RPC publik.
- Output `DEPOSIT <jumlah SOL> <signature> <kind>` → kirim pesan: "Dompet agent menerima <jumlah> SOL" + jenis (transfer masuk / hasil jual bot bila kind=jual-bot) + signature dalam code block.
- Output NO_NEW/BASELINE_OK → diam. Gagal RPC → catat di log harian, coba lagi jadwal berikut (jangan kirim pesan panik).

### 3. Notifikasi posisi manual — penjaga jual per posisi (tiap 5 menit)
- Script: `~/workspace/memecoin-auto-trader/copy-trader/sell-watch.js`, file posisi di `~/workspace/memecoin-auto-trader/positions/<mint-12-karakter-pertama>.json`, satu cron per posisi (`<ticker>-sell-watch`).
- Output NO_ACTION/CLOSED → diam.
- Output SELL → SEGERA kabari: alasan jual (TP +100%/+300%/+900%/trailing/time exit/darurat), jumlah SOL + perkiraan USD, signature dalam code block.
- **Pengaman never-sell-at-loss (hidup di sell-watch.js):** posisi di bawah harga masuk TIDAK PERNAH dijual otomatis — script menahan (HOLD) dan cron melaporkan sekali bahwa posisi minus dan ditahan.
- Posisi closed → kabari sekali dengan ringkasan akhir (total masuk, total keluar, untung/rugi).
- Gagal script 3x berturut-turut → baru kabari Prawira bahwa penjaga posisi itu bermasalah.

### 4. Notifikasi beli wallet whale — `whale-buy-notify` (tiap 1 menit, AUTO-BUY sejak 2026-11-17 22:20 WITA — **STOPPED 2026-11-17 22:45 WITA, kembali notify-only sampai Prawira perintahkan mulai Compounding lagi**)
- Watcher: `~/workspace/memecoin-auto-trader/copy-trader/whale-watch.py` — daemon, poll RPC publik tiap **15 detik** (6 worker paralel; satu siklus penuh dulu ~38 detik sekuensial, sekarang ~3-5 detik) untuk 12 alamat whale (daftar di `~/workspace/memecoin-auto-trader/wallet-lists-whale-12.md`; nama di peta `WALLETS` dalam script). Menulis event ke `whale-trades.log`, state di `whale-watch-state.json` (lastSig per wallet + seen).
- Notifikasi: `~/workspace/memecoin-auto-trader/copy-trader/notify-whale-buys.py` (state: `notify-whale-buys-state.json`), cerminan notify-buys.py. Output per pembelian: `BUY <jam WITA> <nama wallet> <alamat> <simbol> <mint> <jumlah> <SOL atau ?> WHALE`; bila bot sudah membeli: `BOT_BELI <jam WITA> <nama wallet> <alamat> <simbol> <mint> <jumlah> <SOL atau ?> WHALE_BOUGHT <USD dibeli> <signature>` (baris trigger_detected yang berpasangan dengan BOT_BELI TIDAK dilaporkan dua kali).
- **AUTO-BUY (perintah Prawira 2026-11-17 22:20 WITA: "usahakan buy yg potensial dari whales 30 detik setelah whales beli"):** pembelian whale yang lolos semua gerbang (nilai >= $70, RugCheck <= 50 + mint/freeze dicabut, likuiditas >= $5.000, top-10 <= 35%, h1 <= +100%, saldo >= 0,03 SOL; ukuran 20% bankroll maks $2,50) langsung dibeli bot ~30-60 detik setelah tx whale. Yang TIDAK lolos tetap notify-only — Prawira yang putuskan manual. Detail gerbang + uji ada di skill memecoin-auto-trader (§ Auto-buy whale). Cron `whale-buy-notify` membuat sell-watch cron untuk posisi BOT_BELI + memberi tahu Prawira (jumlah USD + signature).
- Deteksi beli (cermin `detectBuys` runner.js + satu filter tambahan): saldo token naik (post > pre > 0, bukan wSOL/stable) DAN wallet mengeluarkan sesuatu di tx yang sama (SOL keluar, atau USDC/USDT berkurang). Transfer masuk biasa (saldo naik, wallet tidak bayar apa-apa) TIDAK dihitung beli. Filter ini TERBUKTI lebih benar dari bot: 3 trigger bot (DRILL Cap, WUKONG Casino, bean AvGi) ternyata transfer masuk (SOL keluar = 0, tidak ada program swap) — whale-watch menolak ketiganya, sementara beli asli Q1vec drgraino terdeteksi persis (amount sama dengan bot).
- getTransaction: jsonParsed + maxSupportedTransactionVersion 0 dulu; bila kena error -32015 (tx versioned v0 — hampir semua swap Jupiter), fallback sekali ke version 1. Tanpa fallback ini monitor melewatkan hampir semua pembelian. Error -32015 TIDAK di-retry (deterministik); 429/413 di-backoff (2s→4s→8s, maks 4x) lalu lanjut, tidak pernah crash.
- Baseline: jalan pertama catat signature terakhir tiap wallet TANPA melapor. `--once` = satu siklus saja (untuk uji). `--self-test` = putar ulang 5 trigger_detected terakhir dalam DRY-RUN (gerbang jalan sungguhan, tidak ada tx). Daemon: `python3 whale-watch.py` (jalan selamanya, poll 15 detik, 6 worker).
- **Token yang diblokir (config `blockedMints`, saat ini PUMP) tidak pernah dilaporkan.**
- Simbol token diambil dari Dexscreener (cache di state); bila gagal, simbol `?`.
- Cron agent membaca output script: baris BUY → kirim SATU pesan WhatsApp berisi semua pembelian baru; NO_NEW/BASELINE_OK → diam.
- Nama wallet whale: Ansem Pumpfun, Frank degods, Unipcs, Gake, Dior, Ansem, Jadawgs; sisanya tanpa nama (label `Whale + 4 karakter awal alamat`: AgmL, 3eGj, Gygj, Nsgx, 13fK).
- Uji tanpa mengubah state: `python3 notify-whale-buys.py --dry-run` (5 pembelian terakhir).

### 5. Pantau holding tiap 30 detik — `holdings-move-notify` (MONITORING SAJA, TIDAK PERNAH JUAL)
- Monitor: `~/workspace/memecoin-auto-trader/copy-trader/holdings-watch.py` — proses loop latar, tiap **30 detik** baca SEMUA token account dompet agent `BupM4zgsie9upSt94UdVAEHaKr1KRWpPMDgvXZGm46qf` via RPC publik (raw JSON-RPC `getTokenAccountsByOwner`, program Token + Token-2022; `getTokenAccountsByOwner` + jsonParsed RUSAK di web3.js versi ini — jangan pakai). Harga dari Dexscreener (batch tokens/v1 dulu, bila gagal endpoint lama per mint); bila Dexscreener gagal juga, fallback quote Jupiter v1 read-only (tidak swap). Nilai USD + kelipatan vs `entryPriceUsd` dari file posisi (`positions/*.json` manual + `state.json` bot).
- Tulis `holdings-watch.log` (satu JSON per baris per mint per siklus: ts, mint, ticker, amount, priceUsd, valueUsd, multVsEntry, changeVsLastCheckPct; dipangkas ke 5000 baris terakhir). Event ke `holdings-events.log` bila: (a) naik/turun **≥10%** sejak harga terakhir yang dilaporkan, ATAU (b) melewati kelipatan vs entry (**0,5x** turun / **2x / 3x / 5x / 10x** naik). Satu event per token per ambang, cooldown 10 menit per ambang yang sama. State: `holdings-watch-state.json` (harga terakhir dilaporkan + ambang yang sudah dilewati + cache simbol).
- Notifikasi: `~/workspace/memecoin-auto-trader/copy-trader/notify-holdings.py` (state: `notify-holdings-state.json`), dibaca cron `holdings-move-notify` tiap 2 menit. Output per event: `MOVE <jam WITA> <ticker> <mint> <naik/turun> <pct>% <harga> <kelipatan>` / `THR <jam WITA> <ticker> <mint> <naik/turun> <pct>% <harga> <kelipatan> lewati <ambang>x`. NO_NEW bila kosong. **Tidak ada BASELINE_OK di notifier ini** (sengaja): log event baru ditulis sejak monitor dibuat, jadi tidak ada tumpukan lama — event pertama pun harus dilaporkan. `--dry-run` = 5 event terakhir tanpa ubah state.
- Watchdog: `holdings-watchdog.sh` (cek via `ps aux`, BUKAN pgrep) + cron `holdings-watchdog` tiap 5 menit. Monitor TIDAK auto-start saat VM restart — watchdog cron yang menyalakannya lagi (paling lambat 5 menit setelah restart).
- **Debu diabaikan:** saldo token < 0,0001 unit tidak dicatat (misal sisa 0,000097 USDC dari swap Jupiter).
- **JANGAN PERNAH jual dari sistem ini** — tidak ada jalur jual di holdings-watch.py maupun notify-holdings.py (tidak baca keypair, tidak panggil Jupiter swap, tidak tulis ke trades.log). Posisi REX buyback 18:19 WITA awalnya TANPA sell-watch cron (perintah Prawira "jangan jual"), TAPI 19:19 WITA Prawira perintahkan "pantau, jangan sampai telat sell" → `rex-sell-watch` dibuat (TP ladder standar, cek tiap 5 menit). Status jual tiap posisi bisa berubah atas perintahnya — cek `cron.list` bila ragu.
- Uji: `python3 holdings-watch.py --once` (satu siklus + cetak semua aset). Bandingkan hasilnya dengan file posisi open — laporkan bila ada aset di dompet tanpa file posisi (atau sebaliknya).

## Format pesan (contoh)

Beli insider:
```
Johnson beli $WISHMAS — 17:56 WITA
`9cmXfuC26anZtH9AUWVzpUxU1UJ7PPogYxftYTepump`
Jumlah: 2.294,45 token
Bot: SKIP — saldo rendah 0,0048 SOL < 0,02 SOL
```

Beli whale (notify-only):
```
🐋 Frank degods beli $DRILL — 18:26 WITA (WHALE)
`Ts2yi5FhTDAmhwTKH6ab6unWeoCMzzjz4JCPtBDRiLL`
Jumlah: 39.000 token
Bot tidak auto-beli — putuskan manual mau ikut atau tidak
```

Deposit:
```
Dompet agent menerima 0,1443 SOL (transfer masuk)
`3cUy2ShZ...`
```

Posisi minus (ditahan):
```
$PICK lagi minus dikit (0,98x harga masuk) — tidak dijual, ditahan dulu sampai balik untung.
```

Pergerakan holding:
```
$RaRa naik 12,12% — $0,00006653 (1,08x harga masuk)
`BLrKuqTC9YhPvLpUsZCRipXw3v3igFWeuYTJ6e5Tpump`
```

## Menambah / mengubah

- **Wallet baru dipantau:** Tier 1 — tambah alamat ke `config.json` bot + peta `WALLETS` di notify-buys.py. Bot hanya bisa memantau ~12 wallet di RPC publik — lebih dari itu deteksi melambat. Whale — tambah alamat ke peta `WALLETS` di whale-watch.py DAN notify-whale-buys.py (dua-duanya); whale TIDAK masuk config bot (auto-buy diatur `whaleAutoBuy` di `config.json`). Daemon whale-watch harus di-restart agar peta baru terbaca.
- **Posisi manual baru:** beli via `buy-once.js`, lengkapi file posisi (entryPriceUsd, decimals, pairAddress, ticker — buy-once.js tidak menulis field itu), buat cron `<ticker>-sell-watch` 5 menit dengan body yang sama seperti cron posisi lain.
- **Ubah kecepatan:** `cron.update` pada `insider-buy-notify` (saat ini 1 menit) atau `whale-buy-notify` (1 menit, dipercepat dari 2 menit 2026-11-17 21:47 WITA). Jangan di bawah 1 menit untuk keduanya — RPC publik sudah berat dan cron agent butuh waktu jalan.
- **Uji script notifikasi tanpa mengubah state:** `python3 notify-buys.py --dry-run` (menampilkan 5 pembelian terakhir yang akan dilaporkan). Whale: `python3 notify-whale-buys.py --dry-run`; uji satu siklus watcher: `python3 whale-watch.py --once`. Holding: `python3 notify-holdings.py --dry-run`; uji satu siklus monitor: `python3 holdings-watch.py --once`.

## Batasan yang diketahui

- Bot mendeteksi beli via perubahan saldo token di RPC publik (poll 5 detik); saat RPC 429/413, deteksi bisa telat beberapa menit — notifikasi 2 menit tidak bisa memperbaiki keterlambatan deteksi itu.
- `solSpentLamports` di event trigger sering 0 (bot tidak mengisinya) — tampilkan `?`, jangan 0.
- Cron agent tidak bisa `chat.send_message` ke chat WhatsApp dari dalam worker — pesan notifikasi harus disampaikan lewat parent (main agent) di chat ini.
- **Whale-watch lebih ketat dari bot (sengaja):** bot menganggap setiap kenaikan saldo token sebagai beli — termasuk transfer masuk/airdrop (terbukti di DRILL/WUKONG/bean). Whale-watch menuntut wallet membayar sesuatu di tx yang sama. Akibatnya whale-watch TIDAK akan melaporkan "beli" yang sebenarnya transfer — itu fitur, bukan bug.
- **Siklus whale-watch dulu ~38 detik** (12 wallet sekuensial, RPC publik ~1–2 detik per panggilan + sleep 0,5 detik antar wallet; daemon tidur 60 detik SETELAH tiap siklus — jadi jeda antar siklus 60 detik + durasi siklus). **Sejak 2026-11-17 22:20 WITA: poll paralel 6 worker, siklus ~3-5 detik + tidur 15 detik** — perlu untuk target beli ~30 detik setelah whale.
- Whale-watch daemon TIDAK auto-start saat VM restart — dijalankan manual (`nohup python3 whale-watch.py > whale-watch.log 2>&1 &`) atau lewat watchdog. Watchdog sudah ada: `whale-watchdog.sh` + cron `whale-watch-watchdog` tiap 5 menit (dibuat parent 2026-11-17 18:28 WITA).
- **Dexscreener dari VM ini sering putus** (IncompleteRead / "Remote end closed connection") — harga tetap didapat lewat 3 lapis fallback (batch tokens/v1 → endpoint lama per mint → quote Jupiter v1); simbol token kadang tertinggal `?` sampai satu panggilan Dexscreener berhasil (cache simbol di state, terisi bertahap). Harga tidak pernah kosong karena fallback Jupiter.
- **Holdings-watch TIDAK auto-start saat VM restart** — watchdog cron `holdings-watchdog` (tiap 5 menit) yang menyalakannya lagi; jeda maksimal 5 menit setelah restart.
- **Aset tanpa file posisi bisa muncul di monitor** (misal KATIA 4.633,44 token ditemukan 2026-11-17 18:27 WITA padahal file posisinya berstatus closed — dibeli 18:23 WITA ~$1 dari dompet agent, tx `4zGEcMcJWW5wjn2Rds1VJfLKBS7C1EZwRqGUSEMXpceJBqCE7kGwBHaUfoS1RNrojJYUhWXyTtM2D2MgmoPaetty`, tidak ada di trades.log maupun state.json bot). Monitor tetap melaporkannya (harga + nilai), tapi kelipatan vs entry memakai `entryPriceUsd` file lama (0,94x) — perlakukan sebagai temuan, bukan posisi resmi, sampai parent memastikan asal-usulnya.
