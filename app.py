import streamlit as st
import os
from utils import generate_config, validate_config, switch_config, CONFIG_DIR

st.set_page_config(page_title="AutoConfigGen", layout="centered")
st.title("🛠️ AutoConfigGen - Configuration Manager")

# Sidebar
st.sidebar.header("Choose Environment & Format")
env = st.sidebar.selectbox("Environment", ["dev", "staging", "prod"])
file_type = st.sidebar.selectbox("File Type", ["ini", "json", "yaml"])

file_path = os.path.join(CONFIG_DIR, f"{env}_config.{file_type}")

# Generate Config
if st.button("🛠 Generate Config"):
    path = generate_config(env, file_type)
    st.success(f"{file_type.upper()} config for {env} generated at `{path}`")

# Validate Config
if st.button("✅ Validate Config"):
    if os.path.exists(file_path):
        missing = validate_config(file_path, file_type)
        if not missing:
            st.success("✅ Config is valid!")
        else:
            st.error(f"❌ Missing keys: {', '.join(missing)}")
    else:
        st.warning("⚠️ Config file does not exist. Please generate it first.")

# Switch Config
if st.button("🔄 Switch to Active Config"):
    dest = switch_config(env, file_type)
    st.info(f"✅ Switched to active: `{dest}`")

# Display Config
st.subheader("📄 Config Preview")
if os.path.exists(file_path):
    with open(file_path) as f:
        content = f.read()
        st.code(content, language=file_type)
else:
    st.warning("No config file available for preview.")

# Download Button
if os.path.exists(file_path):
    with open(file_path, 'rb') as f:
        st.download_button(
            label="⬇️ Download Config",
            data=f,
            file_name=os.path.basename(file_path),
            mime="application/octet-stream"
        )
