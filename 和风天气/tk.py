from tkinter import *
from tkinter.ttk import *
from tkinter.dialog import *
from PIL import ImageTk,Image
from time import sleep
top = Tk() # 窗口界面
top.geometry('400x550') #设置窗口分辨率
top.resizable(0,0) # 锁定窗口大小
top.title('电路分析方法')
# 打开指定图片
def get_image(filename,width,height):
    im = Image.open(filename).resize((width,height))
    return ImageTk.PhotoImage(im)
# 函数项
n = 1 # 计数器
n0 = 1
n1 = 1
pd1 = 0
pd = 0     
def next2():    # 下一步
    global n1,pd1
    if pd1==2:
        window = Jd2_window
        ym = 270
    else:
        window = Jd3_window
        ym = 390
    if(n1%7==1):
        label1 = Label(window,text='(1)选一个节点作为参考节点，标出各节点电压Un1,Un2,Un3···',font=('Arial',10)).place(x=20,y=ym+20*(n1-1))
        n1 += 1
    elif(n1%7==2):
        label2 = Label(window,text='(2)(判断是否有电压源)如果有电压源:',font=('Arial',10)).place(x=20,y=ym+20*(n1-1))
        n1 += 1
    elif(n1%7==3):
        label3 = Label(window,text='  (a)电压源是节点电压,则Unk=(+/-)Usk,不需列该节点的节点方程',font=('Arial',8)).place(x=20,y=ym+20*(n1-1))
        n1 += 1
    elif(n1%7==4):
        label4 = Label(window,text='  (b)电压源介于两节点间,则标出其电流并把它看成电流源,需列出',font=('Arial',8)).place(x=20,y=ym+20*(n1-1))
        label5 = Label(window,text='     该节点电压与电压源的关系式(辅助方程)Usk=(+/-)Unp(+/-)Unq',font=('Arial',8)).place(x=20,y=ym+20*(n1-1))
        n1 += 1
    elif(n1%7==5):
        label6 = Label(window,text='(3)列出网孔的网孔方程标准式',font=('Arial',10)).place(x=20,y=ym+20*(n1-1))
        n1 += 1
    elif(n1%7==6):
        label7 = Label(window,text='(4)若有受控源,则需列出控制量与节点电压的关系式(辅助方程)',font=('Arial',10)).place(x=20,y=ym+20*(n1-1))
        n1 += 1
    elif(n1%7==0):
        if pd1==2:
            U1 = d1/d0
            U2 = d2/d0
            entry9.delete(0, END)
            entry10.delete(0, END)
            entry11.delete(0, END)
            label8 = Label(window,text='解得节点一电压U1=%.2f V' % U1,font=('Arial',16)).place(x=80,y=ym+20*(n1-1)+20)
            label9 = Label(window,text='节点二电压U2=%.2f V' % U2,font=('Arial',16)).place(x=90,y=ym+20*(n1-1)+60)
        else:
            U1 = d4/d3
            U2 = d5/d3
            U3 = d6/d3
            # 清空输入框
            entry12.delete(0, END)
            entry16.delete(0, END)
            entry13.delete(0, END)
            entry14.delete(0, END)
            entry15.delete(0, END)
            label8 = Label(window,text='解得节点一电压U1=%.2f V' % U1,font=('Arial',13)).place(x=80,y=ym+20*(n1-1)+10)
            label9 = Label(window,text='节点二电压U2=%.2f V' % U2,font=('Arial',13)).place(x=90,y=ym+20*(n1-1)+30)
            label10 = Label(window,text='节点三电压U3=%.2f V' % U3,font=('Arial',13)).place(x=90,y=ym+20*(n1-1)+50)
    else:
        n1=1
def solve1(): # 解两个网孔方程
    # 获取数据
    global o0,o1,o2,pd
    z11 = int(entry1.get().split(' ')[0])
    z22 = int(entry1.get().split(' ')[1])
    z12 = int(entry2.get().split(' ')[0])
    z21 = int(entry2.get().split(' ')[1])
    u1 = int(entry3.get().split(' ')[0])
    u2 = int(entry3.get().split(' ')[1])
    o0 = z11*z22-z21*z12
    o1 = u1*z22-u2*z12
    o2 = z11*u2-z21*u1
    # 解方程
    if o0==0:
        label4 = Label(no2_window,text='电路方程无解！',font=('red',13)).place(x=140,y=240)
        # 清空输入框
        entry1.delete(0,END)
        entry2.delete(0,END)
        entry3.delete(0,END)
    else:
        pd = 2
        btn2 = Button(no2_window,text='下一步',font=('Arial',12),command=next1).place(x=200,y=200)
        label0 = Label(no2_window,text='网孔分析法解题步骤',font=('Arial',12)).place(x=20,y=240)
def solve2(): # 解三个网孔方程
    # 获取数据
    global o3,o4,o5,o6,pd
    z11 = int(entry4.get().split(' ')[0])
    z22 = int(entry4.get().split(' ')[1])
    z33 = int(entry4.get().split(' ')[2])
    z12 = int(entry5.get().split(' ')[0])
    z13 = int(entry5.get().split(' ')[1])
    z21 = int(entry6.get().split(' ')[0])
    z23 = int(entry6.get().split(' ')[1])
    z31 = int(entry7.get().split(' ')[0])
    z32 = int(entry7.get().split(' ')[1])
    u1 = int(entry8.get().split(' ')[0])
    u2 = int(entry8.get().split(' ')[1])
    u3 = int(entry8.get().split(' ')[2])
    o3 = z11*z22*z33+z21*z32*z13+z12*z23*z31-z12*z21*z33-z13*z22*z31-z23*z32*z11
    o4 = u1*z22*z33+u2*z32*z13+z12*z23*u3-z12*u2*z33-z13*z22*u3-z23*z32*u1
    o5 = z11*u2*z33+z21*u3*z13+u1*z23*z31-u1*z21*z33-z13*u2*z31-z23*u3*z11
    o6 = z11*z22*u3+z21*z32*u1+z12*u2*z31-z12*z21*u3-u1*z22*z31-u2*z32*z11
    # 解方程
    if o3==0:
        label4 = Label(no3_window,text='电路方程无解！',font=('red',13)).place(x=140,y=350)
        # 清空输入框
        entry4.delete(0,END)
        entry5.delete(0,END)
        entry6.delete(0,END)
        entry7.delete(0,END)
        entry8.delete(0,END)
    else:
        pd = 3
        btn2 = Button(no3_window,text='下一步',font=('Arial',10),command=next1).place(x=200,y=320)
        label0 = Label(no3_window,text='网孔分析法解题步骤',font=('Arial',12)).place(x=20,y=360)
# 两个网孔解题窗口界面
def No2():
    global top,entry1,entry2,entry3,no2_window
    no2_window = Toplevel(top,width=400,height=500) # 创建子窗口
    no2_window.title('两个网孔解法')
    no2_window.resizable(0,0) # 锁定窗口大小
    canvas = Canvas(no2_window,width=400,height=500,bg='pink').place(x=0,y=0) # 背景色
    # 设置组件
    label1 = Label(no2_window,text='请输入自电阻z11和z22(以空格分隔):',font=('Arial',13)).place(x=0,y=20)
    entry1 = Entry(no2_window,fg='blue',width=399)
    entry1.place(x=0,y=50)
    label2 = Label(no2_window,text='请输入两个网孔互电阻z12和z21(以空格分隔):',font=('Arial',13)).place(x=0,y=80)
    entry2 = Entry(no2_window,fg='blue',width=399)
    entry2.place(x=0,y=110)
    label3 = Label(no2_window,text='请输入两个网孔的电压升之和u1和u2(以空格分隔):',font=('Arial',13)).place(x=0,y=140)
    entry3 = Entry(no2_window,fg='blue',width=399)
    entry3.place(x=0,y=170)
    btn1 = Button(no2_window,text='解方程',font=('Arial',12),command=solve1).place(x=100,y=200)
# 三个网孔解题窗口界面
def No3():
    global top,entry4,entry5,entry6,entry7,entry8,no3_window
    no3_window = Toplevel(top,width=400,height=600) # 创建子窗口
    no3_window.title('三个网孔解法')
    no3_window.resizable(0,0) # 锁定窗口大小
    canvas = Canvas(no3_window,width=400,height=600,bg='pink').place(x=0,y=0) # 背景色
    # 设置组件
    label1 = Label(no3_window,text='请输入自电阻z11和z22和z33(以空格分隔):',font=('Arial',10)).place(x=0,y=20)
    entry4 = Entry(no3_window,fg='blue',width=399)
    entry4.place(x=0,y=50)
    label2 = Label(no3_window,text='请输入网孔一与其他两个电阻的互电阻z12与z13(以空格分隔):',font=('Arial',10)).place(x=0,y=80)
    entry5 = Entry(no3_window,fg='blue',width=399)
    entry5.place(x=0,y=110)
    label3 = Label(no3_window,text='请输入网孔二与其他两个电阻的互电阻z21与z23(以空格分隔):',font=('Arial',10)).place(x=0,y=140)
    entry6 = Entry(no3_window,fg='blue',width=399)
    entry6.place(x=0,y=170)
    label4 = Label(no3_window,text='请输入网孔三与其他两个电阻的互电阻z31与z32(以空格分隔):',font=('Arial',10)).place(x=0,y=200)
    entry7 = Entry(no3_window,fg='blue',width=399)
    entry7.place(x=0,y=230)
    label5 = Label(no3_window,text='请输入三个网孔的电压升之u1与u2与u3(以空格分隔):',font=('Arial',10)).place(x=0,y=260)
    entry8 = Entry(no3_window,fg='blue',width=399)
    entry8.place(x=0,y=290)
    btn1 = Button(no3_window,text='解方程',font=('Arial',10),command=solve2).place(x=100,y=320)
def solve3(): # 解两个支路方程
    # 获取数据
    global d0,d1,d2,pd1
    z11 = int(entry9.get().split(' ')[0])
    z22 = int(entry9.get().split(' ')[1])
    z12 = int(entry10.get().split(' ')[0])
    z21 = int(entry10.get().split(' ')[1])
    i1 = int(entry11.get().split(' ')[0])
    i2 = int(entry11.get().split(' ')[1])
    d0 = z11*z22-z21*z12
    d1 = i1*z22+z12*z12
    d2 = z11*i2+z21*i1
    # 解方程
    if d0==0:
        label4 = Label(Jd2_window,text='电路方程无解！',fg='red',font=('黑体',13)).place(x=140,y=240)
        # 清空输入框
        entry9.delete(0,END)
        entry10.delete(0,END)
        entry11.delete(0,END)
    else:
        pd1 = 2
        btn2 = Button(Jd2_window,text='下一步',font=('Arial',12),command=next2).place(x=200,y=200)
        label0 = Label(Jd2_window,text='节点分析法解题步骤',font=('Arial',12)).place(x=20,y=240)
def solve4(): # 解三个支路方程
    # 获取数据
    global d3,d4,d5,d6,pd1
    z11 = int(entry4.get().split(' ')[0])
    z22 = int(entry4.get().split(' ')[1])
    z33 = int(entry4.get().split(' ')[2])
    z12 = int(entry5.get().split(' ')[0])
    z13 = int(entry5.get().split(' ')[1])
    z21 = int(entry6.get().split(' ')[0])
    z23 = int(entry6.get().split(' ')[1])
    z31 = int(entry7.get().split(' ')[0])
    z32 = int(entry7.get().split(' ')[1])
    i1 = int(entry8.get().split(' ')[0])
    i2 = int(entry8.get().split(' ')[1])
    i3 = int(entry8.get().split(' ')[2])
    d3 = z11*z22*z33-z21*z32*z13-z12*z23*z31-z13*z22*z31+z21*z32*z13+z31*z12*z23
    d4 = i1*z22*z33+i2*z32*z13+z12*z23*i3+z12*i2*z33+z13*z22*i3-z23*z32*i1
    d5 = z11*i2*z33+z21*i3*z13+i1*z23*z31+i1*z21*z33-z13*i2*z31+z23*i3*z11
    d6 = z11*z22*i3+z21*z32*i1+z12*i2*z31-z12*z21*i3+i1*z22*z31+i2*z32*z11
    # 解方程
    if d3==0:
        label4 = Label(Jd3_window,text='电路方程无解！',fg='red',font=('黑体',13)).place(x=140,y=350)
        # 清空输入框
        entry12.delete(0,END)
        entry16.delete(0,END)
        entry13.delete(0,END)
        entry14.delete(0,END)
        entry15.delete(0,END)
    else:
        pd1 = 3
        btn2 = Button(Jd3_window,text='下一步',font=('Arial',10),command=next2).place(x=200,y=320)
        label0 = Label(Jd3_window,text='支路分析法解题步骤',font=('Arial',12)).place(x=20,y=360)
# 两个支路解题窗口界面
def Jd2():
    global top,entry9,entry10,entry11,Jd2_window
    Jd2_window = Toplevel(top,width=400,height=500) # 创建子窗口
    Jd2_window.title('支路分析法（二）')
    Jd2_window.resizable(0,0) # 锁定窗口大小
    canvas = Canvas(Jd2_window,width=400,height=500,bg='pink').place(x=0,y=0) # 背景色
    # 设置组件
    label1 = Label(Jd2_window,text='请输入自电导G11和G22(以空格分隔):',font=('Arial',13)).place(x=0,y=20)
    entry9 = Entry(Jd2_window,fg='blue',width=399)
    entry9.place(x=0,y=50)
    label2 = Label(Jd2_window,text='请输入互点导G12和G21(以空格分隔):',font=('Arial',13)).place(x=0,y=80)
    entry10 = Entry(Jd2_window,fg='blue',width=399)
    entry10.place(x=0,y=110)
    label3 = Label(Jd2_window,text='请输入两个节电的电流之和I1和I2(以空格分隔):',font=('Arial',13)).place(x=0,y=140)
    entry11 = Entry(Jd2_window,fg='blue',width=399)
    entry11.place(x=0,y=170)
    btn1 = Button(Jd2_window,text='解方程',font=('Arial',12),command=solve3).place(x=100,y=200)
# 三个节点解题窗口界面
def Jd3():
    global top,entry12,entry13,entry14,entry15,entry16,Jd3_window
    Jd3_window = Toplevel(top,width=400,height=600) # 创建子窗口
    Jd3_window.title('支路分析法（三）')
    Jd3_window.resizable(0,0) # 锁定窗口大小
    canvas = Canvas(Jd3_window,width=400,height=600,bg='pink').place(x=0,y=0) # 背景色
    # 设置组件
    label1 = Label(Jd3_window,text='请输入自电阻G11和G22和G33(以空格分隔):',font=('Arial',10)).place(x=0,y=20)
    entry12 = Entry(Jd3_window,fg='blue',width=399)
    entry12.place(x=0,y=50)
    label2 = Label(Jd3_window,text='请输入支路一与其他两个支路的互电阻G12和G13(以空格分隔):',font=('Arial',10)).place(x=0,y=80)
    entry13 = Entry(Jd3_window,fg='blue',width=399)
    entry13.place(x=0,y=110)
    label3 = Label(Jd3_window,text='请输入支路二与其他两个支路的互电阻G21与G23(以空格分隔):',font=('Arial',10)).place(x=0,y=140)
    entry14 = Entry(Jd3_window,fg='blue',width=399)
    entry14.place(x=0,y=170)
    label4 = Label(Jd3_window,text='请输入支路三与其他两个支路的互电阻G31与G32(以空格分隔):',font=('Arial',10)).place(x=0,y=200)
    entry15 = Entry(Jd3_window,fg='blue',width=399)
    entry15.place(x=0,y=230)
    label5 = Label(Jd3_window,text='请输入三个支路各自的电流和I1与I2与I3(以空格分隔):',font=('Arial',10)).place(x=0,y=260)
    entry16 = Entry(Jd3_window,fg='blue',width=399)
    entry16.place(x=0,y=290)
    btn1 = Button(Jd3_window,text='解方程',font=('Arial',10),command=solve4).place(x=100,y=320)
# 支路解题函数
def slove0():    # 下一步
    try:
        r1 = int(entry01.get())
        r2 = int(entry02.get())
        r3 = int(entry03.get())
        u1 = int(entry04.get())
        o1 = r1*r3+r1*r2+r2*r3
        o2 = u1*r2
        o3 = u1*r1
        o4 = u1*r1+u1*r2
        zl_list = ['(1)标出各支路电流','(2)需列出三条支路以上节点减1个KCL','(3)需列网孔数减电流源数个KVL,','   绕向要避开电流源,优先选择点压源的路径','(4)若有受控源,则需列出控制量与支路电流的关系式']
        i = 0
        ym = 340
        label8 = Label(zl_window,text='                     ',bg='pink',font=('宋体',20)).place(x=160,y=310)
        label0 = Label(zl_window,text='支路分析法解题步骤',font=('宋体',15)).place(x=20,y=310)
        for txt in zl_list:
            label = Label(zl_window,text=txt,font=('宋体',14))
            label.place(x=20,y=ym+i*20)
            i+=1
        if o1==0:
            label11 = Label(zl_window,text='该电路无解！',fg='red',font=('宋体',20)).place(x=180,y=310)
            entry01.delete(0,END)
            entry02.delete(0,END)
            entry03.delete(0,END)
            entry04.delete(0,END)
        else:
            label1 = Label(zl_window,text='列',font=('宋体',18)).place(x=30,y=470)
            label2 = Label(zl_window,text='方',font=('宋体',18)).place(x=30,y=500)
            label3 = Label(zl_window,text='程',font=('宋体',18)).place(x=30,y=530)
            label4 = Label(zl_window,text='KCL:i3=i2+i1     ',font=('宋体',18)).place(x=100,y=470)
            label5 = Label(zl_window,text='KVL:U=R3*i3+R2*i2',font=('宋体',18)).place(x=100,y=500)
            label6 = Label(zl_window,text='    R1*i1-R2*i2=0',font=('宋体',18)).place(x=100,y=530)
            label7 = Label(zl_window,text='解得i1=%0.2f A,i2=%0.2f A,i3=%0.2f A'%(o2/o1,o3/o1,o4/o1),font=('宋体',18)).place(x=100,y=530)
            label8 = Label(zl_window,text='%0.2fA'%(o2/o1),font=('宋体',15),fg='red').place(x=140,y=40)
            label9 = Label(zl_window,text='%0.2fA'%(o3/o1),font=('宋体',15),fg='red').place(x=238,y=75)
            label10 = Label(zl_window,text='%0.2fA'%(o4/o1),font=('宋体',15),fg='red').place(x=360,y=40)
    except ValueError:
        label = Label(zl_window,text='警告：请输入完整数据!',fg='red',font=('宋体',20)).place(x=160,y=310)
# 支路法界面
def zl():
    global top,zl_window,zl_image,entry01,entry02,entry03,entry04
    zl_window = Toplevel(top,width=600,height=600)
    zl_window.title('电路分析法之支路法')
    zl_window.resizable(0,0)
    canvas = Canvas(zl_window,width=600,height=600,bg='pink').place(x=0,y=0) # 背景色
    zl_bg = Label(zl_window,image=zl_image).place(x=0,y=0)
    label01 = Label(zl_window,text='注:在上面个方框填入相对应的值后按解题即可电流值',fg='red',bg='white',font=('宋体',13)).place(x=55,y=275)
    btn = Button(zl_window,text='解题',font=('黑体',13),command=slove0).place(x=500,y=270)
    entry01 = Entry(zl_window,fg='blue',width=5,bg='pink')
    entry01.place(x=75,y=135)
    entry02 = Entry(zl_window,fg='blue',width=5,bg='pink')
    entry02.place(x=365,y=140)
    entry03 = Entry(zl_window,fg='blue',width=5,bg='pink')
    entry03.place(x=450,y=42)
    entry04 = Entry(zl_window,fg='blue',width=5,bg='pink')
    entry04.place(x=500,y=140)
# 菜单项
menubar = Menu(top) # 父菜单
fmenu = Menu(menubar)   # 子菜单
for item in ['看啥呢','没开发呢','看下一个']:
    fmenu.add_command(label = item)
smenu = Menu(menubar)
for item in ['这个有点难','算了','下一个吧']:
    smenu.add_command(label=item)
tmenu = Menu(menubar)
for item in ['假装我是子菜单','不会下一个']:
    tmenu.add_command(label=item)
vmenu = Menu(menubar)
for item in ['你不会以为这些功能真有用吧','不会吧','不会吧']:
    vmenu.add_command(label=item)
menubar.add_cascade(label='文件(F)',menu=fmenu)
menubar.add_cascade(label='编辑(E)',menu=smenu)
menubar.add_cascade(label='视图(V)',menu=tmenu)
menubar.add_cascade(label='关于(G)',menu=vmenu)
top['menu'] = menubar
# 起始界面
image1 = get_image('bg_image2.png',400,550)
zl_image = get_image('zl.png',600,300)
bg = Label(top,image=image1).place(x=0,y=0)
label = Label(top,text='''**************************
*     电路分析方法      *
*                              *
*            by 2院3班组 *
**************************''',width=20,height=5,fg='green',font=('华文行楷',20)).place(x=70,y=15)
label4 = Label(top,text='电路分析方法之支路法',fg='yellow',font=('黑体',16),bg='black').place(x=90,y=180)
btn3 = Button(top,text='进入解题',fg='green',bg='white',font=('Arial',14),command=zl).place(x=155,y=213)
label3 = Label(top,text='电路分析方法之网孔法',fg='yellow',font=('黑体',16),bg='black').place(x=90,y=260)
label2 = Label(top,text='请选择网孔数',font=('黑体',14),fg='yellow',bg='black').place(x=135,y=290)
btn1 = Button(top,text='两个选我',fg='green',bg='white',font=('黑体',13),command=No2).place(x=95,y=330)
btn2 = Button(top,text='三个选我',fg='green',bg='white',font=('黑体',13),command=No3).place(x=210,y=330)
label5 = Label(top,text='电路分析方法之节点法',fg='yellow',font=('黑体',16),bg='black').place(x=90,y=385)
label6 = Label(top,text='请选择节点数',font=('黑体',14),fg='yellow',bg='black').place(x=135,y=415)
btn4 = Button(top,text='两个选我',bg='white',fg='green',font=('黑体',13),command=Jd2).place(x=95,y=455)
btn5 = Button(top,text='三个选我',bg='white',fg='green',font=('黑体',13),command=Jd3).place(x=210,y=455)
top.mainloop()
