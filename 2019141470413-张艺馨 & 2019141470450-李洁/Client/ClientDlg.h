// ClientDlg.h : header file
//

#if !defined(AFX_CLIENTDLG_H__59CB99E6_BED9_43E7_846B_3B73BD74F62F__INCLUDED_)
#define AFX_CLIENTDLG_H__59CB99E6_BED9_43E7_846B_3B73BD74F62F__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
#define WM_SOCKET_READ WM_USER+101
const int WM_SHOWTASK=WM_USER+1;
const int SENDDATE=(17520*3);
/////////////////////////////////////////////////////////////////////////////
// CClientDlg dialog

class CClientDlg : public CDialog
{
// Construction
public:
	void Shaking();
	CString KindChange(DWORD dwFileSize);
	void SendMsg(int type,CString name,CString msg);
	void Hide();
	CClientDlg(CWnd* pParent = NULL);	// standard constructor
	SOCKET clientsock;
	SOCKADDR_IN clientaddr;
	struct sendinfo
	{
		int type;
		char name[20];
		char msg[400];
	};
	CString cuser;
	NOTIFYICONDATAA m_nid;
	int m_strMe;
	CToolTipCtrl ball;
	HBRUSH m_hbr1,m_hbr2;
	BOOL IsEnd,Ishake,IsTrans;
	CString m_strFilePath,m_strFileName,sender,f_ip,Sendto;
	DWORD m_dwFileSize,ByteTotal,pb;
// Dialog Data
	//{{AFX_DATA(CClientDlg)
	enum { IDD = IDD_CLIENT_DIALOG };
	CComboBox	m_ctrUser;
	CProgressCtrl	m_ctrProgress;
	CButton	m_ctrEnd;
	CButton	m_ctrMe;
	CEdit	m_ctrSend;
	CEdit	m_ctrRecv;
	CListBox	m_ctrList;
	CString	m_strRecv;
	CString	m_strSend;
	BOOL	m_strAll;
	CString	m_strUser;
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CClientDlg)
	public:
	virtual BOOL PreTranslateMessage(MSG* pMsg);
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	//{{AFX_MSG(CClientDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg void OnSend();
	afx_msg LRESULT onShowTask(WPARAM wParam,LPARAM lParam); 
	afx_msg LRESULT OnReceive(WPARAM wParam,LPARAM lParam);
	afx_msg void OnSelchangeListUser();
	afx_msg void OnMin();
	afx_msg void OnTimer(UINT nIDEvent);
	afx_msg void OnDestroy();
	afx_msg void OnButtonTans();
	afx_msg void OnButtonEnd();
	afx_msg void OnButtonRecv();
	afx_msg void OnButtonShake();
	afx_msg HBRUSH OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor);
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_CLIENTDLG_H__59CB99E6_BED9_43E7_846B_3B73BD74F62F__INCLUDED_)
