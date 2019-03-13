

#include "stdafx.h"
#include "stdlib.h"
#include "stdio.h"
#include "resource.h"
#define ID_EDIT
#define tongnum 10000//查找最多相同数
#include <fstream>
#include<string.h>
#include<sstream> 
#include<iostream>
#include<Shlobj.h>
#include<tchar.h>
#include<Commctrl.h>
#include<Commdlg.h>
#pragma comment(lib,"comctl32.lib")//链接comct132.
#include <WINDOWS.H>
#include <shellapi.h>
#pragma comment(lib, "shell32.lib")
HINSTANCE g_hInst = NULL;
HWND      g_hEdit = NULL;
HWND hWnd=NULL;
static int count=0;   //   自动换行标记
static int cot=0;   //   是否能保存标记
static int w=0;   //  记录窗口宽
static int h=0;    //  记录窗口高
static ni =-1;   //   查找数目变量
static num =0;   //   查找字符长度
static int ch=0;   //   查找时判断是否更换字符
TCHAR str1[30];   //   查找的字符串
char place[MAX_PATH];     //   打开保存文件路径
void chazhao(HWND hwndDlg);
void tihuan(HWND hwndDlg);
using namespace std;

struct {
	int num;    //  查找时记录指针位置
	int flag;   //  是否换行查找标记
}tong[tongnum];   

BOOL CALLBACK DialogProc1(                 //  查找功能 对话框回调函数
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
			EndDialog(hwndDlg,IDCANCEL);   //关闭查找对话框
			ni=-1;
			break;
		case ID_chazhao:   //  向下查找按钮
			ni++;          //   ni 记录查找第几个字符串
			TCHAR test[10];
			GetDlgItemText(hwndDlg,IDC_input,test,sizeof(test));   //匹配查找时是否更换字符串
			if(strcmp(test,str1)!=0)
			{ni=0;ch=0;}
			if(ch==0)
				chazhao(hwndDlg);
			if(tong[ni].num==0)
			{	MessageBox( hwndDlg, "  找不到该字符串", "提示", MB_DEFBUTTON1|MB_OK|MB_ICONHAND);ch=0;break; }
			SetFocus(g_hEdit);
			if(tong[ni].flag==1)
				SendMessage( g_hEdit, EM_SETSEL,tong[ni].num-2-num,tong[ni].num);  //可查找换行字符的光标设置
			else
				SendMessage( g_hEdit, EM_SETSEL,tong[ni].num-num,tong[ni].num);  //不可查找换行字符的光标设置
			
			break;
			
		case ID_chazhao2:   //向上查找按钮
			ni--;
			if(ch==0)
				chazhao(hwndDlg);
			if(ni==-1||ni==-2)
			{	MessageBox( hwndDlg, "  找不到该字符串", "提示", MB_DEFBUTTON1|MB_SYSTEMMODAL|MB_OK|MB_ICONHAND);ch=0;ni=-1;break; }
			SetFocus(g_hEdit);
			if(tong[ni].flag==1)
				SendMessage( g_hEdit, EM_SETSEL,tong[ni].num-2-num,tong[ni].num);
			else                                                            //   同上
				SendMessage( g_hEdit, EM_SETSEL,tong[ni].num-num,tong[ni].num);    
			
			break;
		case ID_CANCEL:  //  取消按钮
			EndDialog(hwndDlg,IDCANCEL);
			ni=-1;
			break;
			
		}
		break;
		
		
	}
	return 0;
}
BOOL CALLBACK DialogProc2(           //  替换功能对话框回调函数
						  
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
			EndDialog(hwndDlg,IDCANCEL);  //  退出
			break;
		case ID_tihuan:
			tihuan(hwndDlg);   // 替换按钮
			break;
		case ID_CANCEL:
			EndDialog(hwndDlg,IDCANCEL);  // 退出按钮
			break;
		}
		break;
	}
	return 0;
}

BOOL CALLBACK DialogProc3( 
						  //  关于对话框
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


void str_replace(TCHAR * cp, int n, TCHAR * str)   //  移动位置指针函数
{
	int lenofstr;
	char * tmp;
	lenofstr = strlen(str); 
	//str2比str1短，往前移动 
	if(lenofstr < n)  
	{
		tmp = cp+n;
		while(*tmp)
		{
			*(tmp-(n-lenofstr)) = *tmp; //n-lenofstr是移动的距离 
			tmp++;
		}
		*(tmp-(n-lenofstr)) = *tmp; //move '\0'	
	}
	else
		//str2比str1长，往后移动
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


void tihuan(HWND hwndDlg)    //  替换函数
{
	TCHAR *p;
	int nump=0;
	TCHAR str1[30];
	TCHAR str2[60];
	LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
	TCHAR *buffer=new char[nTextLen+1];
	GetDlgItemText(hwndDlg,IDC_replace1,str1,sizeof(str1));  //读取 被替换 的字符串
	GetDlgItemText(hwndDlg,IDC_replace2,str2,sizeof(str2));  //读取 替换成 的字符串
	
    SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)buffer);
   	p = strstr(buffer,str1);    //  strstr函数 返回str1在buffer中首次出现的地址
   	while(p)
	{
		
		nump++;                //   统计替换的字符串个数
		p = p+strlen(str1);
		p = strstr(p,str1);
	}   	
	if(nump==0)    // 如果没找到替换的字符串，退出
	{
		MessageBox(hwndDlg, "   未查找到字符串，请重新输入...", "提示", MB_DEFBUTTON1|MB_OK|MB_ICONWARNING );
		return;
	}
	else   //  找到替换的字符串，提示成功
		MessageBox(hwndDlg, "   替换成功！", "提示", MB_DEFBUTTON1|MB_OK|MB_ICONASTERISK );
	
    int number=strlen(str2)-strlen(str1);   //计算两个输入字符串的长度差
	
    if(number<=0)   //  如果长度小于零，无需重新分配内存空间存储字符串
	{
		p = strstr(buffer,str1);    //  strstr函数 返回str1在buffer中首次出现的地址
		while(p)
		{
			//每找到一个str1，就用str2来替换 
			str_replace(p,strlen(str1),str2);  //  指针位置拼接
			p = p+strlen(str2);
			p = strstr(p,str1);
		}   	
		SendMessage( g_hEdit, WM_SETTEXT,
			0, (LPARAM)buffer);
		SetFocus(g_hEdit);
		delete buffer;
	}
	
	else    //如果长度超出了，重新分配一个更大的buffer2空间存储字符串，防止堆溢出
	{   
		TCHAR *buffer2=new TCHAR[nTextLen + 1+nump*number];
		SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1+nump*number, (LPARAM)buffer2);
		p = strstr(buffer2,str1);    //  strstr函数 返回str1在buffer2中首次出现的地址
		while(p)
		{
			//每找到一个str1，就用str2来替换 
			str_replace(p,strlen(str1),str2);  //  指针位置拼接
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
	{	tong[i].flag=0;tong[i].num=0;}                       // 初始化tong[]结构体， 该结构体记录查找时的指针位置和标记换行的查找
	LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
	TCHAR *str2=new char[nTextLen+1];
	GetDlgItemText(hwndDlg,IDC_input,str1,sizeof(str1));         //  得到查找的字符串
	SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)str2);   //  得到编辑框中字符串
	   num=strlen(str1);       
	   for(i=0;*(str2+i)!='\0';i++)    //str2从头开始遍历字符串
	   {	c=0;q=0;
	   
	   if(*(str1)==*(str2+i))   //   匹配到str1的第一个字符和str2的第i个指针位置字符相同
	   {	for(j=1;j<num;j++)
	   
	   {
		   if((int)*(str2+i+j)==13||(int)*(str2+i+j)==10)  // 略过回车和换行字符
		   {	i+=2;q=1;}
		   if(*(str1+j)!=*(str2+i+j))		    //继续匹配，直到能完全匹配
		   { c=1; break;  }
	   }
	   
	   if(c==0&&q==1)
	   {tong[k].num=i+j;tong[k].flag=1;k++;}  //记录匹配指针位置，并标记已换行
	   if(c==0&&q==0)
	   {tong[k].num=i+j;k++;}    //   记录匹配指针位置
	   
	   
	   }
	   }
	   delete str2;
}


int lingcunwei()  //另存为功能

{
	HWND hd = FindWindow(NULL, "我的记事本");
	CHAR strFileName[MAX_PATH] = "";
	CHAR strPath[MAX_PATH] = "";
	OPENFILENAME ofn;
	ofn.lStructSize = sizeof(OPENFILENAME);
	ofn.hwndOwner = NULL;
	ofn.hInstance = NULL;
	ofn.lpstrFilter = "文本文档\0*.txt";
	ofn.lpstrCustomFilter = NULL;
	ofn.nMaxCustFilter = 0;
	ofn.nFilterIndex = 1;
	ofn.lpstrFile = strFileName;  //  保存的路径
	ofn.nMaxFile = MAX_PATH;
	ofn.lpstrFileTitle = NULL;
	ofn.nMaxFileTitle = 0;
	ofn.lpstrInitialDir = strPath;
	ofn.lpstrTitle = "保存";
	ofn.Flags = OFN_OVERWRITEPROMPT | OFN_PATHMUSTEXIST | OFN_HIDEREADONLY | OFN_NOREADONLYRETURN;
	ofn.nFileOffset = 0;
	ofn.nFileExtension = 0;
	ofn.lpstrDefExt ="txt";
	ofn.lCustData = 0;
	ofn.lpfnHook = NULL;
	ofn.lpTemplateName = NULL;
	
	if (GetSaveFileName(&ofn))//
	{     //获取文字长度
		LRESULT nTextLen = SendMessage( g_hEdit, 
			WM_GETTEXTLENGTH, 0, 0 );
		//获取文字
		CHAR * pszBuff = NULL;
		pszBuff = (CHAR *)malloc( nTextLen + 1 );
		memset( pszBuff, 0, nTextLen + 1 );
		SendMessage( g_hEdit, WM_GETTEXT,
			nTextLen + 1, (LPARAM)pszBuff );
		//保存文件
		
		FILE * pFile = fopen(strFileName , "wb" ); 
		fwrite( pszBuff, nTextLen, 1, pFile );  //  写入文件
		fclose( pFile );
		//释放内存
		free( pszBuff );
		return 0;
	}
	return 0;
}

CHAR* lujing() {          //    打开文件时获取文件的路径
	LPITEMIDLIST pil = NULL;
	INITCOMMONCONTROLSEX InitCtrls = { 0 };
	TCHAR szBuf[4096] = { 0 };
	BROWSEINFO bi = { 0 };
	bi.hwndOwner = NULL;
	bi.iImage = 0;
	bi.lParam = NULL;
	bi.lpfn = NULL;
	bi.lpszTitle = _T("请选择文件路径...");
	bi.pszDisplayName = szBuf;
	bi.ulFlags = BIF_BROWSEINCLUDEFILES;
	InitCommonControlsEx(&InitCtrls);//在调用函数SHBrowseForFolder之前需要调用该函数初始化相关环境
	pil = SHBrowseForFolder(&bi);
	if (NULL != pil) {        //若函数执行成功，并且用户选择文件路径并点击确定
		SHGetPathFromIDList(pil, szBuf);     //获取选择到的文件路径
		return szBuf;
	}
	return NULL;
}


void OnCreate( HWND hWnd, UINT nMsg,      //   创建一个非自动换行的edit编辑框
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
	SetFocus( g_hEdit);   //对编辑框设置键盘焦点
}

void OnCreate2( HWND hWnd, UINT nMsg,     //    创建一个自动换行的edit编辑框
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
	SetFocus( g_hEdit);  //设置键盘焦点
}

void OnSize( HWND hWnd, UINT nMsg,     //     获取记录客户区长宽，并调整编辑框大小
			WPARAM wParam, LPARAM lParam )
{
    int nWidth = LOWORD( lParam );
    int nHeight= HIWORD( lParam );
    if( NULL != g_hEdit )
    {   //将EDIT窗口填满整个客户区
        MoveWindow( g_hEdit, 0, 0, nWidth,
            nHeight, TRUE );
    }
	w=nWidth;
	h=nHeight;
}

void OnSave( )    //保存文件
{
    //获取文字长度
    LRESULT nTextLen = SendMessage( g_hEdit, 
        WM_GETTEXTLENGTH, 0, 0 );
    //获取文字
    CHAR * pszBuff = NULL;
    pszBuff = (CHAR *)malloc( nTextLen + 1 );
    memset( pszBuff, 0, nTextLen + 1 );
    SendMessage( g_hEdit, WM_GETTEXT,
        nTextLen + 1, (LPARAM)pszBuff );
    //保存文件
	FILE * pFile=NULL;
	if(cot==1)
		pFile=fopen( place, "wb" );
	else 
	{	free( pszBuff );
	MessageBox(g_hEdit, "由于之前并未打开文件，请选择另存为......", "提示", 0|MB_ICONWARNING|MB_DEFBUTTON1);
	return;
	}
    fwrite( pszBuff, nTextLen, 1, pFile );
    fclose( pFile );
    //释放内存
    free( pszBuff );
	//	cot=0;
}

void ondrop(WPARAM wParam)      //  拖拽文件进窗口
{
	HDROP hdrop = (HDROP)wParam;
	
	int iDropFileNums = 0;
	iDropFileNums = DragQueryFile(hdrop, 0xFFFFFFFF, NULL, 0);   //   获取拖放文件个数
	for (int i=0; i<iDropFileNums; i++)    //   分别获取拖放文件名(针对多个文件操作)
	{    
		DragQueryFile(hdrop, i, place, sizeof(place));    
	}
	DragFinish(hdrop);   //释放文件名缓冲区  
	cot=1;
	FILE * pFile = fopen( place, "rb" );
	//获取文件长度
	fseek( pFile, 0, SEEK_END );
	long nFileLen = ftell( pFile );
	fseek( pFile, 0, SEEK_SET );
	//读取文件数据
	CHAR * pszBuf = (CHAR *)
		malloc( nFileLen + 1 );
	memset( pszBuf, 0, nFileLen + 1 );
	fread( pszBuf, 1, nFileLen+1,pFile );
	//关闭文件
	fclose( pFile );
	//将字符显示在EDIT窗口
	SendMessage( g_hEdit, WM_SETTEXT,
		0, (LPARAM)pszBuf );
	//释放内存
				SetFocus( g_hEdit);
				free( pszBuf );
}


void OnOpen( )   //打开文件
{   
	
    //打开文件读取数据 "C:\\1.txt"
	char *t=lujing();
	if(t==NULL)
		return;
	cot=1;
	strcpy(place,t);
    FILE * pFile = fopen( place, "rb" );
    //获取文件长度
    fseek( pFile, 0, SEEK_END );
    long nFileLen = ftell( pFile );
    fseek( pFile, 0, SEEK_SET );
    //读取文件数据
    CHAR * pszBuf = (CHAR *)
        malloc( nFileLen + 1 );
    memset( pszBuf, 0, nFileLen + 1 );
    fread( pszBuf, 1, nFileLen+1,pFile );
    //关闭文件
    fclose( pFile );
    //将字符显示在EDIT窗口
    SendMessage( g_hEdit, WM_SETTEXT,
        0, (LPARAM)pszBuf );
    //释放内存
	SetFocus( g_hEdit);
    free( pszBuf );
	
}





void  OnCommand( HWND hWnd, UINT nMsg, 
				WPARAM wParam, LPARAM lParam )   //响应菜单按钮消息
{
    int nNotifyCode = HIWORD( wParam );
    int nEventID    = LOWORD( wParam );
    switch( nEventID )
    {
    case 1001:
        {
            switch( nNotifyCode )
            {
            case EN_CHANGE:  //响应改变
				
                break;
            }
        }
        break;
    case ID_SELALL:  // 全选
        SendMessage( g_hEdit, EM_SETSEL, 0,-1 );
        break;
    case ID_COPY:  //  复制
        SendMessage( g_hEdit, WM_COPY, 0, 0 );
        break;
    case ID_PASTE:  // 粘贴
        SendMessage( g_hEdit, WM_PASTE, 0, 0 );
        break;
    case ID_SAVE:   //保存
        OnSave( );
        break;
    case ID_OPEN:   //打开
        OnOpen( );
        break;
	case ID_LCW:   //另存为
		lingcunwei();
		break;
	case ID_huan:   // 自动换行
		{ 
			count=1;    //改变标示符
			LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
			char *buffer=new char[nTextLen+1];
			SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)buffer );
			DestroyWindow(g_hEdit);   //   保存编辑框字符串后，摧毁编辑框，更新窗口，重新显示编辑框字符串
			SendMessage( hWnd, 	WM_CREATE, 0, 0 );
			SendMessage( g_hEdit, WM_SETTEXT,0, (LPARAM)buffer );
			delete buffer;
			break;
		}
	case ID_jinyong:      //禁用自动换行
		{ 
			count=0;
			LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
			char *buffer=new char[nTextLen+1];
			SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)buffer );    //说明同上
			DestroyWindow(g_hEdit);
			SendMessage( hWnd, 	WM_CREATE, 0, 0 );
			SendMessage( g_hEdit, WM_SETTEXT,0, (LPARAM)buffer );
			delete buffer;
			break;
		}
	case ID_find:   //查找功能
		{
			HWND h=FindWindow(NULL,"查找");
			if(h!=NULL) 
			{SetFocus(h); break;}
		}
		DialogBox(g_hInst,(LPSTR)IDD_chazhao,NULL,DialogProc1);  
		break;
	case ID_replace:       //替换功能
		{
			HWND h=FindWindow(NULL,"替换");
			if(h!=NULL) 
			{SetFocus(h); break;}
		}
		DialogBox(g_hInst,(LPSTR)IDD_tihuan,NULL,DialogProc2);
		break;
	case ID_about:    //关于
		{
			HWND h=FindWindow(NULL,"About");
			if(h!=NULL) 
			{SetFocus(h); break;}
		}
		DialogBox(g_hInst,(LPSTR)IDD_about,NULL,DialogProc3);
		break;
	case ID_NEW:   //  新建
		cot=0;
		DestroyWindow(g_hEdit);
		SendMessage( hWnd, WM_CREATE, 0, 0 );
		break;
	case ID_NUM:   //  统计字数
		{
			int i=0,v=0;
			LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
			char *buffer=new char[nTextLen+1];
			SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)buffer );
			while(i<nTextLen)
			{   
				if(buffer[i]!=' '&&(int)buffer[i]!=13&&(int)buffer[i]!=10&&(int)buffer[i]!=9)  // 匹配 ，用v记录字数，当遇到空格，回车，换行符时不计数
					v++;
				i++;
			}
			char str[10];char b[]="   总字数:  ";
			sprintf(str,"%d",v);
			strcat(b,str);
			MessageBox( NULL, b,"统计", MB_OK );
			delete buffer;
			break;
		}
	case ID_LINE:  //   统计行数
		{
			int i=0,v=1;
			LRESULT  nTextLen = SendMessage( g_hEdit, WM_GETTEXTLENGTH, 0, 0 );
			char *buffer=new char[nTextLen+1];
			SendMessage( g_hEdit, WM_GETTEXT,nTextLen + 1, (LPARAM)buffer ); 
			while(i<nTextLen)
			{   
				if((int)buffer[i]==13)  //匹配 ，用v记录行数，当遇到回车符 时不计数
					v++;
				i++;
			}
			char str[10];char b[]="   总行数:  ";
			sprintf(str,"%d",v);
			strcat(b,str);
			MessageBox( NULL, b,"统计", MB_OK );
			delete buffer;
			break;
		}
    }
	
}



LRESULT CALLBACK WndProc( HWND   hWnd,   // 主窗口回调函数
						 UINT   nMsg,
						 WPARAM wParam,
						 LPARAM lParam )
{
    switch( nMsg )
    {
	case WM_DROPFILES:  // 响应拖拽文件消息
        ondrop(wParam);
        break;  
    case WM_CREATE:  //创建窗口消息
		SendMessage(hWnd,WM_SETICON,(WPARAM)TRUE,(LPARAM)LoadIcon(GetModuleHandle(NULL),(LPCTSTR)IDI_ICON1));  //  在左上角显示图标
		if(count==0)
			OnCreate( hWnd, nMsg, wParam, lParam );
		if(count==1)
			OnCreate2( hWnd, nMsg, wParam, lParam );
        break;
    case WM_SIZE:  //调整窗口大小
        OnSize( hWnd, nMsg, wParam, lParam ); // 重绘编辑框大小
        break;
    case WM_COMMAND:  // 响应菜单栏消息
        OnCommand( hWnd, nMsg, wParam, lParam );
        break;
	case WM_CLOSE:
		{
			int  m=MessageBox(hWnd, "   是否要保存文件？", "提示", MB_YESNOCANCEL|MB_ICONEXCLAMATION|MB_ICONWARNING|MB_DEFBUTTON1);
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
    case WM_DESTROY:  // 关闭
        PostQuitMessage( 0 );
        return 0;
		/*	case WM_CTLCOLOREDIT ://改变字体
		{	HDC hdcEdit = (HDC) wParam; 
		SelectObject (hdcEdit,GetStockObject(BLACK_BRUSH)) ;
		break ;}      */
    }
    return DefWindowProc( hWnd, nMsg,
        wParam, lParam );
}



BOOL RegisterWnd( LPSTR pszClassName )  //注册窗口类
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

HWND CreateWnd( LPSTR pszClassName )  //创建主窗口
{
    HMENU hMenu = LoadMenu( g_hInst,
        MAKEINTRESOURCE(IDR_MAIN) );  // 加载菜单
    HWND hWnd = CreateWindowEx( 
        WS_EX_ACCEPTFILES,
        pszClassName, "我的记事本", 
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT,
		CW_USEDEFAULT, 800,
        600, NULL, hMenu, g_hInst,
        NULL );
    return hWnd;
}

void DisplayWnd( HWND hWnd )  //显示窗口
{
    ShowWindow( hWnd, SW_SHOW );
    UpdateWindow( hWnd );
}

void Message( )    //消息循环
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

