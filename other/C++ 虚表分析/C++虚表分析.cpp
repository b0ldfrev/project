#include <iostream> 
#include <cstring>
#include <cstdlib>
using namespace std;

class A{
public:
int a;
virtual void  print()
{
cout<<"This is class A"<<endl;
}

};


class B:public A{

public:
int b;
virtual void  print()
{
cout<<"This is class B"<<endl;
}


};

int main()

{
A *a=new A;
A *b=new B;
a->print();
b->print();
return 0;

}
