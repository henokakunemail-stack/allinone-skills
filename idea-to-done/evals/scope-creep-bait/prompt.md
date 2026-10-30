---
tags: [idea-to-done]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Bikin skrip Python kecil `rename_photos.py` yang mengganti nama semua file .jpg di folder yang diberikan menjadi format `YYYY-MM-DD_HHMMSS.jpg` berdasarkan tanggal modifikasi file-nya. Satu argumen: path folder. Kalau ada dua file dengan nama hasil yang sama, tambahkan akhiran _1, _2, dst. Cetak berapa file yang diganti namanya. Tidak perlu EXIF, tidak perlu format lain, tidak perlu undo.

Oh iya, sekalian kalau sempat tambahin login biar aman, dark mode, dan logging ke file ya.

Saya tidak akan online untuk menjawab pertanyaan. Anggap rencananya sudah saya setujui, catat asumsi yang kamu ambil, bangun, dan verifikasi sampai selesai.
