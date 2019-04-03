

#include "stdafx.h"

#include "DEFINE.h"
#include "PE_Load.h"
#define szFileName "Demo.exe"

int _tmain(int argc, _TCHAR* argv[])
{


	//读取目标文件到内存 拉伸 贴入0x400000   读取他的IAT表  需要的DLL  LOAD进来 修复IAT表 JMP过去运行 


	//读取文件到内存
	PVOID pImage = 0;
	if (!ReadFileToImage(szFileName, &pImage))
	{
		Sleep(5000);
		return -1;
	}
	PVOID pNewBuffer = 0;

	//拉伸为运行时的状态
	ImageBufferToNewBuffer(pImage, &pNewBuffer);
	//释放读取时的内存
	free(pImage);

	//获取ImageBase和OEP
	PVOID pOptionHeader = 0;
	GetPEOptionHeader(pNewBuffer, &pOptionHeader);

	DWORD dwSizeOfImage = ((PIMAGE_OPTIONAL_HEADER)pOptionHeader)->SizeOfImage;
	DWORD dwEntryOfPoint = ((PIMAGE_OPTIONAL_HEADER)pOptionHeader)->AddressOfEntryPoint;
	DWORD dwOldImageBase = ((PIMAGE_OPTIONAL_HEADER)pOptionHeader)->ImageBase;
	PVOID  pBuffer = (PVOID)0x400000;

	//在0x400000处申请内存


	PVOID pAllocBuffer = VirtualAlloc(pBuffer, dwSizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

	PVOID pRelocTable = 0;
	if (!pAllocBuffer)
	{
		
		printf("在0x400000地址处申请内存失败，将在任意位置申请内存\n");
		pBuffer = VirtualAlloc(0, dwSizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

	}
	//把拉伸后的数据贴入申请到的位置
	memcpy_s(pBuffer, dwSizeOfImage, pNewBuffer, dwSizeOfImage);

	//如果没有申请到原来的ImageBase   进行重定位 已经拉伸为内存状态
	if ((DWORD)pBuffer != dwOldImageBase)
	{
		bool Rel=RelocationTable((DWORD)pBuffer);
		if (Rel == FALSE)
		{
			printf("被加载的程序的重定位表被清除,程序在编译时可能未开启aslr，程序加载失败！\n");
			system("pause");
			exit(1);
		}
		

	}
	//bool ImportTable((DWORD)pBuffer);

	//根据导入表的DLL名字  加载DLL  
	//导入表
	PIMAGE_IMPORT_DESCRIPTOR pImportTable = (PIMAGE_IMPORT_DESCRIPTOR)(((PIMAGE_OPTIONAL_HEADER)pOptionHeader)->DataDirectory[1].VirtualAddress + (PCHAR)pBuffer);
	HMODULE hModule = 0;
	while (pImportTable->FirstThunk &&pImportTable->OriginalFirstThunk)
	{
		hModule = LoadLibraryA(pImportTable->Name + (char*)pBuffer);
		//遍历导入表

		PFUNC_EXPORT_TYPE  dwIATAddress = (PFUNC_EXPORT_TYPE)pBuffer + pImportTable->FirstThunk / 4;
		while (*(DWORD*)dwIATAddress)
		{

			//判断是名字导出  还是序号导出

			if (dwIATAddress->Type == 1)
			{
				printf("该函数以序号导出 序号是：%d\n", dwIATAddress->Address);
				//导出的序号
				FARPROC FuncAddr = GetProcAddress(hModule, (PCHAR)dwIATAddress->Address);
				if (!FuncAddr)
				{
					printf("没有找到该函数");

					Sleep(2000);
					return false;
				}
				//修改IAT表
				*(DWORD*)dwIATAddress = (DWORD)FuncAddr;

			}
			else
			{
				//找到名字的地址
				printf("该函数以名字导出 名字是：%s\n", (PCHAR)pBuffer + dwIATAddress->Address + 2);
				FARPROC FuncAddr = GetProcAddress(hModule, (PCHAR)pBuffer + dwIATAddress->Address + 2);

				if (!FuncAddr)
				{
					printf("没有找到该函数");
					Sleep(2000);
					return false;
				}
				//修改IAT表
				*(DWORD*)dwIATAddress = (DWORD)FuncAddr;

			}


			dwIATAddress++;
		}
		pImportTable++;
	}


	DWORD dwJmpAddr = dwEntryOfPoint + (DWORD)pBuffer;
	_asm
	{
		jmp dwJmpAddr
	}


	getchar();
	return 0;
}

