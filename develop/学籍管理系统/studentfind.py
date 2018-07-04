#-*- coding:utf-8 -*-
import Tkinter
import ttk
import  tkMessageBox
import sys
import MySQLdb
import types
reload(sys)
sys.setdefaultencoding('utf-8')
conn=MySQLdb.connect(
    user='root',
    port=3306,
    passwd='123456',
    host='localhost',
    db='student_database',
    charset='utf8'
)

root=Tkinter.Tk()
root.geometry("690x640")
root.title('学生查询')
title=Tkinter.Label(root,text='成绩查询',width=70,justify=Tkinter.RIGHT)
title.place(x=295,y=10,width=70,height=20)
listboxgrade=Tkinter.Listbox(root,width=600)
listboxgrade.place(x=20,y=80,width=650,height=170)
################################################

acanolabel=Tkinter.Label(root,text='学生名',justify=Tkinter.RIGHT,width=70)
acanolabel.place(x=20,y=50,width=70,height=20)

def find():
    try :
        cur=conn.cursor()
        cur.execute('select sno from student WHERE sname="%s"'%acaname.get())
        b=cur.fetchall()
        if courseno.get()==b[0][0] :
            a=cur.execute('select course.cname,elective.grade from elective,course WHERE course.cno=elective.cno and elective.sno="%s" and course.c_time="%s"'%(courseno.get(),ctimeentry.get()))
            aa=cur.fetchall()
            cur.close()
            listboxgrade.delete(0,'end')
            for aa in aa:
                result='课程名：'+str(aa[0])+'    分数：'+str(aa[1])
                listboxgrade.insert(0,result)
        else :
            tkMessageBox.showinfo(title='通知',message='信息不匹配')
    except :
        tkMessageBox.showinfo(title='通知',message='输入错误')
acaname=Tkinter.StringVar(value="")
cnoentry=Tkinter.Entry(root,width=100,textvariable=acaname)
cnoentry.place(x=80,y=50,width=75,height=20)

acacourselabel=Tkinter.Label(root,text="学号",justify=Tkinter.RIGHT,width=70)
acacourselabel.place(x=158,y=50,width=55,height=20)
#acaname
courseno=Tkinter.StringVar(value="")
cnoentry=Tkinter.Entry(root,width=100,textvariable=courseno)
cnoentry.place(x=200,y=50,width=85,height=20)
#
ctimelabel=Tkinter.Label(root,text='学期',width=70,justify=Tkinter.RIGHT)
ctimelabel.place(x=290,y=50,width=50,height=20)
time=('大一上期','大一下期','大二上期','大二下期','大三上期','大三下期')
ctimeentry=ttk.Combobox(root,values=time,width=70)
ctimeentry.place(x=335,y=50,width=73,height=20)
ctimeentry["state"] = "readonly"
#
findcorebutton=Tkinter.Button(root,text='查询成绩',width=70,command=find)
findcorebutton.place(x=435,y=47,width=80,height=24)

#################################################奖罚查询
def findgain():
    listboxgain.delete(0,'end')
    a=xsno.get()
    cur=conn.cursor()
    print "a"
    a=cur.execute('select gain.sno,student.sname,sanction.san_id,sanction.san_name from gain,sanction,student WHERE gain.san_id=sanction.san_id and gain.sno=student.sno and gain.sno="%s"'%a)
    print "b"
    b=cur.fetchall()
    print "c"
    cur.close()
    print b
    if b:
        for i in b :
            result=u"学号：" +str(i[0])+u"   姓名："+str(i[1])+"   奖罚号："+str(i[2])+"   奖罚名称："+str(i[3])
            listboxgain.insert(0,result)
    else :
        tkMessageBox.showinfo(title='information',message='未找到记录')
title2=Tkinter.Label(root,text='奖罚查询',width=70,justify=Tkinter.RIGHT)
title2.place(x=295,y=270,width=70,height=20)
snolabel=Tkinter.Label(root,width=60,text='学号',justify=Tkinter.RIGHT)
snolabel.place(x=20,y=300,width=65,height=20)
xsno=Tkinter.StringVar(value='')
tsnoentry=Tkinter.Entry(root,textvariable=xsno,width=100)
tsnoentry.place(x=90,y=300,width=80,height=20)

findgainbutton=Tkinter.Button(root,text='查找记录',command=findgain,width=70)
findgainbutton.place(x=190,y=295,width=80,height=28)
listboxgain=Tkinter.Listbox(root,width=600)
listboxgain.place(x=20,y=330,width=650,height=100)
######修复转退查询
def findxfzt():
    listboxxfzt.delete(0,'end')
    try:
        a=xsno2.get()
        cur=conn.cursor()
        b=cur.execute('select * from xfzt WHERE sno="%s"'%a)
        if b==0:
            tkMessageBox.showerror(title='错误',message='没有信息')
        else :
            cur.execute("select student.sno,student.sname,xfzt.xfzt from student,xfzt WHERE student.sno=xfzt.sno and student.sno='%s'" %a)
            c=cur.fetchall()
            cur.close()
            for c in c:
                result=u'学号：'+str(c[0])+'  姓名：'+str(c[1])+'  状态：'+str(c[2])
                listboxxfzt.insert(0,result)

    except:
        tkMessageBox.showerror(title='错误',message='信息不对')
title3=Tkinter.Label(root,text='修复转退查询',width=70,justify=Tkinter.RIGHT)
title3.place(x=295,y=451,width=70,height=20)
snolabel2=Tkinter.Label(root,width=60,text='学号',justify=Tkinter.RIGHT)
snolabel2.place(x=20,y=485,width=65,height=20)
xsno2=Tkinter.StringVar(value='')
tsnoentry=Tkinter.Entry(root,textvariable=xsno2,width=100)
tsnoentry.place(x=90,y=485,width=80,height=20)
findgainbutton=Tkinter.Button(root,text='查找记录',command=findxfzt,width=70)
findgainbutton.place(x=190,y=482,width=80,height=28)
listboxxfzt=Tkinter.Listbox(root,width=600)
listboxxfzt.place(x=20,y=515,width=650,height=100)
root.mainloop()
