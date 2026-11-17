import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="NEUROVERSE | Live Quiz Battle",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- THEME --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');
.stApp {
    background: radial-gradient(circle at 15% 10%, #20245a 0, #10152f 35%, #080b18 78%);
    color: #f5f7ff;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #151a3d, #0b1024);
    border-right: 1px solid #343b78;
}
h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; }
.hero {
    padding: 26px 28px; border-radius: 22px;
    background: linear-gradient(120deg, rgba(95,70,255,.28), rgba(0,214,255,.12));
    border: 1px solid rgba(123,145,255,.45);
    box-shadow: 0 0 35px rgba(62,91,255,.14);
    margin-bottom: 18px;
}
.hero-title { font-family: 'Orbitron', sans-serif; font-size: clamp(25px, 4vw, 42px); font-weight: 800; letter-spacing: 2px; }
.hero-sub { color: #b9c5ff; margin-top: 7px; }
.question-card {
    background: linear-gradient(145deg, rgba(35,44,94,.94), rgba(17,24,53,.96));
    border: 1px solid #5865bd; border-radius: 20px; padding: 25px;
    box-shadow: 0 10px 35px rgba(0,0,0,.22);
}
.q-number { color: #6ce8ff; font-family: 'Orbitron', sans-serif; font-size: 13px; letter-spacing: 2px; }
.q-text { font-size: clamp(19px, 2.4vw, 27px); font-weight: 750; line-height: 1.45; margin: 12px 0 18px; }
.option {
    background: rgba(255,255,255,.06); border: 1px solid rgba(164,177,255,.25);
    border-radius: 12px; padding: 12px 15px; margin: 8px 0; font-size: 16px;
}
.small-muted { color: #aab4df; font-size: 13px; }
div.stButton > button {
    border-radius: 12px; border: 1px solid #6978ed;
    background: linear-gradient(90deg, #6558f5, #287eea);
    color: white; font-weight: 700; min-height: 44px;
}
div.stButton > button:hover { border-color: #7ef0ff; color: white; box-shadow: 0 0 18px rgba(73,214,255,.25); }
div[data-testid="stMetric"] {
    background: rgba(37,47,101,.55); border: 1px solid #39488e;
    padding: 13px; border-radius: 15px;
}
hr { border-color: #303968; }
</style>
""", unsafe_allow_html=True)

QUESTIONS = [
    {
        "question": "Bank Indonesia menaikkan suku bunga kebijakan ketika inflasi sedang tinggi. Apa dampak yang paling mungkin terjadi?",
        "options": [
            "A. Kredit menjadi lebih murah sehingga konsumsi meningkat",
            "B. Kredit menjadi lebih mahal sehingga konsumsi dan investasi cenderung menurun",
            "C. Jumlah uang beredar langsung menjadi tidak terbatas",
            "D. Harga seluruh barang langsung turun menjadi nol",
        ],
        "answer": "B",
        "explanation": "Suku bunga yang lebih tinggi membuat biaya pinjaman meningkat. Konsumsi dan investasi cenderung melambat sehingga tekanan inflasi dapat berkurang."
    },
    {
        "question": "Seseorang menyimpan uang awal sebesar Rp2.000 juta di sistem perbankan. Jika rasio cadangan wajib 20%, berapakah maksimum jumlah uang giral/deposito yang dapat tercipta menurut pengganda sederhana?",
        "options": [
            "A. Rp2.000 juta",
            "B. Rp4.000 juta",
            "C. Rp8.000 juta",
            "D. Rp10.000 juta",
        ],
        "answer": "D",
        "explanation": "Pengganda uang = 1 / 0,20 = 5. Potensi maksimum = Rp2.000 juta × 5 = Rp10.000 juta."
    },
    {
        "question": "Menurut persamaan kuantitas uang MV = PQ, jika jumlah uang beredar (M) naik 20%, sedangkan V dan Q tetap, apa yang terjadi pada tingkat harga (P)?",
        "options": [
            "A. Turun 20%",
            "B. Naik 20%",
            "C. Tidak berubah",
            "D. Naik 40%",
        ],
        "answer": "B",
        "explanation": "Dengan kecepatan perputaran uang (V) dan output (Q) tetap, kenaikan M sebesar 20% diikuti kenaikan P sebesar 20%."
    },
    {
        "question": "Manakah pernyataan yang tepat mengenai jenis uang dan alat pembayaran?",
        "options": [
            "A. Hanya uang kertas yang termasuk uang",
            "B. Uang kartal, uang giral, dan uang kuasi memiliki karakteristik berbeda",
            "C. Semua tabungan dan deposito dapat digunakan langsung seperti uang tunai",
            "D. Uang elektronik selalu berarti jumlah uang baru tercipta di luar nilai yang disimpan",
        ],
        "answer": "B",
        "explanation": "Uang kartal berupa uang kertas dan logam; uang giral berupa simpanan yang dapat digunakan untuk pembayaran; uang kuasi mencakup simpanan tertentu yang tidak langsung dipakai seperti uang tunai."
    },
    {
        "question": "Mengapa bank disebut sebagai lembaga perantara keuangan (financial intermediary)?",
        "options": [
            "A. Karena bank hanya mencetak uang",
            "B. Karena bank menghimpun dana masyarakat dan menyalurkannya kembali dalam bentuk kredit",
            "C. Karena bank menentukan seluruh harga barang",
            "D. Karena bank menggantikan seluruh kegiatan pemerintah",
        ],
        "answer": "B",
        "explanation": "Bank menghimpun dana dari masyarakat, misalnya melalui tabungan dan deposito, kemudian menyalurkannya kepada pihak yang membutuhkan dana."
    },
    {
        "question": "Jika bunga tabungan 5% per tahun sementara inflasi 7% per tahun, bagaimana kecenderungan daya beli uang tabungan tersebut?",
        "options": [
            "A. Daya beli meningkat sekitar 2%",
            "B. Daya beli tetap",
            "C. Daya beli menurun karena bunga riil sekitar -2%",
            "D. Daya beli meningkat sekitar 12%",
        ],
        "answer": "C",
        "explanation": "Perkiraan bunga riil = bunga nominal − inflasi = 5% − 7% = -2%. Artinya, daya beli tabungan cenderung turun."
    },
    {
        "question": "Apa kelemahan utama sistem barter yang mendorong munculnya uang sebagai alat tukar?",
        "options": [
            "A. Tidak membutuhkan barang untuk ditukar",
            "B. Harus ada kebetulan keinginan ganda antara kedua pihak",
            "C. Semua barang memiliki nilai yang sama",
            "D. Tidak dapat digunakan dalam perdagangan",
        ],
        "answer": "B",
        "explanation": "Dalam barter, kedua pihak harus saling menginginkan barang yang ditawarkan pihak lain pada waktu yang sama. Uang mengatasi kesulitan tersebut."
    },
    {
        "question": "Berikut ini yang termasuk empat fungsi dasar uang adalah ...",
        "options": [
            "A. Alat tukar, satuan hitung, penyimpan nilai, dan pembayaran tunda",
            "B. Alat produksi, alat distribusi, alat konsumsi, dan investasi",
            "C. Alat pinjaman, alat tabungan, alat produksi, dan pajak",
            "D. Alat perdagangan, alat investasi, alat ekspor, dan impor",
        ],
        "answer": "A",
        "explanation": "Fungsi dasar uang meliputi alat tukar, satuan hitung, penyimpan nilai, dan standar pembayaran yang ditangguhkan."
    },
    {
        "question": "Berdasarkan materi, rumus yang tepat untuk menghitung M2 adalah ...",
        "options": [
            "A. M2 = Kartal + Giral",
            "B. M2 = M1 − Uang Kuasi",
            "C. M2 = M1 + Uang Kuasi",
            "D. M2 = Kartal + Deposito saja",
        ],
        "answer": "C",
        "explanation": "Secara umum, M2 merupakan M1 ditambah uang kuasi."
    },
    {
        "question": "Manakah yang merupakan salah satu tugas Bank Indonesia sebagai bank sentral?",
        "options": [
            "A. Memberikan pinjaman langsung kepada seluruh masyarakat",
            "B. Menjaga stabilitas nilai rupiah",
            "C. Menjamin seluruh simpanan masyarakat secara langsung",
            "D. Mengelola seluruh kegiatan perdagangan nasional",
        ],
        "answer": "B",
        "explanation": "Salah satu tujuan Bank Indonesia adalah mencapai dan memelihara kestabilan nilai rupiah."
    },
]

def init_state():
    defaults = {
        "q_index": 0,
        "scores": {},
        "attempts": [],
        "selected_player": None,
        "show_answer": False,
        "finished": False,
        "question_started": False,
        "used_players": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

def sorted_scores():
    return sorted(st.session_state.scores.items(), key=lambda x: (-x[1], x[0].lower()))

def add_player(name):
    name = name.strip()
    if not name:
        return False, "Masukkan nama peserta terlebih dahulu."
    if name.lower() in [n.lower() for n in st.session_state.scores]:
        return False, "Nama peserta sudah terdaftar."
    st.session_state.scores[name] = 0
    return True, f"Peserta {name} berhasil ditambahkan."

def reset_quiz():
    for key in ["q_index", "scores", "attempts", "selected_player", "show_answer", "finished", "question_started", "used_players"]:
        if key in st.session_state:
            del st.session_state[key]
    init_state()

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("## ⚡ NEUROVERSE")
    st.caption("LIVE QUIZ BATTLE • HOST PANEL")
    st.markdown("---")
    st.markdown("### 👥 Daftarkan peserta")
    with st.form("add_player_form", clear_on_submit=True):
        new_name = st.text_input("Nama peserta", placeholder="Contoh: Andi")
        add_clicked = st.form_submit_button("＋ Tambah peserta", use_container_width=True)
    if add_clicked:
        ok, msg = add_player(new_name)
        (st.success if ok else st.warning)(msg)

    st.markdown("---")
    st.markdown(f"**Peserta terdaftar: {len(st.session_state.scores)}**")
    if st.session_state.scores:
        for i, (name, score) in enumerate(sorted_scores(), 1):
            st.write(f"{i}. {name} — **{score} poin**")
    else:
        st.caption("Belum ada peserta. Tambahkan nama saat peserta mulai mendapat giliran.")

    st.markdown("---")
    if st.button("↻ Reset seluruh permainan", use_container_width=True):
        reset_quiz()
        st.rerun()

# -------------------- MAIN --------------------
st.markdown("""
<div class="hero">
  <div class="hero-title">⚡ NEUROVERSE</div>
  <div class="hero-sub">THE LIVE QUIZ BATTLE • ANGKAT TANGAN TERCEPAT • TOP 3 WINNERS</div>
</div>
""", unsafe_allow_html=True)

total = len(QUESTIONS)
current = st.session_state.q_index

m1, m2, m3 = st.columns(3)
m1.metric("SOAL", f"{min(current + 1, total)} / {total}" if not st.session_state.finished else f"{total} / {total}")
m2.metric("PESERTA", len(st.session_state.scores))
m3.metric("JUMLAH JAWABAN", len(st.session_state.attempts))

if st.session_state.finished:
    st.markdown("## 🏆 Permainan selesai!")
    st.markdown("### Tiga peserta dengan skor tertinggi")
    ranking = sorted_scores()[:3]
    if not ranking:
        st.info("Belum ada peserta yang mendapatkan poin.")
    else:
        medals = ["🥇", "🥈", "🥉"]
        cols = st.columns(3)
        for i, col in enumerate(cols):
            if i < len(ranking):
                name, score = ranking[i]
                with col:
                    st.markdown(f"""
                    <div class="question-card" style="text-align:center; min-height:150px;">
                      <div style="font-size:38px">{medals[i]}</div>
                      <div style="font-size:19px;font-weight:800">{name}</div>
                      <div style="font-size:25px;color:#6ce8ff;font-family:Orbitron">{score} poin</div>
                    </div>
                    """, unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Papan peringkat lengkap")
    if ranking:
        st.dataframe(
            [{"Peringkat": i, "Nama": n, "Poin": s} for i, (n, s) in enumerate(sorted_scores(), 1)],
            use_container_width=True, hide_index=True
        )
    if st.button("Mulai permainan baru", type="primary"):
        reset_quiz()
        st.rerun()
else:
    q = QUESTIONS[current]
    st.progress((current + 1) / total)
    st.markdown(f"""
    <div class="question-card">
      <div class="q-number">CHALLENGE {current + 1:02d} / {total:02d}</div>
      <div class="q-text">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### PILIHAN JAWABAN")
    for option in q["options"]:
        st.markdown(f'<div class="option">{option}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🎤 Kendali host")
    st.caption("Bacakan soal. Peserta tercepat mengangkat tangan maju ke depan. Pilih atau daftarkan namanya, lalu nilai jawaban lisan peserta.")

    names = list(st.session_state.scores.keys())
    if names:
        selected = st.selectbox(
            "Peserta yang mendapat kesempatan menjawab",
            options=names,
            index=names.index(st.session_state.selected_player) if st.session_state.selected_player in names else 0,
            key=f"player_select_{current}"
        )
        st.session_state.selected_player = selected
    else:
        st.info("Tambahkan nama peserta melalui panel di sebelah kiri setelah ada peserta yang mengangkat tangan.")
        selected = None

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("👁️ Tampilkan kunci jawaban", use_container_width=True):
            st.session_state.show_answer = not st.session_state.show_answer
    with c2:
        if st.button("➡️ Soal berikutnya", use_container_width=True):
            if current < total - 1:
                st.session_state.q_index += 1
                st.session_state.show_answer = False
                st.session_state.selected_player = None
                st.rerun()
            else:
                st.session_state.finished = True
                st.rerun()
    with c3:
        if st.button("🏁 Akhiri kuis", use_container_width=True):
            st.session_state.finished = True
            st.rerun()

    if st.session_state.show_answer:
        st.success(f"Kunci jawaban: **{q['answer']}**")
        st.info(q["explanation"])

    st.markdown("#### Beri nilai jawaban lisan")
    st.caption("Pilih peserta yang maju. Tekan Benar atau Salah setelah peserta menjawab.")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("✅ BENAR (+10 poin)", type="primary", use_container_width=True, disabled=(selected is None)):
            st.session_state.scores[selected] += 10
            st.session_state.attempts.append({
                "soal": current + 1, "peserta": selected, "hasil": "Benar", "poin": 10
            })
            st.success(f"{selected} mendapatkan 10 poin!")
            st.session_state.selected_player = None
            st.rerun()
    with b2:
        if st.button("❌ SALAH (0 poin)", use_container_width=True, disabled=(selected is None)):
            st.session_state.attempts.append({
                "soal": current + 1, "peserta": selected, "hasil": "Salah", "poin": 0
            })
            st.warning(f"Jawaban {selected} dicatat salah. Berikan kesempatan kepada peserta lain jika diperlukan.")
            st.session_state.selected_player = None
            st.rerun()

    st.markdown("---")
    st.subheader("🏆 Papan peringkat sementara")
    if st.session_state.scores:
        rows = [
            {"Peringkat": i, "Peserta": name, "Poin": score}
            for i, (name, score) in enumerate(sorted_scores(), 1)
        ]
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.caption("Peringkat akan muncul setelah peserta didaftarkan.")

if st.session_state.attempts:
    with st.expander("📋 Riwayat jawaban"):
        st.dataframe(st.session_state.attempts, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown('<div class="small-muted">NEUROVERSE • Host mengoperasikan aplikasi. Peserta menjawab secara langsung di depan kelas, tanpa perlu membuka aplikasi di HP.</div>', unsafe_allow_html=True)