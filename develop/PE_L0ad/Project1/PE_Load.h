#pragma once
//��ȡPE�ļ����ڴ��У����ʧ�ܷ���NULL���ɹ��򷵻ظ�PE�ļ����ڴ��еĵ�ַָ�롣
//������Ҫ��ȡ���ļ���

#define  SIZEOF_FILEHEADER 0X14
#define  SIZEOF_SECTIONHEADER 0X28


DWORD ReadFileToImage(const char * lpszFileName, LPVOID* pImageAddr);
//��ӳ���е�PE�ļ�д���ڴ��ļ���
//��������д���ļ���ӡ��ĵ�ַ

DWORD ImageBufferToNewBuffer(LPVOID pImageBase, LPVOID* pNewImage);

//�ж�һ���ļ��Ƿ�ΪPE�ļ����ж�DOSͷ  ��PEͷ�ı��
//������Ҫ�жϵ��ļ���

WORD   GetPEFileHeader(LPVOID  lpImageBase, LPVOID* pOptionHeader = NULL);
//��ȡPE�ļ��Ŀ�ѡ�ļ�ͷ
WORD   GetPEOptionHeader(LPVOID  lpImageBase, LPVOID* pOptionHeader = NULL);
//��ȡ�ڱ�
DWORDLONG   GetPESectionTable(LPVOID  lpImageBase, LPVOID* pSecHeader = NULL, DWORD dwNum = 1);

WORD GetNumberOfSections(LPVOID  lpImageBase);

bool RelocationTable(DWORD chBaseAddress);
