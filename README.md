# Papan Sekolah

A TV noticeboard for the family: each kid's class WhatsApp group, the teachers' key messages and the parents' to-dos.
Open it on the TV browser at https://rashidxniz-arch.github.io/papan-sekolah/ and enter the PIN once.

- `index.html` – the board. It loads `data/board.enc.json` and decrypts it in the browser with the PIN (AES-256-GCM, key from PBKDF2-SHA256).
- `data/board.enc.json` – the encrypted board data, refreshed nightly. The page re-checks it every 30 minutes.
- `tools/extract.js` – pulls the class data out of the Papan Sekolah board HTML into JSON.
- `tools/encrypt.py` – encrypts that JSON with the PIN into `data/board.enc.json`.

Never commit plain JSON or the PIN.
