#-*- coding:utf-8 -*-
import Tkinter
import ttk
import  tkMessageBox
import sys
import MySQLdb
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

teachroot=Tkinter.Tk()
teachroot.title('院系专业管理')
teachroot.geometry('680x500')

# 院系处理

def addaca():
    pp1=re.match("(^[0-9]{0,}$)",varaca_id.get())
    pp2=re.match(u"^[\u4e00-\u9fa5]{0,}$",acaname.get())
    pp3=re.match(u"^[\u4e00-\u9fa5]{0,}$",acamana.get())
    if(pp1 and pp2 and pp3):
        try :
            cur=conn.cursor()
            a=cur.execute('select * from academy WHERE aca_id =%s'%varaca_id.get())
            if a==0:
                cur.execute('insert into academy(aca_id,acaname,aca_mana) VALUES ("%s","%s","%s")'%(varaca_id.get(),acaname.get(),acamana.get()))
                conn.commit()
                cur.close()
                tkMessageBox.showinfo(title='通知',message='插入成功')
            else :
                tkMessageBox.showerror(title='错误',message='插入重复')
        except :
            tkMessageBox.showerror(title='错误',message='插入失败')
    else :
        tkMessageBox.showerror(title='错误',message='输入格式错误')
def showacademy():
    listboxacademy.delete(0,'end')
    cur=conn.cursor()
    a=cur.execute('select * from academy')
    b=cur.fetchall()
    cur.close()
    if a==0:
        tkMessageBox.showerror(title='通知',message='没有学院信息')
    else:
        for i in b:
            result=u'院系号：'+str(i[0])+u'   院系名称：'+str(i[1])+'   系主任姓名：'+ str(i[2])
            listboxacademy.insert(0,result)
def deleteacademy():
    ###
    selection=listboxacademy.curselection()
    if  not selection :
        tkMessageBox.showinfo(title='information',message='没有选择')
    else :
        a=listboxacademy.get(selection)
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
        cur.execute("delete from academy WHERE aca_id=%s"%c_no)
        conn.commit()
        cur.close()
        listboxacademy.delete(selection)
        tkMessageBox.showinfo(title='通知',message='删除成功')
        #######
acamy=Tkinter.Label(teachroot,text='院系管理',width=80,height=30)
acamy.place(x=270,y=20,width=80,height=30)
varaca_id=Tkinter.StringVar(value='')
aca_idlabel=Tkinter.Label(teachroot,text='院系号',justify=Tkinter.RIGHT,width=50)
aca_idlabel.place(x=10,y=60,width=50,height=20)
acaidentry=Tkinter.Entry(teachroot,width=70,textvariable=varaca_id)
acaidentry.place(x=70,y=60,width=70,height=20)
acaname=Tkinter.StringVar(value='')
acanamelabel=Tkinter.Label(teachroot,text='院系名称',width=70,justify=Tkinter.RIGHT)
acanamelabel.place(x=160,y=60,width=70,height=20)
acanameentry=Tkinter.Entry(teachroot,width=70,textvariable=acaname)
acanameentry.place(x=250,y=60,width=70,height=20)
acamana=Tkinter.StringVar(value='')
acamanalabel=Tkinter.Label(teachroot,width=70,text='系主任名称',justify=Tkinter.RIGHT)
acamanalabel.place(x=350,y=60,width=70,height=20)
acamanaentry=Tkinter.Entry(teachroot,width=70,textvariable=acamana)
acamanaentry.place(x=440,y=60,width=70,height=20)
addacabutton=Tkinter.Button(teachroot,width=100,text='添加院系信息',command=addaca)
addacabutton.place(x=550,y=60,width=100,height=20)
showacademybutton=Tkinter.Button(teachroot,width=100,command=showacademy,text='院系信息查询')
showacademybutton.place(x=20,y=90,width=100,height=20)
deleteacabutton=Tkinter.Button(teachroot,text='删除院系信息',command=deleteacademy,width=100)
deleteacabutton.place(x=160,y=90,width=100,height=20)
listboxacademy=Tkinter.Listbox(teachroot,width=600)
listboxacademy.place(x=20,y=120,width=600,height=100)


#专业管理

def deletemajor():
    #####
    selection=listboxmajor.curselection()
    if  not selection :
        tkMessageBox.showinfo(title='information',message='没有选择')
    else :
        a=listboxmajor.get(selection)
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
        cur.execute("delete from major WHERE mno=%s"%c_no)
        conn.commit()
        cur.close()
        listboxmajor.delete(selection)
        tkMessageBox.showinfo(title='通知',message='删除成功')

#添加信息
def addmajor():
    pp1=re.match("(^[0-9]{0,10}$)",mnoentry.get())
    pp2=re.match(u"^[\u4e00-\u9fa5]{0,}$",mnameentry.get())
    pp3=re.match("(^[0-9]{0,10}$)",macaentry.get())
    if(pp1 and pp2 and pp3):
        a=mnoentry.get()
        cur=conn.cursor()
        b=cur.execute('select * from major WHERE mno="%s"and aca_id="%s"'%(mnoentry.get(),macaentry.get()))
        try :
            if b==0:
                cur.execute('insert into major(mno,aca_id,mname) VALUES ("%s","%s", "%s")'%(mnoentry.get(),macaentry.get(),mnameentry.get()))
                conn.commit()
                cur.close()
                tkMessageBox.showinfo(title='通知',message='插入成功')
            else :
                tkMessageBox.showerror(title='错误',message='插入重复')
        except :
            tkMessageBox.showerror(title='错误',message='插入失败')
    else :
        tkMessageBox.showerror(title='错误',message='输入格式错误')
def showmajor():
    listboxmajor.delete(0,'end')
    cur=conn.cursor()
    a=cur.execute('select * from major')
    b=cur.fetchall()
    cur.close()
    if a==0:
        tkMessageBox.showerror(title='错误',message='没有信息')
    else :
        for i in b :
            result="专业号："+ i[0]+"   院系号：" +i[1]+"   专业名称：" +i[2]
            listboxmajor.insert(0,result)
majorlabel =Tkinter.Label(teachroot,text='专业管理',width=70,justify=Tkinter.RIGHT)
majorlabel.place(y=230,x=280,width=70,height=20)
mno=Tkinter.StringVar(value='')
mnolabel =Tkinter.Label(teachroot,text='专业号',justify=Tkinter.RIGHT,width=70)
mnolabel.place(x=10,y=260,width=70,height=20)
mnoentry=Tkinter.Entry(teachroot,width=70,textvariable=mno)
mnoentry.place(x=80,y=260,width=70,height=20)
mname=Tkinter.StringVar(value='')
mnamelabel=Tkinter.Label(teachroot,text='专业名称',width=70,justify=Tkinter.RIGHT)
mnamelabel.place(x=160,y=260,width=70,height=20)
mnameentry=Tkinter.Entry(teachroot,width=70,textvariable=mname)
mnameentry.place(x=240,y=260,width=70,height=20)

cur=conn.cursor()
cur.execute('select aca_id from academy')
maca=cur.fetchall()
cur.close()
macalabel=Tkinter.Label(teachroot,text='院系号',width=50,justify=Tkinter.RIGHT)
macalabel.place(x=325,y=260,width=50,height=20)
macaentry=ttk.Combobox(teachroot,width=50,values=maca)
macaentry.place(x=380,y=260,width=50,height=20)
macaentry["state"] = "readonly"
addmajorbutton=Tkinter.Button(teachroot,width=50,command=addmajor,text="添加专业")
addmajorbutton.place(x=20,y=290,width=50,height=20)
showmajorbutton=Tkinter.Button(teachroot,width=50,command=showmajor,text="显示专业")
showmajorbutton.place(x=90,y=290,width=50,height=20)
deletemajorbutton=Tkinter.Button(teachroot,width=50,command=deletemajor,text="删除专业")
deletemajorbutton.place(x=160,y=290,width=50,height=20)
########定义一个打表
listboxmajor=Tkinter.Listbox(teachroot,width=600)
listboxmajor.place(x=20,y=320,width=600,height=160)
teachroot.mainloop()
conn.close()
