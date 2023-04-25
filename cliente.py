import socket
import sys

# Configurar la conexión al servidor
host = "localhost"
port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

try:

    while True:

    # Enviar una pregunta al servidor
        question = input("cual es tu pregunta: \n")

        if question == "exit":
            s.close()
            sys.exit(0)

        s.send(question.encode())

        # Recibir la respuesta del servidor
        response = s.recv(131072).decode()
        print(f"Respuesta del servidor: {response}")

except KeyboardInterrupt:
    print("interrupcion de teclado")
    s.close()
    
# Cerrar la conexión


