import openai

class ChatGPT:
    #el metodo constructor requiere de la una key para poder hacer uso de la api de OpenAI
    def __init__(self, key):

        #se guarda la key
        openai.api_key = key

        #se crea una lista que contiene diccionarios dentro. Es asi porque asi lo pide la API
        #se indica que el sistema debe responder sin caracteres especiales, pero se le puede dar
        #cualquier indicacion
        self.contexto = [{"role": "system", "content": "las respuestas que daras no deben contener caracteres especiales como forward slash"}]

    #El metodo obtener_respuesta necesita del mensaje/pregunta por parte
    #del usuario, por eso está indicado como parametro
    #La funcion retorna un string
    def obtener_respuesta(self, mensaje) -> str:
        #se añade a la conversacion la pregunta/mensaje del usuario
        #se hace de esa manera porque asi lo pide la api
        self.contexto.append({"role":"user", "content":mensaje})

        #se hace llamada a la api con la clase Chat Completion, pero primero necesitamos indicar
        #el modelo que queremos usar, y la conversacion completa
        #cuando se realiza la peticion, la respuesta se guarda en response
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = self.contexto
        )

        #pero primero necesitamos extraer la respuesta que esta dentro del 
        #json que devolvio la api, asi que se extrae y se guarda en respuesta
        respuesta = response["choices"][0]["message"]["content"]

        #la respuesta se añade a la conversacion, pero indicando que fue respuesta de chatgpt, 
        #por eso tiene el rol de "asistente"
        self.contexto.append({"role":"assistant", "content":respuesta})

        #finalmente, se retorna unicamente la respuesta, el puro string xd
        return respuesta