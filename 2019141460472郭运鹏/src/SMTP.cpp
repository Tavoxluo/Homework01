#include"SMTP.h"
#include"Socket.h"
#include"Base64Test.h"
#include <windows.h>
#include<Winbase.h>
#include<string>
using namespace std;



void SMTP_163(string userName, string passWord) {//n是判断是qq邮箱还是163邮箱

	string toWho = "";//收件人邮箱
	string theSubject = "";//发送的主题
	string theContent = "";//要发送的内容
	string temp = "";//用于下面拼接标准协议的字符串

	LPTSTR lpPath = new char[MAX_PATH];
	LPTSTR S163 = new char[20];
	strcpy(lpPath, "C:\\ip.ini");
	GetPrivateProfileString("SMTP", "163", "", S163, 20, lpPath);
	delete[] lpPath;
	cout << "请输入收件人邮箱" << endl;
	cin >> toWho;
	cout << "请输入邮件主题" << endl;
	cin >> theSubject;
	cout << "请输入邮件内容" << endl;
	cin >> theContent;



	Socket sock(S163, 25); //smtp.163.com 220.181.12.13
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "helo xxxxx" << endl;
	sock.sendSocketMessage("helo xxxxx\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "auth login" << endl;
	sock.sendSocketMessage("auth login\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//用户名 需要base64
	Base64Coder base64_obj;
	base64_obj.Encode(userName.data());//
	char* userBase64Buf = (char*)base64_obj.EncodedMessage();//base64转换
	cout << "c:" << userName << endl;
	sock.sendSocketMessage(userBase64Buf);
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl; //

//	Base64Coder base64_obj;
	base64_obj.Encode(passWord.data());//
	char* PasswordBase64Buf = (char*)base64_obj.EncodedMessage();//base64转换
	cout << "c:" << passWord << endl;
	sock.sendSocketMessage(PasswordBase64Buf);
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "*******************************" << endl;
	temp = "mail from: <" + userName + "@163.com>";
	cout << "c:" << temp << endl;
	sock.sendSocketMessage(temp.data());
	//sock.sendSocketMessage("xxxxx@163.com");
	//sock.sendSocketMessage(">");
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//收件人

	cout << "c:" << "rcpt to: <" << toWho << ">" << endl;
	sock.sendSocketMessage("rcpt to: <");
	sock.sendSocketMessage(toWho.data());
	sock.sendSocketMessage(">");
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//邮件内容
	cout << "c:" << "data" << endl;
	sock.sendSocketMessage("data\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "*********************" << endl;
	cout << "c:" << "发送的邮件内容" << endl;

	//发件人
	temp = "from:" + userName + "@163.com\r\n";//temp临时用于字符串拼接
	sock.sendSocketMessage(temp.data());
	//收件人
	temp = "to:" + toWho + "\r\n";
	sock.sendSocketMessage(temp.data());
	//主题
	temp = "subject:" + theSubject + "\r\n\r\n";
	sock.sendSocketMessage(temp.data());
	//内容
	temp = theContent;
	sock.sendSocketMessage(temp.data());
	sock.sendSocketMessage("\r\n.\r\n");

	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;


	//退出
	cout << "c:" << "quit\r\n" << endl;
	sock.sendSocketMessage("quit\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	sock.CloseSocket();
}

bool testSmtpAuthor_163(string userName, string passWord) {
	LPTSTR lpPath = new char[MAX_PATH];
	LPTSTR S163 = new char[20];
	strcpy(lpPath, "C:\\ip.ini");
	GetPrivateProfileString("SMTP", "163", "", S163, 20, lpPath);
	delete[] lpPath;
	Socket sock(S163, 25); //smtp.163.com
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "helo xxxxx" << endl;
	sock.sendSocketMessage("helo xxxxx\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "auth login" << endl;
	sock.sendSocketMessage("auth login\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//用户名 好像需要base64
	Base64Coder base64_obj;
	base64_obj.Encode(userName.data());
	char* userBase64Buf = (char*)base64_obj.EncodedMessage();//到此为base64转换
	cout << "c:" << userName << endl;
	sock.sendSocketMessage(userBase64Buf);
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//密码(授权码) //同上
//	Base64Coder base64_obj;
	base64_obj.Encode(passWord.data());
	char* PasswordBase64Buf = (char*)base64_obj.EncodedMessage();//到此为base64转换
	cout << "c:" << passWord << endl;
	sock.sendSocketMessage(PasswordBase64Buf);
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	string test(sock.getReviceMessage());//测试密码
	int exist = test.find("235");
	if (exist == string::npos) {
		return false;
	}

	else {
		return true;
	}

}


void SMTP_qq(std::string userName, std::string passWord) {

	string toWho = "";//收件人邮箱
	string theSubject = "";//发送的主题
	string theContent = "";//要发送的内容
	string temp = "";//用于下面拼接标准协议的字符串


	cout << "请输入收件人邮箱" << endl;
	cin >> toWho;
	cout << "请输入邮件主题" << endl;
	cin >> theSubject;
	cout << "请输入邮件内容" << endl;
	cin >> theContent;


	LPTSTR lpPath = new char[MAX_PATH];
	LPTSTR SQQ = new char[20];
	strcpy(lpPath, "C:\\ip.ini");
	GetPrivateProfileString("SMTP", "qq", "", SQQ, 20, lpPath);
	delete[] lpPath;
	Socket sock(SQQ, 25);
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "helo xxxxx" << endl;
	sock.sendSocketMessage("helo xxxxx\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "auth login" << endl;
	sock.sendSocketMessage("auth login\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//用户名 好像需要base64
	Base64Coder base64_obj;
	base64_obj.Encode(userName.data());
	char* userBase64Buf = (char*)base64_obj.EncodedMessage();//到此为base64转换
	cout << "c:" << userName << endl;
	sock.sendSocketMessage(userBase64Buf);
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//密码(授权码) //同上
//	Base64Coder base64_obj;
	base64_obj.Encode(passWord.data());
	char* PasswordBase64Buf = (char*)base64_obj.EncodedMessage();//到此为base64转换
	cout << "c:" << passWord << endl;
	sock.sendSocketMessage(PasswordBase64Buf);
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "*******************************" << endl;
	temp = "mail from: <" + userName + "@qq.com>";
	cout << "c:" << temp << endl;
	sock.sendSocketMessage(temp.data());
	//sock.sendSocketMessage("xxxxx@163.com");
	//sock.sendSocketMessage(">");
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//收件人

	cout << "c:" << "rcpt to: <" << toWho << ">" << endl;
	sock.sendSocketMessage("rcpt to: <");
	sock.sendSocketMessage(toWho.data());
	sock.sendSocketMessage(">");
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//邮件内容
	cout << "c:" << "data" << endl;
	sock.sendSocketMessage("data\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "*********************" << endl;
	cout << "c:" << "发送的邮件内容" << endl;

	//发件人
	temp = "from:" + userName + "@qq.com\r\n";//temp临时用于字符串拼接
	sock.sendSocketMessage(temp.data());
	//收件人
	temp = "to:" + toWho + "\r\n";
	sock.sendSocketMessage(temp.data());
	//主题
	temp = "subject:" + theSubject + "\r\n\r";
	sock.sendSocketMessage(temp.data());
	//内容
	temp = theContent;
	sock.sendSocketMessage(temp.data());
	sock.sendSocketMessage("\r\n.\r\n");

	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;


	//退出
	cout << "c:" << "quit\r\n" << endl;
	sock.sendSocketMessage("quit\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	sock.CloseSocket();
}


bool testSmtpAuthor_qq(std::string userName, std::string passWord) {

	LPTSTR lpPath = new char[MAX_PATH];
	LPTSTR SQQ = new char[20];
	strcpy(lpPath, "C:\\ip.ini");
	GetPrivateProfileString("SMTP", "qq", "", SQQ, 20, lpPath);
	delete[] lpPath;
	Socket sock(SQQ, 25); //SMTP协议专用端口号
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "helo xxxxx" << endl;
	sock.sendSocketMessage("helo xxxxx\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "auth login" << endl;
	sock.sendSocketMessage("auth login\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//用户名 好像需要base64
	Base64Coder base64_obj;
	base64_obj.Encode(userName.data());
	char* userBase64Buf = (char*)base64_obj.EncodedMessage();//到此为base64转换
	cout << "c:" << userName << endl;
	sock.sendSocketMessage(userBase64Buf);
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//密码(授权码) //同上
//	Base64Coder base64_obj;
	base64_obj.Encode(passWord.data());//
	char* PasswordBase64Buf = (char*)base64_obj.EncodedMessage();//到此为base64转换
	cout << "c:" << passWord << endl;
	sock.sendSocketMessage(PasswordBase64Buf);
	sock.sendSocketMessage("\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	string test(sock.getReviceMessage());//测试密码
	int exist = test.find("235");
	if (exist == string::npos) {
		return false;
	}

	else {
		return true;
	}
}