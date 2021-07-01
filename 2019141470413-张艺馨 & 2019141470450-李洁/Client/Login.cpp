// Login.cpp : implementation file
//

#include "stdafx.h"
#include "Client.h"
#include "Login.h"
#include "ado.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CLogin dialog


CLogin::CLogin(CWnd* pParent /*=NULL*/)
	: CDialog(CLogin::IDD, pParent)
{
	//{{AFX_DATA_INIT(CLogin)
	m_strUser = _T("");
	//}}AFX_DATA_INIT
}


void CLogin::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CLogin)
	DDX_Control(pDX, IDC_IPADDRESS1, m_ctrIp);
	DDX_Text(pDX, IDC_EDIT_USER, m_strUser);
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CLogin, CDialog)
	//{{AFX_MSG_MAP(CLogin)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CLogin message handlers

BOOL CLogin::OnInitDialog() 
{
	CDialog::OnInitDialog();
	ado rst;
	CString sql;
	sql.Format("select * from tb_user");
	rst.rstOpen(sql);
	m_strUser=rst.GetFieldValue("NAME");
	// TODO: Add extra initialization here
	u_long   uip   =   inet_addr(rst.GetFieldValue("IP"));
	m_ctrIp.SetAddress(htonl(uip));
	UpdateData(false);
	rst.close();
	return TRUE;  // return TRUE unless you set the focus to a control
	              // EXCEPTION: OCX Property Pages should return FALSE
}

void CLogin::OnOK() 
{
	// TODO: Add extra validation here
	UpdateData(1);
	m_strUser.TrimLeft();
	m_strUser.TrimRight();
	if(m_strUser.IsEmpty())
	{
		MessageBox("«ÎÃÓ–¥Í«≥∆£°",NULL,MB_OK);
		return ;
	}
	BYTE f1,f2,f3,f4;
	m_ctrIp.GetAddress(f1,f2,f3,f4);
	send_ip.Format("%d.%d.%d.%d",f1,f2,f3,f4);
	ado rst;
	CString sql;
	sql.Format("select * from tb_user");
	rst.rstOpen(sql);
	sql.Format("update tb_user set ip='%s',name='%s'where name='%s'",send_ip,m_strUser,rst.GetFieldValue("NAME"));
	rst.ExecuteSQL(sql);
	rst.close();

	CDialog::OnOK();
}
