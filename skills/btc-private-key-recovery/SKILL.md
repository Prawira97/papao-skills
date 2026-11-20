---
name: btc-private-key-recovery
description: Recover a lost Bitcoin private key the legitimate way — what is mathematically impossible, the real recovery paths (wallet.dat, backups, drive forensics), safe tools, and scam warnings. Use when the user lost access to a Bitcoin wallet and asks how to find the private key.
---

# Bitcoin Private Key Recovery — Lost Key Playbook

Skill buatan Papao (2026-11-19) dari riset terverifikasi, bukan dari repo pihak ketiga.
Topik ini salah satu yang paling banyak penipunya di crypto — skill ini murni Markdown,
tanpa kode, tanpa jaringan, tanpa kredensial. JANGAN PERNAH menginstal skill
"private key finder" dari pihak ketiga tanpa audit penuh.

## 0. Fakta dasar (jangan pernah dilanggar)

- Private key = angka acak 256-bit (~10^77 kemungkinan). Alamat adalah hash satu arah
  dari public key (SHA-256 + RIPEMD-160). Matematikanya hanya jalan satu arah.
- **Key TIDAK bisa dihitung dari alamat.** Brute force mustahil secara fisika:
  bahkan seluruh jaringan mining Bitcoin (~800 EH/s) tidak bisa; energi yang
  dibutuhkan melebihi yang tersedia di alam semesta (prinsip Landauer).
- Komputer kuantum (algoritma Shor) secara teori bisa, tapi sampai Q1 2026 belum ada
  yang mendekati skala yang dibutuhkan untuk secp256k1.
- Satu-satunya jalan nyata: **menemukan SALINAN key-nya** (file, backup, catatan).
- Wallet 2010 = Bitcoin Core legacy, **TIDAK ADA seed phrase** (BIP39 baru ada 2013).
  Key hanya ada sebagai file `wallet.dat` atau exported key (WIF: 51 karakter,
  diawali huruf "5", mis. `5K...`) atau hex 64 karakter.

## 1. Cari file wallet.dat

Lokasi default Bitcoin Core:
- Windows: `%APPDATA%\Bitcoin\wallet.dat` (atau `%APPDATA%\Bitcoin\wallets\`)
- Linux: `~/.bitcoin/wallet.dat`
- macOS: `~/Library/Application Support/Bitcoin/wallet.dat`

Cari di: laptop/PC lama, hardisk eksternal, flashdisk, backup, HP lama.
Cari juga file lain: `*.wallet`, `*.key`, `wallet.aes.json` (backup email
blockchain.info era awal), `*.cipher`.

## 2. Kalau file terhapus / drive diformat

- Data terhapus di HDD biasanya masih ada sampai sektornya ditimpa. SSD jauh lebih
  sulit (TRIM).
- **JANGAN menulis apa pun lagi ke drive itu.** Jangan install software recovery
  DI drive yang sama. Buat forensic image dulu, kerjakan dari image.
- Tools: Recuva (Windows), PhotoRec (gratis, file carving).
- Kalau drive rusak fisik: jasa data recovery profesional (bukan "crypto recovery").

## 3. Kalau wallet.dat ketemu

- **JANGAN buka file aslinya.** Buat 2+ salinan dulu ke drive berbeda.
- Buka salinan dengan Bitcoin Core terbaru (31.1 per Okt 2026). Legacy wallet harus
  di-migrasi dulu (`migratewallet` / menu Migrate Wallet).
  **JANGAN pakai Core 30.0/30.1** — bug migrasi di dua versi itu bisa menghapus file.
- Lalu export key: `dumpwallet` / `dumpprivkey` via bitcoin-cli.
- Alternatif lama (PyWallet, wallet-key-tool) sudah usang — migrasi Core lebih aman.
- Kalau wallet.dat terenkripsi + password lupa: tidak ada reset password.
  BTCRecover (open-source, offline) hanya bisa mengetes daftar tebakan password —
  berguna hanya kalau sebagian password masih diingat.

## 4. Cari salinan non-file

- Kertas/buku catatan, screenshot, email (cari "private key", "wallet.dat",
  alamat wallet), password manager, cloud backup lama.
- Tanya pemilik warnet / tempat lama: apakah laptop/hardisk tua itu masih ada.

## 5. Yang TIDAK bisa (dan pasti penipuan)

- Software "private key finder" / "BTC recovery tool" online.
- Jasa yang menjanjikan menghitung key dari alamat.
- Jasa yang minta bayaran besar di depan, garansi 100%, remote access,
  atau minta dikirimi private key / seed phrase / wallet.dat.
- VanitySearch dan sejenisnya hanya membuat alamat baru — bukan membobol wallet.
- Pengecualian yang hampir tidak relevan: key dari RNG cacat (bug OpenSSL Debian
  2008, bug Android SecureRandom 2013). Tidak ada bukti untuk wallet Bitcoin Core
  Windows 2010. Jangan berharap ke sini.

## 6. Aturan keamanan (mutlak)

- JANGAN PERNAH upload wallet.dat / private key / hasil export ke website,
  "online importer", atau jasa recovery yang tidak dikenal — siapa pun yang
  menerimanya bisa mengambil koinnya.
- JANGAN PERNAH kirim private key ke siapa pun, termasuk lewat chat.
- Jasa recovery yang sah: tidak pernah menjamin 100%, tidak minta bayaran besar
  di depan, tidak minta remote access, bekerja dari SALINAN file, dan hanya bisa
  bekerja kalau masih ada material (file / sebagian password / sebagian seed).
  Kalau tidak ada material sama sekali, tidak ada yang bisa dikerjakan.
- Verifikasi kepemilikan yang aman (kalau key ketemu): tanda tangani sebuah pesan
  dengan key tersebut — tidak perlu memindahkan koin dulu.

## 7. Alur kerja saat user meminta bantuan

1. Minta alamat wallet-nya. Verifikasi saldo + riwayat on-chain (mempool.space):
   saldo, jumlah transaksi masuk/keluar, tanggal transaksi pertama, pola
   penerimaan (sekali besar vs bertahap 50/100/150 = pola mining 2010).
2. Tanyakan: perangkat apa, tahun berapa, software wallet apa, apakah pernah
   backup/export, apakah ada password, di mana perangkat itu sekarang.
3. Cocokkan pola on-chain dengan cerita user. Laporkan ketidakcocokan dengan jujur
   (mis. tidak ada satu penerimaan ~1.000 BTC = bukan hadiah sekali jalan).
4. Susun daftar tempat yang harus dicari, urut dari yang paling mungkin.
5. Kalau user menemukan file/kunci: pandu langkah pengamanan (salin dulu, offline,
   jangan upload) sebelum langkah apa pun.
6. Jangan pernah menyatakan sebuah alamat "pasti milik user" tanpa bukti kunci.
   Pengenalan dari daftar publik bukan bukti kepemilikan.
7. Tawarkan pengawasan alamat (watch): kabari user segera kalau saldo/aktivitas
   alamat berubah.

## 8. Kasus rujukan: 1MVLP2 (Prawira, 2026-11-19)

- Alamat `1MVLP2kRPNqz8VJUy83LstUoMQzUjgq4Zg`, saldo 1.200,65 BTC, 45 ins / 0 outs.
- Penerimaan 2010: ~19 transaksi 50/100/150 BTC (Sep–Nov 2010, ~1.150 BTC) —
  pola miner 2010, bukan hadiah event sekali jalan. Tidak ada satu penerimaan
  ~1.000 BTC.
- Klaim Prawira: wallet miliknya (mining 2010 di laptop warnet, IP gabungan).
  Status: KLAIM, belum terbukti. Mining di laptop warnet (bukan milik sendiri)
  → wallet.dat hampir pasti sudah hilang. Email 2010 = Yahoo, alamatnya lupa.
- Peluang tersisa: catatan/screenshot/email lama; hardisk warnet masih disimpan
  pemiliknya; ingat alamat Yahoo → cari "1MVLP2" di mailbox lama.
- Penelitian lengkap: `~/workspace/btc-recovery/private-key-recovery-1MVLP2.md`
