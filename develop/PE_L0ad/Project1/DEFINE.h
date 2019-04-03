#pragma once

typedef struct _FUNC_EXPORT_TYPE
{
	DWORD Address : 31;
	DWORD Type : 1;
}FUNC_EXPORT_TYPE, *PFUNC_EXPORT_TYPE;