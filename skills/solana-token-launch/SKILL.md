# Peluncuran Token Solana

## Aturan keras dulu

- Gunakan HANYA dompet agent yang terpisah dan kecil untuk percobaan peluncuran: `BupM4zgsie9upSt94UdVAEHaKr1KRWpPMDgvXZGm46qf`. Jangan pernah memakai dompet utama user (`95ubFWyurr4GAxPjS3z15HjDnRX3SPNtnrdyRcBjRbY6`) tanpa persetujuan eksplisit user untuk aksi itu.
- Jangan pernah meminta, menyimpan, atau memasukkan seed phrase / private key ke chat, file, log, atau prompt apa pun.
- Jangan pernah menjanjikan profit, harga, atau kesuksesan peluncuran.
- Identifikasi token HANYA lewat mint address. Nama, ticker, logo, dan akun sosial bisa disalin.
- Satu persetujuan user berlaku untuk satu aksi saja (satu pembuatan token, satu pool, satu transaksi).
- Angka biaya platform (pump.fun, Raydium) BERUBAH dan tidak terverifikasi di sini — SELALU cek biaya live di interface resmi sebelum menandatangani. Angka yang ditandai "cek live" di skill ini bukan fakta yang sudah diverifikasi.

## Cara 1: meluncurkan lewat pump.fun

Langkah umum:

1. Buka situs resmi pump.fun dan hubungkan dompet Solana yang sudah didanai SOL.
2. Isi nama token, simbol, deskripsi, gambar, dan tautan opsional.
3. Tinjau pengaturan peluncuran, pembelian awal bila ada, dan seluruh transaksi dompet.
4. Tandatangani transaksi pembuatan.
5. Simpan mint address dan signature transaksi pembuatan.

Biaya (cek live — angka ini historis, bukan harga terverifikasi November 2026):

- Publikasi lama menyebut pembuatan 0 SOL dengan fee 0,015 SOL saat pembeli pertama membeli. Angka ini TIDAK terverifikasi saat ini — cek interface live siapa yang dikenakan biaya (creator, pembeli pertama, atau pihak lain).
- Pembelian awal, network fee, dan biaya pembuatan akun adalah biaya terpisah.

Bonding curve:

- Pembeli berdagang melawan kurva harga yang dikendalikan program sebelum graduation.
- Pembelian menaikkan harga kurva; penjualan menurunkannya.
- Virtual reserve bisa menentukan harga. Reserve atau market cap yang ditampilkan BUKAN likuiditas yang bisa ditarik sepenuhnya.
- Market cap = harga marginal token × supply. Itu bukan berarti SOL sebanyak itu sudah masuk pasar.
- Graduation terjadi saat kondisi penyelesaian program terpenuhi. Ambang dolar yang ditampilkan bisa berubah mengikuti harga SOL.

Tujuan graduation:

- Pump.fun memperkenalkan PumpSwap pada Maret 2025 sebagai tujuan graduation native, menggantikan jalur migrasi Raydium lama untuk graduation baru. Jadi "setiap token pump.fun lulus ke Raydium" sudah kedaluwarsa.
- Saat graduation, program memindahkan aset yang ditentukan ke AMM pool dan perdagangan beralih dari bonding curve ke pool itu. Verifikasi program pool, vault, likuiditas, dan kepemilikan/penguncian likuiditas hasil migrasi. Jangan asumsikan fee migrasi, perlakuan LP, atau aturan revenue creator lama masih berlaku.
- Peluncuran pump.fun normalnya menangani pool graduation-nya sendiri. Membuat pool kedua secara manual adalah keputusan likuiditas terpisah dan bisa memecah perdagangan.

## Cara 2: membuat token langsung (SPL Token / Token-2022)

Pilih program token dulu:

- SPL Token asli: dukungan paling luas, biasanya pilihan paling sederhana untuk token fungible konvensional.
- Token-2022: mendukung extension seperti transfer fee dan transfer hooks. Wallet, exchange, dan program pool mendukung subset extension yang berbeda.

Periksa venue perdagangan yang dituju SEBELUM memilih extension. Beberapa extension harus dikonfigurasi saat inisialisasi; mengubah arah sesudahnya bisa mengharuskan mint baru.

Langkah dasar:

1. Alokasikan mint account rent-exempt yang dimiliki program token pilihan.
2. Inisialisasi decimals, mint authority, dan freeze authority opsional.
3. Buat associated token account untuk menampung supply.
4. Mint supply yang dimaksud.
5. Buat metadata dan verifikasi URI beserta isinya.
6. Distribusikan alokasi dan buat likuiditas.
7. Cabut atau amankan authority sesuai desain token yang dipublikasikan.
8. Verifikasi state akhir on-chain.

Decimals adalah presisi tampilan, bukan supply. Enam dan sembilan adalah pilihan umum. Contoh: satu juta token dengan enam decimals membutuhkan 1.000.000.000.000 raw unit.

Authority:

- **Mint authority** — bisa mencetak supply tambahan. Untuk token fixed-supply, mint semua alokasi yang dibutuhkan dulu, lalu set authority ini ke None. Pencabutan bersifat permanen.
- **Freeze authority** — bisa membekukan akun token. Untuk token permissionless konvensional, hilangkan saat inisialisasi atau cabut. Beberapa desain yang diregulasi sengaja mempertahankannya; ungkapkan dengan jelas.
- **Metadata update authority** — mengendalikan perubahan metadata Metaplex. Ini terpisah dari mint dan freeze authority. Mencabut mint authority TIDAK membuat metadata immutable.

Metadata:

- Metaplex Token Metadata umumnya memakai metadata PDA terpisah yang terkait mint. Isinya antara lain nama, simbol, dan URI yang menunjuk ke JSON berisi deskripsi dan gambar.
- Untuk Metaplex, immutability diatur oleh setting `isMutable` di metadata account. Mengaturnya ke false bersifat permanen. Jangan menggambarkannya sekadar sebagai "mencabut update authority", karena metadata account tetap berisi field update-authority.
- URI metadata yang immutable tidak membuat KONTEN di URI itu immutable. Pakai storage yang tahan lama dan verifikasi gambar dan JSON tetap bisa diakses.
- Mencabut authority dasar tidak menghilangkan kekuatan extension Token-2022. Periksa transfer fee, permanent delegate, transfer hooks, default account state, dan semua authority extension.

## Membuat pool Raydium / Orca

Jenis pool:

- **Raydium CPMM** — constant-product pool, umumnya cocok untuk likuiditas sederhana di seluruh rentang harga. Raydium juga punya pool AMM v4 lama; jangan samakan kebutuhan market-account-nya dengan CPMM.
- **Raydium CLMM** — concentrated liquidity. Kamu memilih rentang harga. Modal lebih terkonsentrasi, tapi posisi berhenti menyediakan likuiditas aktif saat harga keluar dari rentang.
- **Orca Whirlpools** — concentrated-liquidity pool dengan likuiditas berbasis posisi. Fee tier, tick spacing, dan opsi pembuatan harus dicek di interface saat ini.

Harga awal:

- Untuk constant-product pool sederhana, rasio reserve awal menentukan harga awal, sebelum efek fee dan pembulatan.
- Contoh: deposit 100.000.000 TOKEN dan 10 SOL → harga awal = 0,0000001 SOL per TOKEN. Jika total supply 1.000.000.000 TOKEN, fully diluted valuation tersirat = 100 SOL.
- Untuk concentrated liquidity, kamu menginisialisasi harga secara eksplisit dan memilih rentang. Jumlah deposit yang dibutuhkan bergantung pada harga dan rentang itu, bukan sekadar rasio reserve sembarang.
- Periksa urutan token dan decimals dengan hati-hati. Interface bisa menampilkan TOKEN/SOL atau SOL/TOKEN.

Kepemilikan likuiditas:

- Pool constant-product konvensional umumnya menerbitkan LP token fungible yang mewakili bagian atas aset pool.
- Pool concentrated-liquidity umumnya memakai position account, biasa dikendalikan lewat position NFT.
- Memegang aset-aset ini umumnya memungkinkan penarikan likuiditas.

Locking vs burning:

- Locking menaruh kontrol penarikan di bawah locker dengan kondisi rilis yang ditentukan.
- Burning LP token fungible bisa menyerahkan hak penebusannya secara permanen.
- Mentransfer LP token ke alamat yang disebut "burn wallet" BUKAN sama dengan mengeksekusi token burn.
- Posisi concentrated-liquidity butuh mekanisme locking yang kompatibel. Jangan membakar position NFT begitu saja; pahami dulu perilaku protokol dan kontrol penarikan.
- Verifikasi program locker, tanggal unlock, jumlah yang dikunci, penerima, dan kekuatan admin atau emergency-withdrawal apa pun.
- Likuiditas yang dikunci TIDAK mencegah insider menjual holding token mereka.

## Biaya dan anggaran SOL

Angka Solana yang relatif stabil (mekanisme mapan; konfirmasi live sebelum bertindak):

- Base transaction fee: 5.000 lamports per signature, atau 0,000005 SOL.
- Mint account SPL asli: 82 byte; deposit rent-exempt sekitar 0,0014616 SOL.
- Token account SPL asli: 165 byte; deposit rent-exempt sekitar 0,00203928 SOL.
- Konfirmasi angka rent aktual dengan `getMinimumBalanceForRentExemption` untuk ukuran akun yang sebenarnya. Extension Token-2022 memperbesar ukuran akun dan deposit yang dibutuhkan.
- Deposit rent tidak semuanya fee yang hilang permanen. Akun yang memenuhi syarat bisa mengembalikan depositnya saat ditutup dengan benar; menutup mint punya batasan berbeda dan umumnya tidak tersedia untuk mint SPL asli.

Biaya tambahan: alokasi metadata account, storage metadata/gambar, biaya pembuatan pool, vault dan state account pool, position account atau NFT likuiditas, priority fee dan tip opsional, pembelian awal, dan likuiditas awal itu sendiri.

Priority fee: `ceil(compute-unit limit yang diminta × micro-lamports per compute unit / 1.000.000)`. Contoh: 200.000 compute unit pada 10.000 micro-lamports per unit = 2.000 lamports, atau 0,000002 SOL. Limit compute yang diminta menentukan perhitungan ini, bukan compute yang benar-benar dipakai. Tip terpisah.

Biaya pembuatan pool Raydium CPMM pernah tercatat 0,15 SOL (cek live — ini referensi historis, bukan quote terverifikasi November 2026). Jenis dan konfigurasi pool berpengaruh.

Anggaran praktis (planning allowance, bukan quote platform):

- Pembuatan token langsung saja: buffer perencanaan 0,02–0,05 SOL untuk setup sederhana.
- Token langsung + pool: sisakan sekitar 0,3–0,5 SOL untuk overhead setup, lalu tambah likuiditas yang dimaksud. Contoh: 2 SOL likuiditas awal + 0,5 SOL allowance operasional berarti mulai dengan sekitar 2,5 SOL.
- Pump.fun: danai biaya transaksi yang dikutip saat ini, pembelian awal bila ada, dan buffer transaksi kecil. Jadwal fee-nya harus dicek live.
- Peluncuran dengan likuiditas hanya 1–5 SOL bisa berfungsi secara teknis tapi sangat mudah digerakkan harganya. Tidak ada jumlah likuiditas yang "cukup" secara universal.

## Keamanan dan kesalahan umum

Sebelum peluncuran:

- Pakai domain resmi dan verifikasi program ID.
- Pakai dompet deployment khusus; amankan authority treasury yang signifikan dengan hardware wallet atau multisig.
- Periksa supply, decimals, alokasi, metadata, dan kompatibilitas venue.
- Publikasikan mint address dan jadwal alokasi yang tepat.
- Periksa setiap transaksi sebelum menandatangani.

Sebelum mengklaim token sudah final:

- Konfirmasi total supply yang dimaksud.
- Cabut mint authority bila mengklaim fixed supply.
- Cabut freeze authority bila mengklaim akun tidak bisa dibekukan.
- Periksa semua extension Token-2022 beserta authority-nya.
- Putuskan dan ungkapkan apakah metadata tetap mutable.
- Lock atau burn likuiditas sesuai janji, dengan bukti yang bisa diverifikasi secara independen.
- Verifikasi treasury, tim, dan pengaturan vesting.

Kesalahan dan penipuan yang sering terjadi:

- Membuat harga awal yang salah karena decimals atau urutan token terbalik.
- Mengira pencabutan mint authority juga menghapus kontrol freeze atau metadata.
- Memakai extension Token-2022 yang tidak didukung pool target.
- Mengiklankan "LP burned" padahal hanya sebagian kecil yang dibakar.
- Mengunci satu pool sambil mempromosikan pool lain yang likuiditasnya bisa ditarik.
- Mengklaim "100% locked LP" tanpa mengungkapkan likuiditasnya sangat kecil.
- Mempertahankan insider supply besar yang tidak diungkapkan.
- Transfer fee tinggi atau bisa diubah, permanent delegate, atau hook yang membatasi.
- Locker palsu, mint address palsu, dan akun sosial yang disalin.
- Membayar agen "listing", "verifikasi", atau "aktivasi graduation" yang tidak diminta.
- Menganggap label explorer atau skor keamanan otomatis sebagai audit.
- Tidak menyisakan SOL untuk transaksi berikutnya.

## Verifikasi peluncuran (Solscan dan RPC)

Cari di Solscan memakai mint address yang tepat.

- **Mint:** konfirmasi program token pemilik (SPL Token asli atau Token-2022), decimals dan supply saat ini, mint dan freeze authority, extension Token-2022 bila ada, metadata URI, update authority, dan mutabilitas bila ditampilkan. Field explorer yang hilang BUKAN bukti authority dicabut — konfirmasi data akun lewat RPC atau decoder tepercaya bila perlu.
- **Holder:** tinjau akun token terbesar. Bedakan vault pool, akun bonding-curve, locker, akun vesting, dan holder biasa. Nilai konsentrasi setelah akun-akun itu diidentifikasi. Ingat satu owner bisa membagi holding ke banyak wallet.
- **Pool:** konfirmasi kedua mint address termasuk quote asset, kepemilikan pool oleh program Raydium, Orca, atau PumpSwap yang dimaksud, alamat dan saldo vault pool, harga yang dikonfigurasi dan likuiditas aktif. Untuk concentrated liquidity, periksa rentang posisi; likuiditas headline bisa berada di luar rentang perdagangan.
- **LP dan lock:** untuk LP token fungible, verifikasi mint, supply, holder, dan instruksi burn yang sebenarnya. Untuk lock, periksa locker account, aset yang dideposit, jumlah, dan kondisi rilis. Untuk posisi concentrated, verifikasi siapa yang mengendalikan posisi dan apakah likuiditas masih bisa ditarik.
- **Transaksi:** periksa transaksi pembuatan, minting, perubahan authority, inisialisasi pool, graduation, dan locking. Konfirmasi sukses dan status finalized. Baca detail instruksi dan perubahan saldo token. Pakai state akun saat ini BUKAN hanya transaksi lama: screenshot transaksi lama tidak membuktikan state saat ini.
- Cek RPC yang berguna: `getAccountInfo`, `getTokenSupply`, `getTokenLargestAccounts`, `getTransaction`, `getMinimumBalanceForRentExemption`.

## Standar 100% benar (Kecepatan, Ketepatan, Akurasi, Performa)

- **Kecepatan:** cek biaya dan parameter live di interface resmi sebelum bertindak; jangan buang waktu menebak angka yang berubah. Pakai RPC/explorer langsung untuk verifikasi, bukan menunggu browser.
- **Ketepatan:** pilih jalur peluncuran yang tepat (pump.fun vs SPL langsung vs Token-2022) berdasarkan venue dan desain token; pakai mint address yang tepat di setiap langkah.
- **Akurasi:** verifikasi setiap hasil on-chain sebelum melanjutkan; jangan sajikan angka biaya platform sebagai fakta bila belum dicek live; bila belum terkonfirmasi, katakan begitu.
- **Performa:** selesaikan peluncuran sampai terverifikasi (mint + authority + pool + lock), simpan mint address, signature, dan bukti lock; tangani error dengan klasifikasi dan laporkan bila mentok.

## Referensi

- pump.fun: https://pump.fun/
- Dokumentasi publik pump.fun: https://github.com/pump-fun/pump-public-docs
- Dokumentasi token Solana: https://solana.com/docs/tokens
- Biaya transaksi Solana: https://solana.com/docs/core/fees
- Token-2022: https://www.solana-program.com/docs/token-2022
- Metaplex Token Metadata: https://developers.metaplex.com/token-metadata
- Dokumentasi Raydium: https://docs.raydium.io/
- Dokumentasi Orca: https://docs.orca.so/
- Solscan: https://solscan.io/
