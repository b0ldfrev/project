#include<stdio.h>
#include<windows.h>

void test()
{
char tt[10];
char p[20];
gets(p);
strcpy(tt,p);
puts(tt);
} 
int main()
{
test();
return 0;
}