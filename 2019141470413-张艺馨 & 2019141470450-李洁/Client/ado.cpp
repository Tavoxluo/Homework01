#include "stdafx.h"
#include "ado.h"
ado::ado()
{
	::CoInitialize(NULL);
	try
	{
	m_pConnection.CreateInstance(__uuidof(Connection));
//	_bstr_t strConnect="Provider=SQLOLEDB;SERVER=PC-3128999;Database=Honglin;UID=sa;PWD=;";
	//_bstr_t strConnect="driver={SQL server};server=127.0.0.1;DATABASE=db_Client;uid=sa;pwd=";
	_bstr_t strConnect="Provider=Microsoft.Jet.OLEDB.4.0;Data Source=db.db";
	//ntServer
	m_pConnection->Open(strConnect,"","",0);
	}
	catch(_com_error e)
	{
	AfxMessageBox(e.Description());
	
	}
}
ado::~ado()
{
	//m_pRecordset->Close();
///	m_pConnection->Close();
//	m_pRecordset=NULL;
//	m_pConnection=NULL;
//	::CoUninitialize();

}
bool ado::Open(CString srecordset, UINT adCmd)
{
	
	try{
	 m_pRecordset=m_pConnection->Execute((_bstr_t)srecordset,NULL,adCmd);
	}
	catch(_com_error&e)
	{
		this->GetErrors(e);
		return false;
	}
	return true;
}
int ado::GetRecordCount()
{
	int nCount=0;
	try{
	
		m_pRecordset->MoveFirst();
	}
	catch(...)
	{
		return 0;
	}
	if(m_pRecordset->adoEOF)
		return 0;
	while (!m_pRecordset->adoEOF)
	{
		m_pRecordset->MoveNext();
		nCount=nCount+1;	
	}
	m_pRecordset->MoveFirst();
	return nCount;
}
void ado::GetErrors(_com_error eErrors)
{
	/*CString string;
	CFile file;
	
	file.Open("Error.Rxe",CFile::modeWrite|CFile::modeNoTruncate);
	ErrorsPtr pErrors=cnn->GetErrors();
	if (pErrors->GetCount()==0)	
	{
		string=(char*)(_bstr_t)eErrors.ErrorMessage();
		file.Write(string+"\r\n",string.GetLength()+1);
		//::AfxMessageBox(string);
	}
	else
	{
		for (int i=0;i<pErrors->GetCount();i++)
		{
			_bstr_t desc=pErrors->GetItem((long)i)->GetDescription();
			string=(char*)desc;
			file.Write(string+"\r\n",string.GetLength()+1);
			//::AfxMessageBox(string);
		}
	}
	file.Close();
	*/
	ErrorsPtr pErrors=m_pConnection->GetErrors();
	if (pErrors->GetCount()==0)	
		MessageBox(NULL,eErrors.ErrorMessage(),"´í  Îó",MB_OK|MB_ICONEXCLAMATION);	
	else
	{
		for (int i=0;i<pErrors->GetCount();i++)
		{
			_bstr_t desc=pErrors->GetItem((long)i)->GetDescription();
			MessageBox(NULL,desc,"´í  Îó",MB_OK|MB_ICONEXCLAMATION);
		}
	}
}
//_RecordsetPtr&

void ado::rstOpen(CString TSQL)
{
	try
	{
	_bstr_t bstrSQL=TSQL.AllocSysString();
	m_pRecordset.CreateInstance(__uuidof(Recordset));
	//m_pRecordset->Open(bstrSQL,(IDispatch*)m_pConnection,adOpenDynamic,adLockOptimistic,adCmdText);
	m_pRecordset->Open(bstrSQL,m_pConnection.GetInterfacePtr(),adOpenDynamic,adLockOptimistic,adCmdText);
	}
	catch(_com_error e)
	{
	m_pRecordset=m_pConnection->Execute((_bstr_t)TSQL,NULL,adCmdText);
	//return false;
	}
	//return m_pRecordset;
}

CString ado::GetFieldValue(CString Field)
{
    _variant_t Thevalue;
	CString temp;
	
    Thevalue=m_pRecordset->GetCollect((_bstr_t)Field);
	if(Thevalue.vt==VT_EMPTY ||Thevalue.vt==VT_NULL)
		temp="";
	else
	{
		temp=(char*)(_bstr_t)Thevalue;
		temp.TrimRight();
		temp.TrimLeft();
	}
	
	return temp;
}
bool ado::MovePrevious()
{
	try
	{
	m_pRecordset->MovePrevious();
	}
	catch(_com_error e)
	{
	AfxMessageBox(e.Description());
	return false;
	}
	return true;
}
bool ado::Move(int nRecordNum)
{
	try
	{
		if(!m_pRecordset->BOF)
		{
			m_pRecordset->MoveFirst();
		}
			m_pRecordset->Move(nRecordNum);
	}
	catch(_com_error e)
	{
	AfxMessageBox(e.Description());
	return false;
	}
	return true;
}
bool ado::MoveNext()
{
	try
	{
	
	m_pRecordset->MoveNext();
		
	}
	catch(_com_error e)
	{
	AfxMessageBox(e.Description());
	return false;
	}
	return true;
}
bool ado::MoveFirst()
{
	try
	{
	m_pRecordset->MoveFirst();
	}
	catch(_com_error e)
	{
	AfxMessageBox(e.Description());
	return false;
	}
	return true;
}
bool ado::MoveLast()
{
	try
	{
	m_pRecordset->MoveLast();
	}
	catch(_com_error e)
	{
	AfxMessageBox(e.Description());
	return false;
	}
	return true;
}
void ado::ExecuteSQL(CString TSQL)
{
	try
	{
	m_pConnection->Execute((_bstr_t)TSQL,NULL,adCmdText);
	}
	catch(_com_error e)
	{
	AfxMessageBox(e.Description());
	
	}
}
void ado::close()
{
	m_pRecordset->Close();
	m_pConnection->Close();
	m_pRecordset=NULL;
	m_pConnection=NULL;
	::CoUninitialize();
}
void ado::AddNew()
{
	m_pRecordset->AddNew();
}
void ado::Update()
{
	m_pRecordset->Update();
}
void ado::SetFieldValue(CString OField,CString value)
{_bstr_t tt=value.AllocSysString();
_bstr_t ss=OField.AllocSysString();
	m_pRecordset->PutCollect((_variant_t)ss,(_variant_t)tt);
}
bool ado::recordbof()
{
	if(m_pRecordset->BOF)
	{
		return true;
	}else
	{
		return false;
	}
}
bool ado::recordeof()
{
	if(m_pRecordset->adoEOF)
	{
		return true;
	}else
	{
		return false;
	}
}

