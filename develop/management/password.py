#-*- coding:utf-8 -*-
import MySQLdb
import os
import Tkinter
import ttk
import  tkMessageBox
import sys
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

def change():
	try :
		name = entryName.get()
		pwd = entryPwd.get()
		cur=conn.cursor()
		cur.execute('select password from student WHERE sno="%s"'%name)
		b=cur.fetchall()
		cur.close() 
		if pwd == b[0][0]:
			pwd1=varnewPwd.get()
			pwd2=varnewPwd2.get()
			if pwd1==pwd2 and pwd1 and pwd2:
			    cur=conn.cursor()
			    cur.execute('update student set password="%s" WHERE sno="%s"'%(pwd1,name))
			    conn.commit()
			    cur.close()
			    tkMessageBox.showinfo('通知',message = '修改成功')
			else :
			    tkMessageBox.showinfo('通知',message = '两次输入的密码不一致或格式错误')
			    varnewPwd.set('')
			    varnewPwd2.set('')
		else :
			tkMessageBox.showinfo('通知',message = '原密码错误')
			varPwd.set('')
	except :
		tkMessageBox.showinfo('通知',message = '该账号不存在')
root = Tkinter.Tk()
root.geometry("200x200")
root.title('密码修改')
varName = Tkinter.StringVar(value = '')
varPwd = Tkinter.StringVar(value = '')
varnewPwd = Tkinter.StringVar(value = '')
varnewPwd2 = Tkinter.StringVar(value = '')

labelName = Tkinter.Label(root,text = '账户名：',justify = Tkinter.RIGHT,width = 80)
labelName.place(x = 10,y = 10,width = 80,height = 20)
entryName = Tkinter.Entry(root,width = 80,textvariable = varName)
entryName.place(x = 90,y = 10,width = 80,height = 20)
 
labelPwd = Tkinter.Label(root,text = '密码：',justify = Tkinter.RIGHT,width = 80)
labelPwd.place(x = 10,y = 35,width = 80,height = 20)
entryPwd = Tkinter.Entry(root,show = '*',width = 80,textvariable = varPwd)
entryPwd.place(x = 90,y = 35,width = 80,height = 20)
 
labelPwd1 = Tkinter.Label(root,text = '新密密码：',justify = Tkinter.RIGHT,width = 80)
labelPwd1.place(x = 10,y = 60,width = 80,height = 20)
entryPwd1 = Tkinter.Entry(root,show = '*',width = 80,textvariable = varnewPwd)
entryPwd1.place(x = 90,y = 60,width = 80,height = 20)

labelPwd2 = Tkinter.Label(root,text = '确认密码：',justify = Tkinter.RIGHT,width = 80)
labelPwd2.place(x = 10,y = 85,width = 80,height = 20)
entryPwd2 = Tkinter.Entry(root,show = '*',width = 80,textvariable = varnewPwd2)
entryPwd2.place(x = 90,y = 85,width = 80,height = 20)

buttonCancel = Tkinter.Button(root,text = '修改密码',command = change)
buttonCancel.place(x = 55,y = 130,width = 65,height = 25)
 
 
root.mainloop()
