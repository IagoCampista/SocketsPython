import socket
import pickle
import platform

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1243))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Conexão de {address} estabelecida.")

    try:
        while True:
            full_msg = b''
            new_msg = True
            while True:
                msg = clientsocket.recv(16)
                if not msg:  # Verifica se o cliente desconectou
                    print("Cliente desconectado")
                    break

                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_msg += msg

                if len(full_msg) - HEADERSIZE == msglen:
                    received_command = pickle.loads(full_msg[HEADERSIZE:])
                    print(f"Comando recebido: {received_command}")

                    # Respostas baseadas no comando recebido
                    if received_command == "Oi":
                        response = "\nOlá, cliente!"
                    elif received_command == "Nome da Máquina":
                        response = f"\nNome da Máquina: {platform.node()}"
                    else:
                        response = "\nComando desconhecido"

                    # Envia a resposta de volta ao cliente
                    msg = pickle.dumps(response)
                    msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg
                    clientsocket.send(msg)

                    new_msg = True
                    full_msg = b""
            break
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
    
    clientsocket.close()
