

#include "stdafx.h"
#include "stdlib.h"
#include "stdio.h"
#include "resource.h"
#define ID_EDIT
#define tongnum 10000//���������ͬ��
#include <fstream>
#include<string.h>
#include<sstream> 
#include<iostream>
#include<Shlobj.h>
#include<tchar.h>
#include<Commctrl.h>
#include<Commdlg.h>
#pragma comment(lib,"comctl32.lib")//����comct132.
#include <WINDOWS.H>
#include <shellapi.h>
#pragma comment(lib, "shell32.lib")
HINSTANCE g_hInst = NULL;
HWND      g_hEdit = NULL;
HWND hWnd=NULL;
static int count=0;   //   �Զ����б��
static int cot=0;   //   �Ƿ��ܱ�����
static int w=0;   //  ��¼���ڿ�
static int h=0;    //  ��¼���ڸ�
static ni =-1;   //   ������Ŀ����
static num =0;   //   �����ַ�����
static int ch=0;   //   ����ʱ�ж��Ƿ�����ַ�
TCHAR str1[30];   //   ���ҵ��ַ���
char place[MAX_PATH];     //   �򿪱����ļ�·��
void chazhao(HWND hwndDlg);
void tihuan(HWND hwndDlg);
using namespace std;

struct {
	int num;    //  ����ʱ��¼ָ��λ��
	int flag;   //  �Ƿ��в��ұ��
}tong[tongnum];   

BOOL CALLBACK DialogProc1(                 //  ���ҹ��� �Ի���ص�����
						  HWND hwndDlg, 
						  UINT uMsg, 
						  WPARAM wParam, 
						  LPARAM lParam 
						  ){
	
	switch (uMsg)
	{
	case WM_COMMAND:
		switch(LOWORD(wParam))
		{
		case IDCANCEL:
			EndDialog(hwndDlg,IDCANCEL);   //�رղ��ҶԻ���
			ni=-1;
			break;
		case ID_chazhao:   //  ���²��Ұ�ť
			ni++;          //   ni ��¼���ҵڼ����ַ���
			TCHAR test[10];
			GetDlgItemText(hwndDlg,IDC_input,test,sizeof(test));   //ƥ�����ʱ�Ƿ�����ַ���
			if(strcmp(test,str1)!=0)
			{ni=0;ch=0;}
			if(ch==0)
				chazhao(hwndDlg);
			if(tong[ni].num==0)
			{	MessageBox( hwndDlg, "  �Ҳ������ַ���", "��ʾ", MB_DEFBUTTON1|MB_OK|MB_ICONHAND);ch=0;break; }
			SetFocus(g_hEdit);
			if(tong[ni].flag==1)
				SendMessage( g_hEdit, EM_SETSEL,tong[ni].num-2-num,tong[ni].num);  //�ɲ��һ����ַ��Ĺ������
			else
				SendMessage( g_hEdit, EM_SETSEL,tong[ni].num-num,tong[ni].num);  //���ɲ��һ����ַ��Ĺ������
			
			break;
			
		case ID_chazhao2:   //���ϲ��Ұ�ť
			ni--;
			if(ch==0)
				chazhao(hwndDlg);
			if(ni==-1||ni==-2)
			{	MessageBox( hwndDlg, "  �Ҳ������ַ���", "��ʾ", MB_DEFBUTTON1|MB_SYSTEMMODAL|MB_OK|MB_ICONHAND);ch=0;ni=-1;break; }
			SetFocus(g_hEdit);
			if(tong[ni].flag==1)
				SendMessage( g_hEdit, EM_SETSEL,tong[ni].num-2-num,tong[ni].num);
			else                                                            //   ͬ��
				SendMessage( g_hEdit, EM_SETSEL,tong[ni].num-num,tong[ni].num);    
			
			break;
		case ID_CANCEL:  //  ȡ����ť
			EndDialog(hwndDlg,IDCANCEL);
			ni=-1;
			break;
			
		}
		break;
		
		
	}
	return 0;
}
BOOL CALLBACK DialogProc2(           //  �滻���ܶԻ���ص�����
						  
						  HWND hwndDlg, 
						  UINT uMsg, 
						  WPARAM wParam, 
						  LPARAM lParam 
						  )
{
	switch (uMsg)
	{
	case WM_COMMAND:
		switch(LOWORD(wParam))
		{
		case IDCANCEL:
			EndDialog(hwndDlg,IDCANCEL);  //  �˳�
			break;
		case ID_tihuan:
			tihuan(hwndDlg);   // �滻��ť
			break;
		case ID_CANCEL:
			EndDialog(hwndDlg,IDCANCEL);  // �˳���ť
			break;
		}
		break;
	}
	return 0;
}

BOOL CALLBACK DialogProc3( 
						  //  ���ڶԻ���
						  HWND hwndDlg, 
						  UINT uMsg,  
						  WPARAM wParam,
						  LPARAM lParam 
						  )
{
	switch (uMsg)
	{
	case WM_COMMAND:
		if(LOWORD(wParam)==IDCANCEL)
			EndDialog(hwndDlg,IDCANCEL);
		break;
		
	}
	return 0;
}


void str_replace(TCHAR * cp, int n, TCHAR * str)   //  �ƶ�λ��ָ�뺯��
{
	int lenofstr;
	char * tmp;
	lenofstr = strlen(str); 
	//str2��str1�̣���ǰ�ƶ� 
	if(lenofstr < n)  
	{
		tmp = cp+n;
		while(*tmp)
		{
			*(tmp-(n-lenofstr)) = *tmp; //n-lenofstr���ƶ��ľ��� 
			tmp++;
		}
		*(tmp-(n-lenofstr)) = *tmp; //move '\0'	
	}
	else
		//str2��str1���������ƶ�
		if(lenofstr > n)
		{
			tmp = cp;
			while(*tmp) tmp++;
			while(tmp>=cp+n)
			{
				*(tmp+(lenofstr-n)) = *tmp;
				tmp--;
			}   
		}
		strncpy(cp,str,lenofstr);
}


void tihuan(HWND hwndDlg)    //  �滻����
{
	TCHAR *p;
	int nump=0;
	TCHAR str1[30];
	TCHAR str2[60];
	LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
	TCHAR *buffer=new char[nTextLen+1];
	GetDlgItemText(hwndDlg,IDC_replace1,str1,sizeof(str1));  //��ȡ ���滻 ���ַ���
	GetDlgItemText(hwndDlg,IDC_replace2,str2,sizeof(str2));  //��ȡ �滻�� ���ַ���
	
    SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)buffer);
   	p = strstr(buffer,str1);    //  strstr���� ����str1��buffer���״γ��ֵĵ�ַ
   	while(p)
	{
		
		nump++;                //   ͳ���滻���ַ�������
		p = p+strlen(str1);
		p = strstr(p,str1);
	}   	
	if(nump==0)    // ���û�ҵ��滻���ַ������˳�
	{
		MessageBox(hwndDlg, "   δ���ҵ��ַ���������������...", "��ʾ", MB_DEFBUTTON1|MB_OK|MB_ICONWARNING );
		return;
	}
	else   //  �ҵ��滻���ַ�������ʾ�ɹ�
		MessageBox(hwndDlg, "   �滻�ɹ���", "��ʾ", MB_DEFBUTTON1|MB_OK|MB_ICONASTERISK );
	
    int number=strlen(str2)-strlen(str1);   //�������������ַ����ĳ��Ȳ�
	
    if(number<=0)   //  �������С���㣬�������·����ڴ�ռ�洢�ַ���
	{
		p = strstr(buffer,str1);    //  strstr���� ����str1��buffer���״γ��ֵĵ�ַ
		while(p)
		{
			//ÿ�ҵ�һ��str1������str2���滻 
			str_replace(p,strlen(str1),str2);  //  ָ��λ��ƴ��
			p = p+strlen(str2);
			p = strstr(p,str1);
		}   	
		SendMessage( g_hEdit, WM_SETTEXT,
			0, (LPARAM)buffer);
		SetFocus(g_hEdit);
		delete buffer;
	}
	
	else    //������ȳ����ˣ����·���һ�������buffer2�ռ�洢�ַ�������ֹ�����
	{   
		TCHAR *buffer2=new TCHAR[nTextLen + 1+nump*number];
		SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1+nump*number, (LPARAM)buffer2);
		p = strstr(buffer2,str1);    //  strstr���� ����str1��buffer2���״γ��ֵĵ�ַ
		while(p)
		{
			//ÿ�ҵ�һ��str1������str2���滻 
			str_replace(p,strlen(str1),str2);  //  ָ��λ��ƴ��
			p = p+strlen(str2);
			p = strstr(p,str1);
		}   	
		SendMessage( g_hEdit, WM_SETTEXT,
			0, (LPARAM)buffer2);
		SetFocus(g_hEdit);
		delete buffer2;
		
	}
	
}

void chazhao(HWND hwndDlg)
{		   
	
	ch=1;
	int c=0,q=0;
	int i=0,j=0,k=0;
	for(i=0;i<tongnum;i++)
	{	tong[i].flag=0;tong[i].num=0;}                       // ��ʼ��tong[]�ṹ�壬 �ýṹ���¼����ʱ��ָ��λ�úͱ�ǻ��еĲ���
	LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
	TCHAR *str2=new char[nTextLen+1];
	GetDlgItemText(hwndDlg,IDC_input,str1,sizeof(str1));         //  �õ����ҵ��ַ���
	SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)str2);   //  �õ��༭�����ַ���
	   num=strlen(str1);       
	   for(i=0;*(str2+i)!='\0';i++)    //str2��ͷ��ʼ�����ַ���
	   {	c=0;q=0;
	   
	   if(*(str1)==*(str2+i))   //   ƥ�䵽str1�ĵ�һ���ַ���str2�ĵ�i��ָ��λ���ַ���ͬ
	   {	for(j=1;j<num;j++)
	   
	   {
		   if((int)*(str2+i+j)==13||(int)*(str2+i+j)==10)  // �Թ��س��ͻ����ַ�
		   {	i+=2;q=1;}
		   if(*(str1+j)!=*(str2+i+j))		    //����ƥ�䣬ֱ������ȫƥ��
		   { c=1; break;  }
	   }
	   
	   if(c==0&&q==1)
	   {tong[k].num=i+j;tong[k].flag=1;k++;}  //��¼ƥ��ָ��λ�ã�������ѻ���
	   if(c==0&&q==0)
	   {tong[k].num=i+j;k++;}    //   ��¼ƥ��ָ��λ��
	   
	   
	   }
	   }
	   delete str2;
}


int lingcunwei()  //���Ϊ����

{
	HWND hd = FindWindow(NULL, "�ҵļ��±�");
	CHAR strFileName[MAX_PATH] = "";
	CHAR strPath[MAX_PATH] = "";
	OPENFILENAME ofn;
	ofn.lStructSize = sizeof(OPENFILENAME);
	ofn.hwndOwner = NULL;
	ofn.hInstance = NULL;
	ofn.lpstrFilter = "�ı��ĵ�\0*.txt";
	ofn.lpstrCustomFilter = NULL;
	ofn.nMaxCustFilter = 0;
	ofn.nFilterIndex = 1;
	ofn.lpstrFile = strFileName;  //  �����·��
	ofn.nMaxFile = MAX_PATH;
	ofn.lpstrFileTitle = NULL;
	ofn.nMaxFileTitle = 0;
	ofn.lpstrInitialDir = strPath;
	ofn.lpstrTitle = "����";
	ofn.Flags = OFN_OVERWRITEPROMPT | OFN_PATHMUSTEXIST | OFN_HIDEREADONLY | OFN_NOREADONLYRETURN;
	ofn.nFileOffset = 0;
	ofn.nFileExtension = 0;
	ofn.lpstrDefExt ="txt";
	ofn.lCustData = 0;
	ofn.lpfnHook = NULL;
	ofn.lpTemplateName = NULL;
	
	if (GetSaveFileName(&ofn))//
	{     //��ȡ���ֳ���
		LRESULT nTextLen = SendMessage( g_hEdit, 
			WM_GETTEXTLENGTH, 0, 0 );
		//��ȡ����
		CHAR * pszBuff = NULL;
		pszBuff = (CHAR *)malloc( nTextLen + 1 );
		memset( pszBuff, 0, nTextLen + 1 );
		SendMessage( g_hEdit, WM_GETTEXT,
			nTextLen + 1, (LPARAM)pszBuff );
		//�����ļ�
		
		FILE * pFile = fopen(strFileName , "wb" ); 
		fwrite( pszBuff, nTextLen, 1, pFile );  //  д���ļ�
		fclose( pFile );
		//�ͷ��ڴ�
		free( pszBuff );
		return 0;
	}
	return 0;
}

CHAR* lujing() {          //    ���ļ�ʱ��ȡ�ļ���·��
	LPITEMIDLIST pil = NULL;
	INITCOMMONCONTROLSEX InitCtrls = { 0 };
	TCHAR szBuf[4096] = { 0 };
	BROWSEINFO bi = { 0 };
	bi.hwndOwner = NULL;
	bi.iImage = 0;
	bi.lParam = NULL;
	bi.lpfn = NULL;
	bi.lpszTitle = _T("��ѡ���ļ�·��...");
	bi.pszDisplayName = szBuf;
	bi.ulFlags = BIF_BROWSEINCLUDEFILES;
	InitCommonControlsEx(&InitCtrls);//�ڵ��ú���SHBrowseForFolder֮ǰ��Ҫ���øú�����ʼ����ػ���
	pil = SHBrowseForFolder(&bi);
	if (NULL != pil) {        //������ִ�гɹ��������û�ѡ���ļ�·�������ȷ��
		SHGetPathFromIDList(pil, szBuf);     //��ȡѡ�񵽵��ļ�·��
		return szBuf;
	}
	return NULL;
}


void OnCreate( HWND hWnd, UINT nMsg,      //   ����һ�����Զ����е�edit�༭��
			  WPARAM wParam, LPARAM lParam )
{
    g_hEdit = CreateWindow( "EDIT", "",
        WS_CHILD|WS_VISIBLE|WS_HSCROLL|
        WS_VSCROLL|ES_AUTOHSCROLL|
        ES_AUTOVSCROLL|ES_MULTILINE|ES_WANTRETURN, 
        0, 0, 100, 200, hWnd,
        (HMENU)1001, g_hInst, NULL );
	MoveWindow( g_hEdit, 0, 0, w,
		h, TRUE );
	SetFocus( g_hEdit);   //�Ա༭�����ü��̽���
}

void OnCreate2( HWND hWnd, UINT nMsg,     //    ����һ���Զ����е�edit�༭��
			   WPARAM wParam, LPARAM lParam )
{
    g_hEdit = CreateWindow( "EDIT", "",
        WS_CHILD|WS_VISIBLE|
        WS_VSCROLL|
        ES_AUTOVSCROLL|ES_MULTILINE|ES_WANTRETURN, 
        0, 0, 100, 200, hWnd,
        (HMENU)1001, g_hInst, NULL );
	MoveWindow( g_hEdit, 0, 0, w,
		h, TRUE );
	SetFocus( g_hEdit);  //���ü��̽���
}

void OnSize( HWND hWnd, UINT nMsg,     //     ��ȡ��¼�ͻ��������������༭���С
			WPARAM wParam, LPARAM lParam )
{
    int nWidth = LOWORD( lParam );
    int nHeight= HIWORD( lParam );
    if( NULL != g_hEdit )
    {   //��EDIT�������������ͻ���
        MoveWindow( g_hEdit, 0, 0, nWidth,
            nHeight, TRUE );
    }
	w=nWidth;
	h=nHeight;
}

void OnSave( )    //�����ļ�
{
    //��ȡ���ֳ���
    LRESULT nTextLen = SendMessage( g_hEdit, 
        WM_GETTEXTLENGTH, 0, 0 );
    //��ȡ����
    CHAR * pszBuff = NULL;
    pszBuff = (CHAR *)malloc( nTextLen + 1 );
    memset( pszBuff, 0, nTextLen + 1 );
    SendMessage( g_hEdit, WM_GETTEXT,
        nTextLen + 1, (LPARAM)pszBuff );
    //�����ļ�
	FILE * pFile=NULL;
	if(cot==1)
		pFile=fopen( place, "wb" );
	else 
	{	free( pszBuff );
	MessageBox(g_hEdit, "����֮ǰ��δ���ļ�����ѡ�����Ϊ......", "��ʾ", 0|MB_ICONWARNING|MB_DEFBUTTON1);
	return;
	}
    fwrite( pszBuff, nTextLen, 1, pFile );
    fclose( pFile );
    //�ͷ��ڴ�
    free( pszBuff );
	//	cot=0;
}

void ondrop(WPARAM wParam)      //  ��ק�ļ�������
{
	HDROP hdrop = (HDROP)wParam;
	
	int iDropFileNums = 0;
	iDropFileNums = DragQueryFile(hdrop, 0xFFFFFFFF, NULL, 0);   //   ��ȡ�Ϸ��ļ�����
	for (int i=0; i<iDropFileNums; i++)    //   �ֱ��ȡ�Ϸ��ļ���(��Զ���ļ�����)
	{    
		DragQueryFile(hdrop, i, place, sizeof(place));    
	}
	DragFinish(hdrop);   //�ͷ��ļ���������  
	cot=1;
	FILE * pFile = fopen( place, "rb" );
	//��ȡ�ļ�����
	fseek( pFile, 0, SEEK_END );
	long nFileLen = ftell( pFile );
	fseek( pFile, 0, SEEK_SET );
	//��ȡ�ļ�����
	CHAR * pszBuf = (CHAR *)
		malloc( nFileLen + 1 );
	memset( pszBuf, 0, nFileLen + 1 );
	fread( pszBuf, 1, nFileLen+1,pFile );
	//�ر��ļ�
	fclose( pFile );
	//���ַ���ʾ��EDIT����
	SendMessage( g_hEdit, WM_SETTEXT,
		0, (LPARAM)pszBuf );
	//�ͷ��ڴ�
				SetFocus( g_hEdit);
				free( pszBuf );
}


void OnOpen( )   //���ļ�
{   
	
    //���ļ���ȡ���� "C:\\1.txt"
	char *t=lujing();
	if(t==NULL)
		return;
	cot=1;
	strcpy(place,t);
    FILE * pFile = fopen( place, "rb" );
    //��ȡ�ļ�����
    fseek( pFile, 0, SEEK_END );
    long nFileLen = ftell( pFile );
    fseek( pFile, 0, SEEK_SET );
    //��ȡ�ļ�����
    CHAR * pszBuf = (CHAR *)
        malloc( nFileLen + 1 );
    memset( pszBuf, 0, nFileLen + 1 );
    fread( pszBuf, 1, nFileLen+1,pFile );
    //�ر��ļ�
    fclose( pFile );
    //���ַ���ʾ��EDIT����
    SendMessage( g_hEdit, WM_SETTEXT,
        0, (LPARAM)pszBuf );
    //�ͷ��ڴ�
	SetFocus( g_hEdit);
    free( pszBuf );
	
}





void  OnCommand( HWND hWnd, UINT nMsg, 
				WPARAM wParam, LPARAM lParam )   //��Ӧ�˵���ť��Ϣ
{
    int nNotifyCode = HIWORD( wParam );
    int nEventID    = LOWORD( wParam );
    switch( nEventID )
    {
    case 1001:
        {
            switch( nNotifyCode )
            {
            case EN_CHANGE:  //��Ӧ�ı�
				
                break;
            }
        }
        break;
    case ID_SELALL:  // ȫѡ
        SendMessage( g_hEdit, EM_SETSEL, 0,-1 );
        break;
    case ID_COPY:  //  ����
        SendMessage( g_hEdit, WM_COPY, 0, 0 );
        break;
    case ID_PASTE:  // ճ��
        SendMessage( g_hEdit, WM_PASTE, 0, 0 );
        break;
    case ID_SAVE:   //����
        OnSave( );
        break;
    case ID_OPEN:   //��
        OnOpen( );
        break;
	case ID_LCW:   //���Ϊ
		lingcunwei();
		break;
	case ID_huan:   // �Զ�����
		{ 
			count=1;    //�ı��ʾ��
			LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
			char *buffer=new char[nTextLen+1];
			SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)buffer );
			DestroyWindow(g_hEdit);   //   ����༭���ַ����󣬴ݻٱ༭�򣬸��´��ڣ�������ʾ�༭���ַ���
			SendMessage( hWnd, 	WM_CREATE, 0, 0 );
			SendMessage( g_hEdit, WM_SETTEXT,0, (LPARAM)buffer );
			delete buffer;
			break;
		}
	case ID_jinyong:      //�����Զ�����
		{ 
			count=0;
			LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
			char *buffer=new char[nTextLen+1];
			SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)buffer );    //˵��ͬ��
			DestroyWindow(g_hEdit);
			SendMessage( hWnd, 	WM_CREATE, 0, 0 );
			SendMessage( g_hEdit, WM_SETTEXT,0, (LPARAM)buffer );
			delete buffer;
			break;
		}
	case ID_find:   //���ҹ���
		{
			HWND h=FindWindow(NULL,"����");
			if(h!=NULL) 
			{SetFocus(h); break;}
		}
		DialogBox(g_hInst,(LPSTR)IDD_chazhao,NULL,DialogProc1);  
		break;
	case ID_replace:       //�滻����
		{
			HWND h=FindWindow(NULL,"�滻");
			if(h!=NULL) 
			{SetFocus(h); break;}
		}
		DialogBox(g_hInst,(LPSTR)IDD_tihuan,NULL,DialogProc2);
		break;
	case ID_about:    //����
		{
			HWND h=FindWindow(NULL,"About");
			if(h!=NULL) 
			{SetFocus(h); break;}
		}
		DialogBox(g_hInst,(LPSTR)IDD_about,NULL,DialogProc3);
		break;
	case ID_NEW:   //  �½�
		cot=0;
		DestroyWindow(g_hEdit);
		SendMessage( hWnd, WM_CREATE, 0, 0 );
		break;
	case ID_NUM:   //  ͳ������
		{
			int i=0,v=0;
			LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
			char *buffer=new char[nTextLen+1];
			SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)buffer );
			while(i<nTextLen)
			{   
				if(buffer[i]!=' '&&(int)buffer[i]!=13&&(int)buffer[i]!=10&&(int)buffer[i]!=9)  // ƥ�� ����v��¼�������������ո񣬻س������з�ʱ������
					v++;
				i++;
			}
			char str[10];char b[]="   ������:  ";
			sprintf(str,"%d",v);
			strcat(b,str);
			MessageBox( NULL, b,"ͳ��", MB_OK );
			delete buffer;
			break;
		}
	case ID_LINE:  //   ͳ������
		{
			int i=0,v=1;
			LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
			char *buffer=new char[nTextLen+1];
			SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)buffer ); 
			while(i<nTextLen)
			{   
				if((int)buffer[i]==13)  //ƥ�� ����v��¼�������������س��� ʱ������
					v++;
				i++;
			}
			char str[10];char b[]="   ������:  ";
			sprintf(str,"%d",v);
			strcat(b,str);
			MessageBox( NULL, b,"ͳ��", MB_OK );
			delete buffer;
			break;
		}
    }
	
}



LRESULT CALLBACK WndProc( HWND   hWnd,   // �����ڻص�����
						 UINT   nMsg,
						 WPARAM wParam,
						 LPARAM lParam )
{
    switch( nMsg )
    {
	case WM_DROPFILES:  // ��Ӧ��ק�ļ���Ϣ
        ondrop(wParam);
        break;  
    case WM_CREATE:  //����������Ϣ
		SendMessage(hWnd,WM_SETICON,(WPARAM)TRUE,(LPARAM)LoadIcon(GetModuleHandle(NULL),(LPCTSTR)IDI_ICON1));  //  �����Ͻ���ʾͼ��
		if(count==0)
			OnCreate( hWnd, nMsg, wParam, lParam );
		if(count==1)
			OnCreate2( hWnd, nMsg, wParam, lParam );
        break;
    case WM_SIZE:  //�������ڴ�С
        OnSize( hWnd, nMsg, wParam, lParam ); // �ػ�༭���С
        break;
    case WM_COMMAND:  // ��Ӧ�˵�����Ϣ
        OnCommand( hWnd, nMsg, wParam, lParam );
        break;
	case WM_CLOSE:
		{
			int  m=MessageBox(hWnd, "   �Ƿ�Ҫ�����ļ���", "��ʾ", MB_YESNOCANCEL|MB_ICONEXCLAMATION|MB_ICONWARNING|MB_DEFBUTTON1);
			if(m==IDYES)
			{
				if(cot==1)
				{
					OnSave();
					DestroyWindow(hWnd);
					return 0;
				}
				else
					lingcunwei();
			}
			
			if(m==IDNO)
			{
				DestroyWindow(hWnd);
				return 0;
			}
			
			else
				return 0;
		}   
    case WM_DESTROY:  // �ر�
        PostQuitMessage( 0 );
        return 0;
		/*	case WM_CTLCOLOREDIT ://�ı�����
		{	HDC hdcEdit = (HDC) wParam; 
		SelectObject (hdcEdit,GetStockObject(BLACK_BRUSH)) ;
		break ;}      */
    }
    return DefWindowProc( hWnd, nMsg,
        wParam, lParam );
}



BOOL RegisterWnd( LPSTR pszClassName )  //ע�ᴰ����
{
    WNDCLASSEX wce = { 0 };
    wce.cbSize        = sizeof( wce );
    wce.cbClsExtra    = 0;
    wce.cbWndExtra    = 0;
    wce.hbrBackground = HBRUSH(COLOR_WINDOW);
    wce.hCursor       = NULL;
    wce.hIcon         = NULL;
    wce.hIconSm       = NULL;
    wce.hInstance     = g_hInst;
    wce.lpfnWndProc   = WndProc;
    wce.lpszClassName = pszClassName;
    wce.lpszMenuName  = NULL;
    wce.style         = CS_HREDRAW|CS_VREDRAW;
	
    ATOM nAtom = RegisterClassEx( &wce );
    if( 0 ==  nAtom )
    {
        return FALSE;
    }
	
    return TRUE;
}

HWND CreateWnd( LPSTR pszClassName )  //����������
{
    HMENU hMenu = LoadMenu( g_hInst,
        MAKEINTRESOURCE(IDR_MAIN) );  // ���ز˵�
    HWND hWnd = CreateWindowEx( 
        WS_EX_ACCEPTFILES,
        pszClassName, "�ҵļ��±�", 
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT,
		CW_USEDEFAULT, 800,
        600, NULL, hMenu, g_hInst,
        NULL );
    return hWnd;
}

void DisplayWnd( HWND hWnd )  //��ʾ����
{
    ShowWindow( hWnd, SW_SHOW );
    UpdateWindow( hWnd );
}

void Message( )    //��Ϣѭ��
{
    MSG msg = { 0 };
    while( GetMessage( &msg, NULL, 0, 0 ) )
    {
		
        TranslateMessage( &msg );
        DispatchMessage( &msg );
    }
}

int APIENTRY WinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR     lpCmdLine,
                     int       nCmdShow)
{
    g_hInst = hInstance;
    RegisterWnd( "MYWND" );
    HWND hWnd = CreateWnd( "MYWND" );
    DisplayWnd( hWnd );
    Message( );
    return 0;
}

