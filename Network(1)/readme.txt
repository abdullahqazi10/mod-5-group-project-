To connect:

start server.py on laptop
start Client.py in raspberry pi
start Client.py on other laptop
set one client to listen (2) and one to call (1)
caller should first enter name
caller should then add IP of server, port is always 33000
caller should then add ip of destination, port is always 33000


OR:

start server.py on both laptops
start client.py on both Pi's
set one client to listen, the other to call
caller enters name
caller should then add IP of HIS server, port is always 33000
caller should then add IP of OTHER server, port is always 33000
caller enters name again (i think)
caller should then add IP of destination pi, port is always 33000

at any point you can shut down using typing {quit} on client