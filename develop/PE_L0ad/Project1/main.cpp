

#include "stdafx.h"

#include "DEFINE.h"
#include "PE_Load.h"
#define szFileName "Demo.exe"

int _tmain(int argc, _TCHAR* argv[])
{


	//��ȡĿ���ļ����ڴ� ���� ����0x400000   ��ȡ����IAT��  ��Ҫ��DLL  LOAD���� �޸�IAT�� JMP��ȥ���� 


	//��ȡ�ļ����ڴ�
	PVOID pImage = 0;
	if (!ReadFileToImage(szFileName, &pImage))
	{
		Sleep(5000);
		return -1;
	}
	PVOID pNewBuffer = 0;

	//����Ϊ����ʱ��״̬
	ImageBufferToNewBuffer(pImage, &pNewBuffer);
	//�ͷŶ�ȡʱ���ڴ�
	free(pImage);

	//��ȡImageBase��OEP
	PVOID pOptionHeader = 0;
	GetPEOptionHeader(pNewBuffer, &pOptionHeader);

	DWORD dwSizeOfImage = ((PIMAGE_OPTIONAL_HEADER)pOptionHeader)->SizeOfImage;
	DWORD dwEntryOfPoint = ((PIMAGE_OPTIONAL_HEADER)pOptionHeader)->AddressOfEntryPoint;
	DWORD dwOldImageBase = ((PIMAGE_OPTIONAL_HEADER)pOptionHeader)->ImageBase;
	PVOID  pBuffer = (PVOID)0x400000;

	//��0x400000�������ڴ�


	PVOID pAllocBuffer = VirtualAlloc(pBuffer, dwSizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

	PVOID pRelocTable = 0;
	if (!pAllocBuffer)
	{
		
		printf("��0x400000��ַ�������ڴ�ʧ�ܣ���������λ�������ڴ�\n");
		pBuffer = VirtualAlloc(0, dwSizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

	}
	//�������������������뵽��λ��
	memcpy_s(pBuffer, dwSizeOfImage, pNewBuffer, dwSizeOfImage);

	//���û�����뵽ԭ����ImageBase   �����ض�λ �Ѿ�����Ϊ�ڴ�״̬
	if ((DWORD)pBuffer != dwOldImageBase)
	{
		bool Rel=RelocationTable((DWORD)pBuffer);
		if (Rel == FALSE)
		{
			printf("�����صĳ�����ض�λ�����,�����ڱ���ʱ����δ����aslr���������ʧ�ܣ�\n");
			system("pause");
			exit(1);
		}
		

	}
	//bool ImportTable((DWORD)pBuffer);

	//���ݵ�����DLL����  ����DLL  
	//�����
	PIMAGE_IMPORT_DESCRIPTOR pImportTable = (PIMAGE_IMPORT_DESCRIPTOR)(((PIMAGE_OPTIONAL_HEADER)pOptionHeader)->DataDirectory[1].VirtualAddress + (PCHAR)pBuffer);
	HMODULE hModule = 0;
	while (pImportTable->FirstThunk &&pImportTable->OriginalFirstThunk)
	{
		hModule = LoadLibraryA(pImportTable->Name + (char*)pBuffer);
		//���������

		PFUNC_EXPORT_TYPE  dwIATAddress = (PFUNC_EXPORT_TYPE)pBuffer + pImportTable->FirstThunk / 4;
		while (*(DWORD*)dwIATAddress)
		{

			//�ж������ֵ���  ������ŵ���

			if (dwIATAddress->Type == 1)
			{
				printf("�ú�������ŵ��� ����ǣ�%d\n", dwIATAddress->Address);
				//���������
				FARPROC FuncAddr = GetProcAddress(hModule, (PCHAR)dwIATAddress->Address);
				if (!FuncAddr)
				{
					printf("û���ҵ��ú���");

					Sleep(2000);
					return false;
				}
				//�޸�IAT��
				*(DWORD*)dwIATAddress = (DWORD)FuncAddr;

			}
			else
			{
				//�ҵ����ֵĵ�ַ
				printf("�ú��������ֵ��� �����ǣ�%s\n", (PCHAR)pBuffer + dwIATAddress->Address + 2);
				FARPROC FuncAddr = GetProcAddress(hModule, (PCHAR)pBuffer + dwIATAddress->Address + 2);

				if (!FuncAddr)
				{
					printf("û���ҵ��ú���");
					Sleep(2000);
					return false;
				}
				//�޸�IAT��
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

