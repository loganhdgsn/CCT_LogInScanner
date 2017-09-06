import sys
import subprocess
import pymysql
import re
import pymsgbox
import threading
import time
from tkinter import *
from tkinter.ttk import *
conn = pymysql.connect(host='',user = '',passwd='',db='',port =)
cur = conn.cursor()
conn.commit()

#sql = ("insert into User(User,Password,Saved)values('%s','%s','')" % (x,y))
#cur.execute(sql)
#conn.commit()
#sql= "CREATE TABLE cctpeople (cctID INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,firstname VARCHAR(30) NOT NULL,lastname VARCHAR(30) NOT NULL,isadmin BOOL,isclockedon BOOL)"
#cur.execute("CREATE TABLE cctpeople (cctID INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,firstname VARCHAR(30) NOT NULL,lastname VARCHAR(30) NOT NULL,isadmin BOOL,isclockedon BOOL)")
#conn.commit()
cur.execute("ALTER TABLE cctpunches MODIFY COLUMN punchID INT auto_increment")
#cur.execute("insert into cctpeople(firstname,lastname,isadmin,isclockedon)values('Trevor','Delong',1,0)")
#conn.commit()
#cur.execute("CREATE TABLE cctprojects (projectID INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,firstname VARCHAR(30) NOT NULL,lastname VARCHAR(30) NOT NULL,iscomplete BOOL,project LONGTEXT)")
#conn.commit()


class Login(Frame):


    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self._after_id = None
        self.middleOfJob = False
        self.initUI()

    def projectBox(y,self):
        cur.execute("select project from cctprojects where cctID='%s'"%iso)
        genProjects = cur.fetchall()
        for pro in genProjects:
            pro = re.sub('[,()\'{}]', '', str(pro))
            self.lbox.insert(END,pro)

        self.lbox.bind('<<ListboxSelect>>',Login.projectClick)

    def projectClick(event):
        w=event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        value = re.sub('[,()\']', '', str(value))
        #print(value)
        cur.execute("select projectID from cctprojects where cctID = '%s' AND project = '%s'"%(iso,value))
        checkit = cur.fetchone()
        checkit=re.sub('[,()\']', '', str(checkit))
        me.selectProject["text"]="Clock In with Project '%s'"%value
        me.selectProject["command"] = lambda: Login.inWithProject(iso,checkit,value)


    def inWithProject(iso,x,value):
        cur.execute("update cctpeople set isclockedon = 1 where cctID = '%s'" % (iso))
        conn.commit()
        timeIn = time.strftime('%Y-%m-%d %H:%M:%S')
        cur.execute("insert into cctpunches(cctID,selectedproject,punchtime,inorout)values('%s','%s','%s','IN')"%(iso,x,timeIn))
        conn.commit()
        pymsgbox.alert("You are now clocked in and selected the project '%s'"%value,"Update")
        me.lbox.delete(0,END)
        me.pw_entry.focus()
        me.pw_entry.delete(0,END)
        me.userFLLabel["text"] = " "
        me.selectProject["text"]="Clock In"
        me.selectProject["command"] = lambda: Login.clockIn(me.pw_entry.get(),me)

    def clockIn(y,self):
        if y == "outall":
            cur.execute("select cctID from cctpeople where isclockedon = 1")
            remove = cur.fetchall()
            for cout in remove:
                cur.execute("update cctpeople set isclockedon = 0 where cctID = '%s'"%cout)
            sys.exit(0)

        self.pw_entry.focus()
        self.pw_entry.delete(0,END)
        y = y[2:]
        tmp1,tmp2,tmp3 = y.split('^')
        global iso
        global me
        me = self
        iso = int(tmp1)
        firstname = y
        lastname = y
        lastname, firstname = y.split('/')
        firstname = re.sub('[^A-Za-z0-9]+', '', firstname)
        lastname = re.sub('[^A-Za-z0-9]+', '', lastname)
        for i in range(0,10):
            firstname = firstname.replace(str(i),"")
            lastname = lastname.replace(str(i),"")
        me.userFLLabel["text"] = firstname + " " + lastname
        test=cur.execute("select cctID from cctpeople where cctID = '%s'" % (iso))
        if test == 1:
           cur.execute("select isclockedon from cctpeople where cctID = '%s'" % (iso))
           checkisclockedon=cur.fetchone()
           if checkisclockedon[0] == 0:
               Login.projectBox(iso,self)
           else:
             pymsgbox.alert("You are already clocked in","Error")
             me.userFLLabel["text"] = " "
        elif test == 0:
            cur.execute("insert into cctpeople(cctID,firstname,lastname,isadmin,isclockedon)values('%s','%s','%s',0,1)" % (iso,firstname,lastname))
            conn.commit()
            cur.execute("insert into cctprojects(cctID,iscomplete,project)values('%s',0,'Hanging out')"%iso)
            conn.commit()
            Login.projectBox(iso,self)
        return

    def clockOut(y,self):
        self.pw_entry.focus()
        self.pw_entry.delete(0,END)
        y = y[2:]
        tmp1,tmp2,tmp3 = y.split('^')
        global iso
        global me
        me = self
        iso = tmp1
        firstname = y
        lastname = y
        lastname, firstname = y.split('/')
        firstname = re.sub('[^A-Za-z0-9]+', '', firstname)
        lastname = re.sub('[^A-Za-z0-9]+', '', lastname)
        for i in range(0,10):
            firstname = firstname.replace(str(i),"")
            lastname = lastname.replace(str(i),"")
        me.userFLLabel["text"] = firstname + " " + lastname
        test=cur.execute("select firstname, lastname from cctpeople where cctID = '%s'" % (iso))
        if test == 1:
            cur.execute("select isclockedon from cctpeople where cctID = '%s'" % (iso))
            checkisclockedon=cur.fetchone()
            if checkisclockedon[0] == 0:
                pymsgbox.alert("You are already clocked out","Error")
                me.userFLLabel["text"] = " "
            else:
                timeOut = time.strftime('%Y-%m-%d %H:%M:%S')
                cur.execute("update cctpeople set isclockedon = 0 where cctID = '%s'" % (iso))
                conn.commit()
                cur.execute("insert into cctpunches(cctID,selectedproject,punchtime,inorout)values('%s',0,'%s','OUT')"%(iso,timeOut))
                conn.commit()
                pymsgbox.alert("You are now clocked out","Update")
                me.userFLLabel["text"] = " "

        elif test == 0:
            pymsgbox.alert("You were not found in the database. If you are new to the CCT, please clock in for your first time!","Error")
        return

    def initUI(self):
        self.parent.title("Clock In")
        self.pack(fill=BOTH, expand=1)
        Style().configure("TButton", padding=(0, 2, 0, 2), font='serif 10')
        xPlace = 75
        userLabel=Label(self, text = "Name:")
        userLabel.place(x=xPlace-60,y=10)
        userpwLabel=Label(self, text = "Swipe Info:")
        userpwLabel.place(x=xPlace-60,y=50)
        self.selectProject = Button(self, text = "Clock In",command=lambda: Login.clockIn(self.pw_entry.get(),self))
        self.selectProject.place(x=xPlace-30,y=70)
        self.regiButton = Button(self, text = "Clock Out",command=lambda: Login.clockOut(self.pw_entry.get(),self))
        self.regiButton.place(x=xPlace+-30,y=100)
        self.userFLLabel=Label(self, text = "")
        self.userFLLabel.pack()
        self.userFLLabel.place(x=80,y=10)
        self.pw_entry = Entry(self, width=30)
        self.pw_entry.place(x=xPlace+5,y=50)
        self.pw_entry.focus()
        self.lboxLabel=Label(self, text = "Projects:")
        self.lboxLabel.place(x=50,y=130)
        self.lbox=Listbox(self,height = 15,width = 35)
        self.lbox.pack(pady=5)
        self.lbox.place(x=50,y=150)

def main():
    swipe = Tk()
    w, h = swipe.winfo_screenwidth(), swipe.winfo_screenheight()
    swipe.geometry("%dx%d+0+0" % (w-100, h-100))
    app = Login(swipe)
    swipe.mainloop()

if __name__ == '__main__':
    main()
