import streamlit as st
import replicate
import requests
from PIL import Image
from io import BytesIO

st.title("AI Face Swap App")
source_img = st.file_uploader("Carica la foto della persona (Target)", type=["jpg", "png"])
face_img = st.file_uploader("Carica la faccia da inserire (Source)", type=["jpg", "png"])

if source_img and face_img:
    if st.button("Esegui Swap"):
        with st.spinner("Elaborazione in corso..."):
            # Esempio utilizzando un modello su Replicate (necessita REPLICATE_API_TOKEN)
            output = replicate.run(
                "lucataco/faceswap:9a429954840fd4c4b4f0f0d0dcf793d30ad273c5cf143d31988e040656d78200",
                input={"target_image": source_img, "swap_image": face_img}
            )
            response = requests.get(output)
            st.image(Image.open(BytesIO(response.content)), caption="Risultato Finale")
