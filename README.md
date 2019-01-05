# Nestserver
Master computer server files for IMPRESS Nest

To use app-server and app-client:

1) Download app-server, app-client, libserver, libclient
2) Launch app-server from command line:
app-server.py <your public ip> <port>
ex: app-server.py 130.18.64.135 65432
3) Launch app-client from any computer on the same network from command line:
app-client.py <server ip> <port> search <action>
ex: app-client.py 130.18.64.135 65432 search backButton
