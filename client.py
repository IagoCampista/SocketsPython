import socket
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1243))

def send_message(s, message):
    msg = pickle.dumps(message)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', 'utf-8') + msg
    s.send(msg)

while True:
    print("\n\n")
    print("Escolha uma opção:")
    print("1: Diga 'Oi'")
    print("2: Diga o nome da máquina")
    print("3: Sair")
    
    escolha = input("\nDigite o número da opção desejada: ")
    
    if escolha == "1":
        send_message(s, "Oi")
    elif escolha == "2":
        send_message(s, "Nome da Máquina")
    elif escolha == "3":
        print("Saindo...")
        break
    else:
        print("\n\nOpção inválida. Tente novamente.")
        continue

    # Recebe a resposta do servidor
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg)-HEADERSIZE == msglen:
            print("Mensagem completa recebida do servidor:")
            print(pickle.loads(full_msg[HEADERSIZE:]))
            new_msg = True
            full_msg = b""
            break

s.close()
