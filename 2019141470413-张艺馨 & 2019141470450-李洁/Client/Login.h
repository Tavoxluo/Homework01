#if !defined(AFX_LOGIN_H__5FB81E82_703E_4553_9EE9_3A06B2BE8059__INCLUDED_)
#define AFX_LOGIN_H__5FB81E82_703E_4553_9EE9_3A06B2BE8059__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// Login.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CLogin dialog

class CLogin : public CDialog
{
// Construction
public:
	CLogin(CWnd* pParent = NULL);   // standard constructor
	CString send_ip;

// Dialog Data
	//{{AFX_DATA(CLogin)
	enum { IDD = IDD_DIALOG_LOGIN };
	CIPAddressCtrl	m_ctrIp;
	CString	m_strUser;
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CLogin)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CLogin)
	virtual BOOL OnInitDialog();
	virtual void OnOK();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_LOGIN_H__5FB81E82_703E_4553_9EE9_3A06B2BE8059__INCLUDED_)
