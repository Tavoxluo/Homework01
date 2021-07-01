; CLW file contains information for the MFC ClassWizard

[General Info]
Version=1
LastClass=CServerDlg
LastTemplate=CDialog
NewFileInclude1=#include "stdafx.h"
NewFileInclude2=#include "Server.h"

ClassCount=4
Class1=CServerApp
Class2=CServerDlg
Class3=CAboutDlg

ResourceCount=4
Resource1=IDD_SERVER_DIALOG
Resource2=IDR_MAINFRAME
Resource3=IDD_ABOUTBOX
Class4=CClearDlg
Resource4=IDD_DIALOG_CLEAR

[CLS:CServerApp]
Type=0
HeaderFile=Server.h
ImplementationFile=Server.cpp
Filter=N

[CLS:CServerDlg]
Type=0
HeaderFile=ServerDlg.h
ImplementationFile=ServerDlg.cpp
Filter=D
BaseClass=CDialog
VirtualFilter=dWC
LastObject=CServerDlg

[CLS:CAboutDlg]
Type=0
HeaderFile=ServerDlg.h
ImplementationFile=ServerDlg.cpp
Filter=D

[DLG:IDD_ABOUTBOX]
Type=1
Class=CAboutDlg
ControlCount=4
Control1=IDC_STATIC,static,1342177283
Control2=IDC_STATIC,static,1342308480
Control3=IDC_STATIC,static,1342308352
Control4=IDOK,button,1342373889

[DLG:IDD_SERVER_DIALOG]
Type=1
Class=CServerDlg
ControlCount=7
Control1=IDC_BUTTON_MIN,button,1342242817
Control2=IDC_BUTTON_CLEAR,button,1342242816
Control3=IDCANCEL,button,1342242816
Control4=IDC_EDIT4,edit,1344342020
Control5=IDC_STATIC1,static,1342308352
Control6=IDC_STATIC2,static,1342308352
Control7=IDC_STATIC,static,1342308352

[DLG:IDD_DIALOG_CLEAR]
Type=1
Class=CClearDlg
ControlCount=4
Control1=IDOK,button,1342242817
Control2=IDCANCEL,button,1342242816
Control3=IDC_LIST1,SysListView32,1350631425
Control4=IDC_STATIC,button,1342177287

[CLS:CClearDlg]
Type=0
HeaderFile=ClearDlg.h
ImplementationFile=ClearDlg.cpp
BaseClass=CDialog
Filter=D
LastObject=CClearDlg
VirtualFilter=dWC

