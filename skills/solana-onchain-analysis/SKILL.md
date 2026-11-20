# Analisis On-Chain Solana

## Aturan keras dulu

- Verifikasi fakta dari transaksi yang ditandatangani, state akun, dan instruksi program. Label explorer, logo token, klaim sosial, dan ringkasan API adalah petunjuk, BUKAN bukti.
- Jangan pernah mempercayai screenshot saja. Selalu butuh signature atau alamat yang bisa dicek ulang secara independen.
- Jangan pernah meminta, menyimpan, atau memasukkan seed phrase / private key ke chat, file, log, atau prompt apa pun.
- Jangan pernah menyatakan kesimpulan identitas ("wallet ini milik X") dari clustering saja. Clustering adalah bukti keterkaitan, bukan bukti identitas.
- Simpan bukti setiap kesimpulan: alamat, signature, slot, jumlah raw, commitment level, endpoint RPC, dan waktu pengambilan.

## Membaca Solscan dan Solana Explorer

Halaman transaksi — catat signature, slot, block time, fee payer, dan status saat ini. Periksa:

- Fee payer: akun yang membayar fee transaksi.
- Signer: akun yang tanda tangannya mengotorisasi transaksi.
- Recent blockhash dan slot.
- Instruksi dan inner instruction.
- Account key beserta flag writable/signing.
- Log message.
- Compute unit dan prioritization fee.
- Perubahan saldo token dan SOL.
- Field error dan return data bila tersedia.
- Satu transaksi bisa berisi beberapa instruksi. Transfer token bisa bersarang di dalam CPI (cross-program invocation), jadi periksa "inner instructions" juga, bukan hanya instruksi top-level.

Status signature — commitment level Solana:

- processed: node sudah memproses transaksi. Masih bisa di-rollback.
- confirmed: transaksi masuk blok dengan konfirmasi cluster yang cukup.
- finalized: transaksi sudah rooted dan sangat tahan terhadap rollback.
- Untuk klaim yang serius, cek ulang pada commitment finalized. Status explorer bisa berubah saat transaksi masih menyebar.

Method RPC: `getSignatureStatuses`, `getTransaction`, `getBlock`, `getSignaturesForAddress`.

Respons HTTP yang sukses TIDAK membuktikan transaksi sukses. Periksa: field `result` ada; `meta.err` null; status signature non-null; slot dan block time masuk akal; message transaksi dan account key cocok dengan klaim.

Instruksi dan program ID — verifikasi program yang dipanggil lewat program ID-nya, bukan lewat nama instruksi yang ditampilkan. Program umum:

- System Program: `11111111111111111111111111111111`
- SPL Token Program: `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
- Token-2022 Program: alamat lengkapnya ada di dokumentasi Solana saat ini atau di transaksi — jangan pernah mengandalkan tampilan yang terpotong.
- Associated Token Account Program, Compute Budget Program, dan router/DEX/lending/bridge spesifik.
- Label explorer bisa salah, tidak lengkap, atau berdasarkan database label alamat. Salin alamat program lengkap dan verifikasi secara independen.

Perubahan saldo — untuk SOL, bandingkan `meta.preBalances` dan `meta.postBalances` (dalam lamports; sertakan fee transaksi saat merekonsiliasi). Untuk token SPL, bandingkan `meta.preTokenBalances` dan `meta.postTokenBalances`, dan periksa mint address, owner, alamat token account, jumlah raw, decimals, dan index akun. Tampilan "+100 token" hanya bermakna setelah mint, decimals, owner, dan transaksi yang sukses dikonfirmasi.

Membedakan transfer nyata dari tampilan palsu — transfer nyata membutuhkan SEMUA ini:

- Signature valid yang ditemukan lewat endpoint RPC independen.
- `meta.err = null`.
- Status finalized, bila finalitas penting.
- Instruksi transfer token atau CPI yang terverifikasi.
- Mint address yang diharapkan.
- Akun token sumber dan tujuan yang diharapkan.
- Perubahan saldo yang konsisten dengan instruksi.
- Hubungan authority/signature yang benar.
- Tidak ada reversal atau transfer kompensasi sesudahnya yang mengubah interpretasi.

Tanda peringatan: hanya screenshot atau URL explorer tanpa signature; simbol atau logo token cocok dengan aset dikenal tapi mint berbeda; transfer ditampilkan di UI portofolio tanpa transaksi finalized yang sesuai; transaksi gagal tapi instruksi yang dicoba tetap ditampilkan; token account dikendalikan owner yang berbeda dari yang diharapkan; "transfer" yang hanya mengubah metadata, membuat akun, atau memakai program berbahaya dengan label instruksi yang menyesatkan; jumlah token yang baru masuk akal setelah memakai decimals yang salah; akun wSOL atau token perantara yang disangka transfer langsung wallet-ke-wallet.

Selalu salin alamat mint, wallet, token-account, dan program secara lengkap.

## Verifikasi kontrak token

Akun mint — ambil langsung dengan RPC: `getAccountInfo(mint, {encoding:"base64", commitment:"finalized"})`, `getTokenSupply(mint)`, `getTokenLargestAccounts(mint)`. Verifikasi: akun ada; owner-nya SPL Token Program atau Token-2022 Program; data akun ter-decode sebagai mint account; mint address persis yang dipromosikan; akun itu bukan token account, metadata account, atau alamat bernama mirip. Untuk SPL Token klasik, decode layout mint. Untuk Token-2022, decode field mint dasar plus data extension TLV.

Mint authority — baca dari mint account. Authority non-null bisa mencetak supply tambahan. Authority null berarti minting dinonaktifkan permanen untuk mint itu. Authority multisig tetap authority — periksa akun multisig dan threshold signer. Alamat program-derived bisa berarti minting dikendalikan program — analisis program itu sebelum menganggapnya aman. Jangan simpulkan immutability dari website token atau badge explorer.

Freeze authority — baca dari mint account. Authority non-null bisa membekukan akun token dan mencegah transfer atau penarikan. Authority null berarti authority itu sudah dihapus permanen. Authority bisa berupa multisig atau alamat yang dikendalikan program. Periksa apakah akun token yang relevan sedang dibekukan dan periksa perubahan authority secara historis.

Supply dan decimals — pakai `getTokenSupply`, data mint account, dan jumlah raw token-account. Supply adalah jumlah integer base-unit. Jumlah tampilan manusia = raw amount / 10^decimals. Verifikasi: decimals dari mint (bukan dari website), supply saat ini, apakah supply masih bisa bertambah, riwayat burn dan mint bila circulating supply diklaim, dan saldo token-account memakai jumlah raw untuk menghindari kesalahan pembulatan. "Total supply", "circulating supply", dan "maximum supply" adalah klaim yang berbeda.

Metadata dan update authority — untuk metadata gaya Metaplex, temukan metadata PDA dari mint dan verifikasi: alamat metadata account, nama, simbol, URI, creators, update authority, apakah metadata mutable, dan konten URI beserta riwayat hosting-nya bila relevan. Update authority metadata terpisah dari mint authority SPL. Mencabut satu tidak mencabut yang lain. URI, gambar, nama, dan simbol tidak membuktikan kepemilikan, legitimasi, atau supply.

Extension Token-2022 — identifikasi dulu owner mint. Mint Token-2022 bisa berisi extension yang mengubah perilaku secara material. Decode area extension TLV dan periksa bila berlaku: transfer fee dan fee authority, permanent delegate, default account state (termasuk frozen-by-default), transfer hook program, confidential transfer, non-transferable token, konfigurasi interest-bearing, metadata pointer dan token metadata, group atau group-member pointer, konfigurasi pausable, immutable owner dan extension akun terkait, serta konfigurasi transfer-fee dan withheld fee. Verifikasi authority dan nilai extension saat ini langsung dari data akun. Token bisa tampak bisa ditransfer di UI sementara transfer hook, pause authority, fee, atau default state mengubah risiko sebenarnya.

## Melacak wallet

Tetapkan alamat yang benar — konfirmasi alamat base-58 lengkap dan network-nya. Mainnet, devnet, dan test validator Solana bisa berisi akun yang tidak terkait dengan aktivitas mirip. Periksa `getBalance`, `getAccountInfo`, `getSignaturesForAddress`, token account yang dimiliki alamat itu, dan apakah alamat itu system account, PDA, token account, program, deposit exchange, atau multisig.

Sumber pendanaan — lacak inbound SOL atau token transfer yang bermakna paling awal, bukan hanya top-up terbaru. Catat: alamat sumber, alamat tujuan, jumlah dan mint, signature dan slot finalized, apakah sumber itu exchange, bridge, faucet, layanan mirip mixer, treasury, atau wallet lain, dan apakah sumber yang sama mendanai banyak wallet. Pendanaan dari sumber yang sama adalah petunjuk investigasi, bukan bukti kepemilikan bersama.

Wallet terhubung dan clustering — indikator yang berguna: funder yang sama atau jalur pendanaan berulang; pembelian atau penjualan terkoordinasi dalam blok yang sama atau jendela waktu singkat; transfer dan pergerakan saldo yang tersinkronisasi; pemakaian ulang fee payer atau wallet operasional yang sama; endpoint deposit atau penarikan bersama; interaksi berulang dengan program yang sama; hubungan authority, multisig, atau PDA yang sama; pola konstruksi transaksi yang identik. Pakai analisis graf dengan timestamp, jumlah, mint token, slot, dan program ID. Simpan signature persis yang mendukung setiap edge.

Clustering TIDAK BISA membuktikan: dua wallet milik orang yang sama; wallet dikendalikan sebuah proyek; trader berniat memanipulasi pasar; funder bersama adalah beneficial owner; aktivitas tersinkronisasi terkoordinasi dan bukan otomatis, kustodian, atau akibat airdrop. Sampaikan kesimpulan sebagai probabilitas atau hubungan yang teramati, kecuali ada bukti langsung.

Pola transaksi — klasifikasikan aktivitas berdasarkan: pendanaan dan konsolidasi, akuisisi token, transfer ke wallet baru, swap DEX, penambahan/penghapusan likuiditas, interaksi program, burn dan mint, round trip berulang, timing relatif terhadap listing, pengumuman, dan unlock, serta pemakaian ulang payer, signer, dan token-account. Pertimbangkan bot, arbitrageur, market maker, exchange, dan kustodian sebelum melabeli perilaku sebagai mencurigakan.

## Wash trading, volume palsu, dan inflasi jumlah holder

Indikator wash trading: siklus beli-jual berulang antara klaster wallet kecil yang sama; jumlah mirip dan holding period pendek; perubahan posisi net nol atau minimal; volume terkonsentrasi di wallet baru yang didanai; transfer yang didanai satu sumber diikuti trading tersinkronisasi; trade yang dirute lewat pool yang sama dengan sedikit tujuan ekonomi; lonjakan volume tanpa pembeli unik, likuiditas, price discovery, atau pertumbuhan holder yang sesuai; pergerakan melingkar lewat wallet perantara. Bedakan volume swap on-chain dari permintaan organik. Swap bisa dihitung sebagai volume sementara eksposur ekonomi tetap di dalam satu klaster yang dikendalikan.

Sinyal volume dan likuiditas palsu — periksa: reserve pool sebelum dan sesudah trade, price impact dan slippage, kepemilikan dan status lock LP, apakah likuiditas bisa ditarik oleh satu authority, apakah volume berasal dari sedikit wallet atau banyak entitas independen, net flow token dan SOL/USDC, route aggregator dan perilaku self-crossing berulang. Jangan perlakukan rasio volume-terhadap-likuiditas yang tinggi sebagai bukti sendiri; bot legit bisa menghasilkan turnover tinggi.

Inflasi jumlah holder — teknik umum: dusting banyak wallet dengan saldo kecil; membagi holding satu owner ke banyak token account; airdrop farming dan wallet sybil; membuat akun yang tidak pernah bertransaksi sesudahnya; mengirim token ke akun yang tidak bisa diakses, dibekukan, atau ditinggalkan; menghitung token account bukan owner unik; menghitung artefak zero-balance atau closed-account secara salah. Untuk estimasi holder yang bermakna: enumerasi token account untuk mint yang tepat; kecualikan zero balance bila sesuai; resolve owner tiap token account; deduplikasi owner; identifikasi akun frozen, delegated, escrow, vault, pool, burn, treasury, exchange, dan yang dikendalikan program; laporkan jumlah token-account raw DAN jumlah owner yang sudah disesuaikan; tunjukkan konsentrasi berdasarkan top owner dan klaster. Jumlah token account BUKAN jumlah wallet holder.

## Pengecekan programatik

Solana RPC — method yang berguna: `getSignaturesForAddress` (riwayat signature dengan pagination), `getTransaction` (transaksi dan metadata yang ter-parse), `getBlock` (semua transaksi di satu slot), `getSignatureStatuses` (status dan state konfirmasi), `getAccountInfo` (data akun mentah dan owner), `getMultipleAccounts` (baca akun batch), `getTokenSupply` (supply dan decimals), `getTokenAccountBalance` (satu token account), `getTokenAccountsByOwner` (token account milik owner), `getProgramAccounts` (enumerasi akun untuk program, dengan filter), `getTokenLargestAccounts` (akun token terbesar), `getBalance` (saldo SOL). Untuk daftar holder, query program token terkait dengan `getProgramAccounts` memakai filter mint, decode layout token-account, dan paginasi atau proses hasilnya dengan aman. Provider RPC bisa membatasi ukuran hasil; pakai `dataSlice`, filter, batch, atau provider terindeks.

Helius API — tergantung produk dan versi endpoint, Helius umumnya menyediakan: riwayat transaksi alamat yang ditingkatkan, tipe transaksi yang ter-parse dan aktivitas akun, saldo token dan informasi token-account, pencarian aset DAS dan query kepemilikan, serta webhook dan notifikasi gaya streaming. Pakai dokumentasi endpoint saat ini yang tepat dan autentikasi secara privat. Jangan taruh key di script, URL, log, repository, atau chat. Untuk investigasi holder besar, gabungkan hasil Helius terindeks dengan pengecekan RPC Solana langsung. API terindeks bisa lag, menghilangkan tipe instruksi yang tidak didukung, menormalisasi alamat secara salah, atau mengklasifikasikan transaksi secara tidak sempurna.

Yang harus diverifikasi sebelum mempercayai respons API apa pun: periksa status HTTP dan field error respons; konfirmasi network dan alamat yang diminta; verifikasi cursor pagination dan urutan; periksa apakah endpoint memakai data processed, confirmed, atau finalized; ambil ulang signature kritis dengan `getTransaction`; konfirmasi `meta.err` null; bandingkan jumlah yang ter-parse dengan saldo token raw dan decimals mint; verifikasi mint dan program ID; periksa riwayat yang terpotong, ter-deduplikasi, atau hilang; hormati rate limit dan retry hanya dengan retry berbatas yang terdiagnosis; catat waktu pengambilan, slot, commitment, endpoint, dan parameter query; cross-check klaim material dengan provider RPC kedua atau data akun langsung.

## Checklist verifikasi

Klaim token:

- [ ] Mint address persis disalin dan dikonfirmasi secara independen
- [ ] Mint account ada pada commitment finalized
- [ ] Owner adalah program token yang diharapkan
- [ ] Decimals dan raw supply ter-decode dari mint
- [ ] Mint authority diperiksa
- [ ] Freeze authority diperiksa
- [ ] Extension Token-2022 ter-decode dan authority-nya ditinjau
- [ ] Metadata PDA, URI, dan update authority diperiksa
- [ ] Supply saat ini direkonsiliasi dengan riwayat mint/burn bila perlu
- [ ] Jumlah holder ter-deduplikasi berdasarkan owner, bukan jumlah token-account
- [ ] Top holder, pool, treasury, exchange, dan akun program dipisahkan
- [ ] Kepemilikan likuiditas, status lock, dan authority penarikan diperiksa

Klaim wallet:

- [ ] Alamat wallet lengkap dan network dikonfirmasi
- [ ] Jenis akun diidentifikasi
- [ ] Sumber pendanaan dilacak ke signature finalized
- [ ] Token account dan owner dienumerasi
- [ ] Riwayat transaksi diperoleh dengan pagination terverifikasi
- [ ] Hubungan fee payer, signer, dan tujuan diperiksa
- [ ] Wallet terkoordinasi didokumentasikan dengan signature persis
- [ ] Penjelasan kustodian, exchange, bot, treasury, dan airdrop dipertimbangkan
- [ ] Clustering disajikan sebagai bukti keterkaitan, bukan bukti identitas

Klaim transaksi:

- [ ] Signature lengkap di-query secara independen
- [ ] Status finalized bila finalitas penting
- [ ] `meta.err` null
- [ ] Slot dan block time dicatat
- [ ] Fee payer dan signer yang benar diidentifikasi
- [ ] Instruksi top-level dan inner diperiksa
- [ ] Program ID diverifikasi dari account key
- [ ] Saldo SOL pre/post direkonsiliasi dengan fee
- [ ] Saldo token pre/post direkonsiliasi dengan mint dan decimals
- [ ] Owner akun token sumber dan tujuan dikonfirmasi
- [ ] Tidak mengandalkan simbol token, metadata, atau label explorer yang menyesatkan
- [ ] Transaksi lanjutan diperiksa untuk reversal, refund, burn, atau transfer-away

Praktik terbaik: simpan alamat, signature, slot, jumlah raw, commitment level, endpoint RPC, dan timestamp pengambilan yang tepat untuk mendukung setiap kesimpulan.

## Standar 100% benar (Kecepatan, Ketepatan, Akurasi, Performa)

- **Kecepatan:** pakai RPC dan explorer langsung; kerjakan pengecekan independen (mint, holder, transaksi) secara paralel; pakai batch read (`getMultipleAccounts`) dan pagination yang benar.
- **Ketepatan:** periksa alamat dan program ID yang tepat; pakai commitment level yang tepat untuk klaimnya (finalized bila finalitas penting); deduksi owner, bukan token-account.
- **Akurasi:** verifikasi setiap klaim dari data on-chain sebelum menyimpulkannya; jangan sajikan label explorer, logo, atau klaim sosial sebagai bukti; bila belum terkonfirmasi, katakan begitu; sajikan clustering sebagai probabilitas, bukan identitas.
- **Performa:** selesaikan verifikasi sampai checklist tuntas, simpan jejak bukti lengkap (alamat, signature, slot, jumlah raw, endpoint, timestamp), dan laporkan bila mentok.

## Referensi

- Dokumentasi Solana RPC: https://solana.com/docs/rpc
- Solana Explorer: https://explorer.solana.com/
- Solscan: https://solscan.io/
- Dokumentasi token Solana: https://solana.com/docs/tokens
- Token-2022: https://www.solana-program.com/docs/token-2022
- Dokumentasi Helius: https://www.helius.dev/docs
- Dokumentasi Metaplex Token Metadata: https://developers.metaplex.com/token-metadata
