// ClearDlg.cpp : implementation file
//

#include "stdafx.h"
#include "Server.h"
#include "ClearDlg.h"
#include "ServerDlg.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CClearDlg dialog


CClearDlg::CClearDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CClearDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CClearDlg)
		// NOTE: the ClassWizard will add member initialization here
	//}}AFX_DATA_INIT
}


void CClearDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CClearDlg)
	DDX_Control(pDX, IDC_LIST1, m_ctrList);
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CClearDlg, CDialog)
	//{{AFX_MSG_MAP(CClearDlg)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CClearDlg message handlers

BOOL CClearDlg::OnInitDialog() 
{
	CDialog::OnInitDialog();
	
	// TODO: Add extra initialization here
	m_ctrList.InsertColumn(0,"用户名");
	m_ctrList.SetColumnWidth(0,80);
	m_ctrList.InsertColumn(1,"用户IP");
	m_ctrList.SetColumnWidth(1,125);
	m_ctrList.SetExtendedStyle(LVS_EX_FULLROWSELECT|LVS_EX_GRIDLINES);
	RefreshData();
	return TRUE;  // return TRUE unless you set the focus to a control
	              // EXCEPTION: OCX Property Pages should return FALSE
}

void CClearDlg::RefreshData()
{
	for(int i=0;i<MAX;i++)
	{   if(dlg->uinfo[i].userip!="")
		{
			m_ctrList.InsertItem(i,dlg->uinfo[i].username);
			m_ctrList.SetItemText(i,1,dlg->uinfo[i].userip);
		}
	}
	m_ctrList.SetRedraw(true);

}

CString CClearDlg::OnDelete()
{
	int i=m_ctrList.GetSelectionMark();
	name=m_ctrList.GetItemText(i,0);
	return name;
}

void CClearDlg::OnOK() 
{	
	// TODO: Add extra validation here
	int i=m_ctrList.GetSelectionMark();
	if(i<0)
	{
		MessageBox("请选择一个用户");
		return;
	}
	if(AfxMessageBox("确实将该用户踢出聊天室吗?",MB_YESNO)==IDNO)
		return;
	OnDelete();
	CDialog::OnOK();
}
