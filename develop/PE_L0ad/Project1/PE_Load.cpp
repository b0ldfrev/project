#include "stdafx.h"
#include "PE_Load.h"



DWORD  ReadFileToImage(const char * lpszFileName, LPVOID* pImageAddr)
{
	//��free�ͷŴ�ָ��
	//���ļ�
	if (!pImageAddr)
	{
		printf("pImageAddrΪ��ָ��");
		return false;
	}
	FILE* pFile = NULL;
	fopen_s(&pFile, lpszFileName, "rb");
	if (!pFile)
	{
		printf("�ļ� %s ��ʧ��", lpszFileName);
		return NULL;
	}
	//�����ļ�ָ�뵽�ļ�β����ʹ��ftell��ȡ�ļ���С
	fseek(pFile, 0, SEEK_END);
	DWORD dwFileSize = ftell(pFile);
	if (dwFileSize == 0)
	{
		printf("�ļ���С��ȡʧ��");
		return FALSE;
	}
	fseek(pFile, 0, SEEK_SET);
	//����洢�ļ�ӳ��Ŀռ�
	LPVOID pBuffer = malloc(dwFileSize);
	//��ȡ�ļ�
	DWORD dwReadSize = fread(pBuffer, 1, dwFileSize, pFile);
	if (dwReadSize == 0)
	{
		fclose(pFile);
		printf("�ļ���С��ȡʧ��");
		return FALSE;
	}
	*pImageAddr = pBuffer;
	fclose(pFile);
	return dwReadSize;
}

//Filebuffer����Ϊ���ڴ��е�״̬  �ͷŴ�ָ����free
DWORD ImageBufferToNewBuffer(LPVOID pImageBase, LPVOID* pNewImage)
{
	if (!pNewImage || !pImageBase)
	{
		printf("pNewBufferΪNULL");
		return false;
	}
	LPVOID pOptionHeader = nullptr;
	GetPEOptionHeader(pImageBase, &pOptionHeader);
	if (!pOptionHeader)
	{
		printf("pOptionHeaderΪ��ָ��");
		return FALSE;
	}

	DWORD	dwSizeOfImage = ((PIMAGE_OPTIONAL_HEADER32)pOptionHeader)->SizeOfImage;
	DWORD SizeOfHeaders = ((PIMAGE_OPTIONAL_HEADER32)pOptionHeader)->SizeOfHeaders;
	//����ռ�  ��СΪSizeOfImage
	LPVOID pNewBuffer = malloc(dwSizeOfImage);
	//��ֵΪ0
	ZeroMemory(pNewBuffer, dwSizeOfImage);
	//��������ͷ+�ڱ�
	memcpy_s(pNewBuffer, dwSizeOfImage, pImageBase, SizeOfHeaders);
	//�������н����������
	//��ȡVirtualAddress SizeOfRawData 
	LPVOID pSection = NULL;
	GetPESectionTable(pImageBase, &pSection);
	if (!pOptionHeader)
	{
		printf("pSectionΪ��ָ��");
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
		printf("lpImageBaseΪ��ָ��");
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
//��ȡ�ļ��Ŀ�ѡ�ļ�ͷ
//������ӳ���ļ����ڴ��еĻ�ַ


WORD GetPEOptionHeader(LPVOID  lpImageBase, LPVOID* pOptionHeader)
{
	if (!lpImageBase || !pOptionHeader)
	{
		printf("lpImageBaseΪ��ָ��");
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

//��ȡ�ڱ�ĵ�ַ
//������
DWORDLONG GetPESectionTable(LPVOID  lpImageBase, LPVOID* pSecTable, DWORD dwNum)
{
	if (!lpImageBase || !pSecTable)
	{
		printf("lpImageBaseΪ��ָ��");
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
//�ڴ����ƫ��ת��Ϊ�ļ�ƫ��


WORD GetNumberOfSections(LPVOID  lpImageBase)

{
	if (!lpImageBase)
	{
		printf("lpImageBaseΪ��ָ��");
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

	//�ж��Ƿ����ض�λ��
	if ((char*)pLoc == (char*)pDos)
	{
		return FALSE;
	}

	while ((pLoc->VirtualAddress + pLoc->SizeOfBlock) != 0) //��ʼɨ���ض�λ��
	{
		WORD *pLocData = (WORD *)((PBYTE)pLoc + sizeof(IMAGE_BASE_RELOCATION));
		//������Ҫ�������ض�λ���ַ������Ŀ
		int nNumberOfReloc = (pLoc->SizeOfBlock - sizeof(IMAGE_BASE_RELOCATION)) / sizeof(WORD);

		for (int i = 0; i < nNumberOfReloc; i++)
		{
			if ((DWORD)(pLocData[i] & 0x0000F000) == 0x00003000) //����һ����Ҫ�����ĵ�ַ
			{
				DWORD* pAddress = (DWORD *)((PBYTE)pDos + pLoc->VirtualAddress + (pLocData[i] & 0x0FFF));
				DWORD dwDelta = (DWORD)pDos - pNt->OptionalHeader.ImageBase;
				*pAddress += dwDelta;
			}
		}

		//ת�Ƶ���һ���ڽ��д���
		pLoc = (PIMAGE_BASE_RELOCATION)((PBYTE)pLoc + pLoc->SizeOfBlock);
	}

	return TRUE;
}




