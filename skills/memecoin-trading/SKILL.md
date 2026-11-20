# Trading Memecoin Solana

## Aturan keras dulu

- Memecoin sangat volatil dan bisa menjadi tidak bernilai sama sekali. Jangan pernah memakai uang untuk kebutuhan hidup (sewa, makan, utang, darurat).
- Gunakan HANYA dompet agent yang terpisah dan kecil: `BupM4zgsie9upSt94UdVAEHaKr1KRWpPMDgvXZGm46qf`. Jangan pernah memakai dompet utama user (`95ubFWyurr4GAxPjS3z15HjDnRX3SPNtnrdyRcBjRbY6`) untuk trading memecoin.
- Jangan pernah meminta, menyimpan, atau memasukkan seed phrase / private key ke chat, file, log, atau prompt apa pun.
- Jangan pernah menjanjikan profit dan jangan pernah menyatakan target harga sebagai fakta.
- Satu persetujuan user berlaku untuk satu aksi trading saja.

## Evaluasi token sebelum membeli

- Identifikasi mint address yang tepat. Nama, ticker, logo, dan akun sosial bisa disalin.
- Periksa program token: SPL Token asli atau Token-2022. Untuk Token-2022, periksa transfer fee, transfer hooks, default account state, permanent delegate, dan batasan lainnya.
- Mint authority: authority yang masih aktif bisa mencetak supply tambahan. Authority yang sudah dicabut tidak bisa mencetak lagi lewat authority itu.
- Freeze authority: authority yang masih aktif bisa membekukan akun token perorangan dan menghalangi transfer atau penjualan.
- "Ownership renounced" BUKAN pemeriksaan keamanan yang lengkap di Solana. Periksa tiap authority secara terpisah; token Solana tidak selalu punya satu owner ala EVM.
- Bedakan program owner dari mint account, mint authority, metadata update authority, dan holding developer.
- Jika program custom mengendalikan trading, periksa upgrade authority-nya. Kode yang bisa di-upgrade dapat berubah setelah diperiksa.

## Distribusi holder

- Periksa holder terbesar dan kenali dulu akun pool, akun bonding-curve, akun exchange, akun vesting, dan burn address sebelum menafsirkan konsentrasi.
- Kelompokkan akun token berdasarkan wallet owner; satu wallet bisa punya banyak akun token.
- Cari wallet yang terhubung: sumber pendanaan yang sama, pembelian terkoordinasi, transfer sinkron, penjualan bersamaan.
- Periksa holding developer, wallet terkait, dan apakah wallet itu bisa menjual segera.
- Sniper dan pembelian borongan bisa menyebar konsentrasi ke banyak wallet; saldo kecil di wallet developer tidak membuktikan apa-apa.
- Tanda sehat: kepemilikan tersebar di wallet yang tampak independen, holding insider yang terhubung terbatas, partisipasi berkelanjutan.
- Tanda bahaya: sedikit wallet terhubung menguasai sebagian besar supply beredar atau cukup besar untuk mengalahkan likuiditas yang tersedia.
- Jumlah holder saja bukti yang lemah; distribusi dust dan pemecahan wallet bisa menggelembungkannya. Tidak ada angka holder atau konsentrasi "aman" yang universal.

## Likuiditas

- Periksa alamat pool yang sebenarnya, aset, reserve, umur pool, dan kedalaman eksekusi untuk ukuran order yang direncanakan.
- Market cap dan fully diluted valuation TIDAK mengukur berapa banyak uang yang bisa ditarik penjual.
- Periksa price impact saat masuk DAN saat keluar secara hipotetis; likuiditas tipis bisa menggerakkan harga tajam.
- Untuk pool dengan LP token fungible, verifikasi siapa yang memegang LP token itu dan apakah locker yang dikenal mengendalikannya; periksa jumlah lock, masa berlaku, penerima, dan syarat penarikan.
- Verifikasi burn di on-chain. Screenshot atau badge "LP burned" tidak cukup.
- Likuiditas yang tidak dikunci memungkinkan pengendalinya menarik aset dasar; penarikan besar bisa membuat penjualan sangat mahal atau tidak mungkin.
- LP yang dikunci atau dibakar TIDAK mencegah developer dump, pembatasan level token, atau likuiditas yang hilang dari pool lain.

## Cek rug dan sellability

- Gunakan RugCheck dan explorer sebagai alat screening; skor yang bagus bukan jaminan.
- Minta sell quote dan simulasikan transaksi bila didukung.
- Bila cek awal lolos, pembelian minimal lalu penjualan minimal memberi bukti sellability saat ini yang lebih kuat — tetap tidak menjamin exit di masa depan.
- Perhitungkan transfer fee, pembatasan trading, dan apakah route mendukung ekstensi token itu.
- Pola rug yang umum: insider dump, penarikan likuiditas, mint tambahan, exit wallet terkoordinasi, kontrol transfer berbahaya.
- Perlakukan hasil detector dengan hati-hati: tool bisa melewatkan perilaku custom, perubahan izin, pembatasan per-wallet, atau mekanisme baru.

## Sinyal sosial dan momentum

- X: verifikasi riwayat akun, referensi mint address yang konsisten, dan diskusi independen. Follower dan engagement bisa dibeli.
- Telegram/Discord: periksa percakapan yang substansial dan perilaku moderator. Bot dan peserta berbayar bisa memalsukan antusiasme.
- Pertumbuhan holder: bandingkan holder baru dengan perilaku transaksi; airdrop dan pemecahan wallet bisa memalsukan pertumbuhan.
- Volume: periksa peserta unik, ukuran trade, dan interaksi wallet berulang; wash trading bisa menggelembungkan volume.
- Kehadiran sosial mendukung pengecekan identitas; kehadiran sosial TIDAK membuktikan keamanan.

## Tool dan apa yang dicek di masing-masing

- pump.fun: launchpad bonding-curve. Koreksi: "graduation ke Raydium" adalah perilaku lama, bukan asumsi saat ini — PumpSwap adalah venue graduation sekarang; verifikasi transaksi migrasi dan tujuan sebenarnya. Periksa mint address, riwayat creator, progres kurva, pembelian awal, wallet terhubung, dan pool nyata setelah graduation. Bedakan token yang masih di kurva dari token yang sudah di AMM pool.
- Jupiter: aggregator swap. Periksa mint input/output, route, quote yang bisa dieksekusi, price impact, minimum received, fee, dan isi transaksi. Harga atau route yang ditampilkan TIDAK menyatakan token itu aman.
- Birdeye: chart, trade, likuiditas, dan data holder. Periksa kesegaran data, cakupan pool, trade besar, perubahan holder, dan selisih antara likuiditas yang dilaporkan dan kedalaman eksekusi.
- Dexscreener: menemukan pair dan membandingkan harga, volume, likuiditas, umur pair. Periksa chain, mint address, pair address, quote asset, dan aktivitas di pool yang bersaing. Promosi berbayar, boost, dan trending adalah sinyal marketing.
- RugCheck: screening authority, konsentrasi, risiko likuiditas. Baca tiap temuan dan timestamp-nya; selidiki data yang hilang dan peringatan yang belum terjawab.
- Solscan: periksa mint account, authority, program token, holder, transfer, pool account, dan instruksi transaksi. Visibilitas di explorer BUKAN audit kode; verifikasi klaim lock dan pencabutan authority lewat akun dan transaksi yang mendasarinya.

## Alur trading

- Hubungkan dompet trading yang terpisah dan pilih token berdasarkan mint address.
- Sisakan SOL yang cukup untuk fee, priority fee, dan pembuatan akun bila diperlukan.
- Minta quote baru untuk jumlah yang direncanakan.
- Tinjau price impact terpisah dari slippage: price impact berasal dari efek order terhadap likuiditas; toleransi slippage membatasi penurunan eksekusi yang masih diterima.
- Atur toleransi slippage yang berbatas; toleransi tinggi membuka eksekusi yang lebih buruk.
- Tinjau minimum output dan semua fee. Priority fee bisa memperbaiki penjadwalan; tidak menjamin inklusi atau eksekusi.
- Decode dan simulasikan transaksi bila memungkinkan. Verifikasi pergerakan token, penerima, signer, perubahan authority, dan instruksi tambahan sebelum menandatangani.
- Submit, catat signature, dan verifikasi konfirmasi plus perubahan saldo dompet yang sebenarnya.
- Bedakan status processed, confirmed, dan finalized. Jangan anggap animasi antarmuka sebagai settlement.

## Position sizing dan exit

- Ukur tiap posisi supaya kerugian total tetap bisa ditoleransi dalam batas kerugian dompet yang sudah ditentukan.
- Perhitungkan eksposur berkorelasi: beberapa memecoin bisa gagal bersamaan.
- Perhitungkan fee, likuiditas, price impact, dan kemungkinan tidak ada exit.
- Sebelum masuk, tentukan alasan membeli, apa yang membatalkannya, kerugian maksimum yang diterima, dan kondisi exit.
- Tentukan aturan ambil profit sebagian, exit berbasis waktu bila sesuai, dan kapan menutup sisanya.
- Perlakukan stop loss sebagai instruksi atau niat, bukan harga yang dijamin; gap likuiditas, outage, dan transaksi gagal bisa mencegah eksekusi.
- Potong posisi ketika alasan awalnya gagal atau aturan keamanan keras dilanggar. Jangan averaging down secara otomatis.

## Transaksi gagal atau tidak bisa menjual

- Periksa signature dan saldo sebelum mencoba lagi. Timeout tidak membuktikan kegagalan.
- Diagnosis penyebabnya: blockhash kedaluwarsa, SOL tidak cukup, slippage, quote basi, tidak ada route, akun dibekukan, pembatasan transfer, atau kongesti.
- Refresh quote dan bangun ulang transaksi. Gunakan retry berbatas dan verifikasi tiap hasil.
- Kurangi ukuran order bila kedalaman yang jadi masalah. Jangan naikkan slippage secara membabi buta.
- Bila akun dibekukan atau aturan token memblokir transfer, ganti aggregator mungkin tidak membantu.
- Berhenti menambah dana. Simpan detail transaksi dan hindari layanan "recovery" yang meminta key, signature, atau pembayaran di muka.

## Pola penipuan yang harus ditolak

- Token copycat yang meniru token lain; verifikasi identitas sebelum berinteraksi.
- Airdrop palsu yang meminta signature; "kirim SOL untuk dilipatgandakan"; layanan recovery yang meminta key atau pembayaran di muka.
- Alur trading Solana yang meminta setApprovalForAll — itu metode approval NFT di EVM, BUKAN persyaratan swap native Solana.
- Permintaan transfer, perubahan authority, pemberian delegate, atau instruksi yang tidak dijelaskan di luar trade yang dimaksud.

## Checklist DO NOT TRADE

- Identitas mint tidak pasti atau bertentangan antar sumber.
- Mint authority aktif digabung dengan holding developer atau wallet terhubung yang besar.
- Freeze power, permanent delegate, transfer hook, atau kontrol upgrade menimbulkan risiko yang belum terjawab.
- Posisi likuiditas yang dikendalikan developer dan bisa ditarik memasok likuiditas material tanpa pengaman yang terverifikasi independen.
- Klaim lock atau burn LP tidak bisa diverifikasi.
- Holder teratas (setelah mengecualikan akun infrastruktur) menguasai sebagian besar supply atau tampak terkoordinasi.
- Test sale gagal karena pembatasan token, atau tidak ada exit yang bisa dieksekusi.
- Ukuran trade yang direncanakan menyebabkan price impact yang tidak bisa diterima.
- Identitas sosial tidak bisa diverifikasi dan promosi adalah alasan utama membeli.
- Transaksi meminta izin, transfer, signature, atau perubahan authority yang tidak dijelaskan.
- Trade melebihi batas risiko dompet.

## Keandalan trading (praktik terbaik agen, 2026)

- **Validasi sebelum bertindak.** Verifikasi mint address, authority, likuiditas, dan holder dari sumber on-chain sebelum berinteraksi. Jangan bertindak hanya dari satu sumber yang belum dikonfirmasi.
- **Catat setiap trade.** Simpan mint address, jumlah, harga masuk, signature, dan hasil di satu file log. Perbarui segera setelah aksi selesai.
- **Batasi dan diagnosis.** Bila sebuah trade gagal, diagnosis penyebabnya sebelum mencoba lagi; jangan ulangi panggilan yang sama tanpa mengubah pendekatan.
- **Jadikan pola penipuan sebagai kasus regresi.** Setiap pola rug atau kontrak mencurigakan yang ditemukan, catat ciri-cirinya untuk mengenali pola yang sama di token berikutnya.

## Referensi

- Dokumentasi token Solana: https://solana.com/docs/tokens
- Token-2022 extensions: https://www.solana-program.com/docs/token-2022
- Dokumentasi developer Jupiter: https://dev.jup.ag/
- pump.fun: https://pump.fun/
- Dokumentasi Birdeye: https://docs.birdeye.so/
- Dokumentasi API Dexscreener: https://docs.dexscreener.com/
- RugCheck: https://rugcheck.xyz/
- Solscan: https://solscan.io/
