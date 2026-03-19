import streamlit as st
import replicate
import os

# Configurazione della chiave API dai Secrets di Streamlit
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.set_page_config(page_title="AI Face Swap", layout="centered")
st.title("🎭 AI Face Swap")
st.write("Carica due foto per scambiare i volti in pochi secondi")

target_img = st.file_uploader("1. Carica la foto principale (Target)", type=["jpg", "png", "jpeg"])
source_img = st.file_uploader("2. Carica il volto da inserire (Source)", type=["jpg", "png", "jpeg"])

if target_img and source_img:
    if st.button("Avvia lo Swap"):
        with st.spinner("L'intelligenza artificiale sta lavorando..."):
            try:
                # Esecuzione del modello su Replicate
                output = replicate.run(
                    "lucataco/faceswap:9a429954840fd4c4b4f0f0d0dcf793d30ad273c5cf143d31988e040656d78200",
                    input={
                        "target_image": target_img,
                        "swap_image": source_img
                    }
                )
                if output:
                    st.image(output, caption="Ecco il tuo swap!", use_column_width=True)
                    st.balloons()
            except Exception as e:
                st.error(f"Si è verificato un errore: {e}")
                st.info("Assicurati di aver aggiunto il token nei Secrets di Streamlit")
