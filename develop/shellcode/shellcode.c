#include<windows.h>

typedef DWORD (WINAPI *PGETPROCADDRESS) (HMODULE hModule,LPCSTR lpProcName);
typedef int (WINAPI * PMESSAGEBOX) (HWND hWnd,LPCTSTR lpText,LPCTSTR lpCaption,UINT uType);
typedef HMODULE (WINAPI * PLOADLIBRARY) (LPCTSTR lpFileName);

typedef struct UNICODE_STRING
{
	USHORT Length;
	USHORT MaximumLength;
	PWSTR Buffer;
}UNICODE_STRING;

typedef struct PEB_LDR_DATA{
	DWORD Length;
	BYTE initialized;
	PVOID SsHandle;
	LIST_ENTRY InLoadOrderModuleList;
	LIST_ENTRY InMemoryOrderModuleList;
	LIST_ENTRY InInitializationOrderModuleList;
	VOID * EntryInProgress;
}PEB_LDR_DATA;

typedef struct LDR_DATA_TABLE_ENTRY
{
	LIST_ENTRY InLoadOrderModuleList;
	LIST_ENTRY InMemoryOrderModuleList;
	LIST_ENTRY InInitializationOrderModuleList;
	void* DllBase;
	void* EntryPoint;
	ULONG SizeOfImage;
	UNICODE_STRING FullDllName;
	UNICODE_STRING BaseDllName;
	ULONG Flags;
	SHORT LoadCount;
	SHORT TlsIndex;
	HANDLE SectionHandle;
	ULONG CheckSum;
	ULONG TimeDateStamp;
}LDR_DATA_TABLE_ENTRY;

void ShellCode()
{
	LDR_DATA_TABLE_ENTRY *pPLD=NULL,*pBeg=NULL;
	PGETPROCADDRESS pGetProcAddress=NULL;
	PMESSAGEBOX pMessageBox=NULL;
	PLOADLIBRARY pLoadLibrary=NULL;
	WORD *pFirst =NULL,*pLast=NULL;
	DWORD ret =0,i=0;
	DWORD dwKernelBase=0;
	
	char szKernel32[]={'k',0,'e',0,'r',0,'n',0,'e',0,'l',0,'3',0,'2',0,'.',0,'d',0,'l',0,'l',0,0,0};
	char szUser32[]={'U','S','E','R','3','2','.','d','l','l',0};
	char szGetProcAddr[]={'G','e','t','P','r','o','c','A','d','d','r','e','s','s',0};
	char szLoadLibrary[]={'L','o','a','d','L','i','b','r','a','r','y','A',0};
	char szMessageBox[]={'M','e','s','s','a','g','e','B','o','x','A',0};
	
	__asm{
		mov eax,fs:[0x30]
			mov eax,[eax+0x0c]
			add eax,0x0c
			mov pBeg,eax
			mov eax,[eax]
			mov pPLD,eax 
	}
	// 遍历找到kernel32.dll
	while(pPLD!=pBeg)
	{
		pLast=(WORD*)pPLD->BaseDllName.Buffer;
		pFirst=(WORD*)szKernel32;
		while(*pFirst && (*pFirst-32==*pLast||*pFirst==*pLast))
		{	pFirst++,pLast++;}
		if(*pFirst==*pLast)
		{
			dwKernelBase=(DWORD)pPLD->DllBase;
			break;
		}
		pPLD=(LDR_DATA_TABLE_ENTRY*)pPLD->InLoadOrderModuleList.Flink;
	}
	
	// 遍历kernel32.dll的导出表，找到GetProcAddr函数地址
	
	IMAGE_DOS_HEADER *pIDH=(IMAGE_DOS_HEADER *)dwKernelBase; 
	IMAGE_NT_HEADERS *pINGS=(IMAGE_NT_HEADERS *)((DWORD)dwKernelBase+pIDH->e_lfanew);
	IMAGE_EXPORT_DIRECTORY *pIED=(IMAGE_EXPORT_DIRECTORY*)((DWORD)dwKernelBase+
		pINGS->OptionalHeader.
		DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
	
	DWORD *pAddOfFun_Raw=(DWORD*)((DWORD)dwKernelBase+pIED->AddressOfFunctions);
	WORD *pAddOfOrd_Raw=(WORD*)((DWORD)dwKernelBase+pIED->AddressOfNameOrdinals);
	DWORD *pAddOfNames_Raw=(DWORD*)((DWORD)dwKernelBase+pIED->AddressOfNames);
	DWORD dwCnt=0;
	
	char *pFinded=NULL,*pSrc=szGetProcAddr;
	for(;dwCnt<pIED->NumberOfNames;dwCnt++)
	{
		pFinded=(char *)((DWORD)dwKernelBase+pAddOfNames_Raw[dwCnt]);
		while(*pFinded &&*pFinded==*pSrc) 
		{pFinded++;pSrc++;}
		if(*pFinded == *pSrc)
		{
			pGetProcAddress=(PGETPROCADDRESS)((DWORD)dwKernelBase+pAddOfFun_Raw[pAddOfOrd_Raw[dwCnt]]);
			break;
		}
		pSrc=szGetProcAddr;
	}
	// 有了GetProcAddr 可以获得任何api
	pLoadLibrary=(PLOADLIBRARY)pGetProcAddress((HMODULE)dwKernelBase,szLoadLibrary);
	pMessageBox=(PMESSAGEBOX)pGetProcAddress(pLoadLibrary(szUser32),szMessageBox);
	
	// 使用函数
	char szTitle[]={'S','h','e','l','l','C','o','d','e',0};
	char szContent[]={0x48,0x65,0x6c,0x6c,0x6f,0x20,0x57,0x6f,0x72,0x6c,0x64,0x20,0x21,0};
	pMessageBox(NULL,szContent,szTitle,0);
	
}


int main()
{
	ShellCode();
	return 0;
}