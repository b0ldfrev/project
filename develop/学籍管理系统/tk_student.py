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
root.geometry('1300x600')
root.title("学籍系统")
#学号
snolabel=Tkinter.Label(root,text='学号',justify=Tkinter.RIGHT,width=50)
snolabel.place(x=10,y=5,width=50,height=20)
varsno=Tkinter.StringVar(value="")#学号内容
entrysno=Tkinter.Entry(root,width=150,textvariable=varsno)
entrysno.place(x=70,y=5,width=150,height=20)
# 姓名
snamelabel=Tkinter.Label(root,text='姓名',justify=Tkinter.RIGHT,width=50)
snamelabel.place(x=230,y=5,width=50,height=20)
varsname=Tkinter.StringVar(value='')#存储学生姓名 及时变化
entrysname=Tkinter.Entry(root,width=150,textvariable=varsname)#关联变量
entrysname.place(x=300,y=5,width=150,height=20)
#性别
sexlable=Tkinter.Label(root,text='性别',justify=Tkinter.RIGHT,width=50)
sexlable.place(x=460,y=5,width=50,height=20)
sex=Tkinter.IntVar(value=1)#存储性别
radionman=Tkinter.Radiobutton(root,variable=sex,value=1,text='男性')
radionman.place(x=520,y=5,width=50,height=20)
radiowomen=Tkinter.Radiobutton(root,variable=sex,value=0,text='女性')
radiowomen.place(x=580,y=5,width=50,height=20)
#学制
studentxz=[3,4,5,6]
labelxz=Tkinter.Label(root,text='学制',justify=Tkinter.RIGHT,width=50)
labelxz.place(x=10,y=30,width=50,height=20)
xzclass=ttk.Combobox(root,values=tuple(studentxz),width=50)#输入学制
xzclass.place(x=70,y=30,width=50,height=20)
xzclass["state"] = "readonly"
#民族
snation="汉族,阿昌族,白族 ,保安族 ,布朗族 ,布依族 ,朝鲜族,达斡尔族,傣族,德昂族,侗族,东乡族,独龙族,鄂伦春族 ,俄罗斯族,鄂温克族,高山族,仡佬族,哈尼族,哈萨克族,赫哲族,回族,基诺族,京族,景颇族,柯尔克孜族,拉祜族,黎族,傈僳族,珞巴族,满族,毛南族,门巴族,蒙古族,苗族,仫佬族,纳西族,怒族,普米族,羌族,撒拉族,畲族,水族,塔吉克族,塔塔尔族,土族,土家族,佤族,维吾尔族,乌兹别克族,锡伯族 ,瑶族,彝族,裕固族,藏族,壮族"
snation=tuple(snation.split(','))
nationlabel=Tkinter.Label(root,text='民族',justify=Tkinter.RIGHT,width=50)
nationlabel.place(x=130,y=30,width=50,height=20)
nationclass=ttk.Combobox(root,values=snation,width=50)#输入民族
nationclass.place(x=190,y=30,width=70,height=20)
nationclass["state"] = "readonly"
# 地区
area="河北 山西 辽宁 吉林 黑龙江 江苏 浙江 安徽 福建 江西 山东 河南 湖北 湖南 广东 海南 四川 贵州 云南 陕西 甘肃 青海 台湾 香港 澳门 "
area=tuple(area.split())
arealabel=Tkinter.Label(root,text='省份',justify=Tkinter.RIGHT,width=50)
arealabel.place(x=280,y=30,width=50,height=20)
areaclass=ttk.Combobox(root,value=area,width=100)
areaclass.place(x=320,y=30,width=120,height=20)
areaclass["state"] = "readonly"
#政治面貌
zzmm=['共青团员','共产党员','群众']
zzmm=tuple(zzmm)
zzmmlable=Tkinter.Label(root,text="政治面貌",justify=Tkinter.RIGHT,width=70)
zzmmlable.place(x=450,y=30,width=70,height=20)
zzmmclass=ttk.Combobox(root,value=zzmm,width=80)
zzmmclass.place(x=530,y=30,width=80,height=20)
zzmmclass["state"] = "readonly"
#年龄
agevlaue=tuple(range(10,50))
agelabel=Tkinter.Label(root,text="年龄",width=50,justify=Tkinter.RIGHT)
agelabel.place(x=610,y=30,width=70,height=20)
#age=Tkinter.IntVar(value='')#代表年龄的量
ageentry= ttk.Combobox(root,width=50,values=agevlaue)
ageentry.place(x=680,y=30,width=50,height=20)
#年龄统计
agetlabel=Tkinter.Label(root,text="年龄",width=50,justify=Tkinter.RIGHT)
agetlabel.place(x=40,y=120,width=70,height=20)
agetentry= ttk.Combobox(root,width=50,values=agevlaue)
agetentry.place(x=50,y=145,width=50,height=20)
e=Tkinter.Label(root,text="————",width=50,justify=Tkinter.RIGHT)
e.place(x=110,y=140,width=30,height=20)
#地区统计
areatlabel=Tkinter.Label(root,text='地区',justify=Tkinter.RIGHT,width=50)
areatlabel.place(x=155,y=120,width=50,height=20)
areatclass=ttk.Combobox(root,value=area,width=100)
areatclass.place(x=150,y=145,width=60,height=20)
#areatclass["state"] = "readonly"
ee=Tkinter.Label(root,text="————",width=50,justify=Tkinter.RIGHT)
ee.place(x=220,y=140,width=30,height=20)
#政治面貌统计
zzmmtlable=Tkinter.Label(root,text="政治面貌",justify=Tkinter.RIGHT,width=70)
zzmmtlable.place(x=260,y=120,width=70,height=20)
zzmmtclass=ttk.Combobox(root,value=zzmm,width=80)
zzmmtclass.place(x=260,y=145,width=70,height=20)
#zzmmtclass["state"] = "readonly"
#院系号
cur=conn.cursor()
cur.execute('select aca_id from academy')
aca_no=cur.fetchall()
cur.close()
acalabel=Tkinter.Label(root,text='院系号',width=50,justify=Tkinter.RIGHT)
acalabel.place(x=10,y=60,width=50,height=20)
acaput=ttk.Combobox(root,value=aca_no,width=50)
acaput.place(x=70,y=60,width=50,height=20)
def majorchange(event):  #绑定事态函数
    aca_id=acaput.get()
    if aca_id:
        cur=conn.cursor()
        cur.execute('select mno from major WHERE aca_id=%s'%aca_id)
        a=cur.fetchall()
        cur.close()
        mnoentry['values']=a
    else:
        mnoentry.set([])

#专业号
#绑定事态函数
acaput.bind('<<ComboboxSelected>>',majorchange)#！！！！！！！！！！！！！！！
mno=Tkinter.StringVar(value='')
mnolabel= Tkinter.Label(root,text="专业号",width=50,justify=Tkinter.RIGHT)
mnolabel.place(x=120,y=60,width=50,height=20)
mnoentry=ttk.Combobox(root,width=50)
mnoentry.place(x=180,y=60,width=58,height=20)

#入学时间
stime=tuple(range(1970,2050))
timelabel=Tkinter.Label(root,text='入学时间',width=50,justify=Tkinter.RIGHT)
timelabel.place(x=245,y=60,width=50,height=20)
timeclass=ttk.Combobox(root,value=stime,width=70)
timeclass.place(x=310,y=60,width=70,height=20)
#电话号
sphone=Tkinter.StringVar(value='')
phonelabel=Tkinter.Label(root,text='电话号',justify=Tkinter.RIGHT,width=70)
phonelabel.place(x=380,y=60,width=70,height=20)
phoneentry=Tkinter.Entry(root,width=50,textvariable=sphone)
phoneentry.place(x=450,y=60,width=130,height=20)
#定义清除函数
def clearinformation():
    varsno.set(value='')#学号
    varsname.set(value='')#姓名
    sex.set(value=1)#性别
    xzclass.set(value='')#学制
    nationclass.set(value='')#民族
    areaclass.set(value='')#地区
    zzmmclass.set(value='')#政治面貌
    ageentry.set(value='')#年龄
    acaput.set(value='')#院系号
    mnoentry.set(value='')#专业号
    timeclass.set(value='')
    sphone.set(value='')
#定义添加函数
def addinformation():
    pp=re.match("(^[0-9]{10}$)", varsno.get())
    pp2=re.match(u"^[\u4e00-\u9fa5]{0,}$",varsname.get())
    pp3=re.match("^([0-9]{1,2})$",ageentry.get())
    pp4=re.match("(^[0-9]{0,}$)",acaput.get())
    pp5=re.match("(^[0-9]{0,}$)",mnoentry.get())
    pp6=re.match("(^[0-9]{0,}$)",timeclass.get())
    pp7=re.match("(^[0-9]{0,15}$)",sphone.get())
    if (pp and pp2 and pp3 and pp4 and pp5 and pp6 and pp7):
        result=u'学号：\''+varsno.get()+'\' '+u' 姓名：'+varsname.get()+' '+ u'  性别：'+(u'男 ' if sex.get() else u'女 ')+' '+ u' 学制：'+xzclass.get()+' '+ u' 民族：'+nationclass.get()+' '+ u' 省份：'+areaclass.get()+' '+ u' 政治面貌：'+zzmmclass.get()+' '+ u' 年龄：'+ageentry.get()+' '+ u' 院系号：'+acaput.get()+' '+ u' 专业号：'+mnoentry.get()+' '+ u' 入学年份：'+timeclass.get()+' '+ u' 电话号：'+sphone.get()+''
        try :
            cur=conn.cursor()
            a=cur.execute('select * from student WHERE sno=%s'%varsno.get())
            if a==0:
                sql1="insert into student(sno,sname,ssex,sxz,snation,ssage,szzmm,sarea,aca_id,mno,mtime,mphone,password)VALUES ('%s','%s','%s','%s','%s','%d','%s','%s','%s','%s','%s','%s','%s')" % \
                (varsno.get(),varsname.get(),(u'男 ' if sex.get() else u'女 '),xzclass.get(),nationclass.get(),int(ageentry.get()),zzmmclass.get(),areaclass.get(),acaput.get(),mnoentry.get(),timeclass.get(),sphone.get(),varsno.get())
                cur.execute(sql1)
                conn.commit()
                cur.close()
                tkMessageBox.showinfo(title=u'通知',message=u'插入成功')
                listboxstudent.insert(0,result)
            else :
                tkMessageBox.showerror(title='错误',message='该学号已存在')
        except:
            tkMessageBox.showerror(title=u'错误',message=u'插入失败')
    else :
        tkMessageBox.showerror(title=u'错误',message=u'输入格式有误')
#查找学生信息
def findstudent():
    a=varsno.get()
    if a:
        cur=conn.cursor()
        a=cur.execute('select sname,ssex,sxz,snation,ssage,szzmm,sarea,aca_id,mno,mtime,mphone from student WHERE sno=%s'%a)
        b=cur.fetchone()
        cur.close()
        if a ==0 :
            tkMessageBox.showerror(title='错误',message='该学生不存在')
        else:
            varsname.set(b[0])
            sex.set( int (1 if b[1]==u'男'else 0))
            xzclass.set(b[2])
            nationclass.set(b[3])
            ageentry.set(str(b[4]))
            zzmmclass.set(b[5])
            areaclass.set(b[6])
            acaput.set(b[7])
            mnoentry.set(b[8])
            timeclass.set(b[9])
            sphone.set(b[10])
            listboxstudent.delete(0,'end')
            result=u' 学号：\''+varsno.get()+'\' '+u'  姓名：'+varsname.get()+' '+ u'  性别：'+(u'男 ' if sex.get() else u'女 ')+' '+ u'  学制：'+xzclass.get()+' '+ u'  民族：'+nationclass.get()+' '+ u'  省份：'+areaclass.get()+' '+ u'  政治面貌：'+zzmmclass.get()+' '+ u'  年龄：'+ageentry.get()+' '+ u'  院系号：'+acaput.get()+' '+ u'  专业号：'+mnoentry.get()+' '+ u'  入学年份：'+timeclass.get()+' '+ u'  电话号：'+sphone.get()+' '
            listboxstudent.insert(0,result)
    else :
        tkMessageBox.showerror(title='错误',message='请输入学号')

#清除学生信息
def clearallinformain():
    listboxstudent.delete(0,'end')
#定义展示信息的函数
def showallinfo():
    listboxstudent.delete(0,'end')
    cur=conn.cursor()
    a=cur.execute('select sno,sname,ssex,sxz,snation,ssage,szzmm,sarea,aca_id,mno,mtime,mphone from student ')
    b=cur.fetchall()
    cur.close()
    if a == 0 :
        tkMessageBox.showerror(tiltle='错误',message='没有学生信息啊')
    elif a==1:
        b = str(b).replace('u\'','\'')
        b=b.decode("unicode-escape")
        b=b.replace('(','')
        b=b.replace(')','')
        b=b.replace(' ','')
        b=b.split(',')
        result=u'学号 :'+b[0]+';'+u'姓名 ：'+b[1]+';'+ u'性别 ：'+b[2]+';'+ u'学制 ：'+b[3]+';'+ u'民族 ：'+b[4]+';'+ u'省份 ：'+b[7]+';'+ u'政治面貌 ：'+b[6]+';'+ u'年龄 ：'+b[5]+';'+ u'院系号 '+b[8]+';'+ u'专业号 '+b[9]+';'+ u'入学年份 '+b[10]+';'+ u'电话号 '+b[11]+';'
        listboxstudent.insert(0,result)
    else :
        c=list(b)
        for b in c:
            b = str(b).replace('u\'','\'')
            b=b.decode("unicode-escape")
            b=b.replace('(','')
            b=b.replace(')','')
            b=b.replace(' ','')
            b=b.split(',')
            result=u' 学号：'+b[0]+' '+u'　姓名：'+b[1]+' '+ u'　性别：'+b[2]+' '+ u'　学制：'+b[3]+' '+ u'　民族：'+b[4]+' '+ u'　省份：'+b[7]+' '+ u'　政治面貌：'+b[6]+' '+ u'　年龄：'+str(b[5])+' '+ u'　院系号： '+b[8]+' '+ u'　专业号：'+b[9]+' '+ u'　入学年份：'+b[10]+' '+ u'　电话号：'+b[11]+';'
            listboxstudent.insert(0,result)
#定义删除函数
def deletestudent() :
    selection=listboxstudent.curselection()
    if not selection :
        tkMessageBox.showerror(title='错误',message='NO selection')
    else :
        a=listboxstudent.get(selection)
        a=str(a).decode('utf-8')
        a=a.split(';')
        a=a[0].split("'")
        d_sno=a[1]
        cur=conn.cursor()
        cur.execute("delete from student WHERE sno=%s"%d_sno)
        conn.commit()
        cur.close()
        listboxstudent.delete(selection)
        tkMessageBox.showinfo(title='通知',message='删除成功')
####################################################################
#更新功能
def updatestudent():
    pp=re.match("(^[0-9]{10}$)", varsno.get())
    pp2=re.match(u"^[\u4e00-\u9fa5]{0,}$",varsname.get())
    pp3=re.match("^([0-9]{1,2})$",ageentry.get())
    pp4=re.match("(^[0-9]{0,}$)",acaput.get())
    pp5=re.match("(^[0-9]{0,}$)",mnoentry.get())
    pp6=re.match("(^[0-9]{0,}$)",timeclass.get())
    pp7=re.match("(^[0-9]{0,15}$)",sphone.get())
    if (pp and pp2 and pp3 and pp4 and pp5 and pp6 and pp7):
        sno=varsno.get()
        if sno:
            try:
                cur=conn.cursor()
                cur.execute("delete from student WHERE sno=%s"%sno)
                sql1="insert into student(sno,sname,ssex,sxz,snation,ssage,szzmm,sarea,aca_id,mno,mtime,mphone,password)VALUES ('%s','%s','%s','%s','%s','%d','%s','%s','%s','%s','%s','%s','%s')" % \
                (varsno.get(),varsname.get(),(u'男 ' if sex.get() else u'女 '),xzclass.get(),nationclass.get(),int(ageentry.get()),zzmmclass.get(),areaclass.get(),acaput.get(),mnoentry.get(),timeclass.get(),sphone.get(),varsno.get())
                cur.execute(sql1)
                tkMessageBox.showinfo(title='通知',message='修改成功')
                conn.commit()
                cur.close()
            except:
                tkMessageBox.showerror(title='错误',message='修改失败')
        else :
            tkMessageBox.showerror(title='通知',message='更新错误')
    else :
        tkMessageBox.showerror(title=u'错误',message=u'输入格式有误')

#######统计功能
def sum():
    cur=conn.cursor()
    a=agetentry.get()
    b=areatclass.get()
    c=zzmmtclass.get()
    if (a and b and c):
        cur.execute('select count(sno) from student WHERE (ssage="%s" and sarea="%s" and szzmm="%s")'%(a,b,c))
    elif (a and b and (not c)) or (a and c and (not b)) or (b and c and (not a)):
        cur.execute('select count(sno) from student WHERE ((ssage="%s" and sarea="%s") or (sarea="%s" and szzmm="%s") or (ssage="%s" and szzmm="%s"))'%(a,b,b,c,a,c))
    else :
        cur.execute('select count(sno) from student WHERE (ssage="%s" or sarea="%s" or szzmm="%s")'%(a,b,c))
    bb=cur.fetchall()
    cur.close()
    bb=bb[0][0]
    strt="总人数："+str(bb)+" 人"
    tkMessageBox.showinfo(title='通知',message=strt)
    
#########################################教师及学院专业
#统计按钮
buttonsum=Tkinter.Button(root,text='统计人数',command=sum,width=70)
buttonsum.place(x=360,y=136,width=71,height=28)
#
buttonclear=Tkinter.Button(root,text='清除信息',command=clearinformation,width=70)
buttonclear.place(x=20,y=90,width=70,height=20)
buttonadd=Tkinter.Button(root,text='添加学生信息',command=addinformation,width=100)
buttonadd.place(x=110,y=90,width=100,height=20)
buttonfind=Tkinter.Button(root,text='查询学生信息',command=findstudent,width=70)
buttonfind.place(x=230,y=90,width=100,height=20)
buttonclearall=Tkinter.Button(root,width=140,text='清除显示框所有信息',command=clearallinformain)
buttonclearall.place(x=340,y=90,width=140,height=20)
findallstudent=Tkinter.Button(root,width=140,text="查询所有学生信息",command=showallinfo)
findallstudent.place(x=500,y=90,width=140,height=20)
deletesatabase_student=Tkinter.Button(root,width=100,text='删除学生信息',command=deletestudent)
deletesatabase_student.place(x=670,y=90,width=100,height=20)
updatebutton=Tkinter.Button(root,width=100,text='更新学生信息',command=updatestudent)
updatebutton.place(x=800,y=90,width=100,height=20)
#定义一个大的显示窗口
listboxstudent=Tkinter.Listbox(root,width=1200)
listboxstudent.place(x=20,y=180,width=1255,height=400)

root.mainloop()

conn.close()
