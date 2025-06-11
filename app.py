from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import re
import os

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde otros orígenes

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/generar-cuento', methods=['POST'])
def generar_cuento():
    data = request.get_json()
    nombre = data.get("nombre")
    edad = data.get("edad")
    tema = data.get("tema")
    pagina = data.get("pagina", 2)

    try:
        prompt = (
            f"Escribe un cuento para colorear para un niño de {edad} años llamado {nombre}, "
            f"sobre el tema: {tema}. Divide el cuento en {pagina} páginas. "
            f"Cada página debe tener un encabezado 'Página X:' seguido de 2 a 3 frases breves y simples. "
            "El contenido debe ser claro para niños pequeños."
        )

        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        cuento_texto = response.choices[0].message.content

        # Extraer texto de cada página
        matches = re.findall(r"Página\s*\d+:(.*?)(?=Página\s*\d+:|$)", cuento_texto, re.DOTALL)
        paginas = []

        for i, texto in enumerate(matches[:pagina]):
            texto = texto.strip()
            prompt_img = f"Dibujo para colorear, estilo libro infantil, en blanco y negro, sobre: {texto}. Sin color. Dibujo lineal simple."
            try:
                img_response = openai.images.generate(
                    model="dall-e-3",
                    prompt=prompt_img,
                    n=1,
                    size="512x512"
                )
                img_url = img_response.data[0].url
            except Exception as e:
                img_url = None  # en caso de fallo

            paginas.append({"texto": texto, "imagen": img_url})

        return jsonify({"paginas": paginas})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generar-imagen', methods=['POST'])
def generar_imagen():
    data = request.get_json()
    tema = data.get("tema")

    prompt_imagen = f"ilustración en blanco y negro estilo libro para colorear para niños, sobre {tema}, sin color, dibujo lineal simple"

    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt_imagen,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        return jsonify({"url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
