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
    import re
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
            f"El contenido debe ser claro para niños pequeños."
        )

        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        cuento_texto = response.choices[0].message.content

        matches = re.findall(r"Página\s*\d+:(.*?)(?=Página\s*\d+:|$)", cuento_texto, re.DOTALL)

        paginas = [{"texto": m.strip()} for m in matches][:pagina]

        return jsonify({"paginas": paginas})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generar-imagen', methods=['POST'])
def generar_imagen():
    data = request.get_json()
    descripcion = data.get("descripcion") or data.get("texto") or data.get("tema")  # Usa texto por página o tema como fallback

    prompt_imagen = f"Ilustración para colorear estilo libro infantil, blanco y negro, dibujo lineal simple, sobre: {descripcion}"

    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt_imagen,
            n=1,
            size="512x512"  # Tamaño más liviano
        )
        image_url = response.data[0].url
        print("Imagen generada:", image_url)  # <--- AGREGA ESTO
        return jsonify({"url": image_url})
    except Exception as e:
        print("Error al generar imagen:", e)  # <--- Y ESTO
        return jsonify({"error": str(e)}), 500
