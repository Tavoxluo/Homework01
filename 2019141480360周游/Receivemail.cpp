/**
    Email�ͻ��˽��գ�POP3����ʵ��
*/
#include<windows.h>
#include<stdio.h>
#include<WinSock.h>
#include<iostream>
#include <string>
using namespace std;
#pragma comment(lib,"ws2_32.lib")
int OpenSocket(struct sockaddr* addr);//��socket�׽���
// �����ʼ�
int main()
{
    int sockfd = { 0 };
    char buf[1500] = { 0 };
    char rbuf[1500] = { 0 };//POPЭ�鴫���ʼ���Ӧ��
    char login[128] = { 0 };
    char pass[128] = { 0 };
    WSADATA WSAData;
    struct sockaddr_in their_addr = { 0 };
    WSAStartup(MAKEWORD(2, 2), &WSAData);
    memset(&their_addr, 0, sizeof(their_addr));
    their_addr.sin_family = AF_INET;
    their_addr.sin_port = htons(110);
    hostent* hptr = gethostbyname("pop3.163.com"); // �õ���163������
    memcpy(&their_addr.sin_addr.S_un.S_addr, hptr->h_addr_list[0], hptr->h_length);
    printf("IP of pop3.163.com is : %d:%d:%d:%d\n",
        their_addr.sin_addr.S_un.S_un_b.s_b1,
        their_addr.sin_addr.S_un.S_un_b.s_b2,
        their_addr.sin_addr.S_un.S_un_b.s_b3,
        their_addr.sin_addr.S_un.S_un_b.s_b4);
    //OK,163�����IP��ַ�ѻ�ȡ���������Ҫ��ʼ����������
    sockfd = OpenSocket((struct sockaddr*)&their_addr);
    cout << "look:" << sockfd << endl;
    memset(rbuf, 0, 1500);
    while (recv(sockfd, rbuf, 1500, 0) == 0)
    {
        cout << "��������..." << endl;
        Sleep(5);
        sockfd = OpenSocket((struct sockaddr*)&their_addr);
        memset(rbuf, 0, 1500);
    }
    cout << rbuf << endl;//����220��ʾrecv�ɹ�������163����ɹ���

    // USER
    memset(buf, 0, 1500);
    sprintf_s(buf, "%s\r\n", "user 17783445209@163.com");//������������˺�
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // PASSWORD
    sprintf_s(buf, "%s\r\n", "pass RXRFQWJUCNMVBLQD");//�����������
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;
    //cout<<"ͨ��"<<endl;

    //LIST
    memset(buf, 0, 1500);
    sprintf_s(buf, "%s\r\n", "list");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;
    //cout<<"ͨ��List"<<endl;

    //RETR
    string input;
    cout << "�������ѯ����:" << endl;
    getline(cin, input);
    sprintf_s(buf, "%s\r\n", input.c_str());
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;
    //cout<<"ͨ��retr"<<endl;

    // QUIT
    sprintf_s(buf, "QUIT\r\n");
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << "Quit Receive: " << rbuf << endl;

    //������
    closesocket(sockfd);
    WSACleanup();
    return 0;
}
// ��TCP Socket����
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