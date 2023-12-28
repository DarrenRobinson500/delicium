import socket
print(socket.gethostname())
if socket.gethostname() == "Mum_and_Dads":
    print("Success")
else:
    print("Not so successful")