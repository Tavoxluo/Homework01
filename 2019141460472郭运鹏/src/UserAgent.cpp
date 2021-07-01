#include<iostream>
#include<string>
#include"POP3.h"
#include"SMTP.h"
#include <windows.h>
#include<Winbase.h>
using namespace std;
int main() {
	bool ifQuitArgent = false;//控制是否退出各个代理
	int qqOr163 = 0; //qq或163邮箱的选择
	int smtpOrPop3 = 0;//smtp或pop3的选择

	string userName = "";//用户名
	string passWord = "";//密码
	LPTSTR lpPath = new char[MAX_PATH];
	LPTSTR UserName = new char[20];
	LPTSTR PassWord = new char[20];
	strcpy(lpPath, "C:\\ip.ini");
	GetPrivateProfileString("user", "userName", "", UserName, 20, lpPath);
	GetPrivateProfileString("user", "passWord", "", PassWord, 20, lpPath);
	delete[] lpPath;
	cout << "欢迎来到邮件代理系统" << endl;
	cout << "支持163邮箱和qq邮箱的代理" << endl;

	while (qqOr163 != 4) {

		cout << "1.使用qq邮箱代理服务" << endl;
		cout << "2.使用163邮箱代理服务(为@163.com系列)" << endl;
		cout << "3.使用代码绑定的QQ代理服务(此处设计安全问题，未具体设置账号密码)" << endl;
		cout << "4.推出该次使用，关闭程序" << endl;
		cin >> qqOr163;
		system("cls");

		switch (qqOr163)
		{
		case 1:
			cout << "正在申请qq邮件代理系统" << endl;
			cout << "请输入用户名(不包括@xxx的部分，只输入@之前的内容)" << endl;
			cin >> userName;
			cout << "请输入QQsmtp/pop3协议的授权码作为密码（需要手动开通邮箱的smtp/pop3协议得到授权码)" << endl;
			cin >> passWord;
			if (!testSmtpAuthor_qq(userName, passWord)) {//用户名或密码不正确
				cout << "用户名或密码不正确" << endl;
				system("pause");
				system("cls");

				break;
			}
			else {
				system("cls");
				cout << "1.使用SMTP写QQ邮件的服务" << endl;
				cout << "2.使用POP3下载QQ邮件到本地的服务" << endl;
				cout << "3.退出QQ邮箱代理服务" << endl;
				cin >> smtpOrPop3;
				while (smtpOrPop3 != 3) {

					if (smtpOrPop3 == 1) {
						SMTP_qq(userName, passWord);
						system("pause");
						system("cls");
					}
					else if (smtpOrPop3 == 2) {
						POP3_qq(userName, passWord);
						system("pause");
						system("cls");
					}
					else if (smtpOrPop3 == 3) {
					}
					else
					{
						cout << "只能输入1或2或3" << endl;
					}
				}
			}
			break;
		case 2:
			cout << "正在申请163邮件代理系统" << endl;
			cout << "请输入用户名(不包括@xxx的部分，只输入@之前的内容)" << endl;
			cin >> userName;
			cout << "请输入163smtp/pop3协议的授权码作为密码（需要手动开通邮箱的smtp/pop3协议得到授权码)" << endl;
			cin >> passWord;
			if (!testSmtpAuthor_163(userName, passWord)) {//用户名或密码不正确
				cout << "用户名或密码不正确" << endl;
				system("pause");
				system("cls");
				break;
			}
			else {
				system("cls");
				cout << "1.使用SMTP写163邮件的服务" << endl;
				cout << "2.使用POP3下载163邮件到本地的服务" << endl;
				cout << "3.退出163邮箱代理服务" << endl;
				cin >> smtpOrPop3;
				while (smtpOrPop3 != 3) {
					if (smtpOrPop3 == 1) {
						SMTP_163(userName, passWord);
						system("pause");
						system("cls");
					}
					else if (smtpOrPop3 == 2) {
						POP3_163(userName, passWord);
						system("pause");
						system("cls");
					}
					else if (smtpOrPop3 == 3) {
					}
					else
					{
						cout << "只能输入1或2或3" << endl;
					}
				}
			}


			break;
		case 3:
			cout << "使用代码绑定的QQ邮箱代理系统" << endl;
			cout << "1.进入SMTP写邮件代理" << endl;
			cout << "2.进入pop3访问邮箱代理" << endl;
			cout << "3.退出" << endl;
			cin >> smtpOrPop3;
			while (smtpOrPop3 != 3) {
				if (smtpOrPop3 == 1) {

					SMTP_qq(UserName, PassWord);
					system("pause");
					system("cls");
				}
				else if (smtpOrPop3 == 2) {

					POP3_qq(UserName, PassWord);
					system("pause");
					system("cls");
				}
				else if (smtpOrPop3 == 3) {
				}
				else
				{
					cout << "只能输入1,2,3" << endl;
				}
			}
			break;
		case 4:
			system("cls");
			break;
		default:
			cout << "请输入1，2，3，4" << endl;
			break;
		}
	}
}