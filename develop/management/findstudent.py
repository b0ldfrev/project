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
def showscore():
    cur=conn.cursor()
    listboxteacher.delete(0,'end')
    a=cnameentry.get()
    cur.execute('select cno from course WHERE cname="%s"'%a)
    a=cur.fetchall()
    a=a[0][0]
    b=upentry.get()
    c=downentry.get()
    try :
        cur.execute('select mno from major WHERE mname="%s"'%mnameentry.get())
        t=cur.fetchall()
        print t
        t=t[0][0]
        e=cur.execute('select student.sno,student.sname,elective.grade  from elective,course,student,major WHERE course.cno=elective.cno and major.aca_id=student.aca_id and  student.mno =major.mno and course.cno="%s" and elective.sno=student.sno and student.mno="%s" and student.mtime="%s" and elective.grade  BETWEEN %d AND %d order by elective.grade asc'%(str(a),t,timeclass.get(),int(c),int(b)))
        d=cur.fetchall()
        counts.set(str(e))
        per=cur.execute('select student.sno,student.sname,major.mname,elective.grade  from elective,course,student,major WHERE course.cno=elective.cno and major.aca_id=student.aca_id and  student.mno =major.mno and course.cno="%s" and elective.sno=student.sno and student.mno="%s" and student.mtime="%s" and elective.grade  BETWEEN %d AND %d order by elective.grade asc'%(str(a),t,timeclass.get(),0,100))
        cur.close()
        percent=float(e)/float(per)
        percent=round(percent,2)
        percent=percent*100
        percent=str(percent)
        percent+='%'
        varper.set(percent)
        if e==0:
            tkMessageBox.showinfo(title='通知',message='没有信息')
        else:
            for d in d:
                result='学号：'+str(d[0])+'  姓名：'+str(d[1])+'  分数：'+str(d[2])
                listboxteacher.insert(0,result)
    except :
         tkMessageBox.showinfo(title='通知',message='没有')
root=Tkinter.Tk()
root.geometry("750x750")
root.title('成绩查询')
######
majorbael=Tkinter.Label(root,width=70,text='专业',justify=Tkinter.RIGHT)
majorbael.place(x=10,y=20,width=60,height=20)
cur=conn.cursor()
cur.execute('select mname from major')
mname=cur.fetchall()
cur.close()
mnameentry=ttk.Combobox(root,values=mname,width=100)
mnameentry.place(x=75,y=20,width=100,height=20)
mnameentry["state"] = "readonly"

stime=tuple(range(1970,2050))
timelabel=Tkinter.Label(root,text='年级',width=50,justify=Tkinter.RIGHT)
timelabel.place(x=15,y=50,width=50,height=20)
timeclass=ttk.Combobox(root,value=stime,width=70)
timeclass.place(x=75,y=50,width=60,height=20)
timeclass["state"] = "readonly"
####
classbael=Tkinter.Label(root,width=70,text='课程名',justify=Tkinter.RIGHT)
classbael.place(x=180,y=20,width=70,height=20)
cur=conn.cursor()
cur.execute('select distinct(course.cname) from elective,course WHERE course.cno=elective.cno')
cname=cur.fetchall()
cur.close()
cnameentry=ttk.Combobox(root,values=cname,width=100)
cnameentry.place(x=250,y=20,width=100,height=20)
cnameentry["state"] = "readonly"
uplabel=Tkinter.Label(root,text='分数下限',width=70,justify=Tkinter.RIGHT)
uplabel.place(x=370,y=20,width=70,height=20)
downentry=ttk.Combobox(root,values=tuple(range(0,101)),width=50)
downentry.place(x=450,y=20,width=50,height=20)
downlabel=Tkinter.Label(root,text='分数上限',width=70,justify=Tkinter.RIGHT)
downlabel.place(x=510,y=20,width=70,height=20)
upentry=ttk.Combobox(root,values=tuple(range(0,101)),width=50)
upentry.place(x=590,y=20,width=50,height=20)
showscorebutton=Tkinter.Button(root,text='显示成绩',width=70,command=showscore)
showscorebutton.place(x=190,y=50,width=70,height=20)
countlabel=Tkinter.Label(root,text='数量',width=50,justify=Tkinter.RIGHT)
countlabel.place(x=270,y=50,height=20,width=70)
percentlabel=Tkinter.Label(root,text='百分比',width=50,justify=Tkinter.RIGHT)
percentlabel.place(x=400,y=50,height=20,width=70)
varper=Tkinter.StringVar(value="")
percententry=Tkinter.Entry(root,width=50,textvariable=varper)
percententry.place(x=470,y=50,width=50,height=20)
counts=Tkinter.StringVar(value='')
countentry=Tkinter.Entry(root,textvariable=counts,width=50)
countentry.place(x=340,y=50,height=20,width=50)
listboxteacher=Tkinter.Listbox(root,width=600)
listboxteacher.place(x=20,y=100,width=650,height=335)
listboxgrade=Tkinter.Listbox(root,width=600)
listboxgrade.place(x=20,y=500,width=650,height=170)
################################################
cur=conn.cursor()
cur.execute("select acaname from academy")
b=cur.fetchall()
cur.close() #获取院系号
acalabel=Tkinter.Label(root,text='院系名',justify=Tkinter.RIGHT,width=70)
acalabel.place(x=20,y=470,width=70,height=20)
acaentry=ttk.Combobox(root,values=b,width=100)
acaentry.place(x=80,y=470,width=100,height=20)
acanolabel=Tkinter.Label(root,text='学生名',justify=Tkinter.RIGHT,width=70)
acanolabel.place(x=180,y=470,width=70,height=20)
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
acaentry.bind('<<ComboboxSelected>>',comchange)
acaname=ttk.Combobox(root,width=100)
acaname.place(x=240,y=470,width=75,height=20)
acacourselabel=Tkinter.Label(root,text="学号",justify=Tkinter.RIGHT,width=70)
acacourselabel.place(x=318,y=470,width=55,height=20)
#
courseno=Tkinter.StringVar(value="")
cnoentry=Tkinter.Entry(root,width=100,textvariable=courseno)
cnoentry.place(x=360,y=470,width=85,height=20)
#
ctimelabel=Tkinter.Label(root,text='学期',width=70,justify=Tkinter.RIGHT)
ctimelabel.place(x=450,y=470,width=50,height=20)
time=('大一上期','大一下期','大二上期','大二下期','大三上期','大三下期')
ctimeentry=ttk.Combobox(root,values=time,width=70)
ctimeentry.place(x=495,y=470,width=73,height=20)
ctimeentry["state"] = "readonly"
#
findcorebutton=Tkinter.Button(root,text='查询成绩',width=70,command=find)
findcorebutton.place(x=588,y=467,width=80,height=24)

#################################################
root.mainloop()
