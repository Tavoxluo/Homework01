import configparser

cf = configparser.ConfigParser()
cf.read('requirement.ini')
CHAT_SERVER_IP = cf.get('ip', 'chat_server_ip')
FILE_SERVER_IP = cf.get('ip', 'file_server_ip')
PICTURE_SERVER_IP = cf.get('ip', 'picture_server_ip')
CLIENT_IP = cf.get('ip', 'client_ip')

CHAT_SERVER_PORT = int(cf.get('port', 'chat_server_port'))
FILE_SERVER_PORT = int(cf.get('port', 'file_server_port'))
PICTURE_SERVER_PORT = int(cf.get('port', 'picture_server_port'))
CLIENT_PORT = int(cf.get('port', 'client_port'))
