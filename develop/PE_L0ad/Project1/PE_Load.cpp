#include "stdafx.h"
#include "PE_Load.h"



DWORD  ReadFileToImage(const char * lpszFileName, LPVOID* pImageAddr)
{
	//用free释放此指针
	//打开文件
	if (!pImageAddr)
	{
		printf("pImageAddr为空指针");
		return false;
	}
	FILE* pFile = NULL;
	fopen_s(&pFile, lpszFileName, "rb");
	if (!pFile)
	{
		printf("文件 %s 打开失败", lpszFileName);
		return NULL;
	}
	//设置文件指针到文件尾部，使用ftell获取文件大小
	fseek(pFile, 0, SEEK_END);
	DWORD dwFileSize = ftell(pFile);
	if (dwFileSize == 0)
	{
		printf("文件大小获取失败");
		return FALSE;
	}
	fseek(pFile, 0, SEEK_SET);
	//分配存储文件映像的空间
	LPVOID pBuffer = malloc(dwFileSize);
	//读取文件
	DWORD dwReadSize = fread(pBuffer, 1, dwFileSize, pFile);
	if (dwReadSize == 0)
	{
		fclose(pFile);
		printf("文件大小获取失败");
		return FALSE;
	}
	*pImageAddr = pBuffer;
	fclose(pFile);
	return dwReadSize;
}

//Filebuffer拉伸为在内存中的状态  释放此指针用free
DWORD ImageBufferToNewBuffer(LPVOID pImageBase, LPVOID* pNewImage)
{
	if (!pNewImage || !pImageBase)
	{
		printf("pNewBuffer为NULL");
		return false;
	}
	LPVOID pOptionHeader = nullptr;
	GetPEOptionHeader(pImageBase, &pOptionHeader);
	if (!pOptionHeader)
	{
		printf("pOptionHeader为空指针");
		return FALSE;
	}

	DWORD	dwSizeOfImage = ((PIMAGE_OPTIONAL_HEADER32)pOptionHeader)->SizeOfImage;
	DWORD SizeOfHeaders = ((PIMAGE_OPTIONAL_HEADER32)pOptionHeader)->SizeOfHeaders;
	//申请空间  大小为SizeOfImage
	LPVOID pNewBuffer = malloc(dwSizeOfImage);
	//赋值为0
	ZeroMemory(pNewBuffer, dwSizeOfImage);
	//复制所有头+节表
	memcpy_s(pNewBuffer, dwSizeOfImage, pImageBase, SizeOfHeaders);
	//复制所有节里面的内容
	//读取VirtualAddress SizeOfRawData 
	LPVOID pSection = NULL;
	GetPESectionTable(pImageBase, &pSection);
	if (!pOptionHeader)
	{
		printf("pSection为空指针");
		return FALSE;
	}
	DWORD i = 0;
	DWORD dwNumberOfSection = GetNumberOfSections(pImageBase);
	while (i < dwNumberOfSection)
	{
		DWORD dwVirtualAddress = *((DWORD*)pSection + 0xc / 4 + i*SIZEOF_SECTIONHEADER / 4);
		DWORD dwSizeOfRawData = *((DWORD*)pSection + 0x10 / 4 + i*SIZEOF_SECTIONHEADER / 4);
		DWORD PointerToRawData = *((DWORD*)pSection + 0x14 / 4 + i*SIZEOF_SECTIONHEADER / 4);
		memcpy_s((char*)pNewBuffer + dwVirtualAddress, dwSizeOfImage, (char*)pImageBase + PointerToRawData, dwSizeOfRawData);
		i++;
	}
	*pNewImage = pNewBuffer;
	return dwSizeOfImage;
}

WORD   GetPEFileHeader(LPVOID  lpImageBase, LPVOID* pFileHeader)
{
	if (!lpImageBase || !pFileHeader)
	{
		printf("lpImageBase为空指针");
		return 0;
	}
	DWORD dwPEhEaderRVA = ((PIMAGE_DOS_HEADER)lpImageBase)->e_lfanew;
	DWORD* pPESegnature = (DWORD*)((char*)lpImageBase + dwPEhEaderRVA);
	WORD* FileHeader = (WORD*)(++pPESegnature);
	if (pFileHeader)
	{
		*pFileHeader = FileHeader;
	}
	return *FileHeader;
}
//获取文件的可选文件头
//参数：映像文件在内存中的基址


WORD GetPEOptionHeader(LPVOID  lpImageBase, LPVOID* pOptionHeader)
{
	if (!lpImageBase || !pOptionHeader)
	{
		printf("lpImageBase为空指针");
		return 0;
	}
	LPVOID pFileHeader = NULL;
	GetPEFileHeader(lpImageBase, &pFileHeader);
	WORD* pOption = (WORD*)pFileHeader + SIZEOF_FILEHEADER / 2;
	if (pOptionHeader)
	{
		*pOptionHeader = pOption;
	}
	return *pOption;

}

//获取节表的地址
//参数：
DWORDLONG GetPESectionTable(LPVOID  lpImageBase, LPVOID* pSecTable, DWORD dwNum)
{
	if (!lpImageBase || !pSecTable)
	{
		printf("lpImageBase为空指针");
		return 0;
	}
	LPVOID pFileHeader = NULL;
	GetPEFileHeader(lpImageBase, &pFileHeader);
	WORD wSizeOfOptionalHeader = *((WORD*)pFileHeader + 8);
	LPVOID pOptionHeader = NULL;
	GetPEOptionHeader(lpImageBase, &pOptionHeader);
	LPVOID pSectionTable = (char*)pOptionHeader + wSizeOfOptionalHeader + (dwNum - 1)*SIZEOF_SECTIONHEADER;
	if (pSecTable)
	{
		*pSecTable = pSectionTable;
	}

	return *(DWORDLONG*)pSectionTable;
}
//内存相对偏移转换为文件偏移


WORD GetNumberOfSections(LPVOID  lpImageBase)

{
	if (!lpImageBase)
	{
		printf("lpImageBase为空指针");
		return 0;
	}
	LPVOID pFileHeader = nullptr;
	GetPEFileHeader(lpImageBase, &pFileHeader);
	WORD NumberOfSection = *((WORD*)pFileHeader + 1);
	return NumberOfSection;
}



bool RelocationTable(DWORD chBaseAddress)
{
	PIMAGE_DOS_HEADER pDos = (PIMAGE_DOS_HEADER)chBaseAddress;
	PIMAGE_NT_HEADERS pNt = (PIMAGE_NT_HEADERS)(chBaseAddress + pDos->e_lfanew);
	PIMAGE_BASE_RELOCATION pLoc = (PIMAGE_BASE_RELOCATION)(chBaseAddress + pNt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_BASERELOC].VirtualAddress);

	//判断是否有重定位表
	if ((char*)pLoc == (char*)pDos)
	{
		return FALSE;
	}

	while ((pLoc->VirtualAddress + pLoc->SizeOfBlock) != 0) //开始扫描重定位表
	{
		WORD *pLocData = (WORD *)((PBYTE)pLoc + sizeof(IMAGE_BASE_RELOCATION));
		//计算需要修正的重定位项（地址）的数目
		int nNumberOfReloc = (pLoc->SizeOfBlock - sizeof(IMAGE_BASE_RELOCATION)) / sizeof(WORD);

		for (int i = 0; i < nNumberOfReloc; i++)
		{
			if ((DWORD)(pLocData[i] & 0x0000F000) == 0x00003000) //这是一个需要修正的地址
			{
				DWORD* pAddress = (DWORD *)((PBYTE)pDos + pLoc->VirtualAddress + (pLocData[i] & 0x0FFF));
				DWORD dwDelta = (DWORD)pDos - pNt->OptionalHeader.ImageBase;
				*pAddress += dwDelta;
			}
		}

		//转移到下一个节进行处理
		pLoc = (PIMAGE_BASE_RELOCATION)((PBYTE)pLoc + pLoc->SizeOfBlock);
	}

	return TRUE;
}




