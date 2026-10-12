import streamlit as st
from cryptography.fernet import Fernet
import os

# ==============================
# Key file name
# ==============================
KEY_FILE = "secret.key"


# ==============================
# Function to create secret key
# ==============================
def create_secret_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key


# ==============================
# Function to load key
# ==============================
def load_key():
    if not os.path.exists(KEY_FILE):
        return create_secret_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()


# ==============================
# Function to encrypt file
# ==============================
def encrypt_file(file_data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(file_data)
    return encrypted_data


# ==============================
# Function to decrypt file
# ==============================
def decrypt_file(file_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(file_data)
    return decrypted_data


# ==============================
# Streamlit UI
# ==============================

# page configuration and custom CSS for styling
st.set_page_config(page_title="File Encryption App", page_icon="🔐", layout="wide")

# custom CSS
st.markdown(
    """
    <style>
    /* import clean font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Poppins:wght@300;400;600&display=swap');

    /* overall app styling */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #111826, #0d1117);
        color: #e0e0e0;
        font-family: 'Roboto', sans-serif;
    }

    /* hide default chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* glassy container for main content */
    .block-container {
        backdrop-filter: blur(16px);
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        box-shadow: 0 12px 48px 0 rgba(0,0,0,0.4);
        padding: 3rem;
        max-width: 900px;
        margin: auto;
    }

    /* Title styling */
    .title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 0.5rem;
        color: #c5e1a5;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
    }
    .subtitle {
        font-family: 'Roboto', sans-serif;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 2rem;
        color: #a0c4ff;
    }

    /* professional button look */
    .stButton>button {
        background-color: rgba(100, 115, 255, 0.9);
        color: #fff;
        border: none;
        border-radius: 0.6rem;
        padding: 0.8rem 1.8rem;
        font-size: 1.05rem;
        font-weight: 500;
        letter-spacing: 0.03em;
        backdrop-filter: blur(4px);
        transition: transform 0.15s ease, background-color 0.15s ease;
    }
    .stButton>button:hover {
        background-color: rgba(100, 115, 255, 1);
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    /* input/select styling */
    .stFileUploader>div>div {
        padding: 1rem !important;
    }

    /* file uploader card */
    div[data-testid="stFileUploader"] {
        backdrop-filter: blur(12px);
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 14px;
        padding: 1.2rem;
    }

    /* subtle divider line */
    .divider {
        height: 1px;
        background: rgba(255,255,255,0.2);
        margin: 2rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# title and description with styled classes
st.markdown('<div class="title">🔐 File Encryption & Decryption</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Secure and stylish data protection built for professionals</div>', unsafe_allow_html=True)

# Load or create key
key = load_key()
st.info("Using key file: **secret.key** (auto-generated and stored locally)")

# Sidebar menu with glassy styling
st.sidebar.markdown("""
<style>
.sidebar .sidebar-content {
    backdrop-filter: blur(10px);
    background: rgba(30, 30, 40, 0.6);
    color: #e0e0e0;
    border-radius: 0 16px 16px 0;
}
.sidebar .sidebar-content h2 {
    color: #c5e1a5;
}
.sidebar .sidebar-content label {
    color: #a0c4ff;
}
</style>
""", unsafe_allow_html=True)
st.sidebar.title("✨ Menu ✨")
option = st.sidebar.radio(
    "Choose Operation",
    ("Encrypt File", "Decrypt File"),
    index=0,
    key="operation",
)

# central graphic/banner
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(
        "https://raw.githubusercontent.com/streamlit/streamlit/main/frontend/public/favicon.png",
        width=120,
        caption="Streamlit powered",
    )

# File uploader
uploaded_file = st.file_uploader("📄 Upload your file", type=None)

if uploaded_file is not None:
    file_details = f"**{uploaded_file.name}** ({uploaded_file.size} bytes)"
    st.markdown(f"<div style='text-align:center;color:#a0c4ff;margin-top:0.5rem;'>{file_details}</div>", unsafe_allow_html=True)

# ==============================
# Encryption
# ==============================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
if option == "Encrypt File":

    if uploaded_file is not None:
        file_data = uploaded_file.read()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns([1,1])
        with btn_col1:
            if st.button("🔒 Encrypt File"):
                encrypted_data = encrypt_file(file_data, key)
                st.success("✅ File Encrypted Successfully!")
                with btn_col2:
                    st.download_button(
                        label="📥 Download Encrypted",
                        data=encrypted_data,
                        file_name=uploaded_file.name + ".encrypted",
                        mime="application/octet-stream"
                    )
        st.caption("Encrypted files use Fernet symmetric encryption. Keep your secret.key safe!")


# ==============================
# Decryption
# ==============================
elif option == "Decrypt File":

    if uploaded_file is not None:
        file_data = uploaded_file.read()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns([1,1])
        with btn_col1:
            if st.button("🔓 Decrypt File"):
                try:
                    decrypted_data = decrypt_file(file_data, key)
                    st.success("✅ File Decrypted Successfully!")
                    original_name = uploaded_file.name.replace(".encrypted", "")
                    with btn_col2:
                        st.download_button(
                            label="📥 Download Decrypted",
                            data=decrypted_data,
                            file_name="decrypted_" + original_name,
                            mime="application/octet-stream"
                        )
                except Exception as e:
                    st.error("❌ Decryption Failed! Invalid file or key.")
        st.caption("Decrypted output restored to original bytes; verify integrity after download.")
