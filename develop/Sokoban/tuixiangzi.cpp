#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <conio.h>
#include<windows.h>
typedef struct
{
	char name[30];		
	char password[30];
	int check;
}info;


typedef struct
{
	int map[14][16];
}of;
void mainMenu();
void menu1();
void passwordm1(char pw[]);
void passwordm2(char pw[]);
void passwordm3(char pw[]);
int readuser(info user[]);
void printMap(int map[14][16]);	
void readMap(int map[14][16],int n);
int saveFunc(info user[], int n );
int name(info user[]);
int password(info user[],int i);
int play(of secmap[],int map[14][16],info user[],int k);
void up(int map[14][16],int i,int j);
void down(int map[14][16],int i,int j);
void left(int map[14][16],int i,int j);
void right(int map[14][16],int i,int j);

void password2(info user[],int i);
void gister(info user[],int i);

int main()
{
	of secmap[1000];
	info user[20] ;
	int sel,m,k,num;
	int map[14][16];
	mainMenu();
	
	printf("请输入您的选项: \n");
	fflush(stdin);
	sel = getch();
	putchar('\n');
	num=readuser(user);
	switch(sel)
	{
	case '1':
		gister(user,num);
		
		m=1;
		user[num].check=1;
		while(1)
		{
			readMap(map, m);
			m=play(secmap,map,user,num);
			if(m==0) 
				break;
		}
		saveFunc(user,num+1);
		break;
	case '2':
		
		
		k=name(user);
		m=password(user,k);
		menu1();
		printf("请输入您的选项: \n");
		sel = getch();
		putchar('\n');
		switch(sel)
		{
		case '1':
			while(1)
			{
				
				readMap(map, m);
				m=play(secmap,map,user,k);
				
				if(m==0) 
					break;
			}
			saveFunc(user,num);
			break;
		case '2':
			user[k].check=1;
			m=1;
			
			while(1)
			{
				readMap(map, m);
				m=play(secmap,map,user,k);
				
				if(m==0) 
					break;
			}
			saveFunc(user,num);
			break;
			saveFunc(user,num);
			break;
			
		case '3':
			
			password2(user,k);
			saveFunc(user,num);
			break;
		}
		
		
		case '3':
			return 0;
		default:
			printf("输入错误!\n");
			break;
	}
	system("pause");
	return 0;
}


void printMap(int map[][16])
{
	int i,j;
	
	for(i=0;i<14;i++)
	{
		for(j=0;j<16;j++)
		{
			switch(map[i][j])
			{
			case 0:	
				printf("  ");
				break;
			case 1:		
				printf("■");
				break;
			case 2:		
				printf("  ");
				break;
			case 3:	
				printf("×");
				break;
			case 4:		
				
				printf("◎");
				break;
			case 5:		
				printf("☆");
				break;
			case 6:	
				printf("♀");
				break;
				
			case 7:	
				printf("♀");
				break;
			}			
		}
		printf("\n");
	}	
	
}

void readMap(int map[][16],int n)
{
	FILE *fp;
	int i,j;	
	int step;
	
	fp = fopen("map.txt","r");
	
	if(fp == NULL)
	{
		printf("打开地图文件错误!\n");
		exit(1);
	}
	
	if(n<10)
		step = 257*(n-1) + 5;	
	else
		step = 257*9 + 258*(n-10) +5;
	
	fseek(fp, step, SEEK_SET);
	
	for(i=0;i<14;i++)
	{
		for(j=0;j<16;j++)
		{
			map[i][j] = fgetc(fp)-48;
		}
		fgetc(fp);	//get 10
	}
	
}


void mainMenu()
{
	printf("1.  新用户注册\n");
	printf("2.  老用户登陆\n");
	printf("3.  退出游戏\n");
	printf("------------------------------\n");
}


void menu1()
{
	printf("1.  继续游戏\n");
	printf("2.  重新开始游戏\n");
	printf("3.  修改密码\n");
	printf("------------------------------\n");
}

int readuser(info user[])
{
	int i;
	FILE *fp;
	fp = fopen("users.txt", "r");
	if(fp == NULL)
	{
		printf("打开用户文件错误!\n");
		exit(1);
	}
	for(i=0; !feof(fp); i++)
	{
		if(fscanf(fp, "%s%s%d", user[i].name, user[i].password,&user[i].check) == EOF)
			break;
	}
	fclose(fp);
	return i;
	
	
}


int saveFunc(info user[], int n )
{
	int i;
	FILE *fp = fopen("users.txt", "w");	
	if(fp == NULL)
		return -1;
	for(i=0; i<n; i++)
		fprintf(fp, "%s %s %d ", user[i].name, user[i].password, user[i].check);
	fclose(fp);
	return 0;
}







int name(info user[])
{
	int i,c=0;
	char n[30];
	while(1)
	{
		printf("请输入用户名:");
		scanf("%s",n);
		for(i=0;i<10;i++)
		{
			if(strcmp(n,user[i].name)==0)
			{
				return	i;
				c++;
				break;
			}
		}
		
		if(c==0)	
		{
			printf("没有发现用户名，请重新输入!\n");
			continue; 
		}
	}
	
}



void password2(info user[],int i)
{
	char a[30];
	char b[30];
	int j=0;
	
	while(1)
	{
		
		
		
		passwordm2(a);
		
		passwordm3(b);
		if(strcmp(a,b)==0)
			break;
		else
		{
			printf("\n两次输入的密码不一致，请重新输入!\n");
			while(a[j++]!='\0')
				a[j-1]='\0';
			j=0;
			while(b[j++]!='\0')
				b[j-1]='\0';
		}
	}
	j=0;
	while(user[i].password[j++]!='\0')
		user[i].password[j-1]='\0';
	memcpy(user[i].password,a,sizeof(a));
	
	printf("\n修改密码成功\n");
}



void gister(info user[],int i)
{
	char a[30],b[30],c[30];
	int j=0;
    
	
	printf("请输入用户名:");
	gets(c);
	memcpy(user[i].name,c,sizeof(c));
	
	
	while(1)
	{
		
		
		
		passwordm2(a);
		
		passwordm3(b);
		if(strcmp(a,b)==0)
			break;
		else
		{
			printf("\n两次输入的密码不一致，请重新输入!\n");
			while(a[j++]!='\0')
				a[j-1]='\0';
			j=0;
			while(b[j++]!='\0')
				b[j-1]='\0';
		}
	}
	memcpy(user[i].password,a,sizeof(a));
	
	printf("\n注册成功，按任意键继续.....\n");
	getch();
	
}



void passwordm1(char pw[])
{
	char ch;
	int i;
	printf("\r\n请输入密码:");
    i=0;pw[i]=0;
    while (1) {
        ch=getch();
        if (ch==13 || i>=39) break;
        switch (ch) {
        case 27:
            printf("\r请输入密码: %40s"," ");
            printf("\r请输入密码: ");
            i=0;pw[i]=0;
            break;
        case 8:
            if (i>0) {
                i--;
                pw[i]=0;
                printf("\b \b");
            }
            break;
        default:
            pw[i]=ch;
            i++;
            pw[i]=0;
            printf("*");
            break;
        }
    }
    printf("\r\n");
	
}


void passwordm2(char pw[])
{
	char ch;
	int i;
	printf("\r\n请输入新密码:");
    i=0;pw[i]=0;
    while (1) {
        ch=getch();
        if (ch==13 || i>=39) break;
        switch (ch) {
        case 27:
            printf("\r请输入新密码: %40s"," ");
            printf("\r请输入新密码: ");
            i=0;pw[i]=0;
            break;
        case 8:
            if (i>0) {
                i--;
                pw[i]=0;
                printf("\b \b");
            }
            break;
        default:
            pw[i]=ch;
            i++;
            pw[i]=0;
            printf("*");
            break;
        }
    }
    printf("\r\n");
	
}

void passwordm3(char pw[])
{
	char ch;
	int i;
	printf("\r\n请再次输入新密码:");
    i=0;pw[i]=0;
    while (1) {
        ch=getch();
        if (ch==13 || i>=39) break;
        switch (ch) {
        case 27:
            printf("\r请再次输入新密码: %40s"," ");
            printf("\r请再次输入新密码: ");
            i=0;pw[i]=0;
            break;
        case 8:
            if (i>0) {
                i--;
                pw[i]=0;
                printf("\b \b");
            }
            break;
        default:
            pw[i]=ch;
            i++;
            pw[i]=0;
            printf("*");
            break;
        }
    }
    printf("\r\n");
	
	
	
}







int password(info user[],int i)
{
	char pw[30],ch;
	while(1)
	{	
		
		passwordm1(pw);
		
		if(strlen(pw)>12)
		{
			printf("\n密码格式错误!请重新输入\n");
			continue;
		}
		
		else if(strcmp(pw,user[i].password)==0)
			return (user[i].check);
		else
		{
			printf("\n密码错误!请重新输入\n");
			continue; 
		}
		
	}
}


int play(of secmap[],int map[][16],info user[],int k)  
{
	
	int i,j,z=-1,c=0;
	int q=0,e,l=0;
	char input;
	
	
	
	
	
	for(i=0;i<14;i++)
		for(j=0;j<16;j++)
		{
			if(map[i][j]==3||map[i][j]==5)
				
				q++;
		}
		
		
		
		while(1)
			
		{ fflush(stdin);
		system("CLS");
		printf("    控制方向：w上 s下 a左 d右\n    r：悔步（最多3次）\n    e：退出并保存\n    t: 重新开始当前关卡\n");
		printMap(map);
		
		for(i=0,e=0;i<14;i++)
			for(j=0;j<16;j++)
			{
				if(map[i][j]==5)
					e++;
				
			}
			
			if(e==q)
				break;
			z++;
			for(i=0;i<14;i++)
				for(j=0;j<16;j++)
					secmap[z].map[i][j]=map[i][j];
				
				for (i=0;i<14;i++)  
				{  
					for (j=0;j<16;j++)  
					{  
						if (map[i][j]==6||map[i][j]==7)  
							break;  
					}  
					if (map[i][j]==6||map[i][j]==7)  
						break;
				}
				
				
				
				
				
				
				input=getch();
				if(input!='r')
					c=0;
				
				switch (input)  
				{  
				case 'w':  
					
					up(map,i,j);
					break;
					
					
				case 's':  
					
					down(map,i,j);
					break;
					
					
				case 'a':  
					
					left(map,i,j);
					break;
					
					
					
					
				case 'd':  
					
					right(map,i,j);
					break;
					
					
				case 'e':
					return 0;
					
				case 't':
					c=0;
					l=0;
					for(i=0;i<14;i++)
						for(j=0;j<16;j++)
							map[i][j]=secmap[0].map[i][j];
						
						break;
						
						
						
				case 'r':
					c++;
					l++;
					
					
					if(c>=4||l>=4)
					{
						printf("最多只能悔3步! \n按任意键继续");
						getch();
						
						break;
						
					}
					
					
					if(c==1)
					{
						for(i=0;i<14;i++)
							for(j=0;j<16;j++)
								map[i][j]=secmap[z-1].map[i][j];
					}
					
					if(c==2&&z>2)
					{
						for(i=0;i<14;i++)
							for(j=0;j<16;j++)
								map[i][j]=secmap[z-3].map[i][j];
					}
					
					if(c==3&&z>4)
					{
						for(i=0;i<14;i++)
							for(j=0;j<16;j++)
								map[i][j]=secmap[z-5].map[i][j];
					}
					break;
					
					
					
					
					
					
					
				}
				
				
				
				
				
				
}


printf("\n恭喜你，过关了 按任意键继续\n");
getch();
system("CLS");
return (++user[k].check);
}


void up(int map[14][16],int i,int j)
{ 
	
	if(map[i-1][j]==2)  //kong
	{  
		if(map[i][j]==7)
		{
			map[i-1][j]=6; 
			map[i][j]=3;
		}
		else {   
			map[i-1][j]=6; 
			map[i][j]=2;
		}
	}
	
	
	if(map[i-1][j]==4)   //xiangzi
		
	{
		if(map[i][j]==6)
		{
			if(map[i-2][j]==3)
			{
				map[i-2][j]=5;
				map[i-1][j]=6;
				map[i][j]=2;
			}
			else if(map[i-2][j]==2)
			{
				map[i-2][j]=4;
				map[i-1][j]=6;
				map[i][j]=2;
			}
		}
		else if(map[i][j]==7)
			
		{
			if(map[i-2][j]==3)
			{
				map[i-2][j]=5;
				map[i-1][j]=6;
				map[i][j]=3;
			}
			else if(map[i-2][j]==2)
			{
				map[i-2][j]=4;
				map[i-1][j]=6;
				map[i][j]=3;
			}
		}
		
	}
	
	
	
	
	if(map[i-1][j]==5)  //xiangzidaoda
	{
		if(map[i][j]==7)
			
		{
			if(map[i-2][j]==3)
			{
				map[i-2][j]=5;
				map[i-1][j]=7;
				map[i][j]=3;
			}
			else if(map[i-2][j]==2)
			{
				map[i-2][j]=4;
				map[i-1][j]=7;
				map[i][j]=3;
			}
			
		}
		
		
		else if(map[i][j]==6)
			
		{
			if(map[i-2][j]==3)
			{
				map[i-2][j]=5;
				map[i-1][j]=7;
				map[i][j]=2;
			}
			else if(map[i-2][j]==2)
			{
				map[i-2][j]=4;
				map[i-1][j]=7;
				map[i][j]=2;
			}
			
		}
		
	}
	
	
	if(map[i-1][j]==3)  //zhidingweizhi
		
	{
		if(map[i][j]==6)
		{
			map[i-1][j]=7;
			map[i][j]=2;
		}
		else if(map[i][j]==7)
		{
			map[i-1][j]=7;
			map[i][j]=3;
		}
	}
	
	
	
	
	
}


void down( int map[14][16],int i,int j)
{
	
	if(map[i+1][j]==2)  //kong
	{  
		if(map[i][j]==7)
		{
			map[i+1][j]=6; 
			map[i][j]=3;
		}
		else {   
			map[i+1][j]=6; 
			map[i][j]=2;
		}
	}
	
	
	if(map[i+1][j]==4)   //xiangzi
		
	{
		if(map[i][j]==6)
		{
			if(map[i+2][j]==3)
			{
				map[i+2][j]=5;
				map[i+1][j]=6;
				map[i][j]=2;
			}
			else if(map[i+2][j]==2)
			{
				map[i+2][j]=4;
				map[i+1][j]=6;
				map[i][j]=2;
			}
		}
		else if(map[i][j]==7)
			
		{
			if(map[i+2][j]==3)
			{
				map[i+2][j]=5;
				map[i+1][j]=6;
				map[i][j]=3;
			}
			else if(map[i+2][j]==2)
			{
				map[i+2][j]=4;
				map[i+1][j]=6;
				map[i][j]=3;
			}
		}
		
	}
	
	
	
	
	if(map[i+1][j]==5)  //xiangzidaoda
	{
		if(map[i][j]==7)
			
		{
			if(map[i+2][j]==3)
			{
				map[i+2][j]=5;
				map[i+1][j]=7;
				map[i][j]=3;
			}
			else if(map[i+2][j]==2)
			{
				map[i+2][j]=4;
				map[i+1][j]=7;
				map[i][j]=3;
			}
			
		}
		
		
		else if(map[i][j]==6)
			
		{
			if(map[i+2][j]==3)
			{
				map[i+2][j]=5;
				map[i+1][j]=7;
				map[i][j]=2;
			}
			else if(map[i+2][j]==2)
			{
				map[i+2][j]=4;
				map[i+1][j]=7;
				map[i][j]=2;
			}
			
		}
		
	}
	
	
	if(map[i+1][j]==3)  //zhidingweizhi
		
	{
		if(map[i][j]==6)
		{
			map[i+1][j]=7;
			map[i][j]=2;
		}
		else if(map[i][j]==7)
		{
			map[i+1][j]=7;
			map[i][j]=3;
		}
	}
	
	
}



void left(int map[14][16],int i,int j)
{
	
	if(map[i][j-1]==2)  //kong
	{  
		if(map[i][j]==7)
		{
			map[i][j-1]=6; 
			map[i][j]=3;
		}
		else {   
			map[i][j-1]=6; 
			map[i][j]=2;
		}
	}
	
	
	if(map[i][j-1]==4)   //xiangzi
		
	{
		if(map[i][j]==6)
		{
			if(map[i][j-2]==3)
			{
				map[i][j-2]=5;
				map[i][j-1]=6;
				map[i][j]=2;
			}
			else if(map[i][j-2]==2)
			{
				map[i][j-2]=4;
				map[i][j-1]=6;
				map[i][j]=2;
			}
		}
		else if(map[i][j]==7)
			
		{
			if(map[i][j-2]==3)
			{
				map[i][j-2]=5;
				map[i][j-1]=6;
				map[i][j]=3;
			}
			else if(map[i][j-2]==2)
			{
				map[i][j-2]=4;
				map[i][j-1]=6;
				map[i][j]=3;
			}
		}
		
	}
	
	
	
	
	if(map[i][j-1]==5)  //xiangzidaoda
	{
		if(map[i][j]==7)
			
		{
			if(map[i][j-2]==3)
			{
				map[i][j-2]=5;
				map[i][j-1]=7;
				map[i][j]=3;
			}
			else if(map[i][j-2]==2)
			{
				map[i][j-2]=4;
				map[i][j-1]=7;
				map[i][j]=3;
			}
			
		}
		
		
		else if(map[i][j]==6)
			
		{
			if(map[i][j-2]==3)
			{
				map[i][j-2]=5;
				map[i][j-1]=7;
				map[i][j]=2;
			}
			else if(map[i][j-2]==2)
			{
				map[i][j-2]=4;
				map[i][j-1]=7;
				map[i][j]=2;
			}
			
		}
		
	}
	
	
	if(map[i][j-1]==3)  //zhidingweizhi
		
	{
		if(map[i][j]==6)
		{
			map[i][j-1]=7;
			map[i][j]=2;
		}
		else if(map[i][j]==7)
		{
			map[i][j-1]=7;
			map[i][j]=3;
		}
	}
	
	
}



void right(int map[14][16],int i, int j)
{
	
	if(map[i][j+1]==2)  //kong
	{  
		if(map[i][j]==7)
		{
			map[i][j+1]=6; 
			map[i][j]=3;
		}
		else {   
			map[i][j+1]=6; 
			map[i][j]=2;
		}
	}
	
	
	if(map[i][j+1]==4)   //xiangzi
		
	{
		if(map[i][j]==6)
		{
			if(map[i][j+2]==3)
			{
				map[i][j+2]=5;
				map[i][j+1]=6;
				map[i][j]=2;
			}
			else if(map[i][j+2]==2)
			{
				map[i][j+2]=4;
				map[i][j+1]=6;
				map[i][j]=2;
			}
		}
		else if(map[i][j]==7)
			
		{
			if(map[i][j+2]==3)
			{
				map[i][j+2]=5;
				map[i][j+1]=6;
				map[i][j]=3;
			}
			else if(map[i][j+2]==2)
			{
				map[i][j+2]=4;
				map[i][j+1]=6;
				map[i][j]=3;
			}
		}
		
	}
	
	
	
	
	if(map[i][j+1]==5)  //xiangzidaoda
	{
		if(map[i][j]==7)
			
		{
			if(map[i][j+2]==3)
			{
				map[i][j+2]=5;
				map[i][j+1]=7;
				map[i][j]=3;
			}
			else if(map[i][j+2]==2)
			{
				map[i][j+2]=4;
				map[i][j+1]=7;
				map[i][j]=3;
			}
			
		}
		
		
		else if(map[i][j]==6)
			
		{
			if(map[i][j+2]==3)
			{
				map[i][j+2]=5;
				map[i][j+1]=7;
				map[i][j]=2;
			}
			else if(map[i][j+2]==2)
			{
				map[i][j+2]=4;
				map[i][j+1]=7;
				map[i][j]=2;
			}
			
		}
		
	}
	
	
	if(map[i][j+1]==3)  //zhidingweizhi
		
	{
		if(map[i][j]==6)
		{
			map[i][j+1]=7;
			map[i][j]=2;
		}
		else if(map[i][j]==7)
		{
			map[i][j+1]=7;
			map[i][j]=3;
		}
	}
	
	
}












