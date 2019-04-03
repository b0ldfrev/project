#pragma once
//读取PE文件到内存中，如果失败返回NULL，成功则返回该PE文件在内存中的地址指针。
//参数：要读取的文件名

#define  SIZEOF_FILEHEADER 0X14
#define  SIZEOF_SECTIONHEADER 0X28


DWORD ReadFileToImage(const char * lpszFileName, LPVOID* pImageAddr);
//把映像中的PE文件写入内存文件中
//参数：待写入文件的印象的地址

DWORD ImageBufferToNewBuffer(LPVOID pImageBase, LPVOID* pNewImage);

//判断一个文件是否为PE文件，判断DOS头  与PE头的标记
//参数：要判断的文件名

WORD   GetPEFileHeader(LPVOID  lpImageBase, LPVOID* pOptionHeader = NULL);
//获取PE文件的可选文件头
WORD   GetPEOptionHeader(LPVOID  lpImageBase, LPVOID* pOptionHeader = NULL);
//获取节表
DWORDLONG   GetPESectionTable(LPVOID  lpImageBase, LPVOID* pSecHeader = NULL, DWORD dwNum = 1);

WORD GetNumberOfSections(LPVOID  lpImageBase);

bool RelocationTable(DWORD chBaseAddress);
