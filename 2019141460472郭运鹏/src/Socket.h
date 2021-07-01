#pragma once
#include "winsock2.h"  
#include <iostream>  
#pragma comment(lib, "ws2_32.lib")
#include<memory>

class Socket
{
public:
	Socket();
	Socket(const char* ip, const int port);
	bool initialize(const char* ip, const int port);
	bool sendSocketMessage(const char* mesg);
	bool reviceSocketMessage();
	void CloseSocket();
	char* getReviceMessage();
private:

	WSADATA wsd; //WSADATA变量  
	SOCKET sHost; //客户端套接字  
	SOCKADDR_IN addr; //服务器地址     sockaddr将目的地址和端口混合，sockaddr_in不会    

	char bufRecv[512];//接收数据缓冲区  
	int retVal; //返回值  
};

