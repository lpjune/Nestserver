import paramiko

class DronePi():
    def __init__(self, ip):
        self.ssh = paramiko.SSHClient()
        self.ip = ip

    def connect(self):
        "Connect the device to the IP address"
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip, port=22, username="pi", password="raspberry")
        #print('connected to ip address:'+self.ip)


    def read_file(self, remotefilepath, localfilepath):
        ftp_client=self.ssh.open_sftp()
        ftp_client.get(remotefilepath,localfilepath)
        ftp_client.close()
            
    def write_file(self,localfilepath,remotefilepath):
        ftp_client=self.ssh.open_sftp()
        ftp_client.put(localfilepath,remotefilepath)
        ftp_client.close()

    def close(self):
        self.ssh.close()

def main():
    pi = DronePi('169.254.240.225')
    pi.connect()
    pi.read_file("/home/pi/MyCopter/logs/2019-03-05/flight2/flight.tlog","C:\\Python27\\UAV\\flight1.tlog")
    pi.close()

main()
