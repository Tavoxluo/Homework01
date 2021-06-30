; CLW file contains information for the MFC ClassWizard

[General Info]
Version=1
LastClass=CClientDlg
LastTemplate=CDialog
NewFileInclude1=#include "stdafx.h"
NewFileInclude2=#include "Client.h"

ClassCount=4
Class1=CClientApp
Class2=CClientDlg
Class3=CAboutDlg

ResourceCount=4
Resource1=IDD_ABOUTBOX
Resource2=IDR_MAINFRAME
Resource3=IDD_CLIENT_DIALOG
Class4=CLogin
Resource4=IDD_DIALOG_LOGIN

[CLS:CClientApp]
Type=0
HeaderFile=Client.h
ImplementationFile=Client.cpp
Filter=N

[CLS:CClientDlg]
Type=0
HeaderFile=ClientDlg.h
ImplementationFile=ClientDlg.cpp
Filter=D
BaseClass=CDialog
VirtualFilter=dWC
LastObject=CClientDlg

[CLS:CAboutDlg]
Type=0
HeaderFile=ClientDlg.h
ImplementationFile=ClientDlg.cpp
Filter=D

[DLG:IDD_ABOUTBOX]
Type=1
Class=CAboutDlg
ControlCount=4
Control1=IDC_STATIC,static,1342177283
Control2=IDC_STATIC,static,1342308480
Control3=IDC_STATIC,static,1342308352
Control4=IDOK,button,1342373889

[DLG:IDD_CLIENT_DIALOG]
Type=1
Class=CClientDlg
ControlCount=21
Control1=IDC_EDIT_SEND,edit,1350631492
Control2=IDC_EDIT_RECV,edit,1352730628
Control3=IDC_STATIC2,static,1073873419
Control4=IDC_STATIC_FILESIZE,static,1073872896
Control5=IDC_STATIC_RECV,static,1073872896
Control6=IDC_PROGRESS1,msctls_progress32,1082130433
Control7=IDOK,button,1342275585
Control8=IDMIN,button,1342275584
Control9=IDC_LIST_USER,listbox,1352728835
Control10=IDC_STATIC,button,1342210055
Control11=IDC_STATIC,static,1342308352
Control12=IDC_CHECK_ALL,button,1342242819
Control13=IDC_CHECK_ME,button,1342242819
Control14=IDCANCEL,button,1342275584
Control15=IDC_BUTTON_TANS,button,1342275712
Control16=IDC_BUTTON_END,button,1073840128
Control17=IDC_STATIC_FILENAME,static,1073872898
Control18=IDC_BUTTON_RECV,button,1073840128
Control19=IDC_STATIC_SPEED,static,1073872896
Control20=IDC_BUTTON_SHAKE,button,1342275712
Control21=IDC_COMBO_USER,combobox,1344339971

[DLG:IDD_DIALOG_LOGIN]
Type=1
Class=CLogin
ControlCount=7
Control1=IDOK,button,1342242817
Control2=IDCANCEL,button,1342242816
Control3=IDC_STATIC,button,1342177287
Control4=IDC_STATIC,static,1342308352
Control5=IDC_STATIC,static,1342308352
Control6=IDC_EDIT_USER,edit,1350631552
Control7=IDC_IPADDRESS1,SysIPAddress32,1342242816

[CLS:CLogin]
Type=0
HeaderFile=Login.h
ImplementationFile=Login.cpp
BaseClass=CDialog
Filter=D
LastObject=CLogin
VirtualFilter=dWC

