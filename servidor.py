from termcolor import cprint, colored
from chatgpt import ChatGPT
import sys
import threading
import socket

#definimos la direccion y puerto del servidor
host = "localhost"
port = 5000

#lista de sockets de clientes
lista_sockets_clientes = list()

#se abre el archivo key.txt y se lee la clave para usar la api de openai
with open("key.txt", "r") as f:
    api_key = f.readline()
    
    if len(api_key) == 0:
        print(colored("Error:", color="light_red", attrs=["bold"]), "no ha proporcionado ninguna clave.")
        sys.exit(0)

#funcion que realiza cada hilo al momento de conectarse un nuevo cliente
def atender_cliente(cliente, direccion):

    print(colored("Nueva conexion:", color="light_cyan", attrs=["bold"]), f"{direccion}")

    #se carga en ChatGPT la key para la api
    gpt = ChatGPT(api_key)

    while True:
        try:
            #se recibe el mensaje del ciente
            mensaje = cliente.recv(2000).decode()

            #si el mensaje es vacio o tiene la palabra exit, se lanza un socket timeout
            #se cierra el socket y se cierra el hilo
            if mensaje is None or mensaje == "exit":
                raise socket.timeout
            else:
                #sino, se manda el mensaje a ChatGPT, se guarda la respuesta, y se manda al cliente
                respuesta = gpt.obtener_respuesta(mensaje)
                cliente.send(respuesta.encode())

        except socket.timeout :
            #si llega a suceder un error, sale del bloque try-except, se cierra el socket cliente y 
            #se termina el hilo
            print(colored("Cerrando conexion:", color="red", attrs=["bold"]), f"{direccion}")
            break
    
    cliente.close()
        


def main():
    #creamos un socket servidor de protocolo ipv4 y de tipo TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))

    #el servidor tiene una cola de espera de 1, por lo que no pueden esperar los clientes
    #y se les asigna un hilo 
    servidor.listen(1)

    print(colored(f"Listening on {host}:{port}", color="light_magenta", attrs=["bold"]))
   

    while True:
        try:
            #se guarda el socket y direccion dentro de request
            request = servidor.accept()

            #el socket cliente se anade a la lista, y la direccion se guarda en una variable
            lista_sockets_clientes.append(request[0])
            direccion = request[1]

            #se crea un nuevo hilo, especificando que es daemon, para que terminen todos los hilos al finalizar
            #el programa
            hilo = threading.Thread(target=atender_cliente, args=[ lista_sockets_clientes[-1], direccion], daemon=True)

            hilo.start()

        except socket.error as e:
            #si llega a suceder un error, se cierran todos los sockets para no dejar ningun 
            #socket sin usar, cierra el socket servidor y termina el programa
            for cliente in lista_sockets_clientes:
                cliente.close()
            servidor.close()
            print(colored("error:", color="red", attrs=["bold"]), f"{e}")
            sys.exit(0)

        except KeyboardInterrupt as e:
            #si se llega a detectar una interrupcion de teclado, se cierran todos los sockets
            #clientes, se cierra el socket propio del servidor y termina el programa
            for cliente in lista_sockets_clientes:
                cliente.close()

            servidor.close()
            print(colored("\nclosing.", color="red", attrs=["bold"]), f"{e}")
            sys.exit(0)


if __name__ == "__main__":
    main()
