#include"POP3.h"
#include"Socket.h"
#include"Base64Test.h"
#include <windows.h>
#include<fstream>
#include<string>

using namespace std;

void POP3_163(string userName, string passWord) {
	string thePath = "2.txt";//邮件的保存路径
	string whichEmail = "1";//选择哪封邮件
	ofstream outfile(thePath, ios::out);//文件流
	string theContent = "";//邮件的内容
	string temp = "";//临时拼接用字符串

	LPTSTR lpPath = new char[MAX_PATH];
	LPTSTR POP = new char[20];
	strcpy(lpPath, "C:\\ip.ini");
	GetPrivateProfileString("POP", "163", "", POP, 20, lpPath);

	Socket sock(POP, 110);
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//输入用户名
	temp = "user " + userName + "@163.com\r\n";
	cout << "c:" << temp << endl;
	sock.sendSocketMessage(temp.data());//
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//密码
	temp = "pass " + passWord + "\r\n";
	cout << "c:" << "pass ***********" << endl;
	sock.sendSocketMessage(temp.data());//
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "stat" << endl;
	sock.sendSocketMessage("stat\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "list" << endl;
	sock.sendSocketMessage("list\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "请选择你要读取哪一封邮件,（请输入数字）" << endl;
	cin >> whichEmail;

	temp = "retr " + whichEmail + "\r\n";
	cout << "c:" << "retr " << whichEmail << endl;
	sock.sendSocketMessage(temp.data());



	while (1)//不用担心无限循环，在received函数中设置过超时中断
	{

		sock.reviceSocketMessage();
		//	cout << "Server : " << sock.getReviceMessage() << endl;

		string test = sock.getReviceMessage();
		theContent += test;

		if (test.length() == 0)
		{
			break;
		}
	}

	outfile << theContent;

	temp = "邮件成功写入到" + thePath;
	cout << temp << endl;

	cout << "c:" << "quit" << endl;
	sock.sendSocketMessage("quit\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;
}

bool testPopAuthor_163(string userName, string passWord) {

	string temp = "";

	Socket sock("121.195.178.52", 110); //邮箱ip改一下，端口都是25    59.111.192.150学校的
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	temp = "user " + userName + "@163.com\r\n";
	cout << "c:" << temp << endl;
	sock.sendSocketMessage(temp.data());//"user lmom_xa@163.com\r\n"
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//密码
	temp = "pass " + passWord + "\r\n";
	cout << "c:" << "pass ***********" << endl;
	sock.sendSocketMessage(temp.data());
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//生成一个string 使用find判断密码是否成功
	string test(sock.getReviceMessage());//
	int exist = test.find("+OK");
	if (exist == string::npos) {

		return false;
	}

	else {
		return true;
	}
}

void POP3_qq(std::string userName, std::string passWord) {
	string thePath = "1.txt";//邮件的保存路径
	string whichEmail = "1";//选择哪封邮件
	ofstream outfile(thePath, ios::out);//文件流
	string theContent = "";//邮件的内容
	string temp = "";//临时拼接用字符串

	LPTSTR lpPath = new char[MAX_PATH];
	LPTSTR QQ = new char[20];
	strcpy(lpPath, "C:\\ip.ini");
	GetPrivateProfileString("POP", "qq", "", QQ, 20, lpPath);

	Socket sock(QQ, 110);
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//输入用户名
	temp = "user " + userName + "@qq.com\r\n";
	cout << "c:" << temp << endl;
	sock.sendSocketMessage(temp.data());
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//密码
	temp = "pass " + passWord + "\r\n";
	cout << "c:" << "pass ***********" << endl;
	sock.sendSocketMessage(temp.data());
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "stat" << endl;
	sock.sendSocketMessage("stat\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	cout << "c:" << "list" << endl;
	sock.sendSocketMessage("list\r\n");

	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	sock.sendSocketMessage(" \r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;


	cout << "请选择你要读取哪一封邮件,（请输入数字）" << endl;
	cin >> whichEmail;

	temp = "retr " + whichEmail + "\r\n";
	cout << "c:" << "retr " << whichEmail << endl;
	sock.sendSocketMessage(temp.data());



	while (1)
	{

		sock.reviceSocketMessage();
		cout << "Server" << sock.getReviceMessage() << endl;
		//	cout << "Server : " << sock.getReviceMessage() << endl;

		string test = sock.getReviceMessage();
		theContent += test;

		if (test.length() == 0)
		{
			break;
		}
	}

	outfile << theContent;

	temp = "邮件成功写入到" + thePath;
	cout << temp << endl;

	cout << "c:" << "quit" << endl;
	sock.sendSocketMessage("quit\r\n");
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;
}

bool testPopAuthor_qq(std::string userName, std::string passWord) {

	string temp = "";

	Socket sock("121.51.131.77", 110);
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	temp = "user " + userName + "@qq.com\r\n";
	cout << "c:" << temp << endl;
	sock.sendSocketMessage(temp.data());
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//密码
	temp = "pass " + passWord + "\r\n";
	cout << "c:" << "pass ***********" << endl;
	sock.sendSocketMessage(temp.data());
	sock.reviceSocketMessage();
	cout << sock.getReviceMessage() << endl;

	//生成一个string 使用find判断密码是否成功
	string test(sock.getReviceMessage());//
	int exist = test.find("+OK");
	if (exist == string::npos) {

		return false;
	}

	else {
		return true;
	}
}