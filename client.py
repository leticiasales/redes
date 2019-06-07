# Streaming Client
import socket
import datetime
import sys

HOST = 'localhost'
PORT = 50009

s = socket.socket()
s.connect((HOST, PORT))

print('Sending refresh time : ', str(sys.argv[1]))
s.send(sys.argv[1])

expected_value = 1
out_of_order = 0
highest_pckg = 0
missing_pckg = []
ooo_pckg = 0
auxbuf = ''
try:
	while True:
		#Recebendo o pacote
		data = s.recv(32)
		if data != '':
			print(repr(data))
			#Cuidando de possiveis perda de pacotes
			bufdata = data.split(';')
			bufdata[0] = auxbuf+bufdata[0]
			if (bufdata[1]):
				auxbuf = bufdata[1]

				#Separando o numero do pacote
				number = filter(str.isdigit, bufdata[0])
				number = int(number)
				number = number//100
				
				#Failsafe contra packet loss que possa quebrar o cliente
				if number < 1.2*expected_value:

					#Tratadores para verificar packet loss
					if number > highest_pckg:
						highest_pckg = number

					if int(expected_value) == number:
						expected_value = number+1
					else:
						out_of_order+=1
						ooo_pckg = number
					
						if expected_value < number:
							for i in range(expected_value, number):
								missing_pckg.append(i)
						else:
							if expected_value > number:
								missing_pckg.remove(number)

						expected_value = int(highest_pckg)+1

		else:
			#Informacoes ao ter uma conexao perdida
			pckg_loss = float(len(missing_pckg))*100/float(highest_pckg)
			pckg_ooo = float(out_of_order)*100/float(highest_pckg)

			print('Connection with the server has been lost')
			print('Last package lost', ooo_pckg)
			print('Packages lost %.2f'%pckg_loss,'%')
			print('Packages not in order %.2f'%pckg_ooo,'%')
			break

except KeyboardInterrupt:
	#Informacoes ao fechar a conexao
	pckg_loss = float(len(missing_pckg))*100/float(highest_pckg)
	pckg_ooo = float(out_of_order)*100/float(highest_pckg)
	
	print('Connection closed')
	print('Last package lost', ooo_pckg)
	print('Packages lost %.2f'%pckg_loss,'%')
	print('Packages not in order %.2f'%pckg_ooo,'%')

s.close()