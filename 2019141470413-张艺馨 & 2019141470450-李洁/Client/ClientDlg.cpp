// ClientDlg.cpp : implementation file
//

#include "stdafx.h"
#include "Client.h"
#include "ClientDlg.h"
#include "login.h"
#include "mmsystem.h"
//#include ".\skins\SkinPlusPlus.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CAboutDlg dialog used for App About
	//发送数据线程 
static	UINT SendDataThread(LPVOID lpParam); 
	//接收数据线程 
static	UINT ReceiveDataThread(LPVOID lpParam); 	
 
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
// CClientDlg dialog

CClientDlg::CClientDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CClientDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CClientDlg)
	m_strRecv = _T("");
	m_strSend = _T("");
	m_strAll = FALSE;
	m_strUser = _T("");
	//}}AFX_DATA_INIT
	// Note that LoadIcon does not require a subsequent DestroyIcon in Win32
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CClientDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CClientDlg)
	DDX_Control(pDX, IDC_COMBO_USER, m_ctrUser);
	DDX_Control(pDX, IDC_PROGRESS1, m_ctrProgress);
	DDX_Control(pDX, IDC_BUTTON_END, m_ctrEnd);
	DDX_Control(pDX, IDC_CHECK_ME, m_ctrMe);
	DDX_Control(pDX, IDC_EDIT_SEND, m_ctrSend);
	DDX_Control(pDX, IDC_EDIT_RECV, m_ctrRecv);
	DDX_Control(pDX, IDC_LIST_USER, m_ctrList);
	DDX_Text(pDX, IDC_EDIT_RECV, m_strRecv);
	DDX_Text(pDX, IDC_EDIT_SEND, m_strSend);
	DDX_Check(pDX, IDC_CHECK_ALL, m_strAll);
	DDX_CBString(pDX, IDC_COMBO_USER, m_strUser);
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CClientDlg, CDialog)
	//{{AFX_MSG_MAP(CClientDlg)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDOK, OnSend)
	ON_MESSAGE(WM_SHOWTASK,onShowTask)
	ON_MESSAGE(WM_SOCKET_READ,OnReceive)
	ON_LBN_SELCHANGE(IDC_LIST_USER, OnSelchangeListUser)
	ON_BN_CLICKED(IDMIN, OnMin)
	ON_WM_TIMER()
	ON_WM_DESTROY()
	ON_BN_CLICKED(IDC_BUTTON_TANS, OnButtonTans)
	ON_BN_CLICKED(IDC_BUTTON_END, OnButtonEnd)
	ON_BN_CLICKED(IDC_BUTTON_RECV, OnButtonRecv)
	ON_BN_CLICKED(IDC_BUTTON_SHAKE, OnButtonShake)
	ON_WM_CTLCOLOR()
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CClientDlg message handlers

BOOL CClientDlg::OnInitDialog()
{
	CDialog::OnInitDialog();
//	InitializeSkin(_T("Minimized.ssk"));
	// Add "About..." menu item to system menu.
	CLogin dlg;
	if(dlg.DoModal()==IDOK)
	{
		cuser=dlg.m_strUser;
		u_long IpAddress;
		IpAddress=inet_addr(dlg.send_ip);//字符型IP转32位IP
		clientsock=socket(PF_INET,SOCK_STREAM,0);
		if(clientsock==INVALID_SOCKET)
		{
			AfxMessageBox("Create SOCKET Failed");
			WSACleanup(); 
			closesocket(clientsock);
			CClientDlg::OnCancel();
		}
		clientaddr.sin_family=AF_INET;
		clientaddr.sin_addr.s_addr=IpAddress;
		clientaddr.sin_port=htons(4009);//short 网络字节序
		int nConnect=connect(clientsock,(sockaddr *)&clientaddr,sizeof(clientaddr));
		if(nConnect==-1)
		{
			MessageBox("连接过程发生错误！\n请确保IP输入正确无误！",NULL,MB_OK);
			CDialog::OnCancel();
		}
		else
		{
			SendMsg(0,cuser,"");
		}
		WSAAsyncSelect(clientsock,m_hWnd,WM_SOCKET_READ,FD_READ|FD_CLOSE);
		this->SetWindowText(cuser);

	}
	else
	{
		CDialog::OnCancel();
	}

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
	m_strUser=_T("大家");
	m_ctrUser.AddString("大家");
	m_ctrSend.SetFocus();
	UpdateData(false);
	OnMin();
	{
		HBITMAP m_hBitmap;
		CButton* PButton;
		PButton =(CButton *)GetDlgItem(IDC_BUTTON_TANS);
		m_hBitmap =::LoadBitmap(::AfxGetInstanceHandle(),MAKEINTRESOURCE(IDB_BITMAP1));
		PButton->SetBitmap(m_hBitmap);
		PButton =(CButton *)GetDlgItem(IDC_BUTTON_SHAKE);
		m_hBitmap =::LoadBitmap(::AfxGetInstanceHandle(),MAKEINTRESOURCE(IDB_BITMAP2));
		PButton->SetBitmap(m_hBitmap);

	}
	{
		ball.Create(this);  
		ball.AddTool(GetDlgItem(IDC_BUTTON_TANS),"文件传输"); 
		ball.AddTool(GetDlgItem(IDC_CHECK_ALL),"发送信息只有你和对方知道");
		ball.AddTool(GetDlgItem(IDC_CHECK_ME),"只接收发给自己的信息");
		ball.AddTool(GetDlgItem(IDC_BUTTON_SHAKE),"发送窗口抖动");
	}
	Ishake=1;
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CClientDlg::OnSysCommand(UINT nID, LPARAM lParam)
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

void CClientDlg::OnPaint() 
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
HCURSOR CClientDlg::OnQueryDragIcon()
{
	return (HCURSOR) m_hIcon;
}

void CClientDlg::OnSend() 
{
	// TODO: Add your control notification handler code here
	UpdateData(true);
	if(m_strSend=="")
	{
		MessageBox("消息不能为空");
		return;
	}
	if(m_strUser==cuser)
	{
		MessageBox("不能给自己发消息");
		return;
	}
	if(m_strSend=="\/shake")
	{
		OnButtonShake();
	}
	else
	{
		CTime t=CTime::GetCurrentTime();
		CString strTime="(%m-%d %H:%M:%S)";
		strTime=t.Format(strTime);
		int type;
		if(m_strAll==1&&m_strUser!="大家")
		{
			type=2;
			m_strRecv=m_strRecv+"\r\n"+strTime+"你对"+m_strUser+"说:"+m_strSend;
			m_strSend=strTime+cuser+"对你说:"+m_strSend;
		}
		else if(m_strUser=="大家")
		{
			type=1;
			m_strRecv=m_strRecv+"\r\n"+strTime+"你对大家说:"+m_strSend;
			m_strSend=strTime+cuser+"对大家说:"+m_strSend;
		}
		else if(m_strUser!="大家")
		{
			type=1;
			m_strRecv=m_strRecv+"\r\n"+strTime+"你对"+m_strUser+"说:"+m_strSend;
			m_strSend=strTime+cuser+"对"+m_strUser+"说:"+m_strSend;
		}
		if(m_strSend.GetLength()>400)
		{
			MessageBox("字数超出");
			return;
		}
		SendMsg(type,m_strUser,m_strSend);
		GetDlgItem(IDC_EDIT_RECV)->SetWindowText(m_strRecv);
		CEdit *p=new CEdit;
		p=(CEdit *)GetDlgItem(IDC_EDIT_RECV);
		p->LineScroll(p->GetLineCount(),0);
	}
	m_strSend=_T("");
	m_ctrSend.SetFocus();
	GetDlgItem(IDC_EDIT_SEND)->SetWindowText(m_strSend);
}
LRESULT CClientDlg::OnReceive(WPARAM wParam,LPARAM lParam)
{
	sendinfo info;
	int lEvent=WSAGETSELECTEVENT(lParam);
	switch(lEvent)
	{
	case FD_READ:
		{
			int BRead=recv(clientsock, (char*)&info,sizeof(info), 0);
			if(BRead==0)
			{	
				MessageBox("网络中断");
				return 0;
			}
			if (BRead == SOCKET_ERROR)
			{
				MessageBox("接收到一个错误信息. ");
				return 0;
			}
			switch(info.type)
			{
			case 0://new people in
				{
					CString m;
					m=info.msg;
					if(m!="")
					{
						m_strRecv=m_strRecv+m;
						GetDlgItem(IDC_EDIT_RECV)->SetWindowText(m_strRecv);
					}
					m_ctrUser.AddString(info.name);
					m_ctrList.AddString(info.name);
				}
				break;
			case 1://to all or not private
				m_strMe=m_ctrMe.GetCheck();
				if(m_strMe==1&&cuser!=info.name)
					return 0;
				{
					CString shake;
					shake=info.msg;
					if(shake=="\\shake")
					{
						Shaking();
						return 0;
					}
				}
				m_strRecv=m_strRecv+"\r\n\r\n"+info.msg;
				GetDlgItem(IDC_EDIT_RECV)->SetWindowText(m_strRecv);
				break;
			case 2://to me only 私聊
				{
					CString shake;
					shake=info.msg;
					if(shake=="\\shake")
					{	
						Shaking();
						return 0;
					}
				}
				m_strRecv=m_strRecv+"\r\n\r\n"+info.msg;
				GetDlgItem(IDC_EDIT_RECV)->SetWindowText(m_strRecv);
				break;
			case 3:// people out
				m_strRecv=m_strRecv+"\r\n\r\n"+info.msg;
				UpdateData(false);
				m_ctrUser.DeleteString(m_ctrUser.FindString(1,info.name));
				m_ctrList.DeleteString(m_ctrList.FindString(1,info.name));
				break;
			case 4://异常事件
				{
				CString msg;
				msg=info.msg;
				MessageBox(msg);
				break;
				}
			case 5://文件传输请求
				{
					CString sender1;
					int k=0,i=0;
					char *p;
					for(int j=0;j<4;j++,k++)
					{
						i=0;
						p=&info.msg[k];
						while(info.msg[k]!='|')
						{
							k++;i++;
						}
						info.msg[k]='\0';
						if(j==0)
							f_ip=p;
						else if(j==1)
							sender1=p;
						else if(j==2)
							m_strFileName=p;
						else 
							m_dwFileSize=atoi(p);
					}
					if(IsTrans==1)
					{
						SendMsg(7,sender1,"对方正在传输文件，请稍候!");
						return 0;
					}
					sender=sender1;
					CString filesize;
					filesize=KindChange(m_dwFileSize);
					filesize="("+filesize+")";
					m_strRecv=m_strRecv+"\r\n\r\n  "+sender+"请求给你发送文件  "+m_strFileName+filesize;
					GetDlgItem(IDC_EDIT_RECV)->SetWindowText(m_strRecv);
					GetDlgItem(IDC_PROGRESS1)->ShowWindow(SW_SHOW);
					m_ctrEnd.ShowWindow(SW_SHOW);
					m_ctrEnd.SetWindowText("拒绝");
					GetDlgItem(IDC_STATIC_RECV)->ShowWindow(SW_SHOW);
					GetDlgItem(IDC_STATIC_RECV)->SetWindowText("接受文件：");
					GetDlgItem(IDC_STATIC_FILENAME)->ShowWindow(SW_SHOW);
					GetDlgItem(IDC_STATIC_FILENAME)->SetWindowText(m_strFileName);
					GetDlgItem(IDC_STATIC_FILESIZE)->ShowWindow(SW_SHOW);
					GetDlgItem(IDC_STATIC_FILESIZE)->SetWindowText(filesize);
					GetDlgItem(IDC_STATIC2)->ShowWindow(SW_SHOW);
					GetDlgItem(IDC_STATIC2)->SetWindowText("0%");
					GetDlgItem(IDC_BUTTON_RECV)->ShowWindow(SW_SHOW);
					GetDlgItem(IDC_BUTTON_TANS)->ShowWindow(SW_HIDE);
					GetDlgItem(IDC_STATIC_SPEED)->ShowWindow(SW_SHOW);
					GetDlgItem(IDC_STATIC_SPEED)->SetWindowText("速度: 0");
					if(this->IsWindowVisible()!=1)
					{
						::SetForegroundWindow(m_hWnd);
						::ShowWindow(m_hWnd,SW_SHOW);
					}
					IsTrans=1;
				}
				break;
			case 6://开始发送数据线程 
				m_strRecv=m_strRecv+"\r\n"+info.msg;
				GetDlgItem(IDC_EDIT_RECV)->SetWindowText(m_strRecv);
				AfxBeginThread(SendDataThread,this,THREAD_PRIORITY_NORMAL);
				break;
			case 7://文件传输中中止了传输,对方拒绝文件
				IsEnd=1;	IsTrans=0;
				m_strRecv=m_strRecv+"\r\n"+info.msg;
				GetDlgItem(IDC_EDIT_RECV)->SetWindowText(m_strRecv);
				Hide();
				break;
			}
			break;
		}
	case FD_CLOSE:
		{
			m_strRecv=m_strRecv+"\r\n"+"服务器连接已断开!  请重新登陆";
			GetDlgItem(IDC_EDIT_RECV)->SetWindowText(m_strRecv);
			break;
		}
	}
	CEdit *p=new CEdit;
	p=(CEdit *)GetDlgItem(IDC_EDIT_RECV);
	p->LineScroll(p->GetLineCount(),0);
	PlaySound(MAKEINTRESOURCE(IDR_WAVE1),AfxGetResourceHandle(),SND_ASYNC|SND_RESOURCE|SND_NODEFAULT);// 
/*  // 1．获得包含资源的模块句柄：
	HMODULE hmod=AfxGetResourceHandle(); 
//　　2．检索资源块信息：
　　HRSRC hSndResource=FindResource(hmod,MAKEINTRESOURCE(IDR_WAVE1),_T("WAVE"));
//　　3. 装载资源数据并加锁：
　　HGLOBAL hGlobalMem=LoadResource(hmod,hSndResource);
LPCTSTR lpMemSound=(LPCSTR)LockResource(hGlobalMem);
　//　4．播放声音文件：
　　sndPlaySound(lpMemSound,SND_MEMORY);
//　　5．释放资源句柄：
　　FreeResource(hGlobalMem);*/
	HWND Hwnd;
	Hwnd=::GetForegroundWindow();
	if(this->IsWindowVisible()!=1)
		SetTimer(1,300,0);
	else if(Hwnd!=m_hWnd)
		this->FlashWindow(1);
	return 0;
}

void CClientDlg::OnSelchangeListUser() 
{
	// TODO: Add your control notification handler code here
	int i=m_ctrList.GetCurSel();
	m_ctrList.GetText(i,m_strUser);
//	GetDlgItem(IDC_COMBO_USER)->SetWindowText(m_strUser);
	m_ctrUser.SetCurSel(m_ctrUser.FindString(i,m_strUser));
//	m_ctrUser.SelectString(0,m_strUser);
	m_ctrSend.SetFocus();
}

void CClientDlg::OnMin() 
{
	// TODO: Add your control notification handler code here
	m_nid.cbSize = (DWORD)sizeof(NOTIFYICONDATA); 
	m_nid.hWnd = this->m_hWnd; 
	m_nid.uID =IDR_MAINFRAME; 
	m_nid.uFlags = NIF_ICON|NIF_MESSAGE|NIF_TIP ; 
	m_nid.uCallbackMessage = WM_SHOWTASK;

	//自定义的消息名称 WM_SHOWTASK 头函数中定义为WM_USER+1
	m_nid.hIcon = LoadIcon(AfxGetInstanceHandle(),MAKEINTRESOURCE(IDR_MAINFRAME)); 
	CString title;
	title="QC:"+cuser;
	strcpy(m_nid.szTip,title);//当鼠标放在上面时，所显示的内容 
	Shell_NotifyIcon(NIM_ADD,&m_nid);//在托盘区添加图标 
	this->ShowWindow(SW_HIDE);
	m_nid.hIcon=AfxGetApp()->LoadIcon(IDR_MAINFRAME);
	Shell_NotifyIcon(NIM_MODIFY, &m_nid);
	KillTimer(1);
}
LRESULT CClientDlg::onShowTask(WPARAM wParam,LPARAM lParam)   
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
			   KillTimer(1);		
			   m_nid.hIcon=AfxGetApp()->LoadIcon(IDR_MAINFRAME);
				Shell_NotifyIcon(NIM_MODIFY, &m_nid);

          }   
          break;   
    }   
          return   0;  
}
void CClientDlg::OnTimer(UINT nIDEvent) 
{
	// TODO: Add your message handler code here and/or call default
	switch(nIDEvent)
	{
	case 1:
		{
			if(m_nid.hIcon == AfxGetApp()->LoadIcon(IDR_MAINFRAME))
				m_nid.hIcon = AfxGetApp()->LoadIcon(IDI_ICON2);
			else m_nid.hIcon =AfxGetApp()->LoadIcon(IDR_MAINFRAME);
			Shell_NotifyIcon(NIM_MODIFY, &m_nid);
		}
		break;
	case 2:
		{
			CString filesize;
			filesize=KindChange(ByteTotal-pb);
			pb=ByteTotal;
			filesize="速度:"+filesize+"/s";
			GetDlgItem(IDC_STATIC_SPEED)->SetWindowText(filesize);
		}
		break;
	case 3:
		{
			Ishake=1;
			KillTimer(3);
		}
	}

	CDialog::OnTimer(nIDEvent);
}

void CClientDlg::OnDestroy() 
{
	CDialog::OnDestroy();
	// TODO: Add your message handler code here
	if(IsTrans==1)
		SendMsg(7,sender,"\r\n  对方已退出!");
	Shell_NotifyIcon(NIM_DELETE,&m_nid);//在托盘区删除图标 
}

BOOL CClientDlg::PreTranslateMessage(MSG* pMsg) 
{
	// TODO: Add your specialized code here and/or call the base class
//	switch(pMsg->message) 
	{ 
//		case WM_LBUTTONDOWN: 
//		case WM_LBUTTONUP: 
//		case WM_MOUSEMOVE: 
		ball.RelayEvent(pMsg); 
	} 
	return CDialog::PreTranslateMessage(pMsg);
}

void CClientDlg::OnButtonTans() 
{
	// TODO: Add your control notification handler code here
	UpdateData(true);
	if(m_strUser==cuser)
	{
		MessageBox("不能给自己发文件");
		return;
	}
	if(m_strUser=="大家")
	{
		MessageBox("不能给所以人发文件");
		return;
	}
   //打开文件对话框 
	CFileDialog dlg(TRUE,NULL,NULL,OFN_HIDEREADONLY|OFN_OVERWRITEPROMPT,  "所有文件 (*.*)|*.*||"); 
	if(dlg.DoModal()==IDOK) 
	{ 
		m_strFilePath=dlg.GetPathName(); 
		m_strFileName=dlg.GetFileName();
		CFile file(m_strFilePath, CFile::modeRead);
		//获取文件大小
		m_dwFileSize=file.GetLength();
		//关闭文件
		file.Close();
		CString filesize;
		filesize=KindChange(m_dwFileSize);
		GetDlgItem(IDC_PROGRESS1)->ShowWindow(SW_SHOW);
		m_ctrEnd.ShowWindow(SW_SHOW);
		m_ctrEnd.SetWindowText("取消");
		GetDlgItem(IDC_STATIC_RECV)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_STATIC_RECV)->SetWindowText("发送文件：");
		GetDlgItem(IDC_STATIC_FILENAME)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_STATIC_FILENAME)->SetWindowText(m_strFileName);
		GetDlgItem(IDC_STATIC_FILESIZE)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_STATIC_FILESIZE)->SetWindowText(filesize);
		GetDlgItem(IDC_STATIC2)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_STATIC2)->SetWindowText("0%");
		GetDlgItem(IDC_BUTTON_TANS)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_STATIC_SPEED)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_STATIC_SPEED)->SetWindowText("速度: 0");
		CString message;filesize.Format("%d",m_dwFileSize);
		message=cuser+"|"+m_strFileName+"|"+filesize+"|";
		SendMsg(5,m_strUser,message);
		Sendto=m_strUser;
		IsTrans=1;
	} 
}
	//发送数据线程 
UINT SendDataThread(LPVOID lpParam)
{
	CClientDlg *pDlg=(CClientDlg *)lpParam; 
	CFile file;
	if(!file.Open(pDlg->m_strFileName,CFile::modeRead)) 
	{ 
		AfxMessageBox("打开文件出错！"); 
		pDlg->GetDlgItem(IDC_BUTTON_TANS)->ShowWindow(SW_SHOW);
		pDlg->Hide();
		return 0; 
	} 	
	CSocket sockTemp;
	sockTemp.Create(2000);
	sockTemp.Listen(1);
	CSocket sockSend;
	sockTemp.Accept(sockSend);
	AfxMessageBox("成功");
	pDlg->IsEnd=0;
	pDlg->m_ctrProgress.SetRange(0,100);
	int BufSize=SENDDATE;
	int ByteNum=0,nLen=0,pos=0,pos1=0;
	pDlg->ByteTotal=0;pDlg->pb=0;
	CString str,str1;
	LPBYTE pBuf = new BYTE[BufSize]; 
	file.Seek(0, CFile::begin);
	pDlg->SendMsg(2,pDlg->Sendto,"  开始接收数据.......");
	pDlg->SetTimer(2,500,0);
	while(1)
	{
		if(pDlg->IsEnd==1)
			break;
		//一次读取BufSize大小的文件内容
		nLen=file.Read(pBuf,BufSize);

		if(nLen==0)
			break;
		ByteNum=sockSend.Send(pBuf, nLen);
		if(ByteNum==SOCKET_ERROR)
		{ 
			AfxMessageBox("发送失败！"); 
			break;
		}
		pDlg->ByteTotal+=ByteNum;
		pos=int(pDlg->ByteTotal*100.0/pDlg->m_dwFileSize);
		if(pos1!=pos)
		{
			pos1=pos;
			pDlg->m_ctrProgress.SetPos(pos);
		}
		str.Format("%d",pos);
		if(str1!=str)
		{
			str1=str;
			str=str+"%";
			pDlg->GetDlgItem(IDC_STATIC2)->SetWindowText(str); 
		}
	}
	pDlg->KillTimer(2);
	sockSend.Close();
//	Sleep(200);
	file.Close();
	pDlg->IsEnd=0;
	pDlg->IsTrans=0;
	pDlg->Hide();
	pDlg->m_ctrProgress.SetPos(0);
	if(pDlg->ByteTotal==pDlg->m_dwFileSize)
		pDlg->SendMsg(2,pDlg->Sendto,"  文件接收完成!");
	return 0;
}
	//接收数据线程 
UINT ReceiveDataThread(LPVOID lpParam)	
{
	CClientDlg *pDlg=(CClientDlg *)lpParam; 
	//保存文件对话框 
	CFileDialog dlg(FALSE,NULL,NULL,OFN_HIDEREADONLY|OFN_OVERWRITEPROMPT,"所有文件 (*.*)|*.*||"); 
	strcpy(dlg.m_ofn.lpstrFile, pDlg->m_strFileName.GetBuffer(pDlg->m_strFileName.GetLength()));
	while(dlg.DoModal()!=IDOK) 
	{ 
		return 0;
	}     
	pDlg->GetDlgItem(IDC_BUTTON_END)->SetWindowText("中止");
	CSocket sockRecv;
	if(sockRecv.Create(2001)==SOCKET_ERROR)
		sockRecv.Create();
	pDlg->GetDlgItem(IDC_STATIC_FILENAME)->SetWindowText(dlg.GetFileName());
	pDlg->GetDlgItem(IDC_BUTTON_RECV)->ShowWindow(SW_HIDE);//接收按钮 
	pDlg->m_ctrProgress.SetRange(0,100);
	pDlg->SendMsg(6,pDlg->sender,"\r\n  对方已接受请求，建立连接.......");
	while(sockRecv.Connect(pDlg->f_ip,2000)==0)
	{
		Sleep(50); 
	} 
	CFile file; 
	if(!file.Open(dlg.GetPathName(),CFile::modeCreate|CFile::modeWrite))
	{ 
		AfxMessageBox("打开文件出错！"); 
		return 0; 
	} 	
	pDlg->IsEnd=0;
	int BufSize=SENDDATE;
	int ByteNum=0,pos,pos1=0;
	pDlg->ByteTotal=pDlg->pb=0;
	CString str,str1;
	LPBYTE pBuf = new BYTE[BufSize]; 
	pDlg->SendMsg(2,pDlg->sender,"  开始传输数据.......");
	pDlg->SetTimer(2,500,0);
	while(1)
	{
		if(pDlg->IsEnd==1)
			break;
		//一次读取BufSize大小的文件内容
		ByteNum=sockRecv.Receive(pBuf,BufSize);
		if(ByteNum==SOCKET_ERROR) 
		{ 
			AfxMessageBox("接收错误！"); 
			break;
		}
		if(ByteNum==0)
			break;
		file.Write(pBuf,ByteNum);
		pDlg->ByteTotal+=ByteNum;
		pos=int(pDlg->ByteTotal*100.0/pDlg->m_dwFileSize);
		if(pos1!=pos)
		{
			pos1=pos;
			pDlg->m_ctrProgress.SetPos(pos);
		}
		str.Format("%d",pos);
		if(str1!=str)
		{
			str1=str;
			str=str+"%";
			pDlg->GetDlgItem(IDC_STATIC2)->SetWindowText(str); 
		}
	}
	pDlg->KillTimer(2);
	sockRecv.Close();	
	pDlg->IsEnd=0;
	pDlg->IsTrans=0;
	file.Close();
	pDlg->Hide();
	pDlg->m_ctrProgress.SetPos(0);
	if(pDlg->ByteTotal==pDlg->m_dwFileSize)
		pDlg->SendMsg(2,pDlg->sender,"  文件发送完成!");
	return 0;
}

void CClientDlg::OnButtonEnd() 
{
	// TODO: Add your control notification handler code here
	CString kind;
	IsEnd=1;	IsTrans=0;
	GetDlgItem(IDC_BUTTON_END)->GetWindowText(kind);
	if(kind=="拒绝")
	{
		m_strRecv=m_strRecv+"\r\n\r\n"+"  您拒绝了对方的请求！文件传输被取消";
		SendMsg(7,sender,"\r\n  对方拒绝了您的请求!");
		Hide();
	}
	else if(kind=="取消")
	{
		m_strRecv=m_strRecv+"\r\n\r\n"+"  您取消了文件传输";
		SendMsg(7,Sendto,"\r\n  对方取消了文件传输!");
		Hide();
	}
	else if(kind=="中止")
	{
		m_strRecv=m_strRecv+"\r\n\r\n"+"  您中止了文件传输";
		SendMsg(7,sender,"\r\n  对方中止了文件传输!");
	}
	GetDlgItem(IDC_EDIT_RECV)->SetWindowText(m_strRecv);
	CEdit *p=new CEdit;
	p=(CEdit *)GetDlgItem(IDC_EDIT_RECV);
	p->LineScroll(p->GetLineCount(),0);
}

void CClientDlg::OnButtonRecv() 
{
	// TODO: Add your control notification handler code here
	AfxBeginThread(ReceiveDataThread,this,THREAD_PRIORITY_NORMAL); 
}

void CClientDlg::Hide()
{
		GetDlgItem(IDC_PROGRESS1)->ShowWindow(SW_HIDE);
		m_ctrEnd.ShowWindow(SW_HIDE);
		GetDlgItem(IDC_STATIC_RECV)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_STATIC_FILENAME)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_STATIC_FILESIZE)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_STATIC2)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON_TANS)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_BUTTON_RECV)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_STATIC_SPEED)->ShowWindow(SW_HIDE);
}

void CClientDlg::SendMsg(int type, CString name, CString msg)
{
	sendinfo info;
	info.type=type;
	memcpy(info.name,name,name.GetLength()+1);
	memcpy(info.msg,msg,msg.GetLength()+1);
	int charsend=send(clientsock,(char*)&info,sizeof(info),0);
	if(charsend==SOCKET_ERROR)
	{
		MessageBox("发送过程中发生一个错误！",NULL,MB_OK);
		return;
	}
}

CString CClientDlg::KindChange(DWORD dwFileSize)
{
	float size;
	CString filesize;
	if(dwFileSize<1024)
	{
		filesize.Format("%d字节",dwFileSize);
	}
	else if(dwFileSize<(1024*1024))
	{
		size=dwFileSize*1.0/1024;
		filesize.Format("%.1fKB",size);
	}
	else
	{
		size=dwFileSize*1.0/(1024*1024);
		filesize.Format("%.1fMB",size);
	}
	return filesize;
}

void CClientDlg::OnButtonShake() 
{
	// TODO: Add your control notification handler code here
	if(Ishake==0)
		return;
	UpdateData(true);
	int type;
	if(m_strUser!="大家")
	{
		type=2;
		m_strSend=" "+cuser+"对你发送了窗口抖动";
	}
	else if(m_strUser=="大家")
	{
		type=1;
		m_strSend="  "+cuser+"对大家发送了窗口抖动";
	}
	SendMsg(type,m_strUser,"\\shake");
	SendMsg(type,m_strUser,m_strSend);
	Shaking();
	m_strSend=_T("");
	m_ctrSend.SetFocus();
	GetDlgItem(IDC_EDIT_RECV)->SetWindowText(m_strRecv);
	CEdit *p=new CEdit;
	p=(CEdit *)GetDlgItem(IDC_EDIT_RECV);
	p->LineScroll(p->GetLineCount(),0);
	Ishake=0;
	SetTimer(3,10000,0);
}

void CClientDlg::Shaking()
{
	int ty=3;
		CRect   m_rect; 
		this->ShowWindow(SW_SHOW);
//		HWND Hwnd;
//		Hwnd=::GetForegroundWindow();
		::SetForegroundWindow(m_hWnd);
		::GetWindowRect(m_hWnd,&m_rect);  
		int recordy=m_rect.left;
		int recordx=m_rect.top;
		for(int i=0;i<3;i++)
		{
			m_rect.left=recordy;
			m_rect.top=recordx;
			m_rect.top = m_rect.top + ty;  
			m_rect.left = m_rect.left - ty;
			::SetWindowPos(m_hWnd,NULL,m_rect.left,m_rect.top,0,0,SWP_NOSIZE);Sleep(20);
			m_rect.top = m_rect.top -ty;
			::SetWindowPos( m_hWnd,NULL,m_rect.left,m_rect.top,0,0,SWP_NOSIZE);Sleep(20);
			m_rect.top = m_rect.top -ty;
			::SetWindowPos( m_hWnd,NULL,m_rect.left,m_rect.top,0,0,SWP_NOSIZE);Sleep(20);
			m_rect.left=m_rect.left+ty;
			::SetWindowPos( m_hWnd,NULL,m_rect.left,m_rect.top,0,0,SWP_NOSIZE);Sleep(20);
			m_rect.left=m_rect.left+ty;
			::SetWindowPos( m_hWnd,NULL,m_rect.left,m_rect.top,0,0,SWP_NOSIZE);Sleep(20);
			m_rect.top = m_rect.top + ty;  
			::SetWindowPos( m_hWnd,NULL,m_rect.left,m_rect.top,0,0,SWP_NOSIZE);Sleep(20);
			m_rect.top=m_rect.top+ty;
			::SetWindowPos( m_hWnd,NULL,m_rect.left,m_rect.top,0,0,SWP_NOSIZE);Sleep(20);
			m_rect.top=m_rect.top+ty;
			::SetWindowPos( m_hWnd,NULL,m_rect.left,m_rect.top,0,0,SWP_NOSIZE);Sleep(20);
			::SetWindowPos( m_hWnd,NULL,recordy,recordx,0,0,SWP_NOSIZE);Sleep(3);
		}
}

HBRUSH CClientDlg::OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor) 
{
//	HBRUSH hbr = CDialog::OnCtlColor(pDC, pWnd, nCtlColor);
	HBRUSH 	hbr=CreateSolidBrush(RGB(250,250,250));
	// TODO: Change any attributes of the DC here
	
	// TODO: Return a different brush if the default is not desired
	return hbr;
}
//DEL //	HBRUSH hbr = CDialog::OnCtlColor(pDC, pWnd, nCtlColor);
//DEL  CTLCOLOR_BTN（按钮控件）
//DEL  CTLCOLOR_DLG（对话框）
//DEL  CTLCOLOR_EDIT（编辑控件）
//DEL  CTLCOLOR_LISTBOX（列表框）
//DEL  CTLCOLOR_MSGBOX（消息框）
//DEL  CTLCOLOR_SCROLLBAR（滚动条）
//DEL  CTLCOLOR_STATIC（静态框）
//DEL /*	if(nCtlColor==CTLCOLOR_EDIT)
//DEL 	{	
//DEL //			pDC->SetBkMode(TRANSPARENT);
//DEL //			pDC->SetBkColor(RGB(255,0,255));
//DEL //			此处设置字体的颜色
//DEL 			pDC->SetTextColor(RGB(0,0,180));
//DEL 	//		return m_hbr1;


