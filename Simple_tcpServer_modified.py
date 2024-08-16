from socket import *
import random

def criptografar(mensagem, chave):
    mensagem_criptografada = ''
    for letra in mensagem:
        if letra.isalpha():
            if letra.islower():
                mensagem_criptografada += chr((ord(letra) - 97 + chave) % 26 + 97)
            else:
                mensagem_criptografada += chr((ord(letra) - 65 + chave) % 26 + 65)
        else:
            mensagem_criptografada += letra
    return mensagem_criptografada

def decriptografar(mensagem_criptografada, chave):
    mensagem_decriptografada = ''
    for letra in mensagem_criptografada.decode():
        if letra.isalpha():
            if letra.islower():
                mensagem_decriptografada += chr((ord(letra) - 97 - chave) % 26 + 97)
            else:
                mensagem_decriptografada += chr((ord(letra) - 65 - chave) % 26 + 65)
        else:
            mensagem_decriptografada += letra
    return mensagem_decriptografada

# Parâmetros públicos para o algoritmo de Diffie-Hellman
p = 23  # Número primo
g = 5   # Raiz primitiva de p

# Gera um número secreto privado para o servidor
a = random.randint(2, p - 2)

# Calcula o valor público do servidor
A = pow(g, a, p)

serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print("TCP Server\n")

connectionSocket, addr = serverSocket.accept()
print(f"Conexão estabelecida com: {addr}")

connectionSocket.send(str(A).encode())

# Recebe o valor público do cliente
B = int(connectionSocket.recv(1024).decode())

# Calcula a chave secreta compartilhada
s = pow(B, a, p)

while True:
    sentence = connectionSocket.recv(65000)
    if not sentence:
        break

    received = decriptografar(sentence, s)  # Decriptografa a mensagem recebida com a chave secreta
    print("Received From Client: ", received)

    capitalizedSentence = criptografar(received.upper(), s)  # Criptografa a mensagem em maiúsculas com a chave secreta

    connectionSocket.send(capitalizedSentence.encode())

    #sent = decriptografar(capitalizedSentence, s)  # Decriptografa a mensagem enviada para exibição
    print("Sent back to Client: ", capitalizedSentence)

connectionSocket.close()
serverSocket.close()