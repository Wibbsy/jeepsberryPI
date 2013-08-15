
import bluetooth

bd_addr = "78:52:1A:4F:4E:6A"

port =2 

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("hello!!")

sock.close()
