# DeFi Solana

## Aturan keras dulu

- Gunakan dompet agent yang terpisah dan kecil untuk DeFi: `BupM4zgsie9upSt94UdVAEHaKr1KRWpPMDgvXZGm46qf`. Jangan pernah memakai dompet utama user (`95ubFWyurr4GAxPjS3z15HjDnRX3SPNtnrdyRcBjRbY6`) untuk eksperimen DeFi. Jumlah di dompet DeFi dibatasi kecil; hanya sisakan jumlah seukuran transaksi di hot wallet.
- Jangan pernah meminta, menyimpan, atau memasukkan seed phrase / private key ke chat, file, log, atau prompt apa pun.
- Jangan pernah menjanjikan yield, profit, atau harga. APR/APY yang ditampilkan adalah historis atau estimasi, bukan jaminan.
- Verifikasi mint address dari kanal resmi sebelum berinteraksi; ticker dan nama bisa disalin.
- Satu persetujuan user berlaku untuk satu aksi saja (satu swap, satu deposit, satu pinjaman).
- Interface, fee, aset yang didukung, dan parameter risiko protokol BERUBAH — verifikasi parameter transaksi dan pool saat ini tepat sebelum menandatangani.

## Swap Jupiter

Cara kerja Jupiter:

- Jupiter adalah aggregator swap Solana. Ia mencari likuiditas dari banyak venue: AMM, concentrated-liquidity pool, order-book venue, dan aggregator lain.
- Ia bisa memakai satu venue untuk swap sederhana, membagi order ke beberapa venue, merute lewat token perantara seperti USDC atau SOL, atau memakai beberapa leg berurutan bila hasilnya lebih baik.
- Route dipilih dari likuiditas yang tersedia, mint token, harga pool, fee, dan ekspektasi eksekusi. Route terbaik yang ditampilkan tidak dijamin tetap tersedia sampai transaksi mendarat.

Field quote yang harus dipahami:

- Input amount: jumlah pasti token input yang dijual.
- Output amount: output yang diharapkan sebelum toleransi eksekusi.
- Route plan: venue dan token perantara yang dipakai.
- Price impact: estimasi pergerakan harga akibat ukuran trade relatif terhadap likuiditas yang tersedia.
- Slippage tolerance: penurunan eksekusi maksimum yang masih kamu izinkan antara pembuatan quote dan eksekusi.
- Minimum received: ambang on-chain yang bila di bawah itu swap harus gagal.
- Fee: fee trading venue, fee Jupiter atau integrator bila ada, dan biaya network.

Price impact vs slippage:

- Price impact adalah estimasi seberapa besar trade-mu sendiri menggerakkan pasar dibanding harga referensi. Ini terutama soal likuiditas dan ukuran trade.
- Slippage tolerance adalah batas eksekusimu untuk perubahan antara pembuatan quote dan eksekusi transaksi. Ini mencakup pergerakan harga, trade yang bersaing, dan perubahan route setelah quote.
- Contoh: harga referensi menyarankan 100 USDC. Trade-mu punya price impact 0,8% dan dikutip 99,2 USDC. Kamu set slippage 0,5%. Minimum received kira-kira 98,704 USDC, tergantung perhitungan quote yang tepat.
- Setting slippage besar TIDAK memperbaiki harga. Ia hanya mengizinkan eksekusi yang lebih buruk dan bisa membuat transaksi rentan terhadap pergerakan merugikan atau sandwiching. Pakai toleransi terkecil yang masih berhasil untuk aset dan kondisi pasar itu.

Fee:

- Swap bisa mencakup beberapa biaya independen: fee trading venue, fee Jupiter atau platform integrator bila ditampilkan, fee network Solana, priority fee atau landing fee opsional, dan biaya transfer atau pembuatan akun dalam beberapa kasus.
- Jangan asumsikan "0% Jupiter fee" berarti swap gratis. Periksa route dan rincian fee.

Sebelum menandatangani:

1. Konfirmasi mint address token, terutama untuk token bernama mirip atau palsu.
2. Konfirmasi jumlah input yang tepat dan minimum received yang ditampilkan.
3. Buka route dan periksa setiap token perantara dan venue.
4. Periksa price impact. Berhenti bila besarnya tidak wajar.
5. Periksa slippage tolerance. Kecilkan bila likuiditas dan kondisi pasar memungkinkan.
6. Konfirmasi dompet penerima dan pembuatan akun token bila ada.
7. Periksa ringkasan transaksi dompet dan instruksi program. Transaksi harus sesuai dengan swap, tanpa transfer atau approval yang tidak dijelaskan.
8. Simulasikan atau preview transaksi bila dompet menyediakan opsi itu.
9. Konfirmasi transaksi masih baru dan belum lama ditahan sampai quote menjadi basi.
10. Setelah menandatangani, verifikasi signature transaksi di Solana Explorer dan konfirmasi saldo token yang sebenarnya.

Jangan pernah menandatangani transaksi hanya karena sebuah situs berkata "claim", "verify", atau "activate". Transaksi swap tidak boleh mentransfer aset yang tidak terkait secara tiba-tiba.

## Liquidity provision (Raydium dan Orca)

Raydium dan Orca menyediakan pool tempat user mendeposit pasangan token dan mendapat bagian fee trading. Keduanya mendukung desain concentrated-liquidity untuk banyak pool. Beberapa pool atau produk bisa memakai mekanisme berbeda, jadi baca interface pool yang spesifik.

Concentrated liquidity:

- Alih-alih menyediakan modal di semua harga, kamu memilih rentang harga.
- Di dalam rentang, likuiditasmu aktif dan bisa mendapat fee trading.
- Di luar rentang, umumnya tidak mendapat fee swap sampai harga kembali.
- Saat harga bergerak melewati rentang, posisimu makin terkonsentrasi ke satu token.
- Rentang sempit bisa mendapat fee lebih besar per dolar saat aktif, tapi butuh monitoring lebih dan bisa cepat tidak aktif.
- Rentang lebar tidak butuh banyak perawatan tapi biasanya fee per dolar lebih kecil.

Fee yang didapat bergantung pada volume trading lewat pool, bagianmu dari likuiditas aktif, fee tier pool, berapa lama posisi tetap in-range, dan persaingan dari liquidity provider lain. APR atau APY yang ditampilkan adalah historis atau estimasi, bukan jaminan. Reward insentif bisa dibayar dalam token yang volatil dan bisa berakhir atau berubah.

Impermanent loss, dijelaskan sederhana:

- Impermanent loss adalah selisih antara (a) menyimpan kedua token di dompetmu dan (b) menyediakannya ke pool lalu menariknya kembali. Penyebabnya adalah perubahan harga relatif pasangan. Kerugian ini disebut "impermanent" karena bisa menyusut bila harga kembali ke hubungan awal, tapi menjadi nyata saat kamu menarik.
- Contoh kecil: kamu deposit 1 SOL seharga $100 dan $100 USDC → pool mulai dengan $200. SOL naik ke $200 sementara USDC tetap ~$1. Pool menyeimbangkan ke arah memegang lebih banyak USDC dan lebih sedikit SOL. Posisimu mungkin bernilai sekitar $282,84 sebelum fee, sementara sekadar memegang aset awal bernilai $300. Selisih sekitar $17,16 adalah impermanent loss. Fee trading bisa menutupinya; bisa juga tidak cukup.
- Concentrated liquidity bisa memperbesar efek ini karena posisimu berubah komposisi lebih cepat di dekat atau di luar rentang yang dipilih.

Sebelum menambah likuiditas:

- Verifikasi kedua mint address token.
- Periksa umur pool, kedalaman likuiditas, volume harian, fee tier, dan volume terbaru.
- Periksa apakah pool aktif, paused, deprecated, atau tunduk pada permission yang tidak biasa.
- Tinjau harga saat ini relatif terhadap rentang yang kamu usulkan.
- Estimasi seberapa sering posisi bisa keluar dari rentang.
- Periksa apakah insentif bersifat sementara dan token apa yang membayarnya.
- Konfirmasi apakah penarikan permissionless dan apakah ada lockup.
- Baca audit dan pengungkapan keamanan protokol, sambil mengingat audit tidak menghilangkan bug.
- Mulai dengan jumlah yang kamu mampu kehilangannya.
- Hindari pool yang yield tampaknya terutama berasal dari reward token yang baru diterbitkan atau tipis diperdagangkan.

## Staking SOL

Staking native Solana:

- Staking native mendelegasikan SOL ke validator lewat sistem stake-account Solana.
- Reward bervariasi mengikuti inflasi network, performa validator, komisi, dan uptime.
- Staking menjadi aktif atau tidak aktif di batas epoch. Satu epoch kira-kira beberapa hari, tapi durasi tepatnya bisa bervariasi mengikuti kondisi network.
- Menonaktifkan stake umumnya mengharuskan menunggu stake menjadi tidak aktif di batas epoch berikutnya. Selama unstaking, SOL tidak bisa ditransfer bebas sampai deaktivasi selesai.
- Validator bisa punya uptime buruk, komisi tinggi, atau masalah operasional. Risiko slashing secara historis terbatas dibanding beberapa network proof-of-stake lain, tapi risiko teknis dan governance tetap ada.
- Pilih validator dengan memeriksa komisi, performa vote, status delinquent, identitas, dan konsentrasi. Jangan pilih hanya berdasarkan APY tertinggi yang ditampilkan.

Liquid staking token (LST):

- LST mewakili SOL yang di-stake sambil tetap bisa ditransfer dan dipakai di DeFi. Nilainya umumnya naik relatif terhadap SOL seiring reward staking terakru, atau memakai mekanisme akuntansi lain.
- JitoSOL: LST Jito. Bisa menerima reward staking dan mungkin juga mendapat benefit dari reward validator terkait MEV. Risiko: smart-contract dan risiko Jito, risiko validator dan delegasi, likuiditas pasar, dan kemungkinan deviasi dari SOL.
- mSOL: LST Marinade. Mewakili SOL yang didelegasikan lewat sistem pemilihan validator Marinade. Risiko: smart-contract dan governance Marinade, performa validator, likuiditas, dan risiko depeg.
- bSOL: LST BlazeStake. Mewakili SOL yang di-stake lewat BlazeStake. Risiko: protokol dan smart-contract, performa validator, likuiditas, dan depeg.
- Untuk setiap LST, periksa: mint address resmi token, exchange rate atau redemption value saat ini, kedalaman likuiditas instan, antrean redemption atau syarat cooldown, apakah token diterima sebagai collateral di tempat lain, dan audit smart-contract serta pengungkapan insiden terkini.
- LST bisa diperdagangkan di bawah nilai SOL yang mendasarinya saat market stress, bahkan ketika stake yang mendasari tetap sehat.

## Lending dan borrowing (marginfi dan Kamino)

Model umum: protokol seperti marginfi dan Kamino memungkinkan user menyuplai aset dan mendapat bunga variabel, mendeposit collateral, meminjam aset lain terhadap collateral itu, lalu membayar dan menarik, tunduk pada aturan likuiditas dan risiko.

Istilah penting:

- Loan-to-value (LTV): nilai pinjaman dibagi nilai collateral.
- Borrow limit: utang maksimum yang diizinkan di bawah parameter pasar dan aset saat ini.
- Liquidation threshold: titik di mana posisi bisa dilikuidasi.
- Health factor atau skor sejenis: ukuran jarak dari likuidasi.
- Utilization: berapa banyak likuiditas pasar yang sedang dipinjam.

Posisi bisa menjadi tidak aman karena collateral jatuh, aset pinjaman naik, bunga terakru, oracle berubah, atau likuiditas tidak tersedia. Likuidasi biasanya menjual collateral dan mengenakan penalti.

marginfi — sebelum memakai, periksa: collateral factor dan parameter likuidasi pasar saat ini, kurva suku bunga, sumber oracle, penalti likuidasi, caps aset dan likuiditas supply/borrow, serta pengaturan protokol dan asuransi. Hindari meminjam dekat maksimum. Sisakan ruang besar untuk pergerakan pasar yang cepat.

Kamino — Kamino menawarkan lending market dan mungkin juga produk automated liquidity atau vault. Jangan perlakukan semua produk Kamino sebagai identik. Untuk setiap market atau vault, periksa: aset collateral dan borrow yang tepat, LTV dan liquidation threshold, model suku bunga, perilaku oracle dan circuit-breaker, caps, batas penarikan, dan kontrol darurat, serta aturan strategi dan rebalancing untuk produk otomatis.

Praktik borrowing yang konservatif:

- Pinjam hanya untuk tujuan yang jelas.
- Utamakan collateral stabil dan LTV yang moderat.
- Simpan cadangan pembayaran di luar protokol.
- Pasang alert jauh sebelum likuidasi.
- Hindari memakai LST yang volatil atau token tipis sebagai collateral dengan leverage tinggi.
- Jangan pernah menganggap stablecoin akan tetap persis $1.

## Strategi yield untuk user kecil yang berhati-hati

Pilihan kompleksitas rendah:

- Native SOL staking dengan validator bereputasi: risiko utama lockup, performa validator, dan risiko sistem staking.
- Memegang liquid staking token tanpa leverage: menambah risiko protokol, depeg, likuiditas, dan smart-contract.
- Menyuplai stablecoin mayor di lending market yang mapan dengan ukuran moderat: risiko kegagalan smart-contract, kegagalan oracle, depeg stablecoin, lonjakan utilization, dan perubahan rate.
- Menyediakan posisi wide-range di pool SOL/USDC atau aset mayor yang dalam dan mapan: risiko impermanent loss, tidak aktif di luar rentang, kegagalan kontrak, dan fee yang turun.
- Memakai alokasi yang terdiversifikasi, bukan mengonsentrasikan semua dana di satu protokol atau token.

Jangan perlakukan ini sebagai pendapatan yang dijamin. Bandingkan yield yang diharapkan dengan risiko kehilangan principal. APR insentif sering turun cepat, dan reward bisa sulit dijual.

Kontrol operasional:

- Pakai dompet terpisah untuk DeFi.
- Simpan hanya jumlah seukuran transaksi di hot wallet.
- Uji dengan jumlah kecil dulu.
- Bookmark domain resmi dan verifikasi secara independen.
- Cabut approval token atau delegated permission yang tidak dipakai bila memungkinkan.
- Sisakan SOL untuk transaction fee.
- Catat deposit, penarikan, dan tax lot.
- Pakai alert untuk kesehatan lending, rentang pool, dan aktivitas dompet yang tidak biasa.

## Kesalahan umum dan penipuan

Kesalahan umum: mengira ticker atau nama token sama dengan mint address; set slippage berlebihan; mengabaikan price impact; menyediakan concentrated liquidity di rentang yang langsung menjadi tidak aktif; meminjam dekat threshold likuidasi; menghitung emisi reward token sebagai yield berkelanjutan; menganggap audit menjamin keamanan; menandatangani transaksi basi setelah quote berubah; memakai dompet yang sama untuk holding jangka panjang dan DeFi eksperimental; lupa bahwa network, priority, dan account-creation fee mengurangi return; tidak memeriksa apakah pool atau market sudah deprecated; memperlakukan LST sebagai SOL bebas risiko; menerima pesan atau tautan "support" yang tidak diminta.

Penipuan Solana yang sering terjadi: situs airdrop atau claim palsu yang meminta transaksi berbahaya; token palsu memakai ticker dan logo yang sama dengan aset legit; situs Jupiter, Raydium, Orca, staking, atau wallet palsu; layanan "recovery" yang meminta seed phrase atau private key; approval NFT atau token yang diam-diam mentransfer aset; malware atau ekstensi browser yang mengganti alamat wallet yang disalin; validator, karyawan protokol, dan akun support yang dipalsukan; link phishing lewat media sosial, Discord, Telegram, atau iklan pencarian; liquidity pool yang dibuat semata untuk menarik deposit lalu mengeksploitasi pembatasan penarikan atau kekuatan admin.

Jangan pernah mengungkapkan seed phrase, private key, backup wallet, atau signing authority. Tidak ada agen support protokol yang legit membutuhkannya. Bila sebuah transaksi meminta transfer, delegate, approval, atau interaksi program yang tidak dijelaskan, tolak.

## Standar 100% benar (Kecepatan, Ketepatan, Akurasi, Performa)

- **Kecepatan:** pakai quote dan parameter live; jangan buang waktu pada quote basi — refresh quote bila transaksi tertunda. Kerjakan pengecekan independen (mint, pool, rate) secara paralel.
- **Ketepatan:** pilih venue dan produk yang tepat untuk tujuan itu (swap vs LP vs staking vs lending); pakai mint address yang tepat; set slippage sekecil mungkin yang masih berhasil.
- **Akurasi:** verifikasi setiap hasil (signature, saldo aktual, status finalized) sebelum melanjutkan; jangan sajikan APR/APY sebagai jaminan; bila belum terkonfirmasi, katakan begitu.
- **Performa:** selesaikan setiap aksi sampai terverifikasi (tanda tangan + konfirmasi + saldo), catat semua posisi dan transaksi, tangani error dengan klasifikasi dan laporkan bila mentok.

## Referensi

- Staking Solana: https://solana.com/staking
- Dokumentasi developer Jupiter: https://dev.jup.ag/
- Dokumentasi Raydium: https://docs.raydium.io/
- Dokumentasi Orca: https://docs.orca.so/
- Dokumentasi Jito: https://docs.jito.network/
- Dokumentasi Marinade: https://docs.marinade.finance/
- Dokumentasi marginfi: https://docs.marginfi.com/
- Dokumentasi Kamino: https://docs.kamino.finance/
