# N22 — hasil konfirmatori (16 Nov 2026, job Slurm di node l40s, 1 GPU)

Prareg v1.0 (SHA-256 49e6e58b…c3a8), skrip n22_eval.py abc88aa7…f9db, n22_analyze.py 038cf534…ea5c (cocok dengan yang didaftarkan). Output lengkap di klaster: /virtiofs/work/bambang/n22/analysis_N22.txt, results/*.json.

## CyberMetric-2000 (utama, n=2000)
| | Qwen2.5-7B-Instruct | Phi-3.5-mini-instruct |
|---|---|---|
| Akurasi R0–R3 | .884 / .888 / .888 / .882 | .854 / .846 / .837 / .842 |
| Rentang rotasi | 0,6 pp | 1,8 pp |
| H1 sensitivitas urutan (≥3 pp & Cochran Q) | Tidak didukung (p Holm = 1) | Tidak didukung (p Holm = 0,073) |
| H2 akurasi(R0) − benar di 4 rotasi (≥10 pp, batas bawah) | 6,4 pp (lo95 5,3) Tidak | 10,8 pp (lo95 9,3) Sebagian |
| H3 tanpa pertanyaan, batas bawah > 0,30 | .409 (lo95 .389) DIDUKUNG | .420 (lo95 .399) DIDUKUNG |
| H4 urutan kanonik (≥0,55 & p Holm < 0,05) | .491 (p Holm = 1) Tidak | .525 (lo95 .503; p Holm = 0,027) Tidak: titik estimasi < 0,55 |

## SecQA (deskriptif, daya rendah)
| | Qwen v1 (110) | Qwen v2 (100) | Phi v1 (110) | Phi v2 (100) |
|---|---|---|---|---|
| Akurasi R0–R3 | .991/.991/.991/1.0 | .98/.97/.98/.98 | .982/.991/.991/.982 | .98/.98/.96/.99 |
| Q0 (tanpa pertanyaan) | .618 | .760 | .700 | .750 |
| Canon | .491 | — | .536 | .530 |

## Ringkas
- H3 didukung di semua set dan model: pilihan jawaban saja (tanpa pertanyaan) menghasilkan akurasi 41–42% pada CyberMetric-2000 (acak 25%) dan 62–76% pada SecQA.
- H1 tidak didukung: skor kedua model tahan terhadap rotasi opsi.
- H2 hanya sebagian untuk Phi (10,8 pp, batas bawah 9,3); tidak untuk Qwen.
- H4 tidak didukung menurut aturan terdaftar; Phi menunjukkan sinyal kecil (.525, p Holm = 0,027) di bawah ambang .55.
- Batasan: dua model kecil, skoring log-prob huruf, uji tanpa pertanyaan memakai satu prompt, SecQA hanya ~100 soal per split.
