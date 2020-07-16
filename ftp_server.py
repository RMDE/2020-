import os
import socket
from time import sleep
from threading import Thread

ip = []
port = []
th = []
def response(conn,address):
	while True:
		data = str(conn.recv(1048),encoding='utf-8')
		data = data.split(" ")
		if data[0] == "get":
			f = open(data[1],"r")
			size = len(f.read())
			f.close()
			f = open(data[1],"r")
			conn.send(bytes(str(size)+"@",encoding='utf-8'))
			conn.send(bytes("file@2.txt",encoding='utf-8'))
			data = str(conn.recv(1048),encoding='utf-8')
			print("start to transfer....")
			while True:
				data = f.read(1024)
				if len(data) == 0:
					f.close()
					break
				conn.send(bytes(data,encoding='utf-8'))
		elif data[0] == "exit":
			conn.close()
			print("address:"+str(address)+"unconnect")
			return
		elif data[0] == "ls":
			path = os.getcwd()
			lists = [f for f in os.listdir(path)]
			count = 0
			for i in lists:
				count = count+len(i)
			conn.send(bytes(str(count),encoding='utf-8'))
			conn.send(bytes("@print@",encoding='utf-8'))
			data = str(conn.recv(1024),encoding='utf-8')
			print("start to transfer....") 
			for i in lists:
				conn.send(bytes(str(i)+"    ",encoding='utf-8'))
				
		else:
			response = "response:"+data[0]
			conn.send(bytes(str(len(response)),encoding='utf-8'))
			conn.send(bytes("@print@",encoding='utf-8'))
			data = str(conn.recv(1048),encoding='utf-8')
			print("start to transfer....") 
			conn.send(bytes(response,encoding='utf-8'))
		print("end of transfer")

if __name__ == '__main__':
	_ip = '127.0.0.1'
	_port = 8888
	server = socket.socket()
	server.bind((_ip,_port))
	server.listen(20)
	print("server waiting connect...")
	while True:
		conn,address = server.accept()
		ip.append(address[0])
		port.append(address[1])
		print("address:"+str(address)+" connected")
		t = Thread(target=response,args=(conn,address,))
		th.append(t)
		t.start()
	for t in th:
		t.join()
	
		
	

