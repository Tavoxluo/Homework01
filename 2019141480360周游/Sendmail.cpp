/**
    Email�ͻ��˵�ʵ��
*/
#include<windows.h>
#include<stdio.h>
#include<WinSock.h>
#include<iostream>
using namespace std;
#pragma comment(lib,"ws2_32.lib")
/**
    ������Ķ������ļ�������base64���롣���ֱ��뷽�����ȰѶ����ƴ��뻮��Ϊһ����24λ���ĵ�Ԫ��Ȼ���ÿһ��24λ��Ԫ����Ϊ4��
    6λ�顣ÿһ��6λ�鰴���·���ת����ASCII�롣6λ�Ķ����ƴ��빲��64�ֲ�ͬ��ֵ����0��63����A��ʾ0����B��ʾ1....26����д��ĸ
    ������Ϻ󣬽���ȥ����26��Сд��ĸ���ٺ�����10�����֣�����á�+'��ʾ62���á�/����ʾ63��������������һ��ĵȺš�==����һ���Ⱥ�
    ��=���ֱ��ʾ���һ��Ĵ���ֻ��8λ��16λ���س��ͻ��з������ԣ����ǿ����κεط����롣
*/
//�����ʼ�����base64���ܸ�ʽ���͵ģ�����Ҫ�������ݸ�ʽ����
struct Base64Date6
{
    unsigned int d4 : 6;
    unsigned int d3 : 6;
    unsigned int d2 : 6;
    unsigned int d1 : 6;
};
// Э���м��ܲ���ʹ�õ���base64����
char ConvertToBase64(char c6);//�����ݽ��м��ܴ��ͣ����͸�socket�׽���
void EncodeBase64(char* dbuf, char* buf128, int len);//�����ݽ��б���
void SendMail(char* email, char* body);//���ʼ�����socket�׽���
int OpenSocket(struct sockaddr* addr);//��socket�׽���
int main()
{
    char EmailTo[] = "17783445209@163.com";//�����ߵ�����
    char EmailContents[1000];
    char info[100];
    sprintf_s(info, "Subject: %s:\r\n", "���쿼����");
    sprintf_s(EmailContents, "From: \"163����\"<19822920490@163.com>\r\n" "To: \"163����\"<17783445209@163.com>\r\n" "%s\r\n" "����Ϳ�������", info);
    SendMail(EmailTo, EmailContents);
    return 0;
}

/**
    base64�������ƴ���ת����ASCII��
*/
char ConvertToBase64(char uc)
{
    if (uc < 26)
    {
        return'A' + uc;
    }
    if (uc < 52)
    {
        return'a' + (uc - 26);
    }
    if (uc < 62)
    {
        return'0' + (uc - 52);
    }
    if (uc == 62)
    {
        return'+';
    }
    if (uc == 63)
    {
        return '/';
    }
}

/**
    �����ݽ��б���
*/
// base64��ʵ��
void  EncodeBase64(char* dbuf, char* buf128, int len)
{
    struct  Base64Date6* ddd = NULL;
    int i = 0;
    char buf[256] = { 0 }; //����uf�����ֵȫ����ʼ��Ϊ0
    char* tmp = NULL;
    char cc = '\0'; //��Ӧ��ASCIIֵΪ0�����ַ��������ı�־
    memset(buf, 0, 256); //��ʼ�������������ǽ�ĳһ���ڴ��е�����ȫ������Ϊָ����ֵ��memset()����ͨ��Ϊ��������ڴ�����ʼ��������
    //���Ļ���˼�ǽ�buf�е�ǰλ�ú����256���ֽ���0�滻������buf
    strcpy_s(buf, buf128);//��仰����˼�ǰѴ�buf128��ַ��ʼ�Һ���NULL���������ַ������Ƶ���dest��ʼ�ĵ�ַ�ռ�
    for (i = 1; i <= len / 3; i++)
    {
        tmp = buf + (i - 1) * 3;
        cc = tmp[2];
        tmp[2] = tmp[0];
        tmp[0] = cc;
        ddd = (struct Base64Date6*)tmp;
        dbuf[(i - 1) * 4 + 0] = ConvertToBase64((unsigned int)ddd->d1);
        dbuf[(i - 1) * 4 + 1] = ConvertToBase64((unsigned int)ddd->d2);
        dbuf[(i - 1) * 4 + 2] = ConvertToBase64((unsigned int)ddd->d3);
        dbuf[(i - 1) * 4 + 3] = ConvertToBase64((unsigned int)ddd->d4);
    }
    if (len % 3 == 1)
    {
        tmp = buf + (i - 1) * 3;
        cc = tmp[2];
        tmp[2] = tmp[0];
        tmp[0] = cc;
        ddd = (struct Base64Date6*)tmp;
        dbuf[(i - 1) * 4 + 0] = ConvertToBase64((unsigned int)ddd->d1);
        dbuf[(i - 1) * 4 + 1] = ConvertToBase64((unsigned int)ddd->d2);
        dbuf[(i - 1) * 4 + 2] = '=';
        dbuf[(i - 1) * 4 + 3] = '=';
    }
    if (len % 3 == 2)
    {
        tmp = buf + (i - 1) * 3;
        cc = tmp[2];
        tmp[2] = tmp[0];
        tmp[0] = cc;
        ddd = (struct Base64Date6*)tmp;
        dbuf[(i - 1) * 4 + 0] = ConvertToBase64((unsigned int)ddd->d1);
        dbuf[(i - 1) * 4 + 1] = ConvertToBase64((unsigned int)ddd->d2);
        dbuf[(i - 1) * 4 + 2] = ConvertToBase64((unsigned int)ddd->d3);
        dbuf[(i - 1) * 4 + 3] = '=';
    }
    return;
}

// �����ʼ�
void SendMail(char* email, char* body)
{
    int sockfd = { 0 };
    char buf[1500] = { 0 };
    char rbuf[1500] = { 0 };//STMPЭ�鴫���ʼ���Ӧ��״̬�룩
    char login[128] = { 0 };
    char pass[128] = { 0 };
    WSADATA WSAData;
    struct sockaddr_in their_addr = { 0 };
    WSAStartup(MAKEWORD(2, 2), &WSAData);
    memset(&their_addr, 0, sizeof(their_addr));
    their_addr.sin_family = AF_INET;
    their_addr.sin_port = htons(25);
    hostent* hptr = gethostbyname("smtp.163.com"); // �õ���163������
    memcpy(&their_addr.sin_addr.S_un.S_addr, hptr->h_addr_list[0], hptr->h_length);
    printf("IP of smpt.163.com is : %d:%d:%d:%d\n",
        their_addr.sin_addr.S_un.S_un_b.s_b1,
        their_addr.sin_addr.S_un.S_un_b.s_b2,
        their_addr.sin_addr.S_un.S_un_b.s_b3,
        their_addr.sin_addr.S_un.S_un_b.s_b4);
    //OK,163�����IP��ַ�ѻ�ȡ���������Ҫ��ʼ����������
    sockfd = OpenSocket((struct sockaddr*)&their_addr);
    //cout<<"look:"<<sockfd<<endl;
    memset(rbuf, 0, 1500);
    while (recv(sockfd, rbuf, 1500, 0) == 0)
    {
        cout << "��������..." << endl;
        Sleep(5);
        sockfd = OpenSocket((struct sockaddr*)&their_addr);
        memset(rbuf, 0, 1500);
    }
    cout << rbuf << endl;//����220��ʾrecv�ɹ�������163����ɹ���


    // EHLO
    memset(buf, 0, 1500);
    sprintf_s(buf, "ehlo 19822920490@163.com\r\n");//������������
    cout << buf << endl;
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // AUTH LOGIN
    memset(buf, 0, 1500);
    sprintf_s(buf, "auth login\r\n");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // USER
    memset(buf, 0, 1500);
    sprintf_s(buf, "19822920490@163.com");//�����������˻�
    memset(login, 0, 128);
    EncodeBase64(login, buf, strlen(buf));
    sprintf_s(buf, "%s\r\n", login);
    send(sockfd, buf, strlen(buf), 0);
    cout << "Base64 UserName: " << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // PASSWORD
    sprintf_s(buf, "SFMVEJXODVMRDXNV");//�����������
    memset(pass, 0, 128);
    EncodeBase64(pass, buf, strlen(buf));
    sprintf_s(buf, "%s\r\n", pass);
    send(sockfd, buf, strlen(buf), 0);
    cout << "Base64 Password: " << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;
    //cout<<"ͨ��"<<endl;

    // MAIL FROM
    memset(buf, 0, 1500);
    sprintf_s(buf, "mail from:<19822920490@163.com>\r\n");//��д
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    //cout<<"�����˴�"<<endl;
    cout << rbuf << endl;
    //cout<<"����ʧ��"<<endl;

    // RCPT TO ��һ���ռ���
    sprintf_s(buf, "rcpt to:<%s>\r\n", email);
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // DATA ׼����ʼ�����ʼ�����
    sprintf_s(buf, "data\r\n");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // �����ʼ����ݣ�\r\n.\r\n���ݽ������
    sprintf_s(buf, "%s\r\n.\r\n", body);
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // QUIT
    sprintf_s(buf, "quit\r\n");
    send(sockfd, buf, strlen(buf), 0);
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    //������
    closesocket(sockfd);
    WSACleanup();
    return;
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
