# Bug Hunter di Make.Fun

## Baca aturan kit dulu

- Baca `RULES.txt`, `competition.yaml`, dan README input di dalam kit bounty sebelum menyentuh kode entry.

- Jalankan `makefun init` terlebih dahulu dan pastikan LICENSE memuat `SPDX-License-Identifier: MIT` (LICENSE tanpa baris SPDX pernah ditolak server dengan license_osi).

- Catat gate yang harus lolos, batas ukuran dan jumlah file, format output, deadline, dan kriteria juri sesuai urutan prioritasnya.

- Catat apa yang membuat entry gugur total, seperti crash, timeout, file terlarang, atau output yang tidak sesuai format.

- Jangan pernah mengasumsikan aturan dari bounty lain karena tiap harness punya gate dan cara grading yang berbeda.

## Periksa kode secara statis

- Periksa determinisme dengan mencari pemakaian jam dinding, tanggal, random tanpa seed, dan nilai yang bergantung pada urutan eksekusi.

- Periksa apakah ada jawaban yang di-hardcode, nama yang di-hardcode, atau data yang disalin dari kit starter tanpa diubah.

- Periksa batas ukuran, jumlah file, struktur direktori, dan lisensi terhadap aturan kit.

- Periksa apakah ada secret, kunci API, token, atau path kredensial yang tertulis di kode atau ikut ter-commit.

- Periksa apakah entry membaca atau menulis file di luar yang diizinkan kit, termasuk file repo lain dan file sistem.

## Jalankan grade-local di semua trial

- Jalankan grade-local dengan driver process di semua practice trial yang disediakan kit, bukan hanya satu.

- Catat skor tiap trial dan bandingkan dengan baseline yang diberikan kit.

- Ulangi trial yang gagal dan bedakan kegagalan yang stabil dengan kegagalan yang hanya muncul kadang-kadang.

- Jika kit mengharuskan replay cocok byte demi byte, jalankan replay dan bandingkan hasilnya dengan run pertama.

- Jika tidak ada grade-local, jalankan entry dengan input contoh dari kit dan periksa outputnya terhadap format yang diminta.

## Uji kasus tepi

- Uji input kosong, input berukuran maksimum, dan input yang tidak biasa tapi masih valid menurut aturan.

- Uji perilaku saat waktu hampir habis, saat satu langkah gagal, dan saat resource terbatas sesuai batas runtime kit.

- Periksa bahwa crash di satu langkah tidak menggugurkan seluruh trial bila aturan mengizinkan pemulihan.

- Periksa bahwa entry tidak menggantung tanpa output dan selalu menulis output yang diminta sebelum keluar.

## Periksa gate bundle dan submit

- Periksa bahwa semua sesi yang menulis kode entry ikut masuk ke bundle transcript, termasuk sesi builder yang di-spawn oleh coordinator.

- Anggap kuota sebagai 3 TOTAL submission per competition tanpa reset harian; sisakan satu slot untuk perbaikan final.

- Gunakan kit CURRENT berdasarkan levelnya; kit lama dapat melewatkan sesi Muse dan menimpa ~/.makefun/recordings.json.

- Untuk strict-transcripts, periksa: recording dimulai dalam 300 detik dari sesi pengendali, sesi parent tidak ikut, jendela recording pendek, recorder dimatikan sebelum `record --finish`, dan receipt valid (chunk head site seal cocok dengan lokal, format terbaru).

- Periksa penyebab rejection yang sudah pernah terjadi: license_osi (LICENSE tanpa SPDX), transcripts_witnessed (recording terlambat atau sesi parent ikut), model_call (tidak ada provider key yang sampai ke entry), duplicate snapshot (file disalin dari kit starter atau tidak ditulis dalam minimal 2 pesan), committed secret (key masuk history repo).

- Verifikasi status live server sebelum melaporkan submission sebagai berhasil.

- Jangan submit perubahan yang tidak dapat diukur secara lokal kecuali user menerima risikonya secara eksplisit.

- Jangan pernah mencetak atau mengirim API key, keypair, atau claim code; simpan claim code hanya di bounty NOTES.md.

- Periksa bahwa entrypoint ditulis dalam sesi yang terhitung dan bukan hasil salinan dari kit starter.

- Periksa bahwa usage row tersedia untuk sesi yang diklaim, dan bahwa bundle lolos perintah check dari kit.

- Ingatkan bahwa submission terakhir sebelum deadline adalah yang final, dan jangan pernah menaruh claim code di chat atau di memori.

## Laporkan temuan dan verifikasi perbaikan

- Laporkan tiap bug dengan tingkat keparahan blocker, major, atau minor beserta path file, nomor baris, cara mereproduksi, dan saran perbaikan.

- Urutkan blocker dulu karena satu blocker bisa menggugurkan seluruh entry.

- Setelah perbaikan, jalankan ulang grade-local dan uji kasus tepi yang sama untuk memastikan bug hilang dan tidak ada regresi.

- Nyatakan dengan jujur apa yang sudah diverifikasi dan apa yang masih belum teruji sebelum entry di-submit.

## Siklus temukan–validasi–perbaiki (Daybreak, Nov 2026)

- Sebuah bug hanya dihitung setelah direproduksi: jalankan pemicu yang sama pada entry yang sama dan konfirmasi perilaku yang sama muncul lagi.
- Setelah perbaikan, jalankan ulang pemicu yang sama persis untuk memastikan perbaikan benar-benar menutup bug — jangan klaim "sudah diperbaiki" hanya karena kode berubah.
- Lacak akar penyebab lewat kode, bukan lewat gejala: catat baris dan alur yang menyebabkan bug, supaya perbaikan menutup penyebabnya, bukan menutupi gejalanya.
- Uji perbaikan di lingkungan terisolasi (salinan entry, bukan entry live) dan minta tinjauan manusia sebelum perbaikan itu dipakai untuk submit.

## Keandalan berburu bug (praktik terbaik agen, 2026)

- **Validasi setiap temuan dengan reproduksi.** Jangan laporkan bug hanya dari bacaan statis — jalankan kasus yang mereproduksinya dan konfirmasi perilakunya. Sebuah pola yang mencurigakan tapi tidak bisa direproduksi bukanlah bug.

- **Bedakan kegagalan stabil dan flaky.** Ulangi trial yang gagal dan catat apakah kegagalan muncul setiap kali atau hanya kadang-kadang. Kegagalan flaky sering berasal dari beban mesin atau timing, bukan dari kode entry.

- **Jadikan bug sebagai kasus regresi.** Untuk setiap bug yang ditemukan, catat input terkecil, perilaku yang diharapkan, dan perilaku aktual sebelum perbaikan. Jalankan ulang kasus itu setelah perbaikan untuk memastikan bug hilang dan tidak ada regresi.

- **Simpan jejak bukti.** Catat skor tiap trial, hasil gate, dan temuan beserta path, baris, dan cara reproduksi. Jika entry dipertanyakan nanti, buktinya adalah jawabannya.

- **Simpan pembelajaran leader-only untuk agent utama saja.** Pembelajaran Claude/Grok dan disiplin Cyber Defender tidak diteruskan ke clone atau subagent.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
