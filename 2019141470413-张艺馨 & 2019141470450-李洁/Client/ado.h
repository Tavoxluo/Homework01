#import "C:\Program Files\Common Files\System\ado\msado15.dll" no_namespace rename("EOF" ,"adoEOF")
class ado
{
public:
	_ConnectionPtr m_pConnection;
	_RecordsetPtr m_pRecordset;
public:
	ado();
	virtual ~ado();
	void close();
//	bool Move(int nRecordNumber);
	bool MovePrevious();
	bool MoveLast();
	bool MoveNext();
	bool MoveFirst();
	int GetRecordCount();
	//void Open(CString TSQL);
	bool Open(CString srecordset, UINT adCmd);
	void GetErrors(_com_error eErrors);
	CString GetFieldValue(CString Field);
	void AddNew();
	void Update();
	bool Move(int nRecordNum);
	void SetFieldValue(CString OField,CString value);
	void ExecuteSQL(CString SQL);
	bool recordeof();
	bool recordbof();
	void rstOpen(CString TSQL);
};