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
root=Tkinter.Tk()
root.geometry('800x288')
root.title('课程管理')
#------------------------------#
def addcourese():
    pp1=re.match("(^[0-9]{0,}$)",cnoenter.get())
    pp3=re.match("(^[0-9]{1}$)",creditentry.get())
    if(pp1 and pp3):
        try:
            a=cnovar.get()
            cur=conn.cursor()
            a=cur.execute('select * from course WHERE cno=%s'%a)
            print a
            if a!=0 :
                tkMessageBox.showerror(title='通知',message='插入重复')
            else :
                print cnoenter.get()+cnameentry.get()+creditentry.get()+ctimeentry.get()
                cur.execute('insert into course(cno,cname,ccredit,c_time) VALUES ("%s","%s","%d","%s")'%(cnoenter.get(),cnameentry.get(),int(creditentry.get()),ctimeentry.get()))
                conn.commit()
                cur.close()
                tkMessageBox.showinfo(title='通知',message='插入成功')
        except:
            tkMessageBox.showerror(title='失败',message='插入失败')
    else :
        tkMessageBox.showerror(title='失败',message='输入格式错误')
def showcourse():
    listboxcourse.delete(0,'end')
    cur=conn.cursor()
    a=cur.execute("select cno,cname,ccredit,c_time from course")
    b=cur.fetchall()
    cur.close()
    if a==0 :
        tkMessageBox.showerror(title="错误",message="没有信息")
    else :
        for i in b :
            result=u"课程号："+str(i[0])+u"  课程名：" +str(i[1]) +u"   学分："+str(i[2])+u"   开课时间："+str(i[3])+" "   
            print result
            listboxcourse.insert(0,result)
def deletecourse():
    selection=listboxcourse.curselection()
    if  not selection :
        tkMessageBox.showinfo(title='information',message='没有选择')
    else :
        a=listboxcourse.get(selection)
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
        cur.execute("delete from course WHERE cno=%s"%c_no)
        conn.commit()
        cur.close()
        listboxcourse.delete(selection)
        tkMessageBox.showinfo(title='通知',message='删除成功')
def findcourse():
    a=cnovar.get()
    if a:
        cur=conn.cursor()
        a=cur.execute('select cno,cname,ccredit,c_time from course WHERE cno=%s'%a)
        b=cur.fetchone()
        cur.close()
        if a ==0 :
            tkMessageBox.showerror(title='错误',message='该课程不存在')
        else:
            listboxcourse.delete(0,'end')
            result=u"课程号："+str(b[0])+u"  课程名：" +str(b[1]) +u"   学分："+str(b[2])+u"   开课时间："+str(b[3])+" "
            listboxcourse.insert(0,result)
    else :
        tkMessageBox.showerror(title='错误',message='请输入课程号')
def changecourse():
    pp1=re.match("(^[0-9]{0,}$)",cnoenter.get())
    pp3=re.match("(^[0-9]{1}$)",creditentry.get())
    if(pp1 and pp3):
        sno=cnovar.get()
        if sno:
            try:
                cur=conn.cursor()
                cur.execute("delete from course WHERE cno=%s"%sno)
                cur.execute('insert into course(cno,cname,ccredit,c_time) VALUES ("%s","%s","%d","%s")'%(cnoenter.get(),cnameentry.get(),int(creditentry.get()),ctimeentry.get()))
                tkMessageBox.showinfo(title='通知',message='修改成功')
                conn.commit()
                cur.close()
            except:
                tkMessageBox.showerror(title='错误',message='修改失败')
        else :
            tkMessageBox.showerror(title='通知',message='更新错误')
    else :
        tkMessageBox.showerror(title='失败',message='输入格式错误')
cnovar=Tkinter.StringVar(value='')
cnolabel=Tkinter.Label(root,text='课程号',justify=Tkinter.RIGHT,width=70)
cnolabel.place(x=10,y=20,width=70,height=20)
cnoenter=Tkinter.Entry(root,width=70,textvariable=cnovar)
cnoenter.place(x=80,y=20,width=70,height=20)
cnamevar=Tkinter.StringVar(value='')
cnamelabel=Tkinter.Label(root,text='课程名',justify=Tkinter.RIGHT,width=70)
cnamelabel.place(x=160,y=20,width=70,height=20)
cnameentry=Tkinter.Entry(root,width=70,textvariable=cnamevar)
cnameentry.place(x=230,y=20,width=70,height=20)
credit=(range(1,10))
creditlabel=Tkinter.Label(root,text='学分',justify=Tkinter.RIGHT,width=70)
creditlabel.place(x=310,y=20,width=70,height=20)
creditentry=ttk.Combobox(root,values=credit,width=70)
creditentry.place(x=390,y=20,width=70,height=20)
ctime=Tkinter.StringVar(value='')
ctimelabel=Tkinter.Label(root,text='开课时间',width=70,justify=Tkinter.RIGHT)
ctimelabel.place(x=480,y=20,width=70,height=20)
time=('大一上期','大一下期','大二上期','大二下期','大三上期','大三下期')
ctimeentry=ttk.Combobox(root,values=time,width=70)
ctimeentry.place(x=560,y=20,width=70,height=20)
ctime=Tkinter.StringVar(value='')
ctimeentry["state"] = "readonly"
addbutton=Tkinter.Button(root,width=70,text='添加课程',command=addcourese)
addbutton.place(x=650,y=20,width=70,height=20)
showbutton=Tkinter.Button(root,width=70,command=showcourse,text="显示课程")
showbutton.place(x=20,y=50,width=70,height=20)
deletebutton=Tkinter.Button(root,command=deletecourse,width=70,text="删除课程")
deletebutton.place(x=100,y=50,width=70,height=20)
findbutton=Tkinter.Button(root,command=findcourse,width=70,text="查找课程")
findbutton.place(x=180,y=50,width=70,height=20)
changebutton=Tkinter.Button(root,command=changecourse,width=70,text="修改课程")
changebutton.place(x=260,y=50,width=70,height=20)
listboxcourse=Tkinter.Listbox(root,width=600)
listboxcourse.place(x=20,y=70,width=600,height=100)

selectlabel=Tkinter.Label(root,width=70,text="选修管理")
selectlabel.place(x=350,y=180,width=70,height=20)
#######################选修管理
cur=conn.cursor()
cur.execute("select acaname from academy")
b=cur.fetchall()
cur.close() #获取院系号
acalabel=Tkinter.Label(root,text='院系名',justify=Tkinter.RIGHT,width=70)
acalabel.place(x=20,y=220,width=70,height=20)
acaentry=ttk.Combobox(root,values=b,width=100)
acaentry.place(x=100,y=220,width=100,height=20)
acanolabel=Tkinter.Label(root,text='学生名',justify=Tkinter.RIGHT,width=70)
acanolabel.place(x=210,y=220,width=100,height=20)
def comchange(event):
    aca=acaentry.get()
    if aca:
        cur=conn.cursor()
        print acaentry
        cur.execute('select sname from student WHERE aca_id In (select aca_id from academy WHERE acaname="%s" )'%acaentry.get())
        bb=cur.fetchall()
        cur.close()
        acaname['values']=bb
    else:
        acaname.set([])
def addscore():
    pp1=re.match(u"^[\u4e00-\u9fa5]{0,}$",acaname.get())
    pp3=re.match("(^[0-9]{1,2}$)",scoreentry.get())
    if(pp1 and pp3):
        cur=conn.cursor()
        try :
            cur.execute('select sno from student WHERE sname="%s" and aca_id IN (select aca_id from academy WHERE acaname="%s" )'%(acaname.get(),acaentry.get()))
            sn=cur.fetchone()
            sn=str(sn)
            sn=sn.split("'")[1]
            print sn
            cur.execute('select cno from course WHERE cname="%s"'%coursename.get())
            cn=cur.fetchone()
            cn=str(cn)
            cn=cn.split("'")[1]
            print cn
        except :
            tkMessageBox.showerror(title='错误',message='输入的信息有误')
        if acaname.get() and acaentry.get() :
            a=cur.execute('select * from elective WHERE  sno="%s"and cno="%s"'%(sn,cn))
            if a==0:
                p=scoreentry.get()
                if p:
                    cur.execute('insert into elective(sno,cno,grade) VALUES ("%s","%s","%d")'%(sn,cn,int(scoreentry.get())))
                else:
                    cur.execute('insert into elective(sno,cno) VALUES ("%s","%s")'%(sn,cn))
                conn.commit()
                cur.close()
                tkMessageBox.showinfo(title='通知',message="添加成功")
            else :
                tkMessageBox.showerror(title='错误',message='添加的信息已存在')
        else :
            tkMessageBox.showerror(title="通知",message='添加的信息不对')
    else :
        tkMessageBox.showerror(title='失败',message='输入格式错误')
def updatescore():
    pp1=re.match(u"^[\u4e00-\u9fa5]{0,}$",acaname.get())
    pp3=re.match("(^[0-9]{1,3}$)",scoreentry.get())
    if(pp1 and pp3):
        cur=conn.cursor()
        c=coursename.get()
        c=c.encode('utf-8')
        q=acaname.get()
        q=q.encode('utf-8')
        a=cur.execute('select cno from elective WHERE  sno in (select sno from student where sname="%s")'%q)
        b=cur.fetchall()
        aa=cur.execute('select cno from course where cname="%s"'%c)
        bb=cur.fetchall()
        if (bb[0] in b):
            try :
                cur.execute('select sno from student WHERE sname="%s" and aca_id IN (select aca_id from academy WHERE acaname="%s" )'%(acaname.get(),acaentry.get()))
                sn=cur.fetchone()
                sn=str(sn)
                sn=sn.split("'")[1]
                cur.execute('select cno from course WHERE cname="%s"'%coursename.get())
                cn=cur.fetchone()
                cn=str(cn)
                cn=cn.split("'")[1]
                cur.execute('delete from elective WHERE  sno="%s" and cno="%s"'%(sn,cn))
                cur.execute('insert into elective(sno,cno,grade) VALUES ("%s","%s","%d")'%(sn,cn,int(scoreentry.get())))
                conn.commit()
                cur.close()
                tkMessageBox.showinfo(title='通知',message='修改成功')
            except :
                tkMessageBox.showerror(title='error',message='插入失败')
        else:
            tkMessageBox.showerror(title='error',message='未找到该学生选课记录')
    else :
        tkMessageBox.showerror(title='失败',message='输入格式错误')
acaentry.bind('<<ComboboxSelected>>',comchange)
acaname=ttk.Combobox(root,width=100)
acaname.place(x=320,y=220,width=100,height=20)
acacourselabel=Tkinter.Label(root,text="课名",justify=Tkinter.RIGHT,width=70)
acacourselabel.place(x=420,y=220,width=70,height=20)
cur=conn.cursor()
cur.execute('select cname from course ')
bbb=cur.fetchall()
cur.close()
coursename=ttk.Combobox(root,width=100,values=bbb)
coursename.place(x=500,y=220,width=70,height=20)
score=tuple(range(1,101))

scorelabel=Tkinter.Label(root,text='成绩',justify=Tkinter.RIGHT,width=70)
scorelabel.place(x=580,y=220,width=70,height=20)
scoreentry=ttk.Combobox(root,width=70,values=score)
scoreentry.place(x=660,y=220,width=70,height=20)
#scoreentry["state"] = "readonly"
addbutton=Tkinter.Button(root,width=70,command=addscore,text="添加信息")
addbutton.place(x=20,y=250,width=70,height=20)
updatebutton=Tkinter.Button(root,width=70,text="修改成绩",command=updatescore)
updatebutton.place(x=100,y=250,height=20,width=70)

root.mainloop()
conn.close()
