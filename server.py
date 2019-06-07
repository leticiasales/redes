# Streaming Server
import socket
import os
import time
import datetime
import sys
from random import randint

HOST = 'localhost'
PORT = 50009

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print('Waiting for connections')
for i in range(3):
	#Inicializando processos para possiveis conexoes
	process_id = os.fork()

	if process_id == 0:
		childid = os.getpid()
		#print('Child is now waiting for connection')
		try:
			while True:
				#Estabelecendo a conexao
				conn, addr = s.accept()
				print('Client connection accepted with', addr)
				print('Waiting for refresh time with the client: ', i+1)
				st = conn.recv(32)
				sleeptime = float(st)
				print('Connection estabilished with a refresh time of', sleeptime ,'seconds')
				n=1
				while True:
					try:
						#Dado a ser enviado
						value = randint(0, 9)
						value = 'N: ' + str(n) + ' Message: ' + str(value) + ' Id: '+ str(i+1) + '; '
						data = str(value) 
						print ('Server sent:', data)
						#Enviando o dado
						conn.send(data)
						n+=1    
						time.sleep(sleeptime)
					except(socket.error, "error"):
						print('Client connection closed, ID', i+1,'IP', addr)
						break	
		except KeyboardInterrupt:
			sys.exit()
try:
	os.waitpid(-1, 0)
#Fechar o servidor
except KeyboardInterrupt:
	print ('Closing the server')
	sys.exit()