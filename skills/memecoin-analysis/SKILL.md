# Analisis Trading Memecoin — Mencari 100x (10.000%)

Skill analisis untuk menemukan memecoin yang berpotensi naik sangat besar (100x) SEDINI mungkin, dan mengelola trade-nya supaya profit tidak kembali jadi nol. Skill ini MEMAKAI `memecoin-trading` sebagai gerbang keamanan dan `memecoin-auto-trader` untuk aturan eksekusi/risiko.

## Jujur dulu

- **Tidak ada skill yang bisa menjamin 10.000%.** 100x hanya terjadi pada token yang masuk SANGAT awal + narasi meledak + tidak rug — dan untuk setiap 1 token yang 100x, ada ratusan token yang −99% atau rug.
- Yang BISA dilakukan skill ini: (1) menemukan kandidat 100x lebih awal dari kerumunan, (2) membuang kandidat yang hampir pasti rug/scam sebelum uang masuk, (3) mengatur exit supaya kalau tokennya moon, profitnya benar-benar terkunci — bukan balik ke nol.
- Anggap setiap taruhan moonshot sebagai tiket lotre: ukuran kecil, banyak tiket, kerugian per tiket sudah diterima sejak awal.

## 1. Deteksi dini — dari mana kandidat datang

- **Radar wallet insider / smart money (copy-trade):** lacak wallet insider (rat_trader) dan smart money (smart_degen) yang sudah terbukti profit konsisten. Pembelian mereka di token baru = SINYAL untuk dianalisis, BUKAN perintah beli otomatis. Alasannya: insider beli duluan di harga paling bawah — yang ikut belakangan membeli lebih mahal dan sering jadi exit liquidity mereka. Jadi aturan radar: wallet terpantau beli → jalankan semua cek §2 + tabel skor §3 pada token itu → beli hanya bila token lolos DAN kita masih cukup awal (bukan setelah harga sudah naik jauh). Jangan pernah auto-beli setiap gerakan wallet insider tanpa analisis. Token yang supply-nya dikuasai insider tetap DITOLAK (§2), walau yang beli wallet terkenal.
- **pump.fun baru launch:** pantau token yang baru dibuat; periksa progres bonding curve, kecepatan pembelian awal, dan riwayat creator (creator dengan jejak rug = tolak).
- **Dexscreener new pairs / Birdeye trending:** pair baru dengan volume naik cepat + holder bertambah; bedakan volume organik dari wash trading (peserta unik, ukuran trade bervariasi, wallet berulang).
- **Migrasi (graduation):** token yang baru lulus bonding curve ke AMM (PumpSwap sekarang) — verifikasi transaksi migrasi dan pool tujuannya benar, bukan pool palsu.
- **Narasi:** tema yang sedang panas (tren X/Telegram) TAPI mint address konsisten di semua sumber; narasi tanpa mint yang terverifikasi = tolak.

## 2. Analisis on-chain — yang membedakan 100x dari rug

### Struktur holder (paling penting)
- Kelompokkan holder berdasarkan wallet owner (satu wallet bisa punya banyak akun token).
- **Bundler/sniper:** banyak wallet kecil yang didanai dari satu sumber yang sama + beli bersamaan di detik pertama = distribusi palsu. Tolak bila dominan.
- **Dev + insider:** holding developer dan wallet terhubung (sumber dana sama, transfer sinkron) harus kecil dan tidak bisa dump ke likuiditas yang ada.
- **Top 10 holder** (setelah mengecualikan pool, bonding curve, burn, vesting): makin tersebar makin baik. Konsentrasi besar di sedikit wallet terhubung = tolak.
- **Pertumbuhan holder:** holder baru harus tumbuh bersama transaksi beli yang nyata; airdrop dan pemecahan wallet bisa memalsukan angka.

### Keamanan token
- Mint authority aktif + holding dev besar = tolak. Freeze authority aktif, permanent delegate, transfer hook, atau upgrade authority yang belum terjawab = tolak.
- Token-2022: periksa transfer fee dan batasan lain — fee besar memakan profit moonshot.
- **Test sell:** minta sell quote + simulasi; bila lolos, beli minimal lalu jual minimal sebagai bukti sellability saat ini. Gagal jual = tolak, tanpa kecuali.
- RugCheck + Solscan sebagai screening; skor bagus bukan jaminan — baca tiap temuan dan timestamp-nya.

### Likuiditas
- Pool nyata, reserve, umur pool, dan kedalaman eksekusi untuk ukuran order yang direncanakan.
- LP lock/burn harus terverifikasi on-chain (bukan screenshot/badge). LP tidak terkunci = pengendali bisa tarik kapan saja.
- Market cap BUKAN ukuran uang yang bisa ditarik; periksa price impact masuk DAN keluar.

### Momentum dan flow
- Rasio beli/jual, jumlah buyer unik per jam, ukuran trade rata-rata, dan wallet besar yang masuk/keluar.
- Sinyal sehat: buyer unik bertambah, holder bertambah, harga bertahan di atas level sebelumnya setelah koreksi kecil.
- Sinyal bahaya: volume naik tapi holder stagnan (wash), holder besar mulai jual bersamaan, likuiditas menipis.

## 3. Skor kandidat (pakai sebelum beli)

Beri nilai tiap kandidat; beli hanya yang lolos semua baris WAJIB:

| Kriteria | Wajib | Yang dicari |
|---|---|---|
| Identitas mint terverifikasi | Ya | Mint sama di semua sumber |
| Authority aman | Ya | Mint/freeze dicabut atau tidak berbahaya |
| Holder tersebar | Ya | Top 10 (non-infra) kecil, bundler/sniper minimal |
| Likuiditas terverifikasi | Ya | Pool nyata, LP lock/burn on-chain |
| Bisa dijual (test sell) | Ya | Sell quote + simulasi lolos |
| Momentum | Ya | Volume + holder + buyer unik naik |
| Narasi | Tidak | Tema panas = nilai tambah, bukan alasan beli |

Satu baris WAJIB gagal = jangan beli, tidak peduli seberapa panas narasinya.

## 4. Sizing moonshot — cara bertaruh 100x tanpa bangkrut

- **Ukuran tiket lotre:** 1–2% dari bankroll per kandidat (default). Kerugian per tiket sudah diterima di awal.
- **Banyak tiket kecil, bukan satu taruhan besar.** Probabilitas 100x per token sangat kecil; yang menaikkan peluang adalah jumlah kandidat berkualitas yang dicoba, bukan ukuran satu taruhan.
- **Jangan all-in** satu token dengan alasan "yang ini pasti". Tidak ada yang pasti.
- Pisahkan bankroll moonshot dari bankroll compounding biasa; jangan campur.

## 5. Exit moonshot — cara menangkap 100x tanpa balik ke nol

Kebanyakan orang yang "pernah 100x" pulang dengan nol karena tidak pernah menjual. Aturan default:

- **Jual modal awal saat +100% (2x):** setelah ini, posisi yang tersisa adalah "uang rumah" — risiko modal sudah nol.
- **Jual 25% lagi saat +500% (5x).**
- **Jual 25% lagi saat +2000% (20x).**
- **Sisa 25% dibiarkan jalan** dengan trailing stop −40% dari harga tertinggi (lebih longgar dari trade biasa, supaya tidak tercut oleh koreksi normal moonshot).
- **Exit darurat kapan saja:** sinyal rug (likuiditas ditarik, mint tambahan, freeze, dump terkoordinasi) → jual segera, jangan tunggu level TP.
- Catat setiap penjualan: harga, jumlah, alasan, dan sisa posisi.

## 6. Pola penipuan yang harus ditolak

- Token copycat yang meniru token lain; mint address berbeda = token berbeda.
- "Kirim SOL untuk dilipatgandakan", airdrop palsu yang meminta signature, layanan recovery yang meminta key/pembayaran di muka.
- Alur trading yang meminta setApprovalForAll — itu approval NFT di EVM, BUKAN persyaratan swap Solana.
- Transaksi yang meminta izin, transfer, perubahan authority, atau delegate di luar trade yang dimaksud.
- Grup/Channel yang memompa token sambil holder besar diam-diam menjual (periksa flow wallet, jangan percaya chat).

## 7. Alur analisis lengkap (checklist)

1. Temukan kandidat (pump.fun / Dexscreener / Birdeye).
2. Verifikasi mint address di 2+ sumber independen.
3. Jalankan semua cek on-chain (§2) — authority, holder, likuiditas, test sell.
4. Isi tabel skor (§3); satu WAJIB gagal = buang.
5. Tentukan ukuran tiket (1–2% bankroll), harga masuk, dan semua level exit (§5) SEBELUM membeli.
6. Beli lewat Jupiter (quote baru, cek price impact + slippage), catat signature + saldo.
7. Pantau dan jalankan exit otomatis; laporkan hasil ke Prawira.
8. Simpan pola rug/kandidat gagal sebagai kasus regresi untuk screening berikutnya.

## 8. Riset sinyal insider + whale — metodologi (2026-11-17)

Riset wallet adalah fondasi copy-trade: sinyal yang bagus datang dari wallet yang benar, bukan dari daftar yang asal comot. Metodologi ini dibangun dari riset 100 wallet (103 unik terverifikasi) + 12 whale 2026-11-17.

### 8.1 Dari mana wallet ditemukan — sumber yang jalan vs yang mati
- **JALAN: KOL Explorer (kolexplorer.com)** — peringkat realized PnL 30 hari, sumber utama untuk 100 wallet + 12 whale. Data PnL terealisasi, bukan klaim.
- **MATI (jangan buang waktu lagi):** GMGN web/API (Cloudflare 403, termasuk OpenAPI demo key), Birdeye (401 tanpa X-API-KEY), Dexscreener (tidak ada endpoint top-traders), pump.fun frontend API (Cloudflare), Dune (dashboard tidak pernah render), Bitquery GraphQL (terkunci, butuh API key), Solscan API Pro (401). Bila salah satu sumber ini hidup lagi, verifikasi ulang sebelum pakai.
- **Verifikasi wajib:** tiap alamat dicek via RPC publik Solana — saldo SOL > 0, ada aktivitas terakhir, dan (untuk whale) akun token aktif. Alamat tanpa aktivitas = dorman, bukan sinyal. Jangan pakai wallet dari screenshot tanpa verifikasi on-chain.

### 8.2 Tingkatan kualitas sinyal (pakai sebelum bereaksi)
| Tingkat | Ciri | Tindakan |
|---|---|---|
| **A — Akumulasi nyata** | Beli berulang (≥3x) dengan ukuran membesar atau stabil dalam SOL nyata; contoh: 13fK beli AMAZON 3x total ~15 SOL; Dior beli Millionaires 7x, terakhir 0,131 SOL | Sinyal terkuat — analisis token (§2–§3), pertimbangkan beli manual |
| **B — Beli tunggal** | Satu beli, ukuran SOL wajar, wallet belum pernah beli token itu | Pantau; beli hanya bila token lolos semua cek §2–§3 |
| **C — Debu (dust)** | Beli 10 token, atau top-up 0,021 SOL berulang; contoh: Cap+Limfork SAKURA 10 token, Cap+Johnson PEPEDOOM/Jinxel 10 token, Dior 1B 0,021 SOL ×14 | BUKAN sinyal — jangan beli, jangan laporkan berulang |
| **D — Transfer palsu** | Saldo token naik tapi SOL keluar = 0, tidak ada program swap | BUKAN beli — tolak (pelajaran DRILL/WUKONG/bean, lihat memecoin-auto-trader) |

- **Konsensus memperkuat — tapi konsensus debu tetap debu.** ≥2 wallet beli mint yang sama dalam 60 detik = keyakinan lebih tinggi (Cap+Johnson, Cap+Limfork). Tapi bila masing-masing hanya beli 10 token, itu tetap tingkat C — jangan tertipu label "konsensus".
- **Ukuran whale yang penting:** Frank degods paling mungkin diikuti (median hold 2,1 jam, posisi rata-rata $18.400, $PAID +$184,6 ribu); Unipcs posisi rata-rata terbesar ($46.200); 13fK sekali beli terbesar (~148 SOL per koin). Whale hold-nya jam-an, bukan detik-an — sinyal whale lebih santai dari Tier 1.

### 8.3 Caveat yang wajib diingat
- **Scalper ultra-cepat:** kebanyakan insider hold median 7–60 DETIK. Copy PICKS-nya, bukan timing exit-nya — bot poll 5 detik tidak bisa meniru exit mereka.
- **Wallet jackpot historis kebanyakan DORMAN:** dari riset pump.fun, hanya snowball + j1oeQo yang aktif 7 hari terakhir. PnL all-time jutaan dolar tidak berarti aktif sekarang.
- **PnL terkontaminasi:** PnL Bitquery ~26% profit trading asli, 51% creator-gifted, 13% wash loop. PnL besar ≠ skill trading.
- **Satu minggu bagus tidak bertahan:** Cented 30D +$302 ribu tapi 7D −$149 ribu; Dior 90D −$70,6 ribu. Nilai wallet dari 30D, verifikasi ulang tiap kali daftar diganti.
- **Jangan kejar harga (§7 aturan):** token sudah +100%/1 jam = SKIP atau tunggu pullback. 1B ditolak 2026-11-17 (h1 +352% lalu +1012%, MC $4,6 juta → $11,3 juta, RugCheck 24.486) walau Dior beli 14x — 14x debu tetap debu + chase. AMAZON diterima (h1 +81%, di bawah garis +100%, RugCheck 1) — lalu TP1 membuktikan sinyalnya.

### 8.4 Alur riset wallet baru (checklist)
1. Tentukan sudut riset (GMGN / pump.fun / Dexscreener-Birdeye / Dune-Solscan / KOL Explorer) — jalankan paralel, 1 subagent per sudut.
2. Kumpulkan kandidat dengan bukti PnL terealisasi (bukan klaim, bukan screenshot).
3. Verifikasi tiap alamat via RPC publik (saldo + aktivitas terakhir).
4. Buang: dorman (>30 hari tanpa aktivitas), creator (bukan trader), gift/dump mencurigakan, PnL terkontaminasi.
5. Kelompokkan Tier 1 (terkuat) / Tier 2 / Tier 3; simpan di `~/workspace/memecoin-auto-trader/wallet-lists-100.md` (100 wallet) dan `wallet-lists-whale-12.md` (12 whale).
6. Ganti daftar bot HANYA atas perintah Prawira; 12 teratas masuk config (batas RPC publik), sisanya notify-only atau cadangan.

## Referensi

- pump.fun: https://pump.fun/
- Dexscreener: https://docs.dexscreener.com/
- Birdeye: https://docs.birdeye.so/
- RugCheck: https://rugcheck.xyz/
- Solscan: https://solscan.io/
- Jupiter: https://dev.jup.ag/

## Pelajaran lapangan — 2026-11-17 (KATIA, $AI)

- **Filter lotre Prawira: MC < $15.000** untuk tiket $1 (PUMP di MC $1,27 miliar sudah mustahil 10x; token MC $8–12 ribu hanya butuh ~$80–120 ribu untuk 10x).
- **Momentum adalah baris wajib yang paling sering gagal — DAN ATURANNYA DIPERKETAT 2026-11-17 16:40 WITA (pelajaran $AI).** Token yang baru graduate sering −50–70% dalam 1 jam pertama; pantulan 5 menit (+2–3%, buys > sells) belum membuktikan pembalikan. **Aturan baru: momentum LULUS hanya bila m5 positif DAN h1 positif, atau h1 ≥ −10% DAN naik pada 2 cek berurutan DAN harga di atas level 1 jam lalu.** $AI dibeli dengan h1 −48% → −8% (masih negatif) hanya karena pantulan 5 menit bertahan — di bawah aturan baru, $AI DITOLAK. Tokennya tidak pernah naik di atas harga masuk (tertinggi 0,88x) lalu dijual SL −36%. Jangan ulangi: "membaik" bukan "positif".
- **Jangan kejar harga (pelajaran KATIA, aturan baru 2026-11-17).** Bila token sudah +100% dalam 1 jam terakhir, JANGAN masuk di harga pasar — tunggu pullback ke dalam 20% dari low 1 jam, atau konsolidasi datar (±5% selama 15 menit). Bila tidak ada pullback/konsolidasi, SKIP. KATIA dibeli di +170%/1 jam (mengejar) lalu jatuh −61% dan terjual SL −59%.
- **Satu baris wajib gagal = tolak.** Jangan memaksakan kandidat "terdekat" — laporkan terus terang + alasan gagalnya. $AI (Attack Inu, MC $8.167) lolos 5/6 baris, momentum borderline, dibeli $1 hanya karena cek momentum kedua bertahan (+1,85%, buys 3 vs sells 1). **Di bawah aturan momentum yang diperketat, $AI seharusnya DITOLAK (h1 masih negatif) — pembelian itu adalah kesalahan aturan lama, bukan nasib buruk.**
- **LONG ditolak 2026-11-17:** momentum gagal jelas (−73% 1 jam) + holder terbesar 21,31% tidak terverifikasi (kemungkinan vault bonding curve yang sudah ditutup, tapi RPC 429 menghalangi verifikasi) — ketidakpastian = tolak.
- **Celah trailing stop moonbag (pelajaran mihao, MASIH TERBUKA — belum terverifikasi penyebabnya).** Moonbag mihao jatuh ~90% dari puncak 10x ke ~harga masuk (~$5 → ~$0,51) tanpa trailing stop −40% mengeksekusi. Penyebab belum dipastikan (kemungkinan retrace terjadi setelah mode hold dimulai 16:18 WITA, atau cek harga gagal berurutan saat badai RPC 429). Saat mode hold dicabut, verifikasi dulu eksekusi trailing stop di harness dengan retrace cepat yang disimulasikan — jangan andalkan trailing stop yang belum terbukti jalan.
