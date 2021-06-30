import configparser

cf = configparser.ConfigParser()
cf.read('config.ini')
IP = cf.get('ip', 'chat_server_ip')
PORT = int(cf.get('port', 'chat_server_port'))
