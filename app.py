import streamlit as st
import fal_client
import os
import requests
from io import BytesIO

# Configurazione chiave API
if "FAL_KEY" in st.secrets:
    os.environ["FAL_KEY"] = st.secrets["FAL_KEY"]

st.set_page_config(page_title="Pro Face Swap", layout="centered")
st.title("🎭 Pro Face Swap (No-Filter Engine)")

target_file = st.file_uploader("1. Carica la foto principale", type=["jpg", "png", "jpeg"])
source_file = st.file_uploader("2. Carica il volto da inserire", type=["jpg", "png", "jpeg"])

if target_file and source_file:
    if st.button("Esegui lo Swap"):
        with st.spinner("L'intelligenza artificiale sta elaborando..."):
            try:
                # Caricamento file sui server di Fal
                target_url = fal_client.upload(target_file.getvalue(), "image/jpeg")
                source_url = fal_client.upload(source_file.getvalue(), "image/jpeg")
                
                # Esecuzione modello Face Swap
                result = fal_client.subscribe(
                    "fal-ai/face-swap",
                    arguments={
                        "base_image_url": target_url,
                        "swap_image_url": source_url
                    },
                )
                
                if "image" in result:
                    image_url = result["image"]["url"]
                    st.image(image_url, caption="Risultato Finale", use_container_width=True)
                    
                    # Tasto per scaricare l'immagine
                    response = requests.get(image_url)
                    btn = st.download_button(
                        label="Scarica Immagine",
                        data=BytesIO(response.content),
                        file_name="faceswap_result.jpg",
                        mime="image/jpeg"
                    )
                    st.balloons()
            except Exception as e:
                st.error(f"Errore: {e}")
