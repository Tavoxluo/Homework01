#if !defined(AFX_CLEARDLG_H__3F2BC6BA_6510_438E_96AC_0DB3276C77F0__INCLUDED_)
#define AFX_CLEARDLG_H__3F2BC6BA_6510_438E_96AC_0DB3276C77F0__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// ClearDlg.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CClearDlg dialog
class CServerDlg;
class CClearDlg : public CDialog
{
// Construction
public:
	CString OnDelete();
	void RefreshData();
	CClearDlg(CWnd* pParent = NULL);   // standard constructor
CServerDlg *dlg;
CString name;
// Dialog Data
	//{{AFX_DATA(CClearDlg)
	enum { IDD = IDD_DIALOG_CLEAR };
	CListCtrl	m_ctrList;
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CClearDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CClearDlg)
	virtual BOOL OnInitDialog();
	virtual void OnOK();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_CLEARDLG_H__3F2BC6BA_6510_438E_96AC_0DB3276C77F0__INCLUDED_)
