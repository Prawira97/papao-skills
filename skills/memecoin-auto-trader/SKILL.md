# Auto Buy / Auto Sell Memecoin Solana + Compounding

Skill ini adalah playbook trading otomatis memecoin Solana. Ia MEMAKAI skill `memecoin-trading` sebagai gerbang keamanan — tidak ada token yang dibeli tanpa lolos semua cek di sana. Skill ini menambah: sinyal masuk/keluar, aturan compounding, limit risiko, dan loop otomatis.

## Aturan keras dulu

- Memecoin sangat volatil dan bisa menjadi tidak bernilai sama sekali. Jangan pernah memakai uang untuk kebutuhan hidup (sewa, makan, utang, darurat).
- Gunakan HANYA dompet agent yang terpisah dan kecil: `BupM4zgsie9upSt94UdVAEHaKr1KRWpPMDgvXZGm46qf`. Jangan pernah memakai dompet utama user (`95ubFWyurr4GAxPjS3z15HjDnRX3SPNtnrdyRcBjRbY6`) untuk trading memecoin.
- Jangan pernah meminta, menyimpan, atau memasukkan seed phrase / private key ke chat, file, log, atau prompt apa pun.
- Jangan pernah menjanjikan profit dan jangan pernah menyatakan target harga sebagai fakta.
- **Mode auto HANYA aktif setelah Prawira menyetujui parameternya secara tertulis** (modal awal, % risiko per trade, batas kerugian). Persetujuan itu berlaku untuk seluruh loop auto dengan parameter tersebut — bukan per trade. Prawira bisa menghentikan kapan saja dengan kata "jeda" / "stop" (kill switch langsung, tutup semua posisi terbuka yang masih bisa dijual).
- Jangan averaging down secara otomatis. Jangan menambah dana segar secara otomatis.

## Compounding — cara kerja

- **Bankroll** = modal awal + profit terealisasi − kerugian terealisasi. Semua profit hasil jual TETAP di bankroll (tidak ditarik), jadi ukuran posisi tumbuh mengikuti bankroll.
- **Ukuran posisi per trade = 20% dari bankroll SAAT INI** (naik dari 5% atas perintah Prawira 2026-11-17 21:47 WITA; maks $2,5 per beli). Menang → bankroll naik → posisi berikutnya lebih besar. Kalah → bankroll turun → posisi berikutnya lebih kecil otomatis.
- Contoh aritmatika (bukan janji profit): modal 1 SOL → posisi 0,05 SOL. Kalau posisi itu naik 100% dan terjual, bankroll jadi 1,05 SOL dan posisi berikutnya 0,0525 SOL.
- **Amankan modal awal:** begitu bankroll mencapai 2x modal awal, tarik modal awal keluar dari bankroll trading (simpan terpisah) — hanya bila Prawira menyetujuinya. Setelah itu yang dipertaruhkan hanya profit.
- Jangan pernah meminjam / leverage. Jangan pernah memakai dana di luar bankroll yang disetujui.

## Compounding — playbook lanjutan (2026-11-17, pelajaran AMAZON + REX)

- **Studi kasus AMAZON — bukti TP1 menyelamatkan profit.** Beli $1 (15.126,47 token, entry $0,00006611) 18:57 WITA. Harga lari ke 2,50x; TP1 (+100%) jual 50% 19:03 WITA → terima ~0,017372 SOL (~$1,25). Enam menit kemudian token crash −97% ke 0,02x — sisa 50% tinggal ~$0,01. Total: $1,26 dari modal $1 — TETAP UNTUNG hanya karena TP1 sudah dieksekusi. Tanpa TP1, $1 itu jadi ~$0,02. **Pelajaran: TP1 bukan "mengunci sedikit profit" — TP1 adalah yang membedakan pulang untung vs pulang hampir nol. Moonbag (sisa setelah TP1/TP2/TP3) adalah tiket lotre: anggap nilainya bisa jadi ~$0 kapan saja; jangan pernah menghitung nilai moonbag sebagai profit sebelum terjual.**
- **Ukuran beli di bankroll kecil (UPDATE 2026-11-17 21:47 WITA).** Rate naik 5% → 20%, maks $2,5/beli (hard cap, termasuk pengali konsensus). Bankroll ~$10,55 (0,144 SOL): 20% = ~$2,11 per beli; cap $2,5 mengikat saat bankroll > $12,50. Jadi beli bot sekarang ~$2,1 — bukan $1 lagi.
- **Daur profit terealisasi.** Hasil jual TP masuk dompet sebagai SOL → saldo naik → beli berikutnya (tetap $1 di fase ini, membesar nanti). Rantai ini yang disebut compounding — bukan menambah dana segar. Dana segar hanya masuk lewat top-up Prawira (0,146378 SOL 14:55 + 0,1443 SOL 18:01 WITA), dicatat terpisah dari profit.
- **Mode hold MEMBEKUKAN compounding.** Saat `autoSellEnabled: false`, bot tidak merealisasikan apa pun — bankroll hanya bergerak lewat top-up dan harga posisi yang belum terjual. Compounding tetap jalan untuk posisi MANUAL yang punya sell-watch cron sendiri (AMAZON: TP1 dieksekusi penjaga posisinya, bukan bot). Jadi: bila mode hold aktif, tiap posisi manual baru WAJIB dibuatkan sell-watch cron (TP ladder) bila Prawira mau profitnya berputar — kalau tidak, posisi itu hanya ditahan.
- **Akuntansi bankroll yang jujur.** Nilai bankroll = SOL bebas + nilai pasar posisi terbuka − sewa akun token yang terkunci (~0,002 SOL per token, ~0,012 SOL untuk 6 token — kembali hanya bila akun ditutup) − fee swap. Harga SOL dari dual-source (Dexscreener + Jupiter). Jangan laporkan bankroll hanya dari harga puncak posisi — moonbag dihitung di harga SEKARANG.
- **Amankan modal awal (2x bankroll).** Begitu bankroll mencapai 2x modal awal, tarik modal awal keluar (hanya bila Prawira setuju). Di bankroll ~$10, aturan ini belum relevan — catat saja ambangnya, jangan kejar dengan menaikkan ukuran beli.
- **Kasus REX buyback.** Beli ulang $1 18:19 WITA ("jangan jual") → harga osilasi 0,80x–1,49x seharian → 19:19 WITA Prawira perintahkan "pantau, jangan sampai telat sell" → dibuatkan `rex-sell-watch` (TP ladder standar). Pelajaran: perintah "jangan jual" dan "jangan telat sell" bisa berubah dalam hitungan jam — status jual tiap posisi harus bisa dibalik cepat lewat cron (buat/hapus), dan file posisi harus mencatat status terakhirnya, bukan perintah lama.

## Gerbang masuk (wajib lolos semua)

1. Token lolos SEMUA cek skill `memecoin-trading`: mint address benar, authority (mint/freeze) aman, distribusi holder tersebar, likuiditas cukup + terverifikasi, RugCheck lolos, dan **test sell kecil berhasil** (bukti bisa jual).
2. Sinyal momentum (default, bisa diubah Prawira): volume 24 jam naik, holder bertambah, harga bertahan di atas harga 1 jam lalu, dan pair berumur minimal 1 jam (hindari 5 menit pertama yang paling rawan sniper/rug).
3. TIDAK PERNAH beli: token yang gagal satu pun cek gerbang, token tanpa exit yang bisa dieksekusi, atau token yang alasan belinya hanya "katanya bakal naik".

## Aturan keluar (otomatis, tanpa ditanya)

- **Take profit bertingkat (default):** jual 50% posisi saat +100%, jual 25% lagi saat +200%, sisanya 25% dibiarkan jalan dengan trailing stop −30% dari harga tertinggi setelah entry.
- **Stop loss: NONAKTIF sejak 2026-11-17 (aturan Prawira: "Jangan sell yang sudah minus").** Posisi yang sedang minus TIDAK PERNAH dijual otomatis — ditahan sampai pulih ke harga masuk atau lebih, apa pun pemicunya (SL, time exit, trailing, darurat). Jual manual atas perintah Prawira tetap bisa.
- **Exit waktu:** bila dalam 24 jam posisi tidak bergerak naik sama sekali dan tidak ada momentum, tutup posisi (jual) dan catat alasannya.
- **Exit darurat: NONAKTIF sejak 2026-11-17 18:28 WITA (perintah Prawira: "jangan ulangi ini lagi").** Sinyal rug (likuiditas ditarik, mint tambahan, freeze, holder besar jual bersamaan) → **TAHAN + LAPOR ke Prawira dulu**, jangan jual sendiri. Penjualan hanya atas perintahnya.

## Limit risiko (kill switch otomatis)

- Maksimal **3 posisi terbuka** sekaligus.
- Maksimal kerugian harian **10% dari bankroll** → pause loop sampai besok, lapor ke Prawira.
- Maksimal drawdown **−30% dari puncak bankroll** → hentikan mode auto sepenuhnya, tutup posisi yang masih bisa dijual, lapor ke Prawira. Lanjut hanya atas perintahnya.
- Slippage maksimal 3% per swap (default); priority fee dibatasi dan dicatat. Bila quote basi / tidak ada route / saldo SOL tidak cukup → skip trade, catat, jangan kejar.
- Setiap transaksi gagal: diagnosis dulu penyebabnya, retry maksimal 2x dengan pendekatan berbeda, lalu berhenti dan catat. Jangan ulangi panggilan yang sama tanpa perubahan.

## Mode copy-trade Top 12 — Tier 1 (insider)

- **Pantauan:** hanya 12 wallet Tier 1 teratas (peringkat berdasarkan realized profit 30 hari, dari daftar yang diverifikasi 2026-11-17 — 103 wallet diteliti, 25 Tier 1, 12 teratas masuk config; batas RPC publik). Daftar wallet disimpan di file konfigurasi runner; ganti daftar hanya atas perintah Prawira.
- **Pemicu:** begitu salah satu dari 15 wallet membeli token baru, runner langsung membeli token yang sama. Target kecepatan: dalam hitungan detik — bukan nol detik, karena deteksi on-chain + pengiriman transaksi butuh waktu (block ~0,4 detik + delay indexing/API). Tidak ada yang bisa benar-benar simultan.
- **Gerbang cepat (wajib, ~1–2 detik):** sebelum beli, periksa cepat: mint/freeze authority tidak berbahaya, ada likuiditas, dan token bisa dijual (simulasi sell). Satu cek gagal = SKIP, jangan beli. Membeli buta tanpa gerbang = membeli rug yang sengaja dibuat insider untuk dibuang ke pengikutnya.
- **Ukuran beli per copy:** tetap (default: sama untuk semua copy, mis. $1–2 per trade, ditentukan Prawira) — bukan % bankroll, karena kecepatan lebih penting daripada sizing di mode ini.
- **Setelah beli:** posisi copy-trade mengikuti aturan keluar skill ini (TP bertingkat, trailing, time-exit — dan aturan jangan-jual-minus: tidak ada jual otomatis di bawah harga masuk).
- **Batas:** bila 3 copy beruntun rugi, pause copy-trade dan lapor ke Prawira. Kill switch "jeda/stop" berlaku sama.
- **Jangan copy jual mereka secara buta:** jual kita mengikuti aturan exit kita sendiri, bukan gerakan jual insider (mereka sering jual bertahap sambil harga masih naik).

## Auto-buy whale — 2026-11-17 22:20 WITA (perintah Prawira: "usahakan buy yg potensial dari whales 30 detik setelah whales beli")

**⛔ STOPPED 2026-11-17 22:45 WITA (Prawira: "Stop dulu perintah auto trade untuk selama nya sampai saya perintahkan mulai Compounding lgi"): auto-buy whale MATI — config `live:false, whaleAutoBuy:false, killSwitch:true`; whale-watch jalan notify-only (PID 43630); bot copy-trade mati + file STOP; semua sell-watch + dip-watch nonaktif. Nyalakan lagi HANYA atas perintah Prawira.**

- **Dulu notify-only, sekarang AUTO-BUY.** Sampai 22:20 WITA whale hanya dilaporkan; sejak perintah ini, pembelian whale yang lolos SEMUA gerbang di bawah langsung dibeli bot — sama seperti sinyal Tier 1. Yang tidak lolos tetap hanya dilaporkan (notify-only).
- **Kenapa daemon terpisah (bukan masuk runner.js):** RPC publik sudah berat (bot 12 wallet x 5 detik kena 429/413). Menambah 12 wallet ke bot = 24 x 5 detik = makin parah. Jadi whale-watch.py tetap daemon sendiri (`~/workspace/memecoin-auto-trader/copy-trader/whale-watch.py`, PID dicek via `ps aux`, restart lewat `whale-watch-watchdog.sh`).
- **Kecepatan (jujur):** poll 15 detik + 6 worker paralel (satu siklus penuh dulu ~38 detik sekuensial, sekarang ~3-5 detik) + gerbang ~5-10 detik + swap ~10-20 detik = beli mendarat **~30-60 detik setelah tx whale**. Target ~30 detik, bukan jaminan — RPC publik dan Jupiter yang menentukan.
- **Gerbang auto-buy (SEMUA wajib lolos, urutan = handleBuyEvent bot):** (0) config `whaleAutoBuy` true + `live` true + `killSwitch` false — bila tidak, TIDAK ADA pembelian (fail closed); (1) mint tidak diblokir (`blockedMints`); (2) belum ada posisi terbuka untuk mint itu (state.json bot ATAU file positions); (3) **ukuran beli whale POTENSIAL: nilai >= $70 (~1 SOL)** — nilai = jumlah token x harga Dexscreener saat ini, BUKAN solSpent (beli pakai stablecoin punya solSpent 0: Ansem + Dior beli mihao 21:53/22:03 WITA solSpent 0 tapi nilai ~$9.800/~$4.700; debu Dior 0,021 SOL ~$1,50 tertolak di sini); (4) gerbang dasar cermin fastGate: RugCheck skor <= 50, tanpa risiko kritis, mint+freeze authority NULL (dibaca dari field TOP-LEVEL laporan RugCheck — JANGAN dari tokenMeta, tidak ada field itu di sana), likuiditas >= $5.000 (jumlah semua pair, cermin getTokenMarket — JANGAN pairs[0] mentah), quote jual Jupiter OK; (5) gerbang expert cermin expertGate: top-10 holder on-curve <= 35% via getTokenLargestAccounts + getTokenSupply + getMultipleAccounts + is_on_curve (PDA/bonding curve dibuang); data tidak tersedia -> lolos gerbang dasar (fallback bot); (6) **don't-chase (§7): h1 > +100% -> SKIP**, h1 hilang -> SKIP; (7) saldo dompet >= 0,03 SOL; (8) ukuran beli cermin computeBuySize: 20% bankroll, min $1, maks $2,50 hard cap; konsensus >= 2 whale berbeda di mint yang sama dalam 60 detik -> 2x, >= 3 -> 3x.
- **Eksekusi:** `node buy-once.js <mint> <usd>` (satu-satunya penulis keypair di jalur ini), lalu file posisi dilengkapi (entryPriceUsd, decimals, pair + pairAddress, ticker, note sumber whale) supaya sell-watch.js bisa menjaganya. Event `BOT_BELI` ditulis ke `whale-trades.log`; cron `whale-buy-notify` (1 menit) yang membuat sell-watch cron posisi itu + memberi tahu Prawira. Pembelian ganda di mint yang sama dicegah BUY_LOCK (serial) + cek posisi terbuka.
- **Hold mode tetap:** daemon ini TIDAK PERNAH menjual. Penjualan TP (+100%/+300%/+900%) hanya lewat sell-watch cron posisi itu, dengan never-sell-at-loss — sama seperti posisi manual (AMAZON TP1).
- **Uji:** `python3 whale-watch.py --self-test` — putar ulang 5 trigger_detected terakhir dalam DRY-RUN (gerbang jalan sungguhan, buy-once.js --dry-run = TIDAK ada tx, TIDAK ada BOT_BELI, TIDAK ubah state). Hasil 22:28 WITA: is_on_curve benar (dompet agent True, PDA turunan False); debu Dior 0,021 SOL ditolak ukuran; mihao ditolak sudah-ada-posisi; MOON Dior 1 SOL ditolak likuiditas $79 < $5.000 (benar — MOON tinggal $79 likuiditas total saat itu); jalur eksekusi penuh terbukti DRY-RUN OK (ukuran $2,19 dari bankroll $10,94).
- **Perbaikan ikut terbawa 22:26 WITA:** (a) Dexscreener sering menutup koneksi urllib (IncompleteRead/RemoteDisconnected — sementara curl pada URL yang sama berhasil): `http_get_json` (whale-watch) + `get()` (dip-watch) sekarang coba urllib 2x lalu fallback curl; (b) BUG dip-watch.py: cek mint/freeze authority membaca `tokenMeta` yang TIDAK punya field itu (cek selalu lolos = vacuous) — diperbaiki ke field top-level laporan RugCheck (fallback `token.*`), sama seperti gerbang whale.

## Mode Expert Big Win Profit (aktif)

Mode ini menggantikan TP bertingkat biasa. Tujuannya: kunci modal cepat, TAPI biarkan pemenang lari jauh (moonbag) supaya satu token 10x–100x bisa melipatgandakan bankroll.

**Masuk (copy-trade):**
- Beli dasar: **20% dari bankroll saat ini, min $1, maks $2,5** (bukan $1 tetap; naik dari 5%/maks $5 atas perintah Prawira 2026-11-17 21:47 WITA). Ukuran AKHIR (setelah pengali konsensus 2x/3x) juga dibatasi maks $2,5 — tidak ada satu pembelian pun yang melewati $2,5.
- **Sinyal konsensus (keyakinan tinggi):** bila ≥3 dari 12 wallet membeli mint yang sama dalam 60 detik → beli 2x ukuran dasar. Bila ≥5 wallet → 3x ukuran dasar. Total eksposur per mint maks 3x ukuran dasar.
- **Maks 1 posisi terbuka per mint** — pemicu berikutnya untuk mint yang sama di-skip.
- **Gerbang expert (cepat, ~2–3 detik):** mint/freeze dicabut + likuiditas ≥ $5.000 + simulasi jual OK + top-10 holder ≤ 35% + dev holdings ≤ 5% + bundler ≤ 20% (cek via Dexscreener/GMGN; bila data holder/bundler tidak tersedia, lolos dengan gerbang dasar — jangan perlambat copy demi data yang tidak ada). Satu cek gagal = SKIP.
- **Rem saldo:** bila saldo dompet < 0,02 SOL, jangan beli (sisakan untuk fee/jual).

**Keluar — MODE HOLD sejak 2026-11-17 (perintah Prawira: "jangan auto sell dulu, hold sampai ada perintah aku sell").**
Bot sekarang **hanya BELI** — tidak ada jual otomatis sama sekali. Semua posisi ditahan sampai Prawira memerintahkan jual (jual manual via sell-once.js atau perintah di chat). Aturan tangga di bawah ini TETAP TERTULIS sebagai acuan bila mode hold dicabut, tapi saat ini NONAKTIF:
- **+100% (2x):** jual 50% posisi (modal kembali + sedikit profit).
- **+300% (4x):** jual 25% dari posisi awal.
- **+900% (10x):** jual 12,5% dari posisi awal.
- **Sisa 12,5% = moonbag:** trailing stop −40% dari harga tertinggi — TAPI hanya selama harga masih di atas harga masuk. Inilah yang mengejar 20x–100x.
- **Stop loss: NONAKTIF (aturan Prawira 2026-11-17: jangan jual yang sudah minus).** Tidak ada jual otomatis di bawah harga masuk — SL, time exit, trailing, maupun darurat semuanya ditahan bila posisi minus. Posisi ditahan sampai pulih ke harga masuk atau lebih.
- **Time exit:** 24 jam — bila posisi di bawah +100% TAPI masih di atas harga masuk, jual 100%; bila di bawah harga masuk, DITAHAN (aturan jangan-jual-minus); bila di atas +100%, biarkan trailing stop yang bekerja.
- **Exit darurat: NONAKTIF sejak 2026-11-17 18:28 WITA (perintah Prawira: "jangan ulangi ini lagi" — REX terjual otomatis 18:13 WITA oleh cabang ini tanpa pemberitahuan dulu).** Likuiditas < $1.000 atau quote jual hilang → **TAHAN + LAPOR SEKALI** (`HOLD_EMERGENCY`), TIDAK PERNAH jual otomatis — bahkan bila posisi sedang untung. Penjaga jual (sell-watch.js) menandai file posisi (`emergencyActive: true`) dan cron melaporkan sekali ke Prawira; selama darurat aktif, run berikutnya diam (`HOLD_EMERGENCY_ACTIVE`). Begitu likuiditas pulih ≥ $1.000, penanda dihapus. Catatan: token yang benar-benar rug tidak akan pulih; aturan ini mengorbankan perlindungan itu demi memberi kesempatan rebound seperti KATIA. Test 21/21 PASS (2026-11-17).
- Semua profit hasil jual **tetap di bankroll** — ukuran beli berikutnya membesar sendiri (compounding).
- Cara mengaktifkan lagi auto-sell: set `autoSellEnabled: true` di config.json + restart bot (hanya atas perintah Prawira).

**Kecepatan:** polling 5 detik via RPC publik (latensi deteksi 5–30 detik, kadang 429). Jalur naik kelas bila dibutuhkan: RPC berbayar + WebSocket (<2 detik) — butuh biaya + API key, hanya atas perintah Prawira.

## Loop otomatis

1. Setiap 5 menit (default): cek harga semua posisi terbuka → jalankan aturan TP/SL/trailing stop/time-exit bila terpicu.
2. Setiap 30 menit: scan kandidat baru (maksimal 5 kandidat per scan) → jalankan gerbang masuk → beli bila lolos dan masih ada slot posisi + bankroll cukup.
3. Eksekusi swap lewat Jupiter (aggregator): minta quote baru tiap trade, periksa price impact, minimum received, dan fee sebelum submit. Decode + simulasi bila memungkinkan. Catat signature dan verifikasi perubahan saldo yang sebenarnya (processed ≠ confirmed ≠ finalized).
4. Sisakan SOL cukup untuk fee, priority fee, dan pembuatan akun token bila diperlukan.

## Pencatatan dan pelaporan

- **Log setiap trade** di satu file (`~/workspace/memecoin-auto-trader/trades.log`): waktu, mint address, aksi (BUY/SELL), jumlah, harga masuk/keluar, signature, alasan (TP/SL/waktu/darurat), dan bankroll sesudah trade. Perbarui segera setelah aksi selesai.
- **Ringkasan harian ke Prawira:** bankroll, posisi terbuka, trade hari ini (menang/kalah), dan status limit.
- **Lapor langsung** bila: kill switch terpicu, drawdown −30%, satu trade rugi besar, atau token posisi menunjukkan sinyal rug.
- Setiap pola rug / kontrak mencurigakan yang ditemukan dicatat sebagai kasus regresi untuk screening token berikutnya.

## Yang TIDAK dilakukan skill ini

- Tidak menjanjikan profit, tidak menyatakan harga akan naik.
- Tidak memakai dompet utama, tidak meminta seed phrase, tidak menambah dana sendiri.
- Tidak membuka posisi tanpa gerbang masuk, tidak averaging down, tidak memakai leverage.
- Tidak mengirim dana ke siapa pun dan tidak mengikuti "recovery service" apa pun.

## Pelajaran lapangan — 2026-11-17 (KATIA, PUMP, bot ganda, RPC)

- **Stop loss −20% (diperketat dari −30% atas perintah Prawira setelah KATIA terealisasi −59%) — LALU DICABUT 2026-11-17 16:09 WITA atas perintah "Jangan sell yang sudah minus".** SL adalah pemicu, BUKAN jaminan harga: saat crash cepat + jeda cek 5 menit, realisasi bisa jauh di bawah SL. Posisi bot dicek tiap ~5 detik (lebih cepat ketangkap); posisi manual dicek penjaga tiap 5 menit.
- **Rebound setelah SL itu normal — dan inilah alasan SL dicabut.** KATIA dijual di $0,00004243 (−61%) lalu rebound ke ~$0,0000668. Jangan kejar balik masuk tanpa sinyal segar — keputusan SL dinilai dari aturan saat itu, bukan dari harga sesudahnya. RISIKO aturan baru: tanpa SL, token bisa turun sampai $0 dan seluruh $1 per posisi hilang — rebound KATIA bukan jaminan; banyak token mati tidak pernah kembali. Aturan baru: `neverSellAtLoss: true` di config.json + penjaga yang sama di sell-watch.js; harness 82/0 (T2 ditulis ulang + T2c/T2d baru).
- **ATURAN JUAL — TANYA/NOTIFIKASI DULU (koreksi Prawira 2026-11-17 17:43 WITA, pelajaran $AI).** SEBELUM JUAL APA PUN, tanya Prawira dulu di chat WhatsApp, atau minimal beri notifikasi dulu dan tunggu perintahnya — JANGAN PERNAH auto-sell diam-diam. $AI terjual −36% oleh ai-sell-watch tanpa bertanya dan tanpa notifikasi dulu; itu kesalahannya, bukan sekadar aturan SL-nya. Sinyal jual RUGI (SL/time-exit/trailing di bawah harga masuk) TIDAK PERNAH dieksekusi otomatis (dicegah neverSellAtLoss + mode hold). TP untung sesuai ladder yang sudah disetujui Prawira boleh otomatis. Setiap penjaga jual posisi manual baru WAJIB disetel notifikasi-dulu: saat pemicu jual kena, laporkan ke Prawira dan tunggu perintah — jangan langsung jual.
- **MODE HOLD 2026-11-17 16:15 WITA (perintah Prawira: "jangan auto sell dulu, hold sampai ada perintah aku sell").** `autoSellEnabled: false` di config.json — bot HANYA BELI, exit engine nonaktif total (TP, trailing, time exit, darurat semua tidak jalan). Semua posisi ditahan sampai Prawira memerintahkan jual. Berlaku untuk SEMUA posisi bot (bukan hanya Tier 1) — sudah disampaikan ke Prawira bahwa bila maksudnya hanya posisi Tier 1 saja, dia bisa koreksi. Posisi manual $AI TIDAK termasuk mode hold (penjaga jual ai-sell-watch tetap jalan; $AI bukan dari Tier 1) — sudah disampaikan juga. Harness 86 asersi (T-H1 baru: harga 2x + mode hold → tidak ada jual, hold_mode ter-log).
- **PENYEMPURNAAN 2026-11-17 16:40 WITA (perintah Prawira: "Sempurnakan sistem skill trading") — dua aturan baru dari kegagalan hari ini:**
  - **Jangan kejar harga (aturan manual, BERLAKU SEKARANG untuk beli manual/riset):** token sudah +100%/1 jam → jangan masuk di harga pasar; tunggu pullback atau konsolidasi, atau SKIP. (KATIA +170%/1 jam → −59%.)
  - **Gerbang jangan-kejar untuk BOT (RENCANA — BELUM DIIMPLEMENTASI, butuh kode + uji harness):** tambah cek h1 di gerbang beli bot — skip bila token sudah +100% dalam 1 jam (cek cepat via Dexscreener, ~1 detik). Jangan tulis sebagai aktif sebelum kodenya ada dan harness lolos.
  - **Ketahanan RPC (RENCANA — BELUM DIIMPLEMENTASI):** bila RPC utama 429/413 3x berturut-turut, rotasi ke endpoint RPC publik cadangan + log `rpc_throttled`. Deteksi saat ini terdegradasi saat badai 429 (poll_error beruntun di trades.log) — bot selamat karena loop anti-crash, tapi sinyal bisa terlewat. Jangan klaim deteksi "5 detik" saat RPC sedang throttled.
- **blockedMints:** token yang dijual manual atas perintah Prawira masuk ke `blockedMints` di config.json — bot TIDAK PERNAH membeli ulang mint itu (cek di awal handleBuyEvent, log gate_skip "mint diblokir manual"). Terverifikasi live 2026-11-17 (bot menolak beli ulang PUMP).
- **SATU bot saja, SELALU.** pgrep TIDAK BISA DIPAKAI di VM ini (sering lapor "tidak ada" padahal bot jalan) — cek proses HANYA via `ps aux` / `/proc`. Dua bot bersamaan = polling ganda, risiko beli ganda, dan mempercepat habisnya jatah data RPC. watchdog.sh sudah memakai ps aux. Jangan pernah restart bot tanpa memastikan proses lama benar-benar mati (cek via ps aux, bunuh dengan PID persis, bukan pola).
- **RPC publik ada batas data (413 "You have used your data allowance" + 429).** 12 wallet × polling 5 detik itu berat; saat throttle, deteksi menurun (poll_error) tapi bot tetap hidup (loop anti-crash, tidak ada fatal sejak patch 0x1771). 100 wallet TIDAK MUNGKIN di RPC publik — shortlist ~12 terbaik untuk copy live, atau pakai RPC berbayar.
- **Jual manual pakai sell-once.js.** Baca saldo token via JSON-RPC mentah — web3.js getTokenAccountsByOwner dengan jsonParsed RUSAK di versi ini (gagal validasi). Perbaikan yang sama sudah diterapkan di sell-watch.js. Jangan pakai filter {mint, programId} sekaligus — RPC hanya terima SATU filter per panggilan; ambil semua akun lalu saring mint di sisi klien.
- **Sumber wallet insider:** GMGN Smart Money, leaderboard pump.fun, top trader Dexscreener/Birdeye, dashboard Dune, Solscan + RPC langsung — verifikasi PnL terealisasi on-chain sebelum masuk config; jangan pakai wallet dari screenshot tanpa verifikasi. Wallet all-time besar (jutaan dolar PnL) diikuti ratusan ribu orang — fill akan jauh di belakang; wallet 30D/7D yang lebih kecil lebih realistis untuk dicopy.
- **Harness LAMA 76 asersi sudah TIDAK BERLAKU (harness /tmp hilang, dibangun ulang 2026-11-17 ~18:35 WITA).** Harness baru `bash /tmp/ct-test/run-tests.sh` = **53 asersi (31 deteksi + 22 pipeline), PASS=53 FAIL=0**. 4 FAIL lama T-C1/T-C2/T-C3 soal jumlah pembelian adalah ARTEFAK log uji yang menumpuk antar run, BUKAN regresi.
- **Biaya tersembunyi tiket $1:** tiap akun token baru mengunci ~0,002 SOL sewa (rent) — 6 token ≈ 0,012 SOL. Hitung ini dalam P&L; sewa kembali hanya bila akun ditutup.

## Penyempurnaan bot — 2026-11-17 ~18:35 WITA (perintah Prawira: "Terus sempurnakan sistem bot agar lebih canggih, teliti dan terstruktur")

- **FILTER TRANSFER-MASUK — aturan bukti-beli (pelajaran DRILL/WUKONG/bean).** Ketiganya dibeli bot dari sinyal yang ternyata TRANSFER MASUK, bukan beli (SOL keluar = 0, tidak ada program swap; DRILL murni transfer Token-2022), lalu dijual atas perintah Prawira 18:33–18:34 WITA. **Sekarang: transaksi WAJIB dibuktikan PEMBELIAN sebelum handleBuyEvent jalan — ada SOL atau stablecoin (USDC/USDT) yang KELUAR dari wallet dalam tx yang sama.** Transfer masuk murni ditolak dengan reason `transfer_masuk` dan dicatat di trades.log — tidak pernah sampai ke gerbang/beli. Implementasi di `copy-trader/lib/detect.js` (`analyzeTx`), dipakai `runner.js` di `pollWallet` + pertahanan kedua di `handleBuyEvent`. Logika yang sama dengan yang sudah benar di `whale-watch.py` — jangan tulis ulang tanpa membandingkan.
- **Program swap HANYA sinyal, BUKAN gerbang keras — terbukti dari transaksi asli (bukan teori):** transfer bean & WUKONG *mengandung* program pump.fun → gerbang program-swap saja akan MELOLOSKAN transfer palsu; beli asli Q1vec *tidak mengandung* program Jupiter (lewat pump AMM `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`) → gerbang program-swap saja akan MENOLAK beli asli. Jadi: pembayaran (SOL/stablecoin keluar) = gerbang keras; program swap = sinyal yang dicatat saja. Caveat: bila wallet adalah fee payer pada transfer yang ditandatanganinya, `solSpent` kecil (~5.000 lamports) bisa lolos — mitigasi mendatang: ambang `solSpent > 100.000` lamports (beli $1 asli ≈ 13.000.000 lamports).
- **Struktur baru:** `runner.js` (1.139 baris, bersekat §1–§11 dengan header per bagian) + `lib/detect.js` (deteksi murni, bisa diuji tanpa RPC) + `lib/summary.js` (ringkasan harian murni) + `daily-summary.js` (CLI: `node daily-summary.js [YYYY-MM-DD]`). Setiap fungsi: satu tugas, nama jelas. Dokumentasi: `copy-trader/README.md` (ditulis ulang — cara start/stop/restart yang benar, peta seksi, arti log) + `copy-trader/CONFIG.md` (tiap field config: fungsi, nilai aman, akibat bila diubah).
- **Harga SOL dual-source:** Dexscreener + quote Jupiter SOL→USDC; selisih > 5% → log `price_discrepancy`, pakai harga Jupiter. Jangan percaya satu sumber tanpa cek.
- **Ringkasan harian:** tiap pergantian hari bot menulis event `daily_summary` ke trades.log (trigger, beli, skip per alasan, realized PnL, error). Manual: `node daily-summary.js`.
- **Harness baru 53/0 (2026-11-17 ~18:40 WITA):** `bash /tmp/ct-test/run-tests.sh` — 31 deteksi (fixture TRANSAKSI ASLI dari RPC: DRILL/WUKONG/bean ditolak, Q1vec lolos, transfer Token & Token-2022 sintetis, beli USDC, tx error) + 22 pipeline (gerbang, dedup, balance guard, konsensus 2×/3×, exit TP1/hold_minus/hold mode, daily-summary, transfer end-to-end). Semua dry-run, tanpa transaksi asli, tanpa keypair. Verifikasi tambahan: dry-run satu siklus dengan config live (live:false) + 12 wallet Tier 1 asli — 6+ transfer-masuk ditolak langsung (termasuk transfer WUKONG Casino yang dulu dibeli), 1 sinyal beli asli lolos ke dry_run_buy, tidak ada transaksi dikirim.
- **Masih terbuka (bukan blocker restart):** (1) ambang `solSpent > 100.000` lamports untuk fee-payer transfer (desain tercatat, belum diimplementasi); (2) uji jalur `price_discrepancy` (butuh harga Dexscreener vs Jupiter berbeda > 5% secara live — belum terpicu di uji); (3) gerbang jangan-kejar bot (h1 +100% → skip) masih RENCANA, belum diimplementasi; (4) rotasi RPC cadangan saat 429/413 3× berturut-turut masih RENCANA; (5) harness SUDAH dipindah ke lokasi permanen `~/workspace/memecoin-auto-trader/copy-trader/tests/` (run-tests.sh + test-detect.js + test-pipeline.sh) — jangan pakai salinan /tmp lagi.

## Buyback saat harga murah — dip-watch (2026-11-17 19:38 WITA, perintah Prawira: "Pantau token profit yg pernah kita buy... buy back saat harga murah dan jika tidak ada resiko rug")

- **Watchlist (hanya token yang PERNAH untung):** REX (dijual +56% di $0,00000644), mihao (TP1 +100% di ~$0,02302), AMAZON (TP1 +100% di $0,00016551). PUMP (impas) dan token rugi (KATIA#1, $AI, DRILL, WUKONG, bean) TIDAK masuk watchlist.
- **Script:** `copy-trader/dip-watch.py` (check-only, tidak beli) + cron `dip-watch` tiap 15 menit. Cron worker mengeksekusi buyback bila output `TRIGGER`.
- **Gerbang TRIGGER (SEMUA harus lolos):** (1) murah: harga ≤ 0,70x harga jual kita; (2) rug aman: skor RugCheck ≤ 50, tanpa risiko kritis, mint+freeze dicabut; (3) momentum stabil (anti falling-knife): m5 > 0 DAN h1 > −10% — bila m5/h1 tidak tersedia → WAIT; (4) likuiditas ≥ $1.000 DAN quote jual Jupiter OK; (5) saldo dompet ≥ 0,03 SOL; (6) cooldown 24 jam per token (state `dip-watch-state.json`).
- **AMAZON = notify-only (auto=False):** pernah crash −97% + posisi sisa masih terbuka — bila lolos semua gerbang pun hanya dilaporkan ke Prawira, tidak dibeli otomatis. REX + mihao auto-buyback $1.
- **REX = beli HANYA di titik terendah (perintah Prawira 19:43 WITA "Buy back Rex saat titik terendah"):** selain semua gerbang di atas, REX wajib lolos konfirmasi titik terendah — harga sekarang ≥ harga cek 15 menit sebelumnya (jatuh sudah berhenti dan mulai naik lagi). Bila harga masih turun dari cek sebelumnya → WAIT, tidak dibeli walau sudah murah. Riwayat harga disimpan di `dip-watch-state.json` (`prices`, 4 cek terakhir).
- **Eksekusi buyback:** `buy-once.js <mint> 1` → bila file posisi sudah ada (REX closed / AMAZON open), rename dulu dengan suffix tanggal supaya buy-once menulis file baru; mihao tidak punya file posisi (posisi bot di state.json) → buy-once menulis file manual baru (posisi terpisah, TP ladder sendiri). Lalu lengkapi file posisi (entryPriceUsd, decimals, pair, ticker, note "BUYBACK dip") + buat sell-watch cron `<ticker>-sell-watch` (TP ladder) + update `dip-watch-state.json` + lapor ke Prawira (harga buyback vs harga jual, jumlah token, signature).
- **Bukti gerbang bekerja (cek 19:38 WITA):** REX $0,00001224 (h1 +217% — NAIK setelah dijual, bukan murah, WAIT); AMAZON $0,000001404 (murah tapi skor RugCheck 2931 "Low Liquidity" + h1 −97,87% → DIBLOKIR 2 gerbang); mihao tidak ada harga Dexscreener → WAIT (tidak bisa verifikasi).

## Pelajaran dari trade yang profit — 2026-11-17 (perintah Prawira: "Dari yang telah Profit pelajari Skill itu dan simpan di brain memory mu")

Bukti: screenshot Axiom Prawira 19:46 WITA + verifikasi on-chain dompet agent (getTokenAccountsByOwner + getTransaction, signature lengkap).
- **Rex +$0,60 (+28,6% per Axiom; +56% hitungan kami di buyback):** beli ulang di titik rendah setelah shakeout, jual manual ke kekuatan. Pelajaran: entry kedua (buyback) yang untung — entry pertama kena shakeout aturan darurat. Sabar + re-entry > kejar harga.
- **Millionaires +$0,23 (+47,2%, 11 menit):** sinyal akumulasi whale Dior (7x beli) → lonjak cepat → AMBIL PROFIT CEPAT. Dijual manual Prawira 18:52:33 WITA (7.162,78 token → +0,009945 SOL, tx `dAVouHKpMPvMAWqWjCSXPrCJsH1WmLsmwA7vx1evPbW9DKAz5ZU7JPtKiLck8Qnc7oQ56UdyPbPwszx5uyj3Sej`). Pelajaran: token sinyal whale melonjak +40–50% dalam hitungan menit lalu memudar — itu zona ambil profit, bukan zona tahan-menunggu-2x.
- **Q1vec / "cyber attack" (ca) +$0,22 (+22%, setelah ~4 jam chop):** beli copy-trade Tier 1, harga mondar-mandir 0,95–1,20x ~4 jam tanpa lari. Dijual manual Prawira 19:42:46 WITA (11.453,75 token → +0,016199 SOL, tx `4N3xB7YCBxa97Zj73ioP5inx1Azj71UAkrWU5Fepcd61325dCMcY4exEgmU97wS9fJYj2fJkHxD9s4eRnMSYgp26`). Pelajaran: token yang chop berjam-jam tanpa lari — ambil +20% saat datang, jangan tunggu 2x yang mungkin tidak pernah datang.
- **Pump +$0,01 (+0,5%):** keluar impas = modal selamat. Bukan kegagalan.
- **WUKONG −$0,10 (−9,3%):** sinyal transfer palsu — sudah diperbaiki filter transfer-masuk 18:35 WITA.
- **Refund sewa (rent):** Prawira menutup 7 akun token kosong 19:44:46 WITA (tx `Q5iijj8cgEJcoGyWqNos3GWBfpLFbu3tSRFXNQpovatXcSkVYTnN7aRQNDjbZSQkViKTcLwXHAsj97ZvTmv3T27`) → +0,010609 SOL (~$0,77) kembali ke dompet. Pelajaran: tutup akun token kosong setelah jual habis — tiap akun ~0,002 SOL. (Aliran masuk kecil +0,004534 SOL 18:11:31 kemungkinan refund sewa juga — belum teridentifikasi pasti.)
- **Aturan baru — ambil profit dini (TP0, USULAN — BELUM diimplementasi di sell-watch.js):** kebanyakan memecoin kecil puncaknya +20–50% lalu memudar; hanya sedikit yang lari ke 2x+ (AMAZON 2,5x dalam 6 menit, mihao 10x, REX 3x). Usulan: TP0 = jual 25% di +25% (menangkap lonjakan tipe Millionaires/REX), sisa 75% tetap ikut ladder +100%/+300%/+900%. **Aturan chop:** posisi yang mondar-mandir ±20% dari entry >4 jam tanpa lari → keluar saat pop +20% berikutnya (keputusan manual / notifikasi +20%). Menunggu persetujuan Prawira sebelum mengubah sell-watch.js.
- **Catatan pencatatan:** Prawira juga trading manual dari HP (Axiom) di dompet agent yang sama — penjualan Millionaires + Q1vec tidak tercatat di log bot/cron manapun. State bot + file posisi harus dicek silang dengan on-chain (getTokenAccountsByOwner) secara berkala; penjualan manualnya dicatat sesudahnya (state.json Q1vec dihapus 19:49 WITA, file Millionaires ditutup).
