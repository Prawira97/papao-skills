# Mengerjakan Seluruh Jenis Task Web3: Airdrop / Testnet / Mining / Waitlist

Versi 1.0.0 (2026-11-20). Dibuat atas perintah Prawira: satu skill untuk mengerjakan SELURUH jenis task Web3 — airdrop, testnet, mining, waitlist, quest, check-in, klaim, dan apa pun yang berkaitan dengan Web3 — dengan cepat, benar, dan aman.

## Kapan dipakai
Dipakai setiap kali Prawira mengirim link atau perintah yang berkaitan dengan Web3: airdrop, testnet, mining, waitlist, quest harian, check-in, klaim token, faucet, bridge, swap, mint, referral, atau proyek baru yang belum dikenal. Skill ini adalah playbook eksekusinya; `evm-wallet-airdrop` tetap dipakai untuk aturan dompet EVM secara detail.

## Aturan berdiri (tidak boleh dilanggar)
- **Dompet utama hanya untuk connect BARU.** EVM `0xD64d849BD85f3Ff71208EEbC4A08F4785476B76a` / Solana `95ubFWyurr4GAxPjS3z15HjDnRX3SPNtnrdyRcBjRbY6`. JANGAN PERNAH pakai dompet agen (Solana BupM... / EVM 0xfEa9...) untuk connect baru. **Pengecualian:** Ryfinite tetap pakai wallet-nya yang sudah terhubung (`0xe9fbf6...4bc2e4`) karena Passport di-mint ke wallet itu.
- **Prawira yang connect wallet + approve transaksi; Papao tidak pernah sign, tidak pernah pegang seed phrase.** Papao hanya mengarahkan halaman dan menyiapkan langkahnya.
- **Swap / aksi yang memakai dana asli = butuh izin eksplisit per aksi.** Check-in, klaim tanpa signature, dan social task gratis boleh dikerjakan langsung atas perintah umumnya.
- **Jangan pernah kirim dana nyata ke presale / mainnet yang belum terverifikasi.** Poin testnet bukan jaminan token.
- **Jangan buat akun baru bila dia sudah punya akun.** Selalu cek status akun yang ada dulu (login dengan cara yang tersedia).
- **Login adalah tugas Papao** (perintah 2026-11-20 14:21): pakai saved login, Google OAuth, sesi tersimpan; hanya langkah yang mustahil tanpa password yang dia ketik sendiri yang boleh diminta, sekali saja.
- **X tidak bisa dari cloud browser** (x.com HTTP 403). Task X dikerjakan lewat Simular Box (box "main") setelah login — atau dari HP Prawira sendiri bila login box sedang ter-limit.
- **Satu temuan = satu laporan; jangan laporkan "selesai" dari tanda terkirim saja.** Verifikasi hasil di UI / on-chain sebelum melapor (pelajaran Pacifica: Gmail SENT ≠ delivered).

## Alur kerja universal (semua jenis task)
1. **Kenali proyeknya.** Buka link resmi, catat: nama, URL dashboard, chain, jenis task, deadline, dan syaratnya. Bila proyek belum pernah diteliti, tulis laporan riset singkat di `~/workspace/airdrops/research-YYYY-MM-DD.md` (fakta + sumber URL tiap klaim).
2. **Verifikasi legitimasi.** Tim (publik/anonim), pendanaan (terverifikasi/belum), audit, kontrak terverifikasi, kanal resmi. Tandai merah: presale berbayar tak terverifikasi, mainnet belum dikonfirmasi, janji return pasti, tim anonim + minta deposit.
3. **Cek akun yang ada.** Login dengan cara yang tersedia; catat username, saldo poin, status (passport minted? wallet terhubung yang mana? referral berapa?). Jangan buat akun duplikat.
4. **Kerjakan tangga task dari yang termurah:** check-in harian → quest sosial gratis → klaim yang ready → posisi mining/launchpool → task on-chain testnet → referral (hanya teman asli, jangan pernah fake) → waitlist.
5. **Verifikasi tiap hasil.** Saldo berubah? Status quest jadi done? Transaksi terkonfirmasi? Screenshot/state check sebelum melapor.
6. **Laporkan hasil akhir singkat** (apa yang selesai, angka sebelum → sesudah, apa yang gagal + kenapa + jalan keluarnya). Lalu **otomatisasi yang berulang** dengan cron harian bila task-nya harian.

## Playbook per jenis task
- **Check-in harian:** kerjakan tiap hari (cron ~08:52 WITA); catat streak; klaim reward-nya bila ready tanpa signature/bayar.
- **Quest sosial (X / Telegram / Discord):** like, repost, komen, follow, join. X lewat Simular Box setelah login; bila X sedang rate-limit, kerjakan dari HP Prawira atau tunggu limit reda — jangan spam retry.
- **Klaim (claim-ready):** klaim hanya bila tanpa signature/pembayaran; catat gross → net (fee + burn) dan saldo sebelum → sesudah.
- **Mining / Launchpool / staking Gems-poin:** kunci poin sesuai rencana (catat estimasi reward + tanggal matang); jangan commit semua bila dia belum memerintahkan; pantau posisi sampai matang lalu klaim.
- **Faucet testnet:** ambil hanya dari faucet resmi; catat chain ID dan jumlah per hari; jangan pernah bayar untuk token testnet.
- **Testnet quest (bridge / swap / mint / deploy):** kerjakan hanya di testnet resmi dengan token faucet; tiap transaksi butuh izinnya bila ada biaya; simpan hash transaksi sebagai bukti.
- **Waitlist:** daftar dengan email/wallet yang benar; verifikasi email bila diminta; catat posisi/nomor antrean bila ada.
- **Referral:** bagikan link asli miliknya; hanya teman asli yang join; jangan pernah buat akun palsu (melanggar aturan proyek dan berisiko banned).
- **Airdrop checker / eligibility:** cek dengan wallet-nya yang benar; jangan connect wallet ke situs checker yang tidak resmi.

## Perkakas
- **Cloud browser** untuk kebanyakan dApp (login Google, dashboard, klaim). **Simular Box** untuk semua task X (Chrome box; login 24/7, box hibernate di antara task untuk hemat kredit; `box_save` setelah login pertama; bangunkan minimal 1x per 2 minggu supaya box tidak dihapus).
- **Cron harian** untuk check-in + klaim rutin (contoh: `ryfinite-daily-checkin` tiap pagi ~08:52 WITA).
- **Riset per proyek** di `~/workspace/airdrops/research-YYYY-MM-DD.md` — baca lagi sebelum mengerjakan proyek yang sama.
- **Status proyek aktif** (2026-11-20): Ryfinite (QEN berakhir ~3 Des 2026; posisi mining 462 Gems matang ~27 Nov 2026), DogeOs (STOP atas perintahnya 14:12 — jangan lanjut tanpa perintah), Elyon (Season 1 live, 7 langkah, 0 selesai), Forest Road Vault (belum ada token/airdrop terkonfirmasi — hanya social task gratis, jangan deposit USDC).

## Pola bahaya (berhenti dan laporkan)
- Permintaan `setApprovalForAll`, tanda tangan permit, atau pesan yang isinya tidak bisa dibaca → pola drainer; jangan sign.
- Approval tak terbatas ke kontrak tak dikenal → tolak; utamakan jumlah persis.
- Situs meminta seed phrase / private key → berhenti, itu penipuan.
- Janji "convert credit jadi cash" / "recovery wallet berbayar" → penipuan; jangan pernah bayar.
- Program yang minta bayar per report/submit → keluarkan dari daftar (perintah 2026-11-19 23:29).

## Standar 100% benar (perintah Prawira, 2026-11-16)
- **KECEPATAN:** jalan cepat dulu — API/CLI langsung daripada browser bila ada; baca paralel; cache konteks stabil; batasi waktu tiap percobaan.
- **KETEPATAN:** alat yang tepat, target yang tepat, parameter yang tepat.
- **AKURASI:** verifikasi setiap hasil sebelum lanjut; jangan menebak atau mengarang nilai; bila belum terverifikasi, katakan begitu.
- **PERFORMA:** selesaikan sampai tuntas; tangani error dengan benar; tinggalkan jejak bukti (angka sebelum → sesudah, hash, link).

---
*Audit: skill ini murni prosedur kerja (dokumen Markdown, tanpa kode, tanpa install script, tanpa pemanggilan eksternal) — AUDITED SAFE oleh Papao, 2026-11-20.*
