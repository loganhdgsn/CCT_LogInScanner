import sys
import subprocess
import pymysql
import re
import pymsgbox
import time
import datetime
from tkinter import *
from tkinter.ttk import *

conn = pymysql.connect(host='',user = '',passwd='',db='',port =)
cur = conn.cursor()
conn.commit()

class Login(Frame):


    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def markProject(name,aName,aISO,self):
        try:
            self.o.destroy()
        except:
            print()
        try:
            self.markBtn.destroy()
        except:
            print()
        i=0
        selectedISO = ""
        for nam in aName:
            if name == nam:
                selectedISO=aISO[i]
            i=i+1
        selectedISO = re.sub('[,()\']', '', str(selectedISO))

        project=[]
        cur.execute("select project from cctprojects where cctID = '%s' order by project desc"%selectedISO)
        iso = cur.fetchall()
        i=0
        for num in iso:
            project.append(i+1)
            tmp=re.sub('[,()\'{}]', '', str(num))
            project[i]= tmp
            i = i + 1

        projectName = StringVar()
        projectName.set(project)

        self.o = OptionMenu(self, projectName,"Project",*project,command=lambda _: Login.detComplete(projectName.get(),selectedISO,self))
        self.o.pack()
        self.o.place(x=100,y=121)
        return



    def detComplete(pname,ISO,self):
        try:
            self.markBtn.destroy()
        except:
            print("error")
        tmp = 0
        cur.execute("select iscomplete from cctprojects where project = '%s' AND cctID = '%s'"%(pname,ISO))
        slc = cur.fetchone()
        slc = re.sub('[,()\'{}]', '', str(slc))
        print(slc)
        if slc == str(1):
              tmp = 1
              self.markBtn = Button(self, text = "Mark Incomplete",command=lambda: Login.markComplete(pname,ISO,self,tmp))
              self.markBtn.pack()
              self.markBtn.place(x=350,y=81)
        else:
              self.markBtn = Button(self, text = "Mark Complete",command=lambda: Login.markComplete(pname,ISO,self,tmp))
              self.markBtn.pack()
              self.markBtn.place(x=350,y=81)
        return

    def markComplete(pname,ISO,self,corn):
        if corn == 0:
            cur.execute("update cctprojects set iscomplete = 1 where cctID = '%s' AND project = '%s'"%(ISO,pname))
        else:
            cur.execute("update cctprojects set iscomplete = 0 where cctID = '%s' AND project = '%s'"%(ISO,pname))
        self.markBtn.destroy()
        return


    def assignProject(name,assign,aName,aISO):
        i=0
        selectedISO = ""
        for nam in aName:
            if name == nam:
                selectedISO=aISO[i]
            i=i+1
        selectedISO = re.sub('[,()\']', '', str(selectedISO))
        cur.execute("insert into cctprojects(cctID,project,iscomplete)values('%s','%s',0)"%(selectedISO,assign))
        return

    def initUI(self):
        i = 0
        self.parent.title("Reports")
        self.pack(fill=BOTH, expand=1)
        Style().configure("TButton", padding=(0, 2, 0, 2), font='serif 10')
        xPlace = 75

        cur.execute("select cctID from cctpeople")
        iso = cur.fetchall()

        names=[]
        names2=[]
        isonum=[]

        for num in iso:
            names.append(i+1)
            names2.append(i+1)
            isonum.append(i+1)
            cur.execute("select firstname from cctpeople where cctID = '%s'"%num)
            tmp1 = cur.fetchone()
            tmp1 = re.sub('[,()\']', '', str(tmp1))
            cur.execute("select lastname from cctpeople where cctID = '%s'"%num)
            tmp2 = cur.fetchone()
            tmp2 = re.sub('[,()\']', '', str(tmp2))
            names[i]= tmp1 + ' ' + tmp2
            names2[i]= tmp1 + ' ' + tmp2
            isonum[i]=num
            i = i + 1

        nameSelect = StringVar()
        nameSelect.set(names)

        dateLabel=Label(self, text = "Select Name:")
        dateLabel.place(x=10,y=11)
        w = OptionMenu(self, nameSelect,"Name",*names)
        w.pack()
        w.place(x=100,y=11)
        e = Entry(self,width = 40)
        e.pack()
        e.place(x=10,y=41)

        self.genBtn = Button(self, text = "Assign",command=lambda: Login.assignProject(nameSelect.get(),e.get(),names,isonum))
        self.genBtn.place(x=350,y=40)



        nameSelect2 = StringVar()
        nameSelect2.set(names2)

        checkLabel=Label(self, text = "Select Name:")
        checkLabel.place(x=10,y=81)
        c = OptionMenu(self, nameSelect2,"Name",*names2,command=lambda _: Login.markProject(nameSelect2.get(),names2,isonum,self))
        c.pack()
        c.place(x=100,y=81)







def main():

    swipe = Tk()
    swipe.geometry("600x200+400+400")
    app = Login(swipe)
    swipe.mainloop()

if __name__ == '__main__':
    main()
