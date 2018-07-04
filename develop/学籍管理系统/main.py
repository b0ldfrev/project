#-*- coding:utf-8 -*-
import Tkinter
import ttk
import  tkMessageBox
import  os
def showfindstudentxfzt():
    try :
        os.system('tk_zsgc.py')
    except :
        tkMessageBox.showerror(title='错误',message='没有找到该动能')
def showfindstudent():
    try :
        os.system('findstudent.py')
    except :
        tkMessageBox.showerror(title='错误',message='没有找到该动能')
def showstudent():
    try :
        os.system('tk_student.py')
    except :
        tkMessageBox.showerror(title='错误',message='没有找到该动能')
def showgrade():
    try :
        os.system('tkcourse.py')
    except :
        tkMessageBox.showerror(title='错误',message='没有找到该动能')
def teachermajor():
    try :
        os.system('tkmajor.py')
    except :
        tkMessageBox.showerror(title='错误',message='没有找到该动能')
root=Tkinter.Tk()
student1button=Tkinter.Button(root,width=70,text='信息管理',command=showfindstudentxfzt)
student1button.place(x=60,y=20,width=70,height=20)
student2button=Tkinter.Button(root,width=70,text='学生管理',command=showstudent)
student2button.place(x=20,y=70,width=70,height=20)
student3button=Tkinter.Button(root,width=70,text='查询',command=showfindstudent)
student3button.place(x=100,y=70,width=70,height=20)
gradebutton=Tkinter.Button(root,width=70,text='课程管理',command=showgrade)
gradebutton.place(x=20,y=120,width=70,height=20)
techerbutton=Tkinter.Button(root,width=70,text='专业管理',command=teachermajor)
techerbutton.place(x=100,y=120,width=70,height=20)
root.mainloop()
