#ifndef CHATROOM_SERVER_H
#define CHATROOM_SERVER_H

#include <string>

#include "Common.h"

using namespace std;

// 服务端类，用来处理客户端请求
class Server {

public:
    // 无参数构造函数
    Server();

    // 初始化服务器端设置
    void Init();

    // 关闭服务
    void Close();

    // 启动服务端
    void Start();

private:
    // 广播消息给所有客户端
    int SendBroadcastMessage(int clientfd);

    // 服务器端serverAddr信息
    struct sockaddr_in serverAddr;
    
    //创建监听的socket
    int listener;

    // epoll_create创建后的返回值
    int epfd;
    
    // 客户端列表
    list<int> clients_list;
};



#endif //CHATROOM_SERVER_H
