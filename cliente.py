import socket
import sys

#nos permite mostrar colores en la terminal
from termcolor import colored, cprint

#guardamos direccion y puerto del servidor
host = "localhost"
port = 5000

def main():
    #creamos un socket con el protocolo ipv4 y que sea de tipo TCP
    usuario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #establecemos un timeout de 10 segundos, si no responde el servidor el programa se cerrara automaticamente.
    usuario.settimeout(20)

    cprint("Uso: introduce cualquier cosa que quieras preguntar. Para salir escribe exit o presiona Ctrl + C", color="light_magenta", attrs=["bold"])

    try:
        #se conecta al servidor
        usuario.connect((host, port))

        while True:
            #mensaje introducido por el usuario
            mensaje = input(colored("Usuario: ", color="cyan", attrs=["bold"]))

            #si el mensaje es un exit, se lanza una interrupcion de teclado y termina el programa
            if mensaje == "exit":
                raise KeyboardInterrupt

            #manda el mensaje del usuario
            usuario.send(mensaje.encode())

            #guarda la respuesta y la imprime en la terminal
            respuesta = usuario.recv(150000).decode()
            print(colored("ChatGPT:", color="light_green", attrs=["bold"]), f"{respuesta}", "\n")

    #exception en caso de que el servidor no se encuentre activo
    except ConnectionRefusedError:
        print(colored("El servidor no se encuentra activo.", color="light_red", attrs=["bold"]))
        usuario.close()
        sys.exit(0)

    #exception en caso de que el timeout se agote (10 segundos)
    except socket.timeout:
        print(colored("Se ha agotado el tiempo de espera.", color="light_red", attrs=["bold"]))
        usuario.close()
        sys.exit(0)

    #except para un error de socket generico
    except socket.error:
        print(colored("Ha surgido un error.", color="light_red", attrs=["bold"]))
        usuario.close()
        sys.exit(0)

    #exception especial para finalizar el programa con "exit" o Ctrl + C
    #al cerrar el programa de esta manera, se envia el mensaje "exit" al servidor, asegurando una
    #desconexion segura 
    except KeyboardInterrupt:
        print(colored("\nHasta luego!", color="light_blue", attrs=["bold"]))

        mensaje = "exit"
        usuario.send(mensaje.encode())

        usuario.close()
        sys.exit(0)

if __name__ == "__main__":
    main()