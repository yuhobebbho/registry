'''
Created on Jun 3, 2014

@author: ben
'''
'''
Created on Dec 31, 2013

@author: bon
'''

import gtk
import sqlite3,pango
import datetime
import Glob

class New:       
    
    def Ref(self):
        tit='Range Assignment '
        self.dialog = gtk.Dialog(tit, None, 0, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 'Done', gtk.RESPONSE_OK))
        self.dialog.set_default_size(500, 200)
        self.dialog.set_position(gtk.WIN_POS_CENTER)
        self.dialog.set_icon_from_file('BON.jpg')
        #self.dialog.set_opacity(30)
        bg_color = gtk.gdk.Color (60000, 60000, 65535, 0)               
        self.dialog.modify_bg(gtk.STATE_NORMAL, bg_color)
        self.dialog.set_decorated(False)
        self.dialog.set_modal(True)
        tt=gtk.Table(5,2,False)
        tt.set_border_width(10)
        tt.set_row_spacings(10)        
        
        lbl=gtk.Label('New Range')
        lbl.modify_font(pango.FontDescription("calibri 14"))
        lblNFrom=gtk.Label("Number")
        lblFromY=gtk.Label("Volume")
        lblNTo=gtk.Label("Number")
        lblToY=gtk.Label("Year")
        lblTo=gtk.Label("TO")           
        self.txtNFrom=gtk.Entry()
        self.txtNFrom.connect('changed',self.checkInt)
        self.txtVol=gtk.Entry()
        self.txtVol.connect('changed',self.checkInt)
        self.txtNTo=gtk.Entry()
        self.txtNTo.connect('changed',self.checkInt)
        self.txtNToY=gtk.Entry()
        self.txtNToY.set_max_length(4)
        self.txtNToY.connect('changed',self.checkInt)
        
        tt.attach(lblNFrom,0,1,0,1)
        tt.attach(lblFromY,1,2,0,1)
        tt.attach(lblNTo,3,4,0,1)
        tt.attach(lblToY,4,5,0,1)
        tt.attach(self.txtNFrom,0,1,1,2)
        tt.attach(self.txtVol,1,2,1,2)
        tt.attach(lblTo,2,3,1,2)
        tt.attach(self.txtNTo,3,4,1,2)
        tt.attach(self.txtNToY,4,5,1,2)
        
        lblT=gtk.Label('Type')
        self.txtType=gtk.combo_box_new_text()
        self.txtType.append_text("CO")
        self.txtType.append_text("CN")
        self.txtType.append_text("CV")
        self.txtType.append_text("CM")
        lblRet=gtk.Label('Retention Period')
        self.txtRet=gtk.Entry()
        self.txtRet.connect('changed',self.checkInt)
        
        lblAct=gtk.Label('Action')
        self.Act=gtk.combo_box_new_text()
        for i in range(len(Glob.act)):
            self.Act.append_text(str(Glob.act[i][0]))
        lblActDate=gtk.Label('Action Date')
        self.ActDate=gtk.Entry()
        self.ActDate.set_max_length(10)
        self.ActDate.connect('focus-out-event',self.checkdate)
        t=gtk.Table(4,2,False)
        t.attach(lblT,0,1,0,1)
        t.attach(lblRet,1,2,0,1)
        t.attach(lblAct,2,3,0,1)
        t.attach(lblActDate,3,4,0,1)
        t.attach(self.txtType,0,1,1,2)
        t.attach(self.txtRet,1,2,1,2)
        t.attach(self.Act,2,3,1,2)
        t.attach(self.ActDate,3,4,1,2)
        
        self.dialog.vbox.pack_start(lbl, True, True, 0)
        sp=gtk.HSeparator()
        self.dialog.vbox.pack_start(sp, True, True, 0)
        self.dialog.vbox.pack_start(tt, True, True, 0)
        self.dialog.vbox.pack_start(t, True, True, 0)
        sp=gtk.HSeparator()
        self.dialog.vbox.pack_start(sp, True, True, 0)
        self.dialog.show_all()
        res = self.dialog.run()
        self.dialog.hide()
        
        ran=[]
        try:
            ran.append(int(self.txtNFrom.get_text()))
            #ran.append(self.txtNFromY.get_text())
            ran.append(int(self.txtNTo.get_text()))
            ran.append(self.txtNToY.get_text())
            ran.append(int(self.txtType.get_active())+1)
            ran.append(self.txtRet.get_text())
            '''#convert the combo active value to its item value'''
            model = self.Act.get_model()
            active = self.Act.get_active()
            if active < 0:
                ran.append('')
            else:
                ran.append(model[active][0])
            ran.append(self.ActDate.get_text())
            ran.append(self.txtVol.get_text())
        except:
            pass
        return res,ran
    
    def updateNum(self,widget, path, txt,stor):
        if txt!='':
            try:
                if stor[path][2]<int(txt):
                    txt=stor[path][2]
                stor[path][2]=int(txt)
            except:
                pass#stor[path][2]=1
    
    def togg(self,widget,path,stor):
        stor[path][0] = not stor[path][0]
    
    def checkInt(self,widget):
        if widget.get_text()!='':
            try:
                int(widget.get_text())
            except:
                widget.set_text(str((widget.get_text()[:len(widget.get_text())-1])))
                widget.set_position(len(widget.get_text()))
    def checkdate(self,widget,event):
        if widget.get_text()!='':
            try:
                datetime.datetime.strptime(widget.get_text(),'%d/%m/%Y')
            except:
                widget.set_text('')
                msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'Invalid Date format, It SHOULD BE IN THE FORMAT DD/MM/YYYY')
                msgbx.set_decorated(False)
                msgbx.run()
                msgbx.destroy()
                return False
                 

    
    
               
    