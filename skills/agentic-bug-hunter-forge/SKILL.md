# Agentic Bug Hunter Forge — Menciptakan Skill Bug Bounty Hunter Paling Canggih

Versi 1.0.0 (2026-11-20). Dibuat atas perintah Prawira: satu skill yang MENCIPTAKAN skill bug bounty hunter paling canggih yang belum pernah ada — hunter agentic AI yang berburu, membuktikan, dan belajar sendiri.

## Kejujuran dulu
- Ini **bukan** skill pihak ketiga "Agentic-Bug-Hunter" (yang ditunda Prawira 2026-11-17, status CAUTION — jangan install tanpa izinnya, jangan jalankan install_tools.sh-nya, jangan set key FLUXION/ORCAROUTER/REQUESTY yang belum terverifikasi). Skill ini **buatan Papao sendiri dari nol**, murni prosedur kerja, disusun dari metode yang sudah terbukti di 37 temuan valid Prawira.
- Tidak ada klaim benchmark, tidak ada klaim "menjadi" model lain. Yang canggih di sini adalah **kombinasinya** — dan kombinasinya harus dibuktikan lewat hasil tiap wave, bukan lewat nama.

## Apa yang membuat hunter ini paling canggih
Tidak ada satu pun skill di luar sana yang menggabungkan kesembilan ini sekaligus:
1. **Mesin multi-agen SPIDER** — koordinator sebagai otak, hunter paralel per program, validator independen yang memeriksa tiap kandidat. Hunter tidak pernah menilai pekerjaannya sendiri.
2. **Evidence-first gate** — sebuah temuan dihitung Done HANYA bila ada hunt file + PoC yang bisa di-run ulang. Tanpa keduanya, itu bukan temuan — itu hipotesis.
3. **Verifikasi live-state** — sebelum dihitung, buktikan di kondisi live: RPC on-chain, probe API live, status program saat ini. Jangan percaya klaim dari baca kode saja.
4. **Kalibrasi severity yang jujur** — tidak pernah menggelembungkan severity. Kepercayaan triage adalah aset jangka panjang: satu laporan yang digelembungkan merusak sepuluh laporan berikutnya.
5. **Learning loop dari verdict triage** — setiap putusan (diterima / ditolak / duplikat / known issue) dicatat dan mengubah kalibrasi hunter: checklist duplikat bertambah, ambang severity diperbaiki, pola yang ditolak tidak diulang.
6. **Memori deduplikasi lintas program** — audit resmi + daftar known issue dicek SEBELUM PoC dibuat (pelajaran UMA hunt2: Medium gugur sebagai duplikat setelah PoC selesai — buang waktu).
7. **Mesin kecepatan** — API/CLI langsung sebelum browser; baca paralel; ronde dibatasi waktu (10–15 menit); cache konteks stabil.
8. **Notifikasi seketika** — temuan tervalidasi langsung disampaikan ke Prawira saat itu juga, tidak pernah dibatch menunggu akhir wave.
9. **Self-improvement loop** — setiap wave menulis pelajarannya kembali ke skill hunter itu sendiri, jadi wave berikutnya mulai lebih pintar.

## Cara kerja Forge (menciptakan hunter untuk satu program)
1. **Intake.** Terima link program / perintah "hunt X". Catat: nama program, URL scope, reward table, cara lapor, syarat reputasi/deposit, known issues, link audit.
2. **Riset program.** Verifikasi program masih aktif, reward masih berlaku, dan cara lapor yang benar dari SUMBER RESMI (jangan tebak alamat email dari pola — pelajaran Pacifica: security@pacifica.fi tidak ada, yang benar ops@pacifica.fi).
3. **Tulis brief hunter.** Satu file brief per program: scope, permukaan yang belum diuji, hipotesis terkuat, audit yang sudah dibaca, known issues yang harus dihindari, dan definisi Done (hunt file + PoC + duplicate check).
4. **Luncurkan wave.** Koordinator menyebar hunter paralel; validator independen memeriksa tiap kandidat; temuan tervalidasi dilaporkan ke parent saat itu juga.
5. **Arsipkan.** Tiap temuan valid masuk `~/workspace/bug-bounty-muse/valid-findings-archive.md` dengan total yang dikoreksi. Total yang salah lebih buruk daripada total yang tidak ada.
6. **Belajar.** Setelah wave selesai, tulis verdict + pelajaran ke skill ini dan ke arsip: apa yang berhasil, apa yang ditolak triage dan kenapa, pola apa yang harus dicek lebih dulu lain kali.

## Loop hunter (tiap kandidat temuan)
1. **Recon** — baca kode, docs, dan audit terkait permukaan itu.
2. **Hipotesis** — tulis klaimnya dalam satu kalimat + dampaknya + kenapa itu bug, bukan by-design.
3. **Duplicate check** — cari di audit resmi, known issues program, dan arsip temuan sendiri. Bila sudah known/duplikat: GUGUR, catat alasannya, jangan buang waktu ke PoC.
4. **PoC** — bukti yang bisa di-run ulang (Foundry/Hardhat/Jest/live probe). PoC yang tidak bisa diulang = bukan bukti.
5. **Validasi independen** — validator lain me-run ulang PoC dan memeriksa klaim dari nol.
6. **Laporan** — ikut `~/workspace/bug-bounty-muse/report-writing-guide.md`: judul spesifik, ringkasan, severity jujur + CVSS, langkah repro dari nol, PoC, dampak realistis, rekomendasi fix, info tambahan; satu bug per laporan.
7. **Notifikasi** — sampaikan ke Prawira segera setelah tervalidasi.
8. **Belajar** — catat verdict triage begitu ada; perbarui kalibrasi.

## Aturan berdiri (tidak boleh dilanggar)
- **Satu root cause = satu laporan.** Jangan pernah double-report satu root cause ke dua program (contoh: UMA ↔ Across overlap).
- **Program yang minta bayar per report/submit = dibuang dari daftar.** Jangan pernah bayar.
- **Tidak ada submit tanpa perintah eksplisit Prawira per temuan** (dia yang submit sendiri, atau dia yang memerintahkan submit). Pengecualian Flex: temuan Flex difile di tier High form Mantis DENGAN severity jujur + CVSS dinyatakan dan minta re-grade — dan tiap temuan Flex baru tetap tunjukkan trade-off-nya dulu dan tunggu perintah eksplisitnya.
- **Jangan sentuh dana mainnet, jangan sign transaksi, jangan pakai akun palsu.** Hunt read-only di mana program mensyaratkannya; PoC di fork/testnet.
- **Gmail SENT ≠ delivered** — selalu cek bounce mailer-daemon setelah kirim laporan via email.
- **Standar 100% benar:** langkah dihitung hanya bila terverifikasi; laporan hanya berisi fakta terkonfirmasi; bila belum terverifikasi, katakan begitu.

## Skill yang dirangkai Forge ini
- `spider-coordinator`, `spider-task-executor`, `spider-task-validator` (mesin multi-agen)
- `muse-bug-bounty`, `bug-bounty-specialist`, `recon-and-methodology` (metodologi hunt)
- `self-improvement-loop` (belajar dari tiap wave), `skill-curator` (menjaga library tetap ramping)
- `bug_bounty_finding_alert` (notifikasi temuan tervalidasi)
- `~/workspace/bug-bounty-muse/report-writing-guide.md` (standar laporan)
- `~/workspace/bug-bounty-muse/valid-findings-archive.md` (memori temuan + verdict triage)

## Kapan dipakai
Dipakai setiap kali Prawira mengirim link bounty baru, memerintahkan hunt program tertentu, atau memerintahkan wave baru — dan setiap kali hunter perlu ditingkatkan setelah verdict triage. Forge adalah skill yang menciptakan dan memperbaiki hunter; hunter adalah skill yang mengeksekusi perburuan.

---
*Audit: skill ini murni prosedur kerja (dokumen Markdown, tanpa kode, tanpa install script, tanpa pemanggilan eksternal, tanpa kredensial) — AUDITED SAFE oleh Papao, 2026-11-20.*
