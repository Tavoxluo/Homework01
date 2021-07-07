/**
    Email客户端的实现
*/
#include<windows.h>
#include<stdio.h>
#include<WinSock.h>
#include<iostream>
using namespace std;
#pragma comment(lib,"ws2_32.lib")
/**
    对任意的二进制文件，可用base64编码。这种编码方法是先把二进制代码划分为一个个24位长的单元，然后把每一个24位单元划分为4个
    6位组。每一个6位组按以下方法转换成ASCII码。6位的二进制代码共有64种不同的值，从0到63。用A表示0，用B表示1....26个大写字母
    排列完毕后，接下去再排26个小写字母，再后面是10个数字，最后用‘+'表示62，用‘/‘表示63。再用两个连在一起的等号“==”和一个等号
    “=”分别表示最后一组的代码只有8位或16位。回车和换行符都忽略，它们可在任何地方插入。
*/
//由于邮件是以base64加密格式传送的，所以要定义数据格式如下
struct Base64Date6
{
    unsigned int d4 : 6;
    unsigned int d3 : 6;
    unsigned int d2 : 6;
    unsigned int d1 : 6;
};
// 协议中加密部分使用的是base64方法
char ConvertToBase64(char c6);//对数据进行加密传送，传送给socket套接字
void EncodeBase64(char* dbuf, char* buf128, int len);//对数据进行编码
void SendMail(char* email, char* body);//发邮件利用socket套接字
int OpenSocket(struct sockaddr* addr);//打开socket套接字
int main()
{
    char EmailTo[] = "17783445209@163.com";//接收者的邮箱
    char EmailContents[1000];
    char info[100];
    sprintf_s(info, "Subject: %s:\r\n", "明天考试了");
    sprintf_s(EmailContents, "From: \"163邮箱\"<19822920490@163.com>\r\n" "To: \"163邮箱\"<17783445209@163.com>\r\n" "%s\r\n" "明天就考试了亲", info);
    SendMail(EmailTo, EmailContents);
    return 0;
}

/**
    base64将二进制代码转换成ASCII码
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
    对数据进行编码
*/
// base64的实现
void  EncodeBase64(char* dbuf, char* buf128, int len)
{
    struct  Base64Date6* ddd = NULL;
    int i = 0;
    char buf[256] = { 0 }; //数组uf里面的值全部初始化为0
    char* tmp = NULL;
    char cc = '\0'; //对应的ASCII值为0，是字符串结束的标志
    memset(buf, 0, 256); //初始化函数。作用是将某一块内存中的内容全部设置为指定的值。memset()函数通常为新申请的内存做初始化工作。
    //这句的话意思是将buf中当前位置后面的256个字节用0替换并返回buf
    strcpy_s(buf, buf128);//这句话的意思是把从buf128地址开始且含有NULL结束符的字符串复制到以dest开始的地址空间
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

// 发送邮件
void SendMail(char* email, char* body)
{
    int sockfd = { 0 };
    char buf[1500] = { 0 };
    char rbuf[1500] = { 0 };//STMP协议传送邮件的应答（状态码）
    char login[128] = { 0 };
    char pass[128] = { 0 };
    WSADATA WSAData;
    struct sockaddr_in their_addr = { 0 };
    WSAStartup(MAKEWORD(2, 2), &WSAData);
    memset(&their_addr, 0, sizeof(their_addr));
    their_addr.sin_family = AF_INET;
    their_addr.sin_port = htons(25);
    hostent* hptr = gethostbyname("smtp.163.com"); // 用的是163服务器
    memcpy(&their_addr.sin_addr.S_un.S_addr, hptr->h_addr_list[0], hptr->h_length);
    printf("IP of smpt.163.com is : %d:%d:%d:%d\n",
        their_addr.sin_addr.S_un.S_un_b.s_b1,
        their_addr.sin_addr.S_un.S_un_b.s_b2,
        their_addr.sin_addr.S_un.S_un_b.s_b3,
        their_addr.sin_addr.S_un.S_un_b.s_b4);
    //OK,163邮箱的IP地址已获取到，下面就要开始进行连接了
    sockfd = OpenSocket((struct sockaddr*)&their_addr);
    //cout<<"look:"<<sockfd<<endl;
    memset(rbuf, 0, 1500);
    while (recv(sockfd, rbuf, 1500, 0) == 0)
    {
        cout << "重新连接..." << endl;
        Sleep(5);
        sockfd = OpenSocket((struct sockaddr*)&their_addr);
        memset(rbuf, 0, 1500);
    }
    cout << rbuf << endl;//返回220表示recv成功（访问163邮箱成功）


    // EHLO
    memset(buf, 0, 1500);
    sprintf_s(buf, "ehlo 19822920490@163.com\r\n");//发送者邮箱名
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
    sprintf_s(buf, "19822920490@163.com");//发送者邮箱账户
    memset(login, 0, 128);
    EncodeBase64(login, buf, strlen(buf));
    sprintf_s(buf, "%s\r\n", login);
    send(sockfd, buf, strlen(buf), 0);
    cout << "Base64 UserName: " << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // PASSWORD
    sprintf_s(buf, "SFMVEJXODVMRDXNV");//你的邮箱密码
    memset(pass, 0, 128);
    EncodeBase64(pass, buf, strlen(buf));
    sprintf_s(buf, "%s\r\n", pass);
    send(sockfd, buf, strlen(buf), 0);
    cout << "Base64 Password: " << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;
    //cout<<"通过"<<endl;

    // MAIL FROM
    memset(buf, 0, 1500);
    sprintf_s(buf, "mail from:<19822920490@163.com>\r\n");//填写
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    //cout<<"经过此处"<<endl;
    cout << rbuf << endl;
    //cout<<"测试失败"<<endl;

    // RCPT TO 第一个收件人
    sprintf_s(buf, "rcpt to:<%s>\r\n", email);
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // DATA 准备开始发送邮件内容
    sprintf_s(buf, "data\r\n");
    send(sockfd, buf, strlen(buf), 0);
    cout << buf << endl;
    memset(rbuf, 0, 1500);
    recv(sockfd, rbuf, 1500, 0);
    cout << rbuf << endl;

    // 发送邮件内容，\r\n.\r\n内容结束标记
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

    //清理工作
    closesocket(sockfd);
    WSACleanup();
    return;
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
