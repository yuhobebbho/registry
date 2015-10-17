'''
Created on Jun 8, 2014

@author: bon
'''
'''
Created on Nov 26, 2014

@author: bon
'''

import gtk
import pango,os,datetime
import gtk.gdk,Glob
import ser,printing,Conn

class Files:
    def list(self,data):
        self.dialog = gtk.Dialog()#'', None, 0, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 'Done', gtk.RESPONSE_OK))
        self.dialog.set_default_size(1000, 400)
        self.dialog.set_icon_from_file('BON.jpg')
        self.dialog.set_position(gtk.WIN_POS_CENTER)
        #self.dialog.set_opacity(30)
        bg_color = gtk.gdk.Color (60000, 60000, 65535, 0)               
        self.dialog.modify_bg(gtk.STATE_NORMAL, bg_color)
        self.dialog.set_decorated(False)
        self.dialog.set_modal(True)
        
        self.lblLib=gtk.Label("Results")
        self.lblLib.set_size_request(500,30)
        self.lblLib.modify_font(pango.FontDescription("sans 13"))
        self.dialog.vbox.pack_start(self.lblLib, False,False, 0)
        
        self.lst=gtk.ListStore(str,str,str,str,str,str,str,str,str,str,int,bool)
        for i in range(len(data)):
            self.lst.append([Glob.reg[int(data[i][0])][0],data[i][2],data[i][3],data[i][4],data[i][5],data[i][6],data[i][7],data[i][8],data[i][10],data[i][11],int(data[i][13]),False])
       
        renderer = gtk.CellRendererText()
        renderer1 = gtk.CellRendererToggle()
        renderer1.connect("toggled", self.togg,self.lst) 
        renderer2 = gtk.CellRendererText()
        column = gtk.TreeViewColumn('')
        column.pack_start(renderer1, True)
        column.add_attribute(renderer1, "active", 11)  
        column0 = gtk.TreeViewColumn(" Registry ", renderer2, text=0)
        column0.set_min_width(70)
        column0.set_sort_column_id(0)
        column1 = gtk.TreeViewColumn(" Location ", renderer, text=1)
        column1.set_min_width(70)
        column1.set_sort_column_id(1)
        column2 = gtk.TreeViewColumn(" Consign.. ", renderer, text=2)
        column2.set_min_width(70)
        column2.set_sort_column_id(2)
        column3 = gtk.TreeViewColumn(" Box ", renderer, text=3)
        column3.set_min_width(70)
        column3.set_sort_column_id(3)
        column4 = gtk.TreeViewColumn(" Reference ", renderer2, text=4)
        column4.set_min_width(90)
        column4.set_sort_column_id(4)
        column5 = gtk.TreeViewColumn(" Subject ", renderer2, text=5)
        column5.set_min_width(150)
        column5.set_sort_column_id(5)
        column6 = gtk.TreeViewColumn(" Volume ", renderer2, text=6)
        column6.set_min_width(70)
        column6.set_sort_column_id(6)
        column7 = gtk.TreeViewColumn(" Open Date ", renderer2, text=7)
        column7.set_min_width(70)
        column7.set_sort_column_id(7)
        column8 = gtk.TreeViewColumn(" Retention ", renderer2, text=8)
        column8.set_min_width(70)
        column8.set_sort_column_id(8)
        column9 = gtk.TreeViewColumn(" Action ", renderer2, text=9)
        column9.set_min_width(70)
        column9.set_sort_column_id(9)
        
        
        view=gtk.TreeView(self.lst)
        view.set_search_column(5)
        view.connect('key_press_event',self.key)
        view.append_column(column)
        view.append_column(column0)
        view.append_column(column1)
        view.append_column(column2)
        view.append_column(column3)
        view.append_column(column4)
        view.append_column(column5)
        view.append_column(column6)
        view.append_column(column7)
        view.append_column(column8)
        view.append_column(column9)
        
        
        scr=gtk.ScrolledWindow()
        scr.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        scr.add(view)
        scr.set_size_request(200,120)
        
        lblAct=gtk.Label('Action')
        self.cboAct=gtk.combo_box_new_text()
        for i in range(len(Glob.act)):
            self.cboAct.append_text(str(Glob.act[i][0]))
        self.ActDate=gtk.Entry()
        self.ActDate.set_text('Actn. Date')
        self.ActDate.set_max_length(10)
        self.ActDate.connect('focus-out-event',self.checkdate)
        btnApp=gtk.Button('Apply')
        btnApp.connect('button_press_event',self.upAction)
        
        t=gtk.Table(10,10,True)
        t.set_size_request(700,400)
        t.set_border_width(5)
        t.set_col_spacings(5)
        t.set_row_spacings(5)
        t.attach(scr,0,10,0,9)
        t.attach(lblAct,2,4,9,10)
        t.attach(self.cboAct,4,6,9,10)
        t.attach(self.ActDate,6,8,9,10)
        t.attach(btnApp,8,10,9,10)
        btnP=gtk.Button('Print to PDF')
        btnP.connect('button_press_event',self.printData)
        fm=gtk.Frame()
        fm.add(t)
        sp=gtk.HSeparator()
        self.dialog.vbox.pack_start(sp, False,False, 0)
        
        self.dialog.set_border_width(3)
        self.dialog.vbox.pack_start(fm, False,False, 0)
        self.dialog.vbox.pack_start(btnP, False,False, 0)
        self.dialog.show_all()
        res = self.dialog.run()
        self.dialog.hide()
        ser.Files().list()
        return res
    
    def togg(self,widget,path,stor):
        stor[path][11] = not stor[path][11]
        
    def printData(self,widget,ev):
        if self.lst !=[]:
            prt=printing.Print().on_print(self.lst, 'current.pdf')
            #n='start '+str(os.sep.join((os.path.expanduser('~'),'Desktop')))+str('/current.pdf')
            os.system('start current.pdf')
        else:
            msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                    gtk.BUTTONS_OK,'There are no records to Export')
            msgbx.run()
            msgbx.destroy()
    def key(self,widget,event):
        if gtk.gdk.keyval_name(event.keyval)=='Delete' and int(Glob.acc[1])==0:
            sel=widget.get_selection()
            mod,it=sel.get_selected()
            if it:
                msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                        gtk.BUTTONS_YES_NO,'You are about to delete a FILE, Are you sure?')
                #msgbx.set_decorated(False)
                res=msgbx.run()
                msgbx.destroy()
                if res==gtk.RESPONSE_YES: 
                    try:
                        Conn.conDB().ref_list(1, mod[it][10])              
                        mod.remove(it)
                    except:
                        msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'An error Occured, the Record was not Deleted?')
                        #msgbx.set_decorated(False)
                        msgbx.run()
                        msgbx.destroy()
                    

    def upAction(self,widget,event):
        try:
            datetime.datetime.strptime(self.ActDate.get_text(),'%d/%m/%Y')
            if self.cboAct.get_active<0:
                msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'You have Not Selected Nay Action to Take!!')
                msgbx.set_decorated(False)
                res=msgbx.run()
                msgbx.destroy()
            else:
                store=[]
                itr=[]
                model = self.cboAct.get_model()
                active = self.cboAct.get_active()
                for it in range(len(self.lst)):
                    if self.lst[it][11]:
                        if  str(model[active][0])!=str(self.lst[it][9]):
                            stor=[]
                            '''#convert the combo active value to its item value'''
                            stor.append(model[active][0])
                            stor.append(self.ActDate.get_text())
                            stor.append(self.lst[it][10])
                            store.append(stor)
                        else:
                            self.lst[it][11]=False
                            
                if store!=[]:
                    Conn.conDB().recordUp(store)
                for row in self.lst:
                    if row[11]:
                        self.lst.remove(row.iter)
        except:
            msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'The Action Date is not Correct')
            msgbx.set_decorated(True)
            res=msgbx.run()
            msgbx.destroy()        
                
    
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
        
    