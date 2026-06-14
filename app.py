import streamlit as st
from google import genai
from google.genai import types

# 1. SETUP TAMPILAN WEB
st.title("🤖 Polyglot AI Tutor")
st.write("Halo! Aku tutor bahasa Inggris, Jepang, dan Jerman-mu. Yuk mulai latihan!")

# 2. INISIALISASI GEMINI CLIENT
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. KUNCI INSTRUKSI SISTEM (Dibuat lebih fleksibel agar pintar mendeteksi input pendek)
system_prompt = (
    "Kamu adalah Polyglot Tutor yang ramah, santai, dan suportif. Tugas utama kamu adalah membantu "
    "pengguna belajar Bahasa Inggris, Jepang, dan Jerman. Pengguna mungkin akan menginput teks pendek "
    "seperti nama bahasa saja (misal: 'jepang', 'inggris', 'belajar jerman'). Jika itu terjadi, langsung "
    "pahami bahwa mereka ingin belajar bahasa tersebut, lalu sapa mereka dengan ramah dan tawarkan materi dasar.\n"
    "Jika pengguna membuat kesalahan tata bahasa (grammar/structure) dalam ketiga bahasa tersebut, koreksi dengan sopan."
)

# 4. BUAT MEMORI CHAT (Jika belum ada)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat lama jika pengguna sedang mengobrol
for message in st.session_state.messages:
    display_role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(display_role):
        st.markdown(message["content"])

# 5. ALUR INTERAKSI (USER INPUT)
if user_input := st.chat_input("Ketik sesuatu (misal: 'jepang' atau 'belajar inggris')"):
    
    # Tampilkan pesan pengguna di layar
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Simpan ke memori dengan role 'user'
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 6. KIRIM KE AI DAN AMBIL RESPON
    with st.chat_message("assistant"):
        # Format riwayat chat agar dipahami API
        formatted_contents = [
            types.Content(role=m["role"], parts=[types.Part.from_text(text=m["content"])])
            for m in st.session_state.messages
        ]
        
        # Panggil Gemini dengan Instruksi Sistem
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=formatted_contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )
        
        # Tampilkan jawaban AI di layar
        st.markdown(response.text)
        
        # Simpan jawaban AI ke memori (SEKARANG SUDAH MASUK DI DALAM BLOK IF YANG BENAR)
        st.session_state.messages.append({"role": "model", "content": response.text})
