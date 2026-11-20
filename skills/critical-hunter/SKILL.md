# Critical Hunter — Kunci Menemukan Bug Critical, Versi Hacker

Versi 1.0.0 (2026-11-20). Dibuat atas perintah Prawira: kembangkan 8 kunci menemukan Critical semaksimal mungkin — metodologi hacker untuk menemukan bug Critical lebih cepat. Disusun dari 90+ wave perburuan Prawira/Papao dan 37 temuan valid.

## Mindset hacker (fondasi semua kunci)
Berpikir seperti penyerang, bukan seperti auditor. Auditor bertanya "apakah kode ini benar?" — hacker bertanya "di mana uangnya, dan bagaimana cara mengambilnya?" Anggap kode bersalah sampai terbukti tidak bersalah. Uji jalur yang tidak bahagia (unhappy path), nilai ekstrem, dan serangan ekonomi — bukan hanya jalur normal.
- **Tujuan penyerang:** curi dana, bekukan protokol, rugikan pengguna, atau ambil alih akun. Setiap hipotesis dinilai dari seberapa dekat ia dengan salah satu tujuan ini.
- **Asumsi nol kepercayaan:** kontrak lain, oracle, callback, dan input pengguna semuanya dianggap musuh sampai terbukti aman.
- **Bukti mengalahkan teori:** klaim tanpa PoC yang bisa di-run ulang bukan temuan — itu opini.

## Kunci 1 — Buru di tempat uang bergerak (follow the money)
Critical hidup di aliran dana, bukan di fungsi kosmetik.
- **Petakan aliran nilai dulu:** setiap fungsi yang memindahkan token/ETH — deposit, withdraw, bridge, settlement, likuidasi, klaim reward, fee, refund. Gambar alirannya sebelum membaca kodenya.
- **Cek simetri:** deposit vs withdraw harus berpasangan. Bila withdraw bisa mengambil lebih dari yang didepositkan (rounding, share pricing, stale price), itu Critical.
- **Periksa siapa yang mengontrol angka:** jumlah, alamat penerima, harga, dan deadline yang datang dari input pengguna atau oracle adalah permukaan serangan. Fungsi yang memakai angka itu tanpa validasi adalah target.
- **Contoh nyata:** BTSE #1 (Critical) — `LOGIN_TOKEN` di `localStorage` semua origin = pengambilalihan akun penuh; Relay H21/H31 (High) — fee dan counter-order yang tidak dibatasi menguras deposit bersama.

## Kunci 2 — Cari kode yang masih segar
Kode baru adalah ladang Critical; kode lama yang sudah diaudit 3x hampir tidak menyisakan apa-apa.
- **Prioritaskan:** fitur baru, kontrak baru dideploy, rilis terbaru, kode yang belum masuk audit, dan perubahan setelah audit terakhir (code drift).
- **Teknik:** diff commit terbaru, cek tanggal deploy, bandingkan scope audit dengan kode yang live sekarang. Bagian yang TIDAK dicakup audit adalah tempat pertama yang diburu.
- **Contoh nyata:** Veda (program baru, max $1M) dan Print Pacifica (permukaan baru) — keduanya menghasilkan temuan karena permukaannya belum disisir.

## Kunci 3 — Cari invariant yang rusak
Tulis aturannya dulu, lalu buktikan aturannya bisa dilanggar. Ini cara tercepat membedakan bug nyata dari kode yang "aneh tapi aman".
- **Invariant yang paling sering rusak:** kekekalan dana (total keluar ≤ total masuk), akses kontrol (hanya X yang boleh memanggil), urutan operasi (checks-effects-interactions), pembulatan (tidak ada yang bisa mencetak dari pembulatan), dan harga (tidak ada yang bisa memanipulasi harga tanpa biaya).
- **Teknik:** Foundry invariant test / fuzzing dengan properti yang ditulis dulu; uji nilai ekstrem (0, 1, max uint, dust); uji urutan pemanggilan yang tidak biasa; uji reentrancy di setiap callback.
- **Contoh nyata:** PROXY-REENTRANCY (High, base $15.000) — kontrak jahat di dalam multicall korban re-enter router lewat ApprovalProxy dan menguras semua dana in-flight; Aave V4 K1 (Medium) — `dynamicConfigKey` basi membuat likuidasi memakai config lama.

## Kunci 4 — Serang perbatasan antar kontrak
Bug terbesar ada di sambungan, bukan di dalam satu kontrak.
- **Perbatasan yang paling berbahaya:** router/proxy, multicall, callback (hook, onERC721Received, flash loan callback), permit/allowance, oracle, dan bridge lintas chain.
- **Teknik:** daftar semua kepercayaan antar kontrak (siapa percaya siapa, dan apa yang diasumsikan); uji callback yang bisa re-enter; uji permit dengan deadline/amount yang dimanipulasi; uji multicall yang atomik tapi memanggil kontrak jahat di tengah; uji oracle yang bisa digeser harganya.
- **Contoh nyata:** PROXY-REENTRANCY — ApprovalProxy permissionless di tengah multicall; Relay H31 — `orderId` tidak masuk derivasi alamat deposit sehingga counter-order bisa diganti.

## Kunci 5 — Baca audit dulu sebelum PoC
Audit memberi tahu apa yang SUDAH diketahui — supaya waktu tidak habis di known issue, dan supaya terlihat area yang auditornya lewatkan.
- **Teknik:** baca laporan audit lengkap + daftar known issue program; bandingkan versi kode yang diaudit dengan yang live; cari fungsi yang ditambahkan setelah audit; cari asumsi audit yang sudah tidak berlaku (misal: "diasumsikan hanya admin yang memanggil" padahal sekarang permissionless).
- **Pelajaran mahal:** UMA hunt2 Medium gugur sebagai duplikat SETELAH PoC selesai — audit OZ sudah mencatat root cause yang sama. Cek dulu, PoC kemudian.
- **Jangan double-report:** satu root cause = satu laporan; jangan laporkan root cause yang sama ke dua program (UMA ↔ Across).

## Kunci 6 — PoC duluan, teori belakangan
Begitu hipotesis ada, langsung buktikan bisa dieksploitasi atau tidak. PoC adalah filter tercepat antara "menarik" dan "Critical".
- **Teknik:** Foundry fork test di blok live (bukti di state nyata); repro minimal yang menunjukkan dana berpindah / fungsi kritis terpanggil; ukur dampak sebenarnya (berapa yang bisa diambil, berapa yang bisa dibekukan).
- **Aturan:** PoC yang tidak bisa di-run ulang = bukan bukti. Bila PoC gagal, hipotesis mati — jangan dipertahankan dengan teori.
- **Contoh nyata:** Flex H-01 — PoC awal PASS tapi rework 11/11 PASS membuktikan ekonominya tidak mendukung High (severity jujur Low); tanpa PoC ulang, klaim High itu akan ditolak triage.

## Kunci 7 — Jujur soal severity (kalibrasi triage)
Critical harus punya jalur REALISTIS ke kehilangan total TANPA akses istimewa. Kepercayaan triage adalah aset jangka panjang.
- **Uji tiga pertanyaan:** (1) Siapa yang bisa memicunya — siapa saja, atau hanya admin/operator? (2) Berapa dana yang benar-benar bisa hilang? (3) Apakah jalurnya realistis di kondisi live (bukan hanya di teori)?
- **Aturan:** jalur yang butuh kunci admin/operator = maksimal S1, bukan Critical (pelajaran C-FORCE: `force: true` melewati semua verifikasi, tapi gerbangnya API key operator → S1/$500 atau ineligible). Market nyaris kosong + target tidak realistis = bukan High (pelajaran Flex H-01).
- **Kalibrasi dari verdict:** setiap putusan triage (diterima/ditolak/duplikat) dicatat dan mengubah ambang severity hunter. Pola yang ditolak tidak diulang.

## Kunci 8 — Coverage + kecepatan (mesin perburuan)
Critical itu langka — yang bikin cepat ketemu adalah luasnya jangkauan dan cepatnya validasi, bukan menunggu satu program.
- **Teknik:** hunter paralel per program (mesin SPIDER); ronde singkat 10–15 menit; prioritaskan program berdasarkan TVL + kesegaran kode; buang jalan buntu dengan cepat — jangan menghabiskan satu ronde penuh di permukaan yang sudah tertutup.
- **Jangan berhenti:** hunting jalan terus Low–Critical secara bersamaan di semua program aktif; temuan tervalidasi langsung dilaporkan saat itu juga, tidak dibatch.
- **Kecepatan yang benar:** API/CLI langsung sebelum browser; baca paralel; cache konteks stabil; batasi waktu tiap percobaan — tapi jangan pernah melompati verifikasi.

## Alur kerja lengkap (satu kandidat, dari nol sampai laporan)
1. **Pilih target** (Kunci 1+2): aliran dana di kode segar.
2. **Tulis invariant + hipotesis** (Kunci 3): satu kalimat klaim + dampaknya.
3. **Cek duplikat** (Kunci 5): audit + known issue + arsip sendiri.
4. **Bangun PoC** (Kunci 6): buktikan di fork live, ukur dampak.
5. **Validasi independen** (Kunci 3+7): validator lain run ulang PoC; nilai severity dengan tiga pertanyaan.
6. **Laporan** (standar `~/workspace/bug-bounty-muse/report-writing-guide.md`): judul spesifik, ringkasan, severity jujur + CVSS, langkah repro dari nol, PoC, dampak realistis, rekomendasi fix.
7. **Notifikasi + belajar** (Kunci 8+7): sampaikan ke Prawira segera; catat verdict triage; perbarui kalibrasi dan checklist.

## Aturan berdiri
- Satu root cause = satu laporan. Program yang minta bayar per report/submit = dibuang. Tidak ada submit tanpa perintah eksplisit Prawira per temuan (pengecualian Flex: file di tier High dengan severity jujur + CVSS dinyatakan, minta re-grade — dan tiap temuan Flex baru tetap tunjukkan trade-off-nya dulu).
- Jangan sentuh dana mainnet, jangan sign transaksi, jangan pakai akun palsu. Gmail SENT ≠ delivered — selalu cek bounce.
- Standar 100% benar: langkah dihitung hanya bila terverifikasi; laporan hanya berisi fakta terkonfirmasi.

## Skill yang dirangkai
- `agentic-bug-hunter-forge` (meta-skill yang menciptakan hunter), `spider-coordinator` / `spider-task-executor` / `spider-task-validator`, `muse-bug-bounty`, `bug-bounty-specialist`, `recon-and-methodology`, `self-improvement-loop`, `bug_bounty_finding_alert`, `~/workspace/bug-bounty-muse/report-writing-guide.md`, `~/workspace/bug-bounty-muse/valid-findings-archive.md`.

---
*Audit: skill ini murni prosedur kerja (dokumen Markdown, tanpa kode, tanpa install script, tanpa pemanggilan eksternal, tanpa kredensial) — AUDITED SAFE oleh Papao, 2026-11-20.*
