#pragma once
#include<stdio.h>
#include<stdlib.h>
#include<Windows.h>


class Base64Coder
{
	// Internal bucket class.
	class TempBucket
	{
	public:
		BYTE		nData[4];
		BYTE		nSize;
		void		Clear() { memset(nData, 0, 4); nSize = 0; };
	};

	PBYTE					m_pDBuffer;
	PBYTE					m_pEBuffer;
	DWORD					m_nDBufLen;
	DWORD					m_nEBufLen;
	DWORD					m_nDDataLen;
	DWORD					m_nEDataLen;

public:
	Base64Coder();
	virtual ~Base64Coder();

public:
	virtual void		Encode(const PBYTE, DWORD);
	virtual void		Decode(const PBYTE, DWORD);
	virtual void		Encode(LPCTSTR sMessage);
	virtual void		Decode(LPCTSTR sMessage);

	virtual LPCTSTR		DecodedMessage() const;
	virtual LPCTSTR		EncodedMessage() const;
	virtual PBYTE		DecodedMessage(DWORD& nLenMessage) const;

	virtual void		AllocEncode(DWORD);
	virtual void		AllocDecode(DWORD);
	virtual void		SetEncodeBuffer(const PBYTE pBuffer, DWORD nBufLen);
	virtual void		SetDecodeBuffer(const PBYTE pBuffer, DWORD nBufLen);

protected:
	virtual void		_EncodeToBuffer(const TempBucket& Decode, PBYTE pBuffer);
	virtual ULONG		_DecodeToBuffer(const TempBucket& Decode, PBYTE pBuffer);
	virtual void		_EncodeRaw(TempBucket&, const TempBucket&);
	virtual void		_DecodeRaw(TempBucket&, const TempBucket&);
	virtual BOOL		_IsBadMimeChar(BYTE);

	static  char		m_DecodeTable[256];
	static  BOOL		m_Init;
	void				_Init();
};

