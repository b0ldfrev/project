#-*- coding:utf-8 -*-
import Tkinter
import ttk
import  tkMessageBox
import  os
def teacher():
    try :
        os.system('teacherlog.py')
    except :
        tkMessageBox.showerror(title='错误',message='没有找到该动能')

def student():
    try :
        os.system('studentlog.py')
    except :
        tkMessageBox.showerror(title='错误',message='没有找到该动能')
def exit():
    root.quit()
root=Tkinter.Tk()
student1button=Tkinter.Button(root,width=100,text='管理员登录',command=teacher)
student1button.place(x=60,y=20,width=70,height=30)
student2button=Tkinter.Button(root,width=100,text='学生登陆',command=student)
student2button.place(x=60,y=60,width=70,height=30)
student3button=Tkinter.Button(root,width=100,text='退出',command=exit)
student3button.place(x=60,y=100,width=70,height=30)
root.mainloop()
