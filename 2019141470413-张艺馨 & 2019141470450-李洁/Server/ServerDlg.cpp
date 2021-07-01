// ServerDlg.cpp : implementation file
//

#include "stdafx.h"
#include "Server.h"
#include "ServerDlg.h"
#include "ClearDlg.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	//{{AFX_DATA(CAboutDlg)
	enum { IDD = IDD_ABOUTBOX };
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAboutDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	//{{AFX_MSG(CAboutDlg)
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
	//{{AFX_DATA_INIT(CAboutDlg)
	//}}AFX_DATA_INIT
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAboutDlg)
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
	//{{AFX_MSG_MAP(CAboutDlg)
		// No message handlers
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CServerDlg dialog

CServerDlg::CServerDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CServerDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CServerDlg)
	m_strMsg = _T("");
	//}}AFX_DATA_INIT
	// Note that LoadIcon does not require a subsequent DestroyIcon in Win32
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CServerDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CServerDlg)
	DDX_Text(pDX, IDC_EDIT4, m_strMsg);
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CServerDlg, CDialog)
	//{{AFX_MSG_MAP(CServerDlg)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_MESSAGE(WM_SERVER_ACCEPT, OnServerAccept)
	ON_MESSAGE(WM_SHOWTASK,onShowTask)
	ON_BN_CLICKED(IDC_BUTTON_MIN, OnButtonMin)
	ON_WM_DESTROY()
	ON_BN_CLICKED(IDC_BUTTON_CLEAR, OnButtonClear)
	ON_WM_CTLCOLOR()
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CServerDlg message handlers

BOOL CServerDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon
	// TODO: Add extra initialization here
	if(InitSocket()==false)
	{
		AfxMessageBox("请检查服务器是否已经打开");
		CServerDlg::OnCancel();
	}
	OnButtonMin();
	this->SetWindowText("QC服务器");
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CServerDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CServerDlg::OnPaint() 
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, (WPARAM) dc.GetSafeHdc(), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CServerDlg::OnQueryDragIcon()
{
	return (HCURSOR) m_hIcon;
}


bool CServerDlg::InitSocket()
{
	WSADATA wsaData; 		//初始化TCP协议 
	BOOL ret = WSAStartup(MAKEWORD(2,2), &wsaData); 
	if(ret != 0) 
	{ 
		MessageBox("Initial TCP Protocol Failed!"); 
		return false; 
	} 
	for(int i=0;i<MAX1;i++)
	{
		SocketAccept[i]=INVALID_SOCKET;
	}
	ListeningSocket=socket(AF_INET,SOCK_STREAM,0);
	if(ListeningSocket==INVALID_SOCKET)
	{
		MessageBox("Create SOCKET Failed");
		WSACleanup(); 
		closesocket(ListeningSocket);
		return false;
	}
	serveraddr.sin_family=AF_INET;
	serveraddr.sin_addr.s_addr=0;//INADDR_ANY
	serveraddr.sin_port=htons(4009);
	WSAAsyncSelect(ListeningSocket,m_hWnd,WM_SERVER_ACCEPT,FD_ACCEPT|FD_READ|FD_CLOSE);
	/*设置为异步通讯模式，并为它注册各种网络异步事件，
	  其中m_hWnd 为应用程序的主对话框或主窗口的句柄
	  当检测到相应时间后才为窗口句柄发送消息*/
	if(bind(ListeningSocket,(sockaddr *)&serveraddr,sizeof(serveraddr))==SOCKET_ERROR)
	{
		MessageBox("Bind Failed");
		WSACleanup(); 
		closesocket(ListeningSocket);
		return false;
	}
	if(listen(ListeningSocket,20)==SOCKET_ERROR)
	{
		MessageBox("Listen Failed");
		WSACleanup(); 
		closesocket(ListeningSocket);
		return false;
	}
	HostInfo();
	m_strMsg="Now server is working!\r\nWaiting for client's connecting .......";
	UpdateData(false);
	return true;
}
LRESULT CServerDlg::OnServerAccept(WPARAM wParam,LPARAM lParam)
//wParam参数标识了网络事件发生的套接口.lParam的低字指明了发生的网络事件.
{
	int iEvent=WSAGETSELECTEVENT(lParam); //调用Winsock API函数，得到网络事件类型
//	SOCKET CurSock= (SOCKET)wParam;//调用Winsock API函数，得到发生此事件的客户端套接字 
	switch(iEvent) 
	{ 
		case FD_ACCEPT://客户端连接请求事件 
			OnAccept(wParam,lParam); 
			break; 
		case FD_CLOSE://客户端断开事件: 
			OnClose(wParam,lParam); 
			break; 
		case FD_READ://网络数据包到达事件 
			OnReceive(wParam,lParam); 
			break; 
		default: break; 
	} 
	return 0;
}

void CServerDlg::OnAccept(WPARAM wParam,LPARAM lParam)
{
	int i,addrlen;
	for(i=0;i<MAX1&&SocketAccept[i]!=INVALID_SOCKET;i++){}
	if(i==MAX1)      
		return ;
	sockaddr_in clientsocket;
	addrlen=sizeof(clientsocket);
	SocketAccept[i]=accept(ListeningSocket,(sockaddr *)&clientsocket,&addrlen);
	/*accept函数从处于监听状态的流套接字s的客户连接请求队列中取出排在最前的一个客户请求，并且创建一个新的套接字来与客户套接字创建连接通道，
	如果连接成功，就返回新创建的套接字的描述符，以后与客户套接字交换数据的是新创建的套接字；
	如果失败就返回 INVALID_SOCKET。该函数的第一个参数指定处于监听状态的流套接字；
	操作系统利用第二个参数来返回新创建的套接字的地址结构；
	操作系统利用第三个参数来返回新创建的套接字的地址结构的长度。*/
	if(i==MAX)
	{
		sendinfo err;
		err.type=4;//异常
		CString m;
		m="服务器已达到最大连接数";
		memcpy(err.msg,m,m.GetLength()+1);
		send(SocketAccept[i],(char*)&err,sizeof(err),0);
		Sleep(500);
		closesocket(SocketAccept[i]);
		SocketAccept[i]=INVALID_SOCKET;
		return;
	}
	uinfo[i].userip=inet_ntoa(clientsocket.sin_addr);//32位ip转字符型ip；
	people.Format("%d",atoi(people)+1);
	GetDlgItem(IDC_STATIC2)->SetWindowText(people);

}
vResourceStream a ;
void CServerDlg::OnClose(WPARAM wParam,LPARAM lParam)
{
	int i;
	for(i=0;i<MAX1&&SocketAccept[i]!=wParam;i++){}
	if(i==MAX1) return;
	sendinfo info;
	info.type=3;//people exit
	CTime t=CTime::GetCurrentTime();
	CString strTime="[%y-%m-%d %H:%M:%S]",s;
	strTime=t.Format(strTime);
	s=uinfo[i].username;
	memcpy(info.name,s,s.GetLength()+1);
	CString m;
	m=strTime+"系统消息:\r\n  用户"+uinfo[i].username+"退出聊天室";
	m_strMsg=m_strMsg+"\r\n"+strTime+"用户"+uinfo[i].username+"(IP:"+uinfo[i].userip+")退出服务器";
	UpdateData(FALSE);
	people.Format("%d",atoi(people)-1);
	GetDlgItem(IDC_STATIC2)->SetWindowText(people);
	CEdit *edit=new CEdit;
	edit=(CEdit *)GetDlgItem(IDC_EDIT4);
	edit->LineScroll(edit->GetLineCount(),0);
	memcpy(info.msg,m,m.GetLength()+1);
	for(int j=0;j<MAX&&SocketAccept[j]!=INVALID_SOCKET;j++)
	{
		if(i!=j)
			send(SocketAccept[j],(char*)&info,sizeof(info),0);
	}
	uinfo[i].userip="";
	uinfo[i].username="";
	closesocket(SocketAccept[i]);
	SocketAccept[i]=INVALID_SOCKET;

}

void CServerDlg::OnReceive(WPARAM wParam,LPARAM lParam)
{
	int i;
	for(i=0;i<MAX1&&SocketAccept[i]!=wParam;i++){}
	if(i==MAX1) return;
	int read;
	sendinfo info;
	read=recv(SocketAccept[i],(char *)&info,sizeof(info),0);
	switch(info.type)
	{
	case 1:// to all
		int j;
		for(j=0;j<MAX&&SocketAccept[j]!=INVALID_SOCKET;j++)
		{
			if(i!=j)
			send(SocketAccept[j],(char *)&info,sizeof(info),0);
		}
		break;
	case 2://to somebody
	case 6://接受文件
	case 7:
		for(j=0;j<MAX&&uinfo[j].username!=info.name;j++){}//&&uinfo[j].userip==
		send(SocketAccept[j],(char *)&info,sizeof(info),0);
		break;
	case 0://new people in
		for(j=0;j<MAX&&uinfo[j].username!=info.name;j++)
		{
		}
		if(uinfo[j].username==info.name)
		{
			sendinfo err;
			err.type=4;//异常
			CString m;
			m="该用户昵称已经存在，请更换";
			memcpy(err.msg,m,m.GetLength()+1);
			send(SocketAccept[i],(char*)&err,sizeof(err),0);
			uinfo[i].userip="";
			closesocket(SocketAccept[i]);
			SocketAccept[i]=INVALID_SOCKET;
		}
		else
		{
			CTime t=CTime::GetCurrentTime();
			CString strTime="[%y-%m-%d %H:%M:%S]",s;
			strTime=t.Format(strTime);
			s=info.name;
			uinfo[i].username=info.name;
			s="\r\n"+strTime+"系统消息:\r\n  "+s+"进入聊天室";
			m_strMsg=m_strMsg+"\r\n"+strTime+"用户"+uinfo[i].username+"(IP:"+uinfo[i].userip+")进入服务器";
			UpdateData(FALSE);
			CEdit *edit=new CEdit;
			edit=(CEdit *)GetDlgItem(IDC_EDIT4);
			edit->LineScroll(edit->GetLineCount(),0);
			memcpy(info.msg,s,s.GetLength()+1);//MessageBox("a");
			for(j=0;j<MAX;j++)
			{
				if(SocketAccept[j]!=INVALID_SOCKET)
				send(SocketAccept[j],(char*)&info,sizeof(info),0);
			}
			for(j=0;j<MAX;j++)
			{
				if(i!=j&&uinfo[j].username!="")
				{
					sendinfo namelist;
					CString name,ms;
					namelist.type=0;
					name=uinfo[j].username;
					ms="";
					memcpy(namelist.msg,ms,ms.GetLength()+1);
					memcpy(namelist.name,name,name.GetLength()+1);
					send(SocketAccept[i],(char*)&namelist,sizeof(info),0);
				}
			}
		}
		break;
	case 5://request for sending file
		{
			CString smsg;
			smsg=info.msg;
			smsg=uinfo[i].userip+"|"+smsg;
			memcpy(info.msg,smsg,smsg.GetLength()+1);
			for(j=0;j<MAX&&uinfo[j].username!=info.name;j++){}//&&uinfo[j].userip==
			send(SocketAccept[j],(char *)&info,sizeof(info),0);
		}
		break;

	}
}
LRESULT CServerDlg::onShowTask(WPARAM wParam,LPARAM lParam)   
         //wParam接收的是图标的ID，而lParam接收的是鼠标的行为   
{  
	SetForegroundWindow();
	if(wParam!=IDR_MAINFRAME)   
		return   1;   
	switch(lParam)   
	{   
		case   WM_RBUTTONUP://右键起来时弹出快捷菜单，这里只有一个“关闭”   
		{   
				LPPOINT   lpoint=new   tagPOINT;   
                 ::GetCursorPos(lpoint);//得到鼠标位置   
                  CMenu   menu;   
                  menu.CreatePopupMenu();//声明一个弹出式菜单   
                  //增加菜单项“关闭”，点击则发送消息WM_DESTROY给主窗口（已   
                  //隐藏），将程序结束。   
                  menu.AppendMenu(MF_STRING,WM_DESTROY,"关闭");
                  //确定弹出式菜单的位置   
                  menu.TrackPopupMenu(TPM_LEFTALIGN,lpoint->x,lpoint->y,this);   
                  //资源回收   
                  HMENU   hmenu=menu.Detach();   
                  menu.DestroyMenu();   
                  delete   lpoint;   

		}   
          break;   
          case   WM_LBUTTONDBLCLK://双击左键的处理   
          {   
               this->ShowWindow(SW_SHOW);//简单的显示主窗口完事儿  
          }   
          break;   
    }   
          return   0;  
/*

if( lParam == WM_RBUTTONDOWN )

{

CMenu* menu;

menu = new CMenu();

menu->LoadMenu(IDR_MENU1);// 菜单是要提前做好的

CMenu* pPopup=menu->GetSubMenu(0);

::SetMenuDefaultItem(pPopup->m_hMenu,0,TRUE); //设置粗体字

CPoint Point;

GetCursorPos(&Point);

pPopup->TrackPopupMenu(TPM_LEFTALIGN,Point.x,Point.y,AfxGetMainWnd(),NULL);

}

return 0;*/

}  

void CServerDlg::OnButtonMin() 
{
	// TODO: Add your control notification handler code here
	m_nid.cbSize = (DWORD)sizeof(NOTIFYICONDATA); 
	m_nid.hWnd = this->m_hWnd; 
	m_nid.uID = IDR_MAINFRAME; 
	m_nid.uFlags = NIF_ICON|NIF_MESSAGE|NIF_TIP ; 
	m_nid.uCallbackMessage = WM_SHOWTASK;

	//自定义的消息名称 WM_SHOWTASK 头函数中定义为WM_USER+1
	m_nid.hIcon = LoadIcon(AfxGetInstanceHandle(),MAKEINTRESOURCE(IDR_MAINFRAME)); 
	strcpy(m_nid.szTip,"QC服务器");//当鼠标放在上面时，所显示的内容 
	Shell_NotifyIcon(NIM_ADD,&m_nid);//在托盘区添加图标 
	this->ShowWindow(SW_HIDE);
}


void CServerDlg::OnDestroy() 
{
	CDialog::OnDestroy();
	Shell_NotifyIcon(NIM_DELETE,&m_nid);//在托盘区删除图标 
	// TODO: Add your message handler code here
}



void CServerDlg::OnButtonClear() 
{
	// TODO: Add your control notification handler code here
	CClearDlg dlg;dlg.dlg=this;
	if(dlg.DoModal()==IDOK)
	{	
		for(int i=0;i<MAX&&uinfo[i].username!=dlg.name;i++)
		{
		}
		sendinfo info;
		info.type=3;
		CTime t=CTime::GetCurrentTime();
		CString strTime="[%y-%m-%d %H:%M:%S]",s;
		strTime=t.Format(strTime);
		s=uinfo[i].username;
		memcpy(info.name,s,s.GetLength()+1);
		CString m;
		m=strTime+"系统消息:\r\n  用户"+uinfo[i].username+"被踢出聊天室";
		m_strMsg=m_strMsg+"\r\n"+strTime+"用户"+uinfo[i].username+"(IP:"+uinfo[i].userip+")被管理员踢出出服务器";
		UpdateData(FALSE);
		CEdit *edit=new CEdit;
		edit=(CEdit *)GetDlgItem(IDC_EDIT4);
		edit->LineScroll(edit->GetLineCount(),0);
		memcpy(info.msg,m,m.GetLength()+1);
		for(int j=0;j<MAX&&SocketAccept[j]!=INVALID_SOCKET;j++)
		{
			send(SocketAccept[j],(char*)&info,sizeof(info),0);
		}
		uinfo[i].userip="";
		uinfo[i].username="";
		closesocket(SocketAccept[i]);
		SocketAccept[i]=INVALID_SOCKET;
		people.Format("%d",atoi(people)-1);
		GetDlgItem(IDC_STATIC2)->SetWindowText(people);
	}
}




HBRUSH CServerDlg::OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor) 
{
	HBRUSH hbr = CDialog::OnCtlColor(pDC, pWnd, nCtlColor);
	
	// TODO: Change any attributes of the DC here
	// TODO: Return a different brush if the default is not desired
	return hbr;
}

void CServerDlg::HostInfo()
{
	char wsHostName[128];                                                                             // 存储主机名
	if (gethostname(wsHostName,128)==0)                                                   //正确的情况
	{
		hostent* pHost;
		pHost = gethostbyname(wsHostName);                                                     //pHost返回的是指向主机的列表
		LPCSTR psz = inet_ntoa(*(struct in_addr *)pHost->h_addr_list[0]);//得到指向ip的psz变量
		CString list;
		list=psz;
		list="  IP地址:"+list;
		list=wsHostName+list;
		list="主机名:"+list;
		GetDlgItem(IDC_STATIC1)->SetWindowText(list);
		people='0';
		GetDlgItem(IDC_STATIC2)->SetWindowText(people);
	}
}
