/**
    Email客户端接收（POP3）的实现
*/
#include<windows.h>
#include<stdio.h>
#include<WinSock.h>
#include<iostream>
#include <string>
using namespace std;
#pragma comment(lib,"ws2_32.lib")
int OpenSocket(struct sockaddr* addr);//打开socket套接字
// 发送邮件
int main()
{
    int sockfd = { 0 };
    char buf[1500] = { 0 };
    char rbuf[1500] = { 0 };//POP协议传送邮件的应答
    char login[128] = { 0 };
    char pass[128] = { 0 };
    WSADATA WSAData;
    struct sockaddr_in their_addr = { 0 };
    WSAStartup(MAKEWORD(2, 2), &WSAData);
    memset(&their_addr, 0, sizeof(their_addr));
    their_addr.sin_family = AF_INET;
    their_addr.sin_port = htons(110);
    hostent* hptr = gethostbyname("pop3.163.com"); // 用的是163服务器
    memcpy(&their_addr.sin_addr.S_un.S_addr, hptr->h_addr_list[0], hptr->h_length);
    printf("IP of pop3.163.com is : %d:%d:%d:%d\n",
        their_addr.sin_addr.S_un.S_un_b.s_b1,
        their_addr.sin_addr.S_un.S_un_b.s_b2,
        their_addr.sin_addr.S_un.S_un_b.s_b3,
        their_addr.sin_addr.S_un.S_un_b.s_b4);
    //OK,163邮箱的IP地址已获取到，下面就要开始进行连接了
    sockfd = OpenSocket((struct sockaddr*)&their_addr);
    cout << "look:" << sockfd << endl;
    memset(rbuf, 0, 1500);
    while (recv(sockfd, rbuf, 1500, 0) == 0)
    {
        cout << "重新连接..." << endl;
        Sleep(5);
        sockfd = OpenSocket((struct sockaddr*)&their_addr);
        memset(rbuf, 0, 1500);
    }
    cout << rbuf << endl;//返回220表示recv成功（访问163邮箱成功）

    // USER
    memset(buf, 0, 1500);
    sprintf_s(buf, "%s\r\n", "user 17783445209@163.com");//输入你的邮箱账号
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // PASSWORD
    sprintf_s(buf, "%s\r\n", "pass RXRFQWJUCNMVBLQD");//你的邮箱密码
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;
    //cout<<"通过"<<endl;

    //LIST
    memset(buf, 0, 1500);
    sprintf_s(buf, "%s\r\n", "list");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;
    //cout<<"通过List"<<endl;

    //RETR
    string input;
    cout << "请输入查询命令:" << endl;
    getline(cin, input);
    sprintf_s(buf, "%s\r\n", input.c_str());
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;
    //cout<<"通过retr"<<endl;

    // QUIT
    sprintf_s(buf, "QUIT\r\n");
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << "Quit Receive: " << rbuf << endl;

    //清理工作
    closesocket(sockfd);
    WSACleanup();
    return 0;
}
// 打开TCP Socket连接
int OpenSocket(struct sockaddr* addr)
{
    int sockfd = 0;
    sockfd = socket(PF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
    {
        cout << "Open sockfd(TCP) error!" << endl;
        exit(-1);
    }
    if (connect(sockfd, addr, sizeof(struct sockaddr)) < 0)
    {
        cout << "Connect sockfd(TCP) error!" << endl;
        exit(-1);
    }
    return sockfd;
}