#-*- coding:utf-8 -*-
import MySQLdb
import os
import Tkinter
import ttk
import  tkMessageBox
import sys
import re
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
def addsan():
    pp1=re.match("(^[0-9]{0,}$)",san_nameentry.get())
    pp2=re.match(u"^[\u4e00-\u9fa5]{0,}$",san_identry.get())
    if(pp1 and pp2):
        try:
            a=san_identry.get()
            b=san_nameentry.get()
            cur=conn.cursor()
           # c=cur.execute('select * from gain WHERE  sno="%s" and san_id="%s"'%(a,b))
            c=cur.execute('select * from sanction WHERE san_id="%s"'%a)
            if c==0:
               # cur.execute('insert into gain(sno,san_id) VALUES ("%s","%s")'%(a,b))
                cur.execute('insert into sanction VALUES ("%s","%s")'%(b,a))
                conn.commit()
                cur.close()
                tkMessageBox.showinfo(title='通知',message='插入成功')
            else :
                tkMessageBox.showerror(title="错误",message="插入错误")
        except :
            tkMessageBox.showerror(title='错误',message='插入错误')
    else :
        tkMessageBox.showerror(title='错误',message='输入格式有误')
def updatesan():
    pp1=re.match("(^[0-9]{0,}$)",san_nameentry.get())
    pp2=re.match(u"^[\u4e00-\u9fa5]{0,}$",san_identry.get())
    if(pp1 and pp2):
        try:
            a=san_identry.get()
            b=san_nameentry.get()
            cur=conn.cursor()
            c=cur.execute('select * from sanction WHERE san_id="%s"'%b)
            if c!=0:
                print "z"+a
                cur.execute('delete from sanction WHERE san_id="%s"'%b)
                cur.execute('insert into sanction VALUES ("%s","%s")'%(b,a))
                conn.commit()
                cur.close()
                tkMessageBox.showinfo(title='通知',message='更新成功')
            else :
                tkMessageBox.showerror(title="错误",message="更新错误")
        except :
            tkMessageBox.showerror(title='错误',message='信息不全')
    else:
        tkMessageBox.showerror(title='错误',message='输入格式有误')
def gainstudent():
    pp=re.match("(^[0-9]{0,6}$)",acaentry.get())
    if pp:
        try :
            b=acaentry.get()
            c=xsno.get()
            cur=conn.cursor()
            d=cur.execute('select sno from gain WHERE san_id="%s" '%b)
            d=cur.fetchall()
            if d[0][0]!=c:
                cur.execute('insert into gain VALUES ("%s","%s")'%(c,b))
                conn.commit()
                cur.close()
                tkMessageBox.showinfo(title='通知',message='插入成功')
            else :
                tkMessageBox.showerror(title='错误',message='重复操作')
        except:
            tkMessageBox.showerror(title='错误',message='错误操作')
    else :
        tkMessageBox.showerror(title='错误',message='输入格式有误')
        
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
        
def deletecourse():
###
    selection=listboxgain.curselection()
    if  not selection :
        tkMessageBox.showinfo(title='information',message='没有选择')
    else :
        a=listboxgain.get(selection)
        #print a
        a=str(a).decode('utf-8')
        #print a
        a=a.split(' ')
        #print a
        aa=a[0].split("：")
        bb=a[6].split("：")
        #print aa
        #print bb
        c_no=aa[1]
        t_no=bb[1]
        print c_no
        cur=conn.cursor()
        cur.execute("delete from gain WHERE sno=%s and san_id=%s"%(c_no,t_no))
        conn.commit()
        cur.close()
        listboxgain.delete(selection)
        tkMessageBox.showinfo(title='通知',message='删除成功')
####
root=Tkinter.Tk()
root.title("奖罚修退管理")
root.geometry("800x500")
san_id=Tkinter.StringVar(value='')
san_idlabel=Tkinter.Label(root,text='奖罚名称',width=70,justify=Tkinter.RIGHT)
san_idlabel.place(x=10,y=10,width=70,height=20)
san_identry=Tkinter.Entry(root,textvariable=san_id,width=70)
san_identry.place(x=90,y=10,width=70,height=20)
san_name=Tkinter.StringVar(value='')
san_namelable=Tkinter.Label(root,width=70,text="奖罚号",justify=Tkinter.RIGHT)
san_namelable.place(x=170,y=10,width=70,height=20)
san_nameentry=Tkinter.Entry(root,width=70,textvariable=san_name)
san_nameentry.place(x=250,y=10,width=70,height=20)
addbutton=Tkinter.Button(root,width=50,command=addsan,text='添加奖罚')
updatebutton=Tkinter.Button(root,width=70,command=updatesan,text='更改奖罚')
addbutton.place(x=350,y=10,width=70,height=20)
updatebutton.place(x=450,y=10,width=70,height=20)
######学生奖罚管理
label=Tkinter.Label(root,width=70,text='学生奖惩管理',justify=Tkinter.RIGHT)
label.place(x=310,y=58,width=70,height=20)
#
snolabel=Tkinter.Label(root,width=70,text='学号',justify=Tkinter.RIGHT)
snolabel.place(x=120,y=90,width=65,height=20)
xsno=Tkinter.StringVar(value='')
tsnoentry=Tkinter.Entry(root,textvariable=xsno,width=100)
tsnoentry.place(x=170,y=90,width=80,height=20)
#
cur=conn.cursor()
cur.execute("select san_id from sanction")
b=cur.fetchall()
cur.close() 
acalabel=Tkinter.Label(root,text='奖惩号',justify=Tkinter.RIGHT,width=70)
acalabel.place(x=10,y=90,width=70,height=20)
acaentry=ttk.Combobox(root,values=b,width=100)
acaentry.place(x=80,y=90,width=45,height=20)
#
gainbutton=Tkinter.Button(root,width=100,command=gainstudent,text='奖罚')
gainbutton.place(x=260,y=90,width=80,height=20)
findgainbutton=Tkinter.Button(root,text='查找记录',command=findgain,width=70)
findgainbutton.place(x=350,y=90,width=80,height=20)
deletegainbutton=Tkinter.Button(root,text='删除记录',command=deletecourse,width=70)
deletegainbutton.place(x=450,y=90,width=80,height=20)
listboxgain=Tkinter.Listbox(root,width=600)
listboxgain.place(x=70,y=120,width=600,height=100)


#########修复转退管理
def deletexfzt():
#
    selection=listboxxfzt.curselection()
    if  not selection :
        tkMessageBox.showinfo(title='information',message='没有选择')
    else :
        a=listboxxfzt.get(selection)
        #print a
        a=str(a).decode('utf-8')
        #print a
        a=a.split(' ')
        #print a
        a=a[0].split("：")
        #print a
        c_no=a[1]
        print c_no
        cur=conn.cursor()
        cur.execute("delete from xfzt WHERE sno=%s"%c_no)
        conn.commit()
        cur.close()
        listboxxfzt.delete(selection)
        tkMessageBox.showinfo(title='通知',message='删除成功')
#

def addxfzt():
    try :
        a=xzztsnoentry.get()
        b=xzztcontententry.get()
        cur=conn.cursor()
        c=cur.execute('select * from xfzt WHERE sno="%s"'%a)
        if c==0:
            cur.execute('insert into xfzt VALUES ("%s","%s")'%(str(a),str(b)))
            conn.commit()
            cur.close()
            tkMessageBox.showinfo(title='通知',message='插入成功')
        else :
            tkMessageBox.showerror(title='错误',message='插入重复')
    except :
        tkMessageBox.showerror(title='错误',message='信息不对')
def findxfzt():
    listboxxfzt.delete(0,'end')
    try:
        a=xzztsnoentry.get()
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
xzftlabel=Tkinter.Label(root,text='修复转退管理',width=100)
xzftlabel.place(x=300,y=230,width=100,height=20)
xzztsno=Tkinter.StringVar(value='')
xzztlabel=Tkinter.Label(root,text='学号',justify=Tkinter.RIGHT,width=50)
xzztlabel.place(x=10,y=260,width=50,height=20)
xzztsnoentry=Tkinter.Entry(root,textvariable=xzztsno,width=100)
xzztsnoentry.place(x=70,y=260,width=100,height=20)
xzztcontent=Tkinter.StringVar(value='')
xzztcontentlabel=Tkinter.Label(root,text='内容',justify=Tkinter.RIGHT,width=50)
xzztcontentlabel.place(x=180,y=260,width=100,height=20)
xzztcontententry=Tkinter.Entry(root,textvariable=xzztcontent,width=150)
xzztcontententry.place(x=280,y=260,width=150,height=20)
addbutton=Tkinter.Button(root,width=70,text='增加记录',command=addxfzt)
addbutton.place(x=440,y=260,width=70,height=20)
findbutton=Tkinter.Button(root,width=70,text='查找记录',command=findxfzt)
findbutton.place(x=520,y=260,width=70,height=20)
deltebutton=Tkinter.Button(root,command=deletexfzt,width=50,text='删除记录')
deltebutton.place(x=600,y=260,width=70,height=20)

listboxxfzt=Tkinter.Listbox(root,width=600)
listboxxfzt.place(x=70,y=300,width=600,height=100)
root.mainloop()
conn.close()
