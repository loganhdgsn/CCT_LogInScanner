import sys
import subprocess
import pymysql
import re
import pymsgbox
import datetime
from tkinter import *
from tkinter.ttk import *
import xlwt

#check into shared method for python file
conn = pymysql.connect(host='',user = '',passwd='',db='',port =)
cur = conn.cursor()
conn.commit()


class Login(Frame):


    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def typeCheck(dtype,date1,date2,complete):
        if dtype == 2:
            year, month, day = map(int, date1.split('-'))
            date4 = datetime.datetime(year, month, day)
            year, month, day = map(int, date2.split('-'))
            date5 = datetime.datetime(year, month, day)
            print(date5)

        if date4<date5:
            print("less")
        elif date4>date5:
            print("greater")

    def makeReport(ntype,name,dtype,date1,date2,complete):
        i=0

        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Report")


        if dtype == 2:
            year, month, day = map(int, date1.split('-'))
            date4 = datetime.datetime(year, month, day)
            year, month, day = map(int, date2.split('-'))
            date5 = datetime.datetime(year, month, day)


        if ntype == 1:
            if dtype == 1:
                cur.execute("select cctID from cctpunches")
                iso = cur.fetchall()
                pnames=[]
                cur.execute("select selectedProject from cctpunches")
                tmppro = cur.fetchall()

                for num in iso:
                    pnames.append(i+1)
                    cur.execute("select firstname from cctpeople where cctID = '%s'"%num)
                    tmp1 = cur.fetchone()
                    tmp1 = re.sub('[,()\']', '', str(tmp1))
                    cur.execute("select lastname from cctpeople where cctID = '%s'"%num)
                    tmp2 = cur.fetchone()
                    tmp2 = re.sub('[,()\']', '', str(tmp2))
                    pnames[i]= tmp1 + ' ' + tmp2
                    sheet1.write(i+1,0,str(pnames[i]))
                    cur.execute("select punchtime from cctpunches")
                    tmpdates = cur.fetchall()
                    tmpdate = re.sub(' ','0',str(tmpdates[i]))
                    tmpdate = tmpdate[19:]
                    tmpdate = re.sub(',','-',tmpdate)
                    tmpyear,tmpmnth,tmpday,tmps4,tmps5,tmps6,tmps7 = tmpdate.split('-')
                    if len(tmpmnth) == 3:
                        tmpmnth=tmpmnth[1:]

                    if len(tmpday) == 3:
                        tmpday=tmpday[1:]

                    #insert date
                    sheet1.write(i+1,2,str(tmpday + '-' + tmpmnth + '-' + tmpyear))







                    pro = re.sub('[,()]', '', str(tmppro[i]))
                    if pro == '0':
                        pro = "Clocked Out"
                    else:
                        cur.execute("select project from cctprojects,cctpunches where cctprojects.projectID = cctpunches.selectedProject AND selectedProject = '%s'"%pro)
                        pro=cur.fetchone()
                        pro=re.sub('[,()\']', '', str(pro))

                    sheet1.write(i+1,1,str(pro))








                    cur.execute("select inorout from cctpunches")
                    tmpinorout = cur.fetchall()
                    sheet1.write(i+1,3,str(tmpinorout[i]))
                    i = i + 1

            elif dtype==2:
                cur.execute("select cctID from cctpeople")
                loopname = cur.fetchall()

                for nam in loopname:
                    nam=re.sub('[(),\']', '', str(nam))
                    cur.execute("select firstname from cctpeople where cctID = '%s'"%nam)
                    tmpfn = cur.fetchone()
                    tmpfn=re.sub('[(),\']', '', str(tmpfn))
                    cur.execute("select lastname from cctpeople where cctID = '%s'"%nam)
                    tmpln = cur.fetchone()
                    tmpln=re.sub('[(),\']', '', str(tmpln))
                    cur.execute("select cctID from cctpeople where firstname = '%s' AND lastname = '%s'"%(tmpfn,tmpln))
                    iso = cur.fetchone()
                    iso = re.sub('[()\']', '', str(iso))
                    cur.execute("select punchID from cctpunches,cctpeople where cctpunches.cctID=cctpeople.cctID AND cctpeople.firstname = '%s' AND cctpeople.lastname = '%s'"%(tmpfn,tmpln))
                    pID = cur.fetchall()


                    for num in pID:
                        num = re.sub('[(),\']', '', str(num))
                        print(num)
                        cur.execute("select punchtime from cctpunches,cctpeople where cctpunches.punchID='%s' AND cctpunches.cctID=cctpeople.cctID AND cctpeople.cctID = '%s'"%(num,iso))
                        tmpdate = cur.fetchone()
                        tmpdate = re.sub('[()\']', '', str(tmpdate))
                        tmpdate = re.sub(' ','0',tmpdate)
                        tmpdate = tmpdate[17:]
                        tmpdate = re.sub(',','-',tmpdate)
                        tmpyear,tmpmnth,tmpday,tmps4,tmps5,tmps6,tmps7 = tmpdate.split('-')
                        tmpdate = tmpdate[0:10]

                        if len(tmpmnth) == 3:
                            tmpmnth=tmpmnth[1:]

                        if len(tmpday) == 3:
                            tmpday=tmpday[1:]


                        year, month, day = map(int, tmpdate.split('-'))
                        conDate = datetime.datetime(int(tmpyear), int(tmpmnth), int(tmpday))
                        print(conDate)

                        if date4<=conDate and date5>=conDate:

                            print("yes")
                            #insert name
                            sheet1.write(i+1,0,str(tmpfn + ' ' + tmpln))
                            #insert date
                            sheet1.write(i+1,2,str(tmpday + '-' + tmpmnth + '-'+tmpyear))

                            #insert projects
                            cur.execute("select selectedProject from cctpeople,cctprojects,cctpunches where \
                            cctpunches.cctID=cctpeople.cctID AND cctpunches.punchID = '%s'"%(num))
                            pro=cur.fetchone()
                            pro = re.sub('[,()]', '', str(pro))
                            print(pro)
                            if pro == '0':
                                pro = "Clocked Out"
                            else:
                                cur.execute("select project from cctprojects,cctpunches where \
                                cctprojects.projectID = cctpunches.selectedProject AND cctpunches.selectedProject = '%s' and cctpunches.punchID = '%s'"%(pro,num))
                                pro=cur.fetchone()
                                pro=re.sub('[,()\']', '', str(pro))
                            sheet1.write(i+1,1,str(pro))


                            #insert clock in or out
                            cur.execute("select inorout from cctpeople,cctpunches where cctpunches.punchID = '%s' AND cctpunches.cctID = cctpeople.cctID"%num)
                            tmpinorout = cur.fetchone()
                            sheet1.write(i+1,3,str(tmpinorout))

                        i = i + 1


        elif ntype == 2:
            if dtype == 1:
                i=0
                tmpfn,tmpln= name.split(' ')
                cur.execute("select cctID from cctpeople where firstname = '%s' AND lastname = '%s'"%(tmpfn,tmpln))
                iso = cur.fetchone()
                iso = re.sub('[()\']', '', str(iso))
                cur.execute("select punchID from cctpunches,cctpeople where cctpunches.cctID=cctpeople.cctID AND cctpeople.firstname = '%s' AND cctpeople.lastname = '%s'"%(tmpfn,tmpln))
                pID = cur.fetchall()
                for num in pID:
                    num = re.sub('[(),\']', '', str(num))
                    cur.execute("select punchtime from cctpunches,cctpeople where cctpunches.punchID='%s' AND cctpunches.cctID=cctpeople.cctID AND cctpeople.cctID = '%s'"%(num,iso))
                    tmpdate = cur.fetchone()
                    tmpdate = re.sub('[()\']', '', str(tmpdate))
                    tmpdate = re.sub(' ','0',tmpdate)
                    tmpdate = tmpdate[17:]
                    tmpdate = re.sub(',','-',tmpdate)
                    tmpyear,tmpmnth,tmpday,tmps4,tmps5,tmps6,tmps7 = tmpdate.split('-')
                    tmpdate = tmpdate[0:10]

                    if len(tmpmnth) == 3:
                        tmpmnth=tmpmnth[1:]

                    if len(tmpday) == 3:
                        tmpday=tmpday[1:]

                    year, month, day = map(int, tmpdate.split('-'))
                    conDate = datetime.datetime(int(tmpyear), int(tmpmnth), int(tmpday))

                    #insert name
                    sheet1.write(i+1,0,str(tmpfn + ' ' + tmpln))
                    #insert date
                    sheet1.write(i+1,2,str(tmpday + '-' + tmpmnth + '-'+tmpyear))

                    #insert projects
                    cur.execute("select selectedProject from cctpeople,cctprojects,cctpunches where \
                    cctpunches.cctID=cctpeople.cctID AND cctpunches.punchID = '%s'"%(num))
                    pro=cur.fetchone()
                    pro = re.sub('[,()]', '', str(pro))
                    if pro == '0':
                        pro = "Clocked Out"
                    else:
                       cur.execute("select project from cctprojects,cctpunches where \
                       cctprojects.projectID = cctpunches.selectedProject AND cctpunches.selectedProject = '%s' and cctpunches.punchID = '%s'"%(pro,num))
                       pro=cur.fetchone()
                       pro=re.sub('[,()\']', '', str(pro))
                    sheet1.write(i+1,1,str(pro))


                    #insert clock in or out
                    cur.execute("select inorout from cctpeople,cctpunches where cctpunches.punchID = '%s' AND cctpunches.cctID = cctpeople.cctID"%num)
                    tmpinorout = cur.fetchone()
                    sheet1.write(i+1,3,str(tmpinorout))

                    i = i + 1




            elif dtype==2:
                i=0
                tmpfn,tmpln= name.split(' ')
                cur.execute("select cctID from cctpeople where firstname = '%s' AND lastname = '%s'"%(tmpfn,tmpln))
                iso = cur.fetchone()
                iso = re.sub('[()\']', '', str(iso))
                cur.execute("select punchID from cctpunches,cctpeople where cctpunches.cctID=cctpeople.cctID AND cctpeople.firstname = '%s' AND cctpeople.lastname = '%s'"%(tmpfn,tmpln))
                pID = cur.fetchall()


                for num in pID:
                    num = re.sub('[(),\']', '', str(num))
                    print(num)
                    cur.execute("select punchtime from cctpunches,cctpeople where cctpunches.punchID='%s' AND cctpunches.cctID=cctpeople.cctID AND cctpeople.cctID = '%s'"%(num,iso))
                    tmpdate = cur.fetchone()
                    tmpdate = re.sub('[()\']', '', str(tmpdate))
                    tmpdate = re.sub(' ','0',tmpdate)
                    tmpdate = tmpdate[17:]
                    tmpdate = re.sub(',','-',tmpdate)
                    tmpyear,tmpmnth,tmpday,tmps4,tmps5,tmps6,tmps7 = tmpdate.split('-')
                    tmpdate = tmpdate[0:10]

                    if len(tmpmnth) == 3:
                        tmpmnth=tmpmnth[1:]

                    if len(tmpday) == 3:
                        tmpday=tmpday[1:]


                    year, month, day = map(int, tmpdate.split('-'))
                    conDate = datetime.datetime(int(tmpyear), int(tmpmnth), int(tmpday))
                    print(conDate)

                    if date4<=conDate and date5>=conDate:

                        print("yes")
                        #insert name
                        sheet1.write(i+1,0,str(tmpfn + ' ' + tmpln))
                        #insert date
                        sheet1.write(i+1,2,str(tmpday + '-' + tmpmnth + '-'+tmpyear))

                        #insert projects
                        cur.execute("select selectedProject from cctpeople,cctprojects,cctpunches where \
                        cctpunches.cctID=cctpeople.cctID AND cctpunches.punchID = '%s'"%(num))
                        pro=cur.fetchone()
                        pro = re.sub('[,()]', '', str(pro))
                        print(pro)
                        if pro == '0':
                            pro = "Clocked Out"
                        else:
                            cur.execute("select project from cctprojects,cctpunches where \
                            cctprojects.projectID = cctpunches.selectedProject AND cctpunches.selectedProject = '%s' and cctpunches.punchID = '%s'"%(pro,num))
                            pro=cur.fetchone()
                            pro=re.sub('[,()\']', '', str(pro))
                        sheet1.write(i+1,1,str(pro))


                        #insert clock in or out
                        cur.execute("select inorout from cctpeople,cctpunches where cctpunches.punchID = '%s' AND cctpunches.cctID = cctpeople.cctID"%num)
                        tmpinorout = cur.fetchone()
                        sheet1.write(i+1,3,str(tmpinorout))

                    i = i + 1



        sheet1.write(0,0,"Name")
        sheet1.write(0,1,"Selected Project")
        sheet1.write(0,2,"Punch Time")
        sheet1.write(0,3,"In or Out")

        for i in range(0,4):
            if i == 1:
                sheet1.col(i).width = 10000
            else:
                sheet1.col(i).width = 5000

        book.save("CCTReport.xls")

    def initUI(self):
        i = 0
        self.parent.title("Reports")
        self.pack(fill=BOTH, expand=1)
        Style().configure("TButton", padding=(0, 2, 0, 2), font='serif 10')
        xPlace = 75

        cur.execute("select cctID from cctpeople")
        iso = cur.fetchall()

        #cur.execute("select lastname from cctpeople")
        #lname = cur.fetchall()
        names=[]

        for num in iso:
            names.append(i+1)
            cur.execute("select firstname from cctpeople where cctID = '%s'"%num)
            tmp1 = cur.fetchone()
            tmp1 = re.sub('[,()\']', '', str(tmp1))
            cur.execute("select lastname from cctpeople where cctID = '%s'"%num)
            tmp2 = cur.fetchone()
            tmp2 = re.sub('[,()\']', '', str(tmp2))
            names[i]= tmp1 + ' ' + tmp2
            i = i + 1

        nameSelect = StringVar()
        nameSelect.set(names)
        #print(names)

        userpwLabel=Label(self, text = "Select Name/s:")
        userpwLabel.place(x=10,y=11)
        v = IntVar()
        b = Radiobutton(self, text="All", variable=v, value=1)
        b.pack()
        b.place(x=110,y=10)
        a = Radiobutton(self, text="Specific", variable=v, value=2)
        a.pack()
        a.place(x=150,y=10)
        w = OptionMenu(self, nameSelect,"Name", *names)
        w.pack()
        w.place(x=230,y=10)


        dateLabel=Label(self, text = "Select Date:")
        dateLabel.place(x=10,y=41)
        da = IntVar()
        d = Radiobutton(self, text="All", variable=da, value=1)
        d.pack()
        d.place(x=110,y=40)
        c = Radiobutton(self, text="Specific", variable=da, value=2)
        c.pack()
        c.place(x=150,y=40)

        self.date1 = Entry(self, width=10)
        self.date1.place(x=220,y=40)
        self.date1.focus()

        dashLabel=Label(self, text = "-to-")
        dashLabel.place(x=305,y=40)

        self.date2 = Entry(self, width=10)
        self.date2.place(x=330,y=40)
        self.date2.focus()

        self.ll=Label(self, text = "Format: yyyy-mm-dd")
        self.ll.pack()
        self.ll.place(x=225,y=60)

        com = 1
        self.genBtn = Button(self, text = "Generate Report",command=lambda: Login.makeReport(v.get(),nameSelect.get(),da.get(),self.date1.get(),self.date2.get(),com))
        self.genBtn.place(x=xPlace+5,y=100)

def main():

    swipe = Tk()
    swipe.geometry("500x200+400+400")
    app = Login(swipe)
    swipe.mainloop()

if __name__ == '__main__':
    main()
