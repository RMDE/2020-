import socket
from time import sleep
def client(ip='127.0.0.1',port=8888):
	conn = socket.socket()
	try:
		conn.connect((ip,port))
	except:
		print("connect fail")
		return
	print("connecting to "+str(ip)+":"+str(port)+" success!")
	while True:
		data = input(">>> ")
		conn.send(bytes(data,encoding='utf-8'))
		if data == "exit":
			return
		rtn = str(conn.recv(1024),encoding='utf-8')
		rtn = rtn.split("@")
		size = int(rtn[0])
		count = 0
		conn.send(bytes("start",encoding='utf-8'))
		if rtn[1] == 'file':
			print("file open")
			try:
				f = open(rtn[2],"w")
			except:
				print("file open fail")
				continue
		while count<size:
			data = str(conn.recv(1024),encoding='utf-8')
			count = count+len(data)
			if rtn[1] == "print":
				print(data)
			else:
				f.write(data)
		if rtn[1] == 'file':
			print("file close")
			f.close()

if __name__ == '__main__':
	client("127.0.0.1",8888)
