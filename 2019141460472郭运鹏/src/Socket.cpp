#include"Socket.h"

#include<string>
#include<iostream>

using namespace std;

Socket::Socket() {
	initialize("127.0.0.1", 4999);
};
Socket::Socket(const char* ip, const int port) {
	initialize(ip, port);
};
void Socket::CloseSocket() {
	closesocket(sHost);
	WSACleanup();
}
bool Socket::initialize(const char* ip, const int port) {
	WSADATA wsd;//初始化网络环境
	if (WSAStartup(MAKEWORD(2, 2), &wsd) != 0)//加载套接字库  使用2.2版本的Socket，响应的库绑定
	{
		cout << "WSAStartup failed!" << endl;//加载失败的提示
		return -1;
	}

	//创建套接字  
	sHost = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);//socket(int af, int type,int protocol) AF_INET表示IPV4地址，AP_INET6表示IPV6   SOCK_STREAM（流格式/面向连接，TCP)
	if (INVALID_SOCKET == sHost)//如果创建失败的返回
	{
		cout << "socket failed!" << endl;
		WSACleanup();//释放套接字资源，解除与Socket库的绑定  
		return  -1;
	}


	addr.sin_family = AF_INET;
	//如果编译通不过 属性 c++ 常规  sdl 改成否
	addr.sin_addr.s_addr = inet_addr(ip);//设置服务端地址，将一个IP字符串转化为一个网络字节序的整数值
	addr.sin_port = htons((short)port);//htons将端口号由主机字节序转换为网络字节序的整数值
	int nServAddlen = sizeof(addr);


	//连接服务器  
	retVal = connect(sHost, (LPSOCKADDR)&addr, sizeof(addr));
	if (SOCKET_ERROR == retVal)
	{
		cout << "connect failed!" << endl;
		closesocket(sHost); //关闭套接字  
		WSACleanup(); //释放套接字资源  
		return -1;
	}
}


bool Socket::sendSocketMessage(const char* mesg) {

	retVal = send(sHost, mesg, strlen(mesg), 0); //    该函数的第一个参数指定发送端套接字描述符；第二个参数指明一个存放应用程序要发送数据的缓冲区；第三个参数指明实际要发送的数据的字节数；第四个参数一般置0。
	if (SOCKET_ERROR == retVal)
	{
		cout << "send failed!" << endl;
		closesocket(sHost); //关闭套接字  
		WSACleanup(); //释放套接字资源  
		return -1;
	}
}

bool Socket::reviceSocketMessage() {

	ZeroMemory(bufRecv, 512);

	//设置接收超时
	int timeout = 4000;
	setsockopt(sHost, SOL_SOCKET, SO_SNDTIMEO, (char*)&timeout, sizeof(timeout));
	setsockopt(sHost, SOL_SOCKET, SO_RCVTIMEO, (char*)&timeout, sizeof(timeout));

	int theRecLen = recv(sHost, bufRecv, 512, 0);
	if (SOCKET_ERROR == retVal)
	{
		cout << "revice failed!" << endl;
		closesocket(sHost); //关闭套接字  
		WSACleanup(); //释放套接字资源  
		return false;
	}
	return true;

}

char* Socket::getReviceMessage()
{
	return bufRecv;
}