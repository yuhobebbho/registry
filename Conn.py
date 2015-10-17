'''
Created on May 30, 2014

@author: ben
'''
import pyodbc
import gtk
import tools
import cPickle
import socket
import sys
import Glob
class conDB:
    def server(self,data):  
        try:      
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to server and send data
            sock.connect((Glob.host,int(Glob.port)))
            sock.send(data)
            # Receive data from the server and shut down
            received = sock.recv(1048576)
            sock.close()
            rec=cPickle.loads(received)
            return rec
        except:
            msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                       gtk.BUTTONS_OK,'System cannot start, Failure to connect to te server')
            msgbx.set_decorated(False)
            msgbx.run()
            msgbx.destroy()  
    
    def reg(self,opt,data): 
        if int(opt)==0:        
            row=self.server('select*from reg')
            lst=[]
            for r in range(len(row)):
                lst.append([row[r][0],row[r][1]])
            return lst 
        elif int(opt)==1:
            self.server("update reg set reg='" +str(data[0])+"' where id="+str(data[1]))
        elif int(opt)==2:
            self.server("insert into reg values('" +str(data)+"',NULL)")
        elif int(opt)==3:
            self.server("delete from reg where id=" +str(data))          
    
    def actions(self,opt,data): 
        if int(opt)==0:
            row=self.server('select*from action')
            lst=[]
            for r in range(len(row)):
                lst.append([row[r][0],row[r][1]])
            return lst
        elif int(opt)==1:
            row=self.server("update action set action='" +str(data[0])+"' where id="+str(data[1]))
        elif int(opt)==2:
            row=self.server("insert into action values('" +str(data)+"',NULL)")
          
        elif int(opt)==3:
            row=self.server("delete from action where id=" +str(data))
            
    
    def ser(self,opt,data): 
        if int(opt)==0:
            row=self.server('select*from serie')
            lst=[]
            for r in range(len(row)):
                lst.append([row[r][0],row[r][1]])
            return lst
        elif int(opt)==1:
            row=self.server("update serie set serie='" +str(data[0])+"' where id="+str(data[1]))
        elif int(opt)==2:
            row=self.server("insert into serie values('" +str(data)+"',NULL)")
          
        elif int(opt)==3:
            row=self.server("delete from serie where id=" +str(data))
                    
    def ref(self,opt,data):
        if int(opt)==0:
            row=self.server("select*from ref")
            lst=[]
            for r in range(len(row)):
                lst.append([row[r][0],row[r][1]])
            return lst 
        
        elif int(opt)==1:
            self.server("update ref set name='" +str(data[1])+"' where ref='"+str(data[0])+"'")
        elif int(opt)==2:
            self.server("insert into ref values('" +str(data[0])+"','" + str(data[1])+"')")
        
        elif int(opt)==3:
            self.server("delete from ref where ref='" +str(data)+"'")
            
    
          
    def ref_list(self,opt,data):
        if int(opt)==0:
            lst=self.server(data)
            return lst
        elif int(opt)==1: 
            self.server("delete from record where id="+str(data))
        
                     
    def newEntry(self,data):        
        for i in range(len(data)):
            try:
                self.server("insert into record values('" +str(data[i][0])+"','"+str(data[i][1])+"','"+\
                str(data[i][2])+"','"+str(data[i][3])+"','"+str(data[i][4])+"','"+str(data[i][5])+"','"+\
                str(data[i][6])+"','"+str(data[i][7])+ "','"+str(data[i][8])+"','"+str(data[i][9])+"','"+\
                str(data[i][10])+"','"+str(data[i][11])+"','"+str(data[i][12])+"',NULL)")
            except:
                pass
        
    def rang(self,sql):
        
        self.cnx=pyodbc.connect("dsn=DPPCmas")
        self.cur=self.cnx.cursor()
        self.cur.execute(sql)
        row=self.cur.fetchall()
        rw=[]
        cat=[0,'CO','CN','CV','CM']
        for r in range(len(row)):
            if row[r][2]==1:
                rw.append([str(row[r][1])+"-"+cat[int(row[r][2])]+"-"+str(row[r][3])+"-"+str(row[r][5]),row[r][8],row[r][6],row[r][20]])
            else:
                rw.append([str(row[r][1])+"-"+cat[int(row[r][2])]+"-"+str(row[r][3])+"-"+str(row[r][5]),row[r][7],row[r][6],row[r][20]])
        self.cur.close()
        self.cnx.commit()
        self.cnx.close()
        return rw 
    
    def acc(self,opt,ac):
        if int(opt)==0:
            r=self.server("select*from registry where nam='"+ac[0]+"' and nam2='"+ac[1]+"'")
            lst=[]
            try:
                lst.append(r[0][0])
                lst.append(r[0][2])
            except:
                pass
            return lst
        elif int(opt)==1:
            self.server("insert into registry values('" +ac[0]+"','"+ac[1]+"',"+str(ac[2])+")")
    
    def recordUp(self,data):
        for d in range(len(data)):
            self.server("update record set act='"+str(data[d][0])+"',actdate='"+\
                             str(data[d][1])+"' where id ="+str(data[d][2]))
        