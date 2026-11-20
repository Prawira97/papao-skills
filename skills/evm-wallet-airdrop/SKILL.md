# Pengelola Dompet EVM dan Airdrop

## Kelola dompet dengan aman

- Gunakan satu dompet khusus berbatas kecil untuk airdrop dan testnet, dan jangan pernah memakai dompet utama user untuk tugas berisiko.

- Jangan pernah menulis seed phrase atau private key ke file, chat, skill, atau log apa pun.

- Simpan kredensial hanya lewat Secure Vault dan jangan pernah meminta user mengirimkannya lewat chat.

- Pisahkan aktivitas mainnet dan testnet agar token testnet dan aset nyata tidak tercampur.

- Periksa alamat dompet dengan checksum sebelum mengirim apa pun dan cocokkan dengan alamat yang user berikan.

- Catat dompet mana yang dipakai untuk proyek apa, dan jangan pernah memakai satu dompet untuk semua proyek tanpa sepengetahuan user.

## Periksa sebelum berinteraksi

- Verifikasi setiap alamat kontrak dan URL dApp dari kanal resmi proyek sebelum berinteraksi.

- Nilai kelayakan sebelum mulai: periksa apakah konversi, alokasi, snapshot, dan listing diumumkan atau masih tidak jelas.

- Periksa kredibilitas tim, status mainnet, riwayat proyek, dan kanal resmi sebelum menghabiskan waktu.

- Bandingkan waktu, biaya, dan risiko setiap langkah dengan nilai airdrop yang mungkin diperoleh.

- Anggap presale berbayar yang belum terverifikasi atau mainnet yang belum dikonfirmasi sebagai tanda bahaya; jangan kirim dana nyata.

- Jangan pernah berinteraksi dengan kontrak yang belum terverifikasi atau dengan tautan dari pesan yang tidak diminta.

- Baca apa yang diminta transaksi sebelum menyetujuinya, termasuk kontrak tujuan, fungsi yang dipanggil, token yang bergerak, dan biayanya.

- Tolak permintaan approval tak terbatas ke kontrak yang tidak dikenal dan utamakan jumlah persis lalu cabut approval setelah selesai.

- Waspadai pola drainer seperti permintaan setApprovalForAll, tanda tangan permit, atau pesan yang isinya tidak bisa dibaca.

- Jika ada yang tidak cocok antara yang dijanjikan proyek dan yang diminta transaksi, hentikan dan tanyakan ke user.

## Minta persetujuan sebelum transaksi

- Jangan pernah mengirim transaksi, menandatangani pesan, atau memberi approval tanpa persetujuan user untuk aksi itu.

- Jika browser agen tidak memiliki ekstensi wallet, minta user menghubungkan wallet melalui WalletConnect/MetaMask atau browser miliknya sendiri.

- Biarkan user menghubungkan wallet dan menyetujui setiap transaksi; agen hanya mengarahkan halaman dan tidak pernah menandatangani.

- Tunjukkan ke user ringkasan tiap aksi sebelum dieksekusi, yaitu jaringan, kontrak tujuan, apa yang bergerak, dan perkiraan biaya.

- Patuhi batas yang user tetapkan untuk nilai dan biaya, dan hentikan bila satu aksi melewati batas itu.

- Tetapkan batas pengeluaran di muka untuk sesi ini (nilai maksimum dan biaya maksimum) sebelum berinteraksi dengan proyek apa pun, dan catat batas itu di log — jangan mulai tanpa batas yang jelas. (Gemini 4, Nov 2026: agen menetapkan spending cap di muka dan menyimpan receipt.)
- Simpan receipt tiap aksi (hash transaksi, biaya, dan apa yang bergerak) dan cocokkan dengan batas yang ditetapkan; bila total mendekati batas, berhenti dan laporkan ke user sebelum melanjutkan.

- Jangan pernah menandatangani pesan buta atau transaksi yang isinya tidak bisa dijelaskan dengan kata-kata biasa.

- Satu persetujuan berlaku untuk satu aksi saja dan tidak berlaku untuk aksi berikutnya.

## Jalankan task testnet

- Kerjakan task testnet hanya di jaringan testnet resmi dan hanya dengan token testnet dari faucet resmi.

- Ikuti alur quest secara berurutan: hubungkan wallet, ambil faucet, kirim transaksi, delegasikan, mint badge, selesaikan tugas sosial harian, lalu tautkan akun X dan Telegram.

- Verifikasi dan catat bukti setelah setiap langkah sebelum melanjutkan ke langkah berikutnya.

- Catat chain ID, RPC, batas faucet, saldo awal, saldo akhir, dan jumlah transaksi untuk setiap quest.

- Perlakukan poin sebagai poin saja sampai rasio konversi, alokasi, snapshot, dan listing token diumumkan secara resmi — poin tidak menjamin token.

- Jangan pernah membayar dengan uang nyata untuk token testnet dan jangan pernah membeli token testnet dari pihak ketiga.

- Ikuti langkah task sesuai urutan yang diminta proyek dan verifikasi tiap langkah selesai sebelum lanjut ke langkah berikutnya.

- Catat faucet yang dipakai, saldo testnet, dan bukti tiap langkah selesai.

- Jika sebuah task testnet meminta koneksi ke mainnet atau meminta aset nyata, hentikan dan tanyakan ke user.

## Jalankan task airdrop

- Periksa syarat eligibilitas dari pengumuman resmi proyek sebelum mengerjakan apa pun.

- Kerjakan hanya task yang user setujui dan hanya dengan satu dompet per orang per proyek sesuai aturan proyek.

- Jangan pernah membuat banyak akun untuk menggarap satu airdrop yang sama dan jangan pernah membantu user mengelabui aturan proyek.

- Periksa status klaim lewat kanal resmi dan klaim hanya dari alamat klaim resmi yang sudah diverifikasi.

- Catat tiap proyek, dompet yang dipakai, task yang selesai, hash transaksi, dan tenggat klaim.

- Simpan tautan referral yang digunakan, identitas proyek, dan persentase atau tarif penghasilan referral; laporkan penghasilan referral berdasarkan catatan resmi proyek dan jangan membuat akun tambahan untuk meningkatkan referral.

- Ingatkan user tentang tenggat klaim sebelum lewat dan tentang biaya klaim bila ada.

## Catat semuanya

- Simpan log tiap dompet, proyek, task, hash transaksi, dan hasil di satu file yang mudah dicari.

- Perbarui log segera setelah satu aksi selesai agar tidak ada langkah yang hilang atau terulang.

- Laporkan ringkasan berkala ke user berisi task yang selesai, yang masih berjalan, dan yang butuh persetujuan.

- Jangan pernah mencatat seed phrase, private key, atau kredensial apa pun di dalam log.

## Keandalan dan kecepatan (praktik terbaik agen, 2026)

- **Validasi sebelum bertindak.** Verifikasi alamat, kontrak, dan URL dari kanal resmi sebelum berinteraksi. Jangan pernah bertindak hanya dari satu sumber yang belum dikonfirmasi.

- **Kerjakan pengecekan independen secara paralel.** Verifikasi alamat kontrak, URL dApp, dan syarat eligibilitas tidak saling bergantung; lakukan bersamaan untuk menghemat waktu, lalu kumpulkan hasilnya sebelum memutuskan.

- **Catat pola penipuan sebagai kasus regresi.** Setiap pola drainer atau kontrak mencurigakan yang ditemukan, catat ciri-cirinya (fungsi yang dipanggil, pola approval, alamat). Gunakan catatan itu untuk mengenali pola yang sama di proyek berikutnya.

- **Simpan jejak bukti tiap aksi.** Catat hash transaksi, alamat, dan bukti penyelesaian segera setelah aksi selesai. Jejak ini adalah bukti jika status klaim atau saldo dipertanyakan nanti.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
