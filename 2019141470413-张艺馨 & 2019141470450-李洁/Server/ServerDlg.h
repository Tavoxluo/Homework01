// ServerDlg.h : header file
//

#if !defined(AFX_SERVERDLG_H__8D9F6C58_9279_4463_B20B_624468A51336__INCLUDED_)
#define AFX_SERVERDLG_H__8D9F6C58_9279_4463_B20B_624468A51336__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
const int WM_SERVER_ACCEPT=WM_USER+101;
const int WM_SHOWTASK=WM_USER+1;
const int WM_SHOW=WM_USER+2;
#define MAX1 5
const int MAX=MAX1-1;
/////////////////////////////////////////////////////////////////////////////
// CServerDlg dialog

class CServerDlg : public CDialog
{
// Construction
public:
	void HostInfo();
	void OnReceive(WPARAM wParam,LPARAM lParam);
	void OnClose(WPARAM wParam,LPARAM lParam);
	void OnAccept(WPARAM wParam,LPARAM lParam);
	CServerDlg(CWnd* pParent = NULL);	// standard constructor
	SOCKET SocketAccept[MAX1];
	SOCKET ListeningSocket;
	SOCKADDR_IN serveraddr;
	struct sendinfo
	{
		int type;
		char name[20];
		char msg[400];
	};
	struct userinfo
	{
		CString username;
		CString userip;
	};
	userinfo uinfo[MAX1];
	CString people;
 /*   typedef struct _NOTIFYICONDATA { 
        DWORD cbSize;         
   //以字节为单位的这个结构的大小
        HWND hWnd;      
   //接收托盘图标通知消息的窗口句柄
        UINT uID; //应用程序定义的该图标的ID号
        UINT uFlags;          
   //设置该图标的属性
        UINT uCallbackMessage;   
   //应用程序定义的消息ID号，此消息传递给hWnd
        HICON hIcon;            
   //图标的句柄
      char szTip[64];          
   //鼠标停留在图标上显示的提示信息
    } NOTIFYICONDATA, *PNOTIFYICONDATA;*/
	NOTIFYICONDATAA m_nid;

// Dialog Data
	//{{AFX_DATA(CServerDlg)
	enum { IDD = IDD_SERVER_DIALOG };
	CString	m_strMsg;
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CServerDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	//{{AFX_MSG(CServerDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg LRESULT OnServerAccept(WPARAM wParam,LPARAM lParam);
	afx_msg LRESULT onShowTask(WPARAM wParam,LPARAM lParam); 
	afx_msg void OnButtonMin();
	afx_msg void OnDestroy();
	afx_msg void OnButtonClear();
	afx_msg HBRUSH OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor);
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
private:
	bool InitSocket();
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_SERVERDLG_H__8D9F6C58_9279_4463_B20B_624468A51336__INCLUDED_)
