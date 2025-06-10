from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Cliente de OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/generar-cuento', methods=['POST'])
def generar_cuento():
    data = request.get_json()
    nombre = data.get("nombre")
    edad = data.get("edad")
    tema = data.get("tema")

    try:
        prompt = (
            f"Escribe un cuento para colorear dividido en 3 páginas. "
            f"Está dirigido a un niño de {edad} años llamado {nombre}, "
            f"y el tema es: {tema}. Haz que cada página tenga texto breve y adecuado para colorear."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7
        )

        cuento_texto = response.choices[0].message.content

        # Dividir en páginas
        paginas = [{"texto": parte.strip()} for parte in cuento_texto.split("\n\n") if parte.strip()]

        return jsonify({"paginas": paginas})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
