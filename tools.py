'''
Created on Jun 13, 2014

@author: bon
'''

import gtk,gtk.gdk
import pango
import Glob,Conn

class Tools:
    def back(self,page):
        self.dialog = gtk.Dialog('', None, 0, ('Close', gtk.RESPONSE_CANCEL))
        self.dialog.set_default_size(600, 400)
        self.dialog.set_icon_from_file('BON.jpg')
        self.dialog.set_position(gtk.WIN_POS_CENTER)
        #self.dialog.set_opacity(30)
        bg_color = gtk.gdk.Color (60000, 60000, 65535, 0)               
        self.dialog.modify_bg(gtk.STATE_NORMAL, bg_color)
        self.dialog.set_decorated(False)
        self.dialog.set_modal(True)
        
        self.lblcase=gtk.Label("Preferences")
        self.lblcase.set_size_request(500,30)
        self.lblcase.modify_font(pango.FontDescription("sans 13"))
        self.dialog.vbox.pack_start(self.lblcase, False,False, 0)
        
        sp=gtk.HSeparator()
        self.dialog.vbox.pack_start(sp, False,False, 0)
        ntbk=gtk.Notebook()
        bg_color = gtk.gdk.Color (50000, 50000, 65535, 0)        
        ntbk.modify_bg(gtk.STATE_NORMAL, bg_color)
        ntbk.show()
        
        ntbk.prepend_page(Actions().taken(), gtk.Label(" Actions Takable "))
        ntbk.prepend_page(Registry().reg(), gtk.Label(" Registry "))
        ntbk.prepend_page(Reference().ref(), gtk.Label(" Reference "))
        ntbk.prepend_page(Series().ser(), gtk.Label(" Series "))
        ntbk.set_current_page(page)
        
        self.dialog.vbox.pack_start(ntbk, False,False, 0)
        self.dialog.set_border_width(3)
        #self.dialog.vbox.pack_start(sp, False,False, 0)
        self.dialog.show_all()
        res = self.dialog.run()
        self.dialog.hide()
        
        return res

class Actions:
    def taken(self):
        self.dialog = gtk.VBox(False,5)
        bg_color = gtk.gdk.Color (60000, 60000, 65535, 0)        
        self.dialog.modify_bg(gtk.STATE_NORMAL, bg_color)
        fx=gtk.Fixed()
        h=gtk.HBox(False,5)
        
        view = gtk.TreeView()
        self.acts=gtk.ListStore(str,int)
        
        self.lblAct=gtk.Label('Action')
        self.txtAct=gtk.Entry()
        self.txtAct.set_size_request(200,27)
        self.txtAct.connect('key_press_event',self.key,view)
        btn=gtk.Button("Add")
        btn.set_size_request(150,27)
        btn.connect('button_press_event',self.addAct,view)
        fx.put(self.lblAct,10,10)
        fx.put(self.txtAct,120,10)
        fx.put(btn,340,10)
        fmedpp=gtk.Frame()
        fmedpp.set_size_request(580,50)
        fmedpp.add(fx)
        h.pack_start(fmedpp,False, False, 0)
        #self.dialog.vbox.pack_start(fmedpp, False,False, 0)
        
        fmesum=gtk.Frame()
        
        for i in range(len(Glob.act)):
            self.acts.append([str(Glob.act[i][0]),Glob.act[i][1]])
        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited',self.editAct,self.acts)
        column0 = gtk.TreeViewColumn("  Action ", renderer, text=0)
        view.set_model(self.acts)
        view.modify_font(pango.FontDescription("calibri 12"))
        view.append_column( column0 )
        view.connect('key_press_event',self.keyAct)
        
        scrl=gtk.ScrolledWindow()
        scrl.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        scrl.add(view)
        scrl.set_size_request(200,200)
        
        sp=gtk.HSeparator()
        
        self.dialog.pack_start(h, False,False, 0)
        self.dialog.pack_start(scrl, False,False, 0)
        self.dialog.pack_start(sp, False,False, 0)
        
        return self.dialog
    
    def addAct(self,widget,ev,view):
        if self.txtAct.get_text()!='':
            try:
                for i in range(len(self.acts)):
                    if str(self.acts[i][0]).upper()==str(self.txtAct.get_text()).upper():
                        raise Exception('Exists')
                Conn.conDB().actions(2,self.txtAct.get_text())
                Glob.act=Conn.conDB().actions(0,0)
                self.acts.clear()
                self.txtAct.set_text('')
                for i in range(len(Glob.act)):
                    self.acts.append([str(Glob.act[i][0]),Glob.act[i][1]])
                view.set_model(self.acts)
            except:
                msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                                gtk.BUTTONS_OK,'The Action could not be add becasue it cannot acquire a unique ID')
                msgbx.set_decorated(False)
                msgbx.set_position(gtk.WIN_POS_CENTER)
                res=msgbx.run()
                msgbx.destroy()
    
    def editAct(self,widget,path, txt,stor):
        if txt!='' and int(Glob.acc[1])==1:
            stor[path][0]=(txt)
            Glob.act[int(path)][0]=txt
            Conn.conDB().actions(1, stor[path])
            
    def key(self,widget,event,view):
        
        if gtk.gdk.keyval_name(event.keyval)=='Return':
            self.addAct(widget, event, view)
    
    def keyAct(self,widget,event):
        if gtk.gdk.keyval_name(event.keyval)=='Delete' and int(Glob.acc[1])==1:
            sel=widget.get_selection()
            mod,it=sel.get_selected()
            if it:
                msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                        gtk.BUTTONS_YES_NO,'You are about to delete a Action, Are you sure?')
                #msgbx.set_decorated(False)
                msgbx.set_position(gtk.WIN_POS_CENTER)
                res=msgbx.run()
                msgbx.destroy()
                if res==gtk.RESPONSE_YES: 
                    try:
                        Conn.conDB().actions(3, mod[it][1])              
                        mod.remove(it)
                        Glob.act=[]
                        for i in range(len(self.acts)):
                            Glob.ref.append([self.acts[i][0],self.acts[i][1]])
                    except:
                        msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'An error Occured, the Action was not Deleted?')
                        #msgbx.set_decorated(False)
                        msgbx.set_position(gtk.WIN_POS_CENTER)
                        msgbx.run()
                        msgbx.destroy()    
        
class Registry:
    def reg(self):
        self.dialog = gtk.VBox(False,5)
        bg_color = gtk.gdk.Color (60000, 60000, 65535, 0)        
        self.dialog.modify_bg(gtk.STATE_NORMAL, bg_color)
        fx=gtk.Fixed()
        h=gtk.HBox(False,5)
        
        view = gtk.TreeView()
        self.regs=gtk.ListStore(str,int)
        
        self.lblReg=gtk.Label('Registry')
        self.txtReg=gtk.Entry()
        self.txtReg.set_size_request(200,27)
        self.txtReg.connect('key_press_event',self.key,view)
        btn=gtk.Button("Add")
        btn.set_size_request(150,27)
        btn.connect('button_press_event',self.addReg,view)
        fx.put(self.lblReg,10,10)
        fx.put(self.txtReg,120,10)
        fx.put(btn,340,10)
        fmedpp=gtk.Frame()
        fmedpp.set_size_request(580,50)
        fmedpp.add(fx)
        h.pack_start(fmedpp,False, False, 0)
        #self.dialog.vbox.pack_start(fmedpp, False,False, 0)
        
        fmesum=gtk.Frame()
        
        for i in range(len(Glob.reg)):
            self.regs.append([str(Glob.reg[i][0]),Glob.reg[i][1]])
        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited',self.editReg,self.regs)
        column0 = gtk.TreeViewColumn("  Registries ", renderer, text=0)
        view.set_model(self.regs)
        view.modify_font(pango.FontDescription("calibri 12"))
        view.append_column( column0 )
        view.connect('key_press_event',self.keyReg)
        
        scrl=gtk.ScrolledWindow()
        scrl.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        scrl.add(view)
        scrl.set_size_request(200,200)
        
        sp=gtk.HSeparator()
        
        self.dialog.pack_start(h, False,False, 0)
        self.dialog.pack_start(scrl, False,False, 0)
        self.dialog.pack_start(sp, False,False, 0)
        
        return self.dialog
    
    def addReg(self,widget,ev,view):
        if self.txtReg.get_text()!='':
            try:
                for i in range(len(self.regs)):
                    if str(self.regs[i][0]).upper()==str(self.txtReg.get_text()).upper():
                        raise Exception('Exists')
                Conn.conDB().reg(2,self.txtReg.get_text())
                Glob.reg=Conn.conDB().reg(0,0)
                self.regs.clear()
                self.txtReg.set_text('')
                for i in range(len(Glob.reg)):
                    self.regs.append([str(Glob.reg[i][0]),Glob.reg[i][1]])
                view.set_model(self.regs)
            except:
                msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                                gtk.BUTTONS_OK,'The Registry could not be add becasue it cannot acquire a Unique ID')
                msgbx.set_decorated(False)
                msgbx.set_position(gtk.WIN_POS_CENTER)
                res=msgbx.run()
                msgbx.destroy()
        
    def editReg(self,widget,path, txt,stor):
        if txt!=''and int(Glob.acc[1])==1:
            stor[path][0]=(txt)
            Glob.reg[int(path)][0]=txt
            Conn.conDB().reg(1, stor[path])
            
    def key(self,widget,event,view):
        
        if gtk.gdk.keyval_name(event.keyval)=='Return':
            self.addReg(widget, event, view)
    
    def keyReg(self,widget,event):
        if gtk.gdk.keyval_name(event.keyval)=='Delete' and int(Glob.acc[1])==1:
            sel=widget.get_selection()
            mod,it=sel.get_selected()
            if it:
                msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                        gtk.BUTTONS_YES_NO,'You are about to delete a Registry, Are you sure?')
                #msgbx.set_decorated(False)
                msgbx.set_position(gtk.WIN_POS_CENTER)
                res=msgbx.run()
                msgbx.destroy()
                if res==gtk.RESPONSE_YES: 
                    try:
                        Conn.conDB().reg(3, mod[it][1])              
                        mod.remove(it)
                        Glob.reg=[]
                        for i in range(len(self.regs)):
                            Glob.reg.append([self.regs[i][0],self.regs[i][1]])
                    except:
                        msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'An error Occured, the Registry was not Deleted?')
                        #msgbx.set_decorated(False)
                        msgbx.set_position(gtk.WIN_POS_CENTER)
                        msgbx.run()
                        msgbx.destroy()
    

class Reference:
    def ref(self):
        self.dialog = gtk.VBox(False,5)
        bg_color = gtk.gdk.Color (60000, 60000, 65535, 0)        
        self.dialog.modify_bg(gtk.STATE_NORMAL, bg_color)
        fx=gtk.Fixed()
        h=gtk.HBox(False,5)
        
        view = gtk.TreeView()
        self.refs=gtk.ListStore(str,str)
        
        self.lblRef=gtk.Label('Reference')
        self.lblSub=gtk.Label('Subject')
        self.txtRef=gtk.Entry()
        self.txtRef.set_size_request(150,27)
        self.txtSub=gtk.Entry()
        self.txtSub.set_size_request(350,27)
        self.txtSub.connect('key_press_event',self.key,view)
        btn=gtk.Button("Add")
        btn.set_size_request(150,27)
        btn.connect('button_press_event',self.addRef,view)
        fx.put(self.lblRef,10,10)
        fx.put(self.lblSub,170,10)
        fx.put(self.txtRef,10,40)
        fx.put(self.txtSub,170,40)
        fx.put(btn,370,10)
        fmedpp=gtk.Frame()
        fmedpp.set_size_request(580,75)
        fmedpp.add(fx)
        h.pack_start(fmedpp,False, False, 0)
        #self.dialog.vbox.pack_start(fmedpp, False,False, 0)
        
        fmesum=gtk.Frame()
        
        for i in range(len(Glob.ref)):
            self.refs.append([str(Glob.ref[i][0]),Glob.ref[i][1]])
        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited',self.editRef,self.refs)
        renderer1 = gtk.CellRendererText()
        column0 = gtk.TreeViewColumn("  Reference ", renderer1, text=0)
        column0.set_sort_column_id(0)
        column1 = gtk.TreeViewColumn("  Subject ", renderer, text=1)
        column1.set_sort_column_id(1)
        view.set_model(self.refs)
        view.modify_font(pango.FontDescription("calibri 12"))
        view.append_column( column0 )
        view.append_column( column1 )
        view.connect('key_press_event',self.keyRef)
        view.set_search_column(0)
        
        scrl=gtk.ScrolledWindow()
        scrl.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        scrl.add(view)
        scrl.set_size_request(200,200)
        
        sp=gtk.HSeparator()
        
        self.dialog.pack_start(h, False,False, 0)
        self.dialog.pack_start(scrl, False,False, 0)
        self.dialog.pack_start(sp, False,False, 0)
        
        return self.dialog
    
    def addRef(self,widget,ev,view):
        if self.txtRef.get_text()!='' and self.txtSub.get_text()!='':
            try:
                for i in range(len(self.refs)):
                    if str(self.refs[i][0]).upper()==str(self.txtRef.get_text()).upper():
                        raise Exception('Exists')
                data=[]
                data.append(self.txtRef.get_text())
                data.append(self.txtSub.get_text())
                Conn.conDB().ref(2,data)
                Glob.ref.append(([self.txtRef.get_text(),self.txtSub.get_text()]))
                self.refs.append([self.txtRef.get_text(),self.txtSub.get_text()])
                self.txtRef.set_text('')
                self.txtSub.set_text('')
                
            except:
                msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                                gtk.BUTTONS_OK,'The Reference could not be add becasue it cannot acquire a Unique ID')
                msgbx.set_decorated(False)
                msgbx.set_position(gtk.WIN_POS_CENTER)
                res=msgbx.run()
                msgbx.destroy()
        
    def editRef(self,widget,path, txt,stor):
        if txt!='' and int(Glob.acc[1])==1:
            stor[path][1]=(txt)
            Glob.ref[int(path)][1]=txt
            Conn.conDB().ref(1, stor[path])
            
    def key(self,widget,event,view):
        
        if gtk.gdk.keyval_name(event.keyval)=='Return':
            self.addRef(widget, event, view)
        
    def keyRef(self,widget,event):
        if gtk.gdk.keyval_name(event.keyval)=='Delete' and int(Glob.acc[1])==1:
            sel=widget.get_selection()
            mod,it=sel.get_selected()
            if it:
                msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                        gtk.BUTTONS_YES_NO,'You are about to delete a Reference, Are you sure?')
                #msgbx.set_decorated(False)
                msgbx.set_position(gtk.WIN_POS_CENTER)
                res=msgbx.run()
                msgbx.destroy()
                if res==gtk.RESPONSE_YES: 
                    try:
                        Conn.conDB().ref(3, mod[it][0])              
                        mod.remove(it)
                        Glob.ref=[]
                        for i in range(len(self.refs)):
                            Glob.ref.append([self.refs[i][0],self.refs[i][1]])
                    except:
                        msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'An error Occured, the Reference was not Deleted?')
                        #msgbx.set_decorated(False)
                        msgbx.set_position(gtk.WIN_POS_CENTER)
                        msgbx.run()
                        msgbx.destroy()
    
    
class Series:
    def ser(self):
        self.dialog = gtk.VBox(False,5)
        bg_color = gtk.gdk.Color (60000, 60000, 65535, 0)        
        self.dialog.modify_bg(gtk.STATE_NORMAL, bg_color)
        fx=gtk.Fixed()
        h=gtk.HBox(False,5)
        
        view = gtk.TreeView()
        self.regs=gtk.ListStore(str,int)
        
        self.lblReg=gtk.Label('Registry')
        self.txtReg=gtk.Entry()
        self.txtReg.set_size_request(200,27)
        self.txtReg.connect('key_press_event',self.key,view)
        btn=gtk.Button("Add")
        btn.set_size_request(150,27)
        btn.connect('button_press_event',self.addReg,view)
        fx.put(self.lblReg,10,10)
        fx.put(self.txtReg,120,10)
        fx.put(btn,340,10)
        fmedpp=gtk.Frame()
        fmedpp.set_size_request(580,50)
        fmedpp.add(fx)
        h.pack_start(fmedpp,False, False, 0)
        #self.dialog.vbox.pack_start(fmedpp, False,False, 0)
        
        fmesum=gtk.Frame()
        
        for i in range(len(Glob.ser)):
            self.regs.append([str(Glob.ser[i][0]),Glob.ser[i][1]])
        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited',self.editReg,self.regs)
        column0 = gtk.TreeViewColumn("  Registries ", renderer, text=0)
        view.set_model(self.regs)
        view.modify_font(pango.FontDescription("calibri 12"))
        view.append_column( column0 )
        view.connect('key_press_event',self.keyReg)
        
        scrl=gtk.ScrolledWindow()
        scrl.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        scrl.add(view)
        scrl.set_size_request(200,200)
        
        sp=gtk.HSeparator()
        
        self.dialog.pack_start(h, False,False, 0)
        self.dialog.pack_start(scrl, False,False, 0)
        self.dialog.pack_start(sp, False,False, 0)
        
        return self.dialog
    
    def addReg(self,widget,ev,view):
        if self.txtReg.get_text()!='':
            try:
                for i in range(len(self.regs)):
                    if str(self.regs[i][0]).upper()==str(self.txtReg.get_text()).upper():
                        raise Exception('Exists')
                Conn.conDB().ser(2,self.txtReg.get_text())
                Glob.ser=Conn.conDB().ser(0,0)
                self.regs.clear()
                self.txtReg.set_text('')
                for i in range(len(Glob.ser)):
                    self.regs.append([str(Glob.ser[i][0]),Glob.ser[i][1]])
                view.set_model(self.regs)
            except:
                msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                                gtk.BUTTONS_OK,'The Series could not be add becasue it cannot acquire a Unique ID')
                msgbx.set_decorated(False)
                msgbx.set_position(gtk.WIN_POS_CENTER)
                res=msgbx.run()
                msgbx.destroy()
        
    def editReg(self,widget,path, txt,stor):
        if txt!=''and int(Glob.acc[1])==1:
            stor[path][0]=(txt)
            Glob.ser[int(path)][0]=txt
            Conn.conDB().ser(1, stor[path])
            
    def key(self,widget,event,view):
        
        if gtk.gdk.keyval_name(event.keyval)=='Return':
            self.addReg(widget, event, view)
    
    def keyReg(self,widget,event):
        if gtk.gdk.keyval_name(event.keyval)=='Delete' and int(Glob.acc[1])==1:
            sel=widget.get_selection()
            mod,it=sel.get_selected()
            if it:
                msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                        gtk.BUTTONS_YES_NO,'You are about to delete a Series, Are you sure?')
                #msgbx.set_decorated(False)
                msgbx.set_position(gtk.WIN_POS_CENTER)
                res=msgbx.run()
                msgbx.destroy()
                if res==gtk.RESPONSE_YES: 
                    try:
                        Conn.conDB().ser(3, mod[it][1])              
                        mod.remove(it)
                        Glob.ser=[]
                        for i in range(len(self.regs)):
                            Glob.ser.append([self.regs[i][0],self.regs[i][1]])
                    except:
                        msgbx=gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'An error Occured, the Series was not Deleted?')
                        #msgbx.set_decorated(False)
                        msgbx.set_position(gtk.WIN_POS_CENTER)
                        msgbx.run()
                        msgbx.destroy()

