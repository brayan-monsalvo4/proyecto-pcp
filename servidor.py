import socket
import threading
import openai
import sys

openai.api_key = "aqui va la clave"


def handle_client(cliente, direccion):
    print(f"New connection from {direccion}")
    contexto = [{"role":"system", "content":"las respuestas que daras no deben contener caracteres especiales como forward slash"}]

    while True:
        try:
            data = cliente.recv(1024).decode()

            if not data or data == "exit":
                cliente.close()
                print(f"Disconnected {direccion}")
                break
            
            contexto.append({"role":"user", "content":data})

            # Use la API de OpenAI para generar una respuesta
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = contexto,
                temperature = 0.4,
                n = 1,
                max_tokens = 2048
            )

            respuesta = response["choices"][0]["message"]["content"]
            # Envíe la respuesta al cliente
            cliente.send(respuesta.encode())

        except Exception as e:
            print(f"Error: {e}")
            break


def main(clientes):
    # Configurar el servidor
    host = "localhost"
    port = 5000


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()

    print(f"Listening on {host}:{port}")

    # Aceptar nuevas conexiones de socket y generar hilos de ejecución
    while True:
        try:
            tupla = s.accept()
            clientes.append(tupla[0])
            direccion = tupla[1]
            thread = threading.Thread(target=handle_client, args=(clientes[-1], direccion))
            thread.start()
        except KeyboardInterrupt:
            print("interrupcion de teclado xd")
            for socket_cliente in clientes:
                socket_cliente.close()
            sys.exit(0) 
            
            

if __name__ == "__main__":
    lista_clientes_activos = list()
    main(lista_clientes_activos)
