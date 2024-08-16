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

# Gera um número secreto privado para o cliente
b = random.randint(2, p - 2)

# Calcula o valor público do cliente
B = pow(g, b, p)

serverName = "10.1.70.33"
serverPort = 13000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Recebe o valor público do servidor
A = int(clientSocket.recv(1024).decode())


clientSocket.send(str(B).encode())

# Calcula a chave secreta compartilhada
s = pow(A, b, p)

sentence = input("Input lowercase sentence: ")
sentence_criptografada = criptografar(sentence, s)  # Criptografar a mensagem
clientSocket.send(sentence_criptografada.encode())

modifiedSentence = clientSocket.recv(65000)
text = decriptografar(modifiedSentence, s)  # Decriptografa a mensagem recebidaa
print("Received from Make Upper Case Server: ", text)

clientSocket.close()