from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
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

    try:
        prompt = f"Escribe un cuento para colorear para un niño de {edad} años llamado {nombre}, sobre el tema: {tema}. Divide el cuento en 3 páginas con texto breve por página."
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        cuento_texto = response.choices[0].message.content
        paginas = [{"texto": parte.strip()} for parte in cuento_texto.split("\n\n") if parte.strip()]
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
