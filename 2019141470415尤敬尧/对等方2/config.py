
import configparser



class Config():
    __cf = configparser.ConfigParser() #便于读取.ini文件
    __ttl = 0
    def get_attr(self):
        """
        :return:ini文件中配置好的本地节点的属性
        """
        while True:
            try:
                peer = dict()
                peer['ip_addr'] = self.__cf.get("Peer-0", "ip_addr")
                peer['port_number'] = self.__cf.get("Peer-0", "port_number")
                peer['share_dir'] = self.__cf.get("Peer-0", "share_dir")
                peer['ttl'] = self.__cf.get("Peer-0", "ttl")
                peer_str = self.__cf.get("Netpeers", "peer_addr")

                peer_str = peer_str[1 : len(peer_str)-1]

                peer_list = peer_str.split(',')
                peer['peer_addr'] = peer_list
                peer_str = self.__cf.get("Netpeers", "peer_ports")
                peer_str = peer_str[1 : len(peer_str)-1]
                peer_list = peer_str.split(', ')
                if not peer_list:
                    for i in range(len(peer_list)):
                        peer_list[i] = int(peer_list[i])
                else:
                   # peer_list = [int(i) for i in peer_list]
                   peer['peer_ports'] = peer_list
                break
            except:
                pass
        return peer


    def __init__(self):
        self.__cf.read("config.ini")