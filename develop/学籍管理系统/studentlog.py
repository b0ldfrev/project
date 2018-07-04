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

def login():
	name = entryName.get()
	pwd = entryPwd.get()
	cur=conn.cursor()
	cur.execute('select password from student WHERE sno="%s"'%name)
	b=cur.fetchall()
	cur.close() 
	if pwd == b[0][0]:
		os.system('studentfind.py')
	else:
		tkMessageBox.showinfo('Python tkinter',message = '密码错误')
		
def cancel():
	varName.set('')
	varPwd.set('')

def change():
    try :
        os.system('password.py')
    except :
        tkMessageBox.showerror(title='错误',message='没有找到该动能') 
	
root = Tkinter.Tk()
root.geometry("200x140")
root.title('学生登陆')
varName = Tkinter.StringVar(value = '')
varPwd = Tkinter.StringVar(value = '')
labelName = Tkinter.Label(root,text = '账户名：',justify = Tkinter.RIGHT,width = 80)
labelName.place(x = 10,y = 10,width = 80,height = 20)
entryName = Tkinter.Entry(root,width = 80,textvariable = varName)
entryName.place(x = 90,y = 10,width = 80,height = 20)
 
labelPwd = Tkinter.Label(root,text = '密码：',justify = Tkinter.RIGHT,width = 80)
labelPwd.place(x = 10,y = 35,width = 80,height = 20)
entryPwd = Tkinter.Entry(root,show = '*',width = 80,textvariable = varPwd)
entryPwd.place(x = 90,y = 35,width = 80,height = 20)
 
buttonOk = Tkinter.Button(root,text = '登陆',command = login)
buttonOk.place(x = 40,y = 70,width =50,height = 20)
buttonCancel = Tkinter.Button(root,text = '清空',command = cancel)
buttonCancel.place(x = 100,y = 70,width = 50,height = 20)
buttonCancel = Tkinter.Button(root,text = '修改密码',command = change)
buttonCancel.place(x = 58,y = 100,width = 80,height = 25)
 
 
root.mainloop()
