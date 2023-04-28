import openai

class ChatGPT:
    def __init__(self, key):
        openai.api_key = key
        self.contexto = [{"role": "system", "content": "las respuestas que daras no deben contener caracteres especiales como forward slash"}]

    def obtener_respuesta(self, mensaje) -> str:
        self.contexto.append({"role":"user", "content":mensaje})

        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = self.contexto
        )

        respuesta = response["choices"][0]["message"]["content"]

        self.contexto.append({"role":"assistant", "content":respuesta})

        return respuesta