'''
Created on May 30, 2014

@author: ben
'''
import pygtk
pygtk.require('2.0')
import gtk
import gtk.gdk,pango
import os,new,ser,Conn,Glob,tools,log
import cPickle
class Reg:
    def __init__(self):
        #Glob.init()
        self.back=gtk.Window(gtk.WINDOW_TOPLEVEL)
        try:
            infile=open('conf.dat','r')
            data = cPickle.load(infile)
            infile.close()
            Glob.host=data[0]
            Glob.port=data[1]
            
        except:
            msgbx=gtk.MessageDialog(self.back,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                       gtk.BUTTONS_OK,'System cannot start, Missing Configuration File')
            msgbx.set_decorated(False)
            msgbx.run()
            msgbx.destroy()
            
        Glob.reg=Conn.conDB().reg(0,0)
        Glob.act=Conn.conDB().actions(0,0)
        Glob.ref=Conn.conDB().ref(0,0)
        Glob.ser=Conn.conDB().ser(0,0)
        
        #self.back=gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.back.connect("destroy", lambda wid: gtk.main_quit())
        self.back.set_icon_from_file('BON.jpg')
        self.back.maximize()
        self.back.set_title("Registry")
        self.v=gtk.VBox(False,0)
        self.h=gtk.HBox(False,0)
        self.mbar=gtk.MenuBar()
        menuF=gtk.Menu()
        menuT=gtk.Menu()
        menuR=gtk.Menu()
        self.file=gtk.MenuItem('File')
        self.report=gtk.MenuItem('Reports')
        self.tools=gtk.MenuItem('Tools')
        nw=gtk.MenuItem('New files for Retention')
        nw.connect('button_press_event',self.new)
        cl=gtk.MenuItem('Close')
        cl.connect('button_press_event',self.dest)
        rp=gtk.MenuItem('Reports')
        #rp.connect('button_press_event',self.reports)
        mt=gtk.MenuItem('Material Estimates')
        #mt.connect('button_press_event',self.materials)
        wk=gtk.MenuItem('Duration Estimate')
        #wk.connect('button_press_event',self.Wk_Plan)
        act=gtk.MenuItem('Actions Taken')
        act.connect('button_press_event',self.pref,0)
        ref=gtk.MenuItem('File References')
        ref.connect('button_press_event',self.pref,1)
        reg=gtk.MenuItem('Preferences')
        reg.connect('button_press_event',self.pref,2)
        Acct=gtk.MenuItem('New User Account')
        Acct.connect('button_press_event',self.pref,3)
        menuF.append(nw)
        menuF.append(cl)
        self.file.set_submenu(menuF)
        self.mbar.append(self.file)
        menuR.append(rp)
        menuR.append(mt)
        menuR.append(wk)
        self.report.set_submenu(menuR)
        #self.mbar.append(self.report)
        #menuT.append(act)
        #menuT.append(ref)
        menuT.append(reg)
        self.tools.set_submenu(menuT)
        self.mbar.append(self.tools)
        org=gtk.Label('REGISTRY INFO SYS')
        org.modify_font(pango.FontDescription("sans 18"))
        org.set_size_request(300,35)
        tt=gtk.Table(1,3,False)
        tt.set_size_request(300,40)
        
        btnN=gtk.Button('New')
        btnN.connect('button_press_event',self.new)
        tt.attach(btnN,0,1,0,1)
        
        btnF=gtk.Button('Find')
        btnF.connect('button_press_event',self.find)
        tt.attach(btnF,3,4,0,1)
        self.v.pack_start(self.mbar,False,False,0)
        self.v.pack_start(org,False,True,0)
        self.v.pack_start(tt,False,True,0)
        self.back.add(self.v)
        self.back.show()
        res,acc=log.log().login('Login')
        if res==gtk.RESPONSE_OK:
            try:
                ac=Conn.conDB().acc(0,acc)
                if ac!=[]:
                    Glob.acc=ac
                    menuT.append(Acct)
                    self.back.show_all()
                else:
                    msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'You have entered Either a Wrong User Name or Password,CORRECT ENTRY!! ')
                    msgbx.set_position(gtk.WIN_POS_CENTER)
                    res=msgbx.run()
                    msgbx.destroy()
                    self.destroy()
                    raise Exception('No Account')
            except:
                pass

    def main(self):
        gtk.main()
        
    
    def dest(self,widget,event):
        gtk.main_quit()
    
    def pref(self,widget,event,page):
        if page==3:
            res,acc=log.log().login('Create')
            if res==gtk.RESPONSE_OK:
                try:
                    Conn.conDB().acc(1,acc)
                except:
                    msgbx=gtk.MessageDialog(self.back,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                        gtk.BUTTONS_OK,'The Account Could not be Created as it ALREADY EXISTS')
                    #msgbx.set_decorated(False)
                    msgbx.run()
                    msgbx.destroy()
        else:
            tools.Tools().back(page)
        
    def find(self,widget,event):
        ser.Files().list()
    
    def new(self, widget,event):
        res,stor=new.new().Reg()
        if res==gtk.RESPONSE_OK and stor!=[]:
            Conn.conDB().newEntry(stor)
        
if __name__=='__main__':
    bk=Reg()
    bk.main()
    