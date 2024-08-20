from socket import *
import random


def criptografar(mensagem, chave):
    mensagem_criptografada = ''
    for letra in mensagem:
        mensagem_criptografada += chr((ord(letra) + chave))
    return mensagem_criptografada


def decriptografar(mensagem_criptografada, chave):
    mensagem_decriptografada = ''
    for letra in mensagem_criptografada:
            mensagem_decriptografada += chr((ord(letra) - chave))
    return mensagem_decriptografada


def primo_fast(N):
    i = 2
    while i < N:
        R = N % i
        if R == 0:
            return False
        i += 1
    else:
        return True


def diffie_hellman(g, b, p):
    if not primo_fast(p):
        raise 'p não é primo!'
    
    return (pow(g, b, p))


p = 23  # Número primo
g = 5   # Raiz


b = random.randint(2, p - 2) # Senha do server


B = diffie_hellman(g, b, p) # Que vai ser enviado


serverName = "10.1.70.33"
serverPort = 13000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


# Recebe o valor público do servidor
A = int(clientSocket.recv(1024).decode())


clientSocket.send(str(B).encode())


# Calcula a chave secreta compartilhada
s = diffie_hellman(A, b, p)


sentence = input("insira sentença: ")
sentence_criptografada = criptografar(sentence, s)  # Criptografar a mensagem
clientSocket.send(sentence_criptografada.encode())


modifiedSentence = clientSocket.recv(65000).decode()
print(modifiedSentence)
text = decriptografar(modifiedSentence, s)  # Decriptografa a mensagem recebidaa
print("Recebido: ", text)


clientSocket.close()