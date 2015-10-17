'''
Created on Mar 23, 2014

@author: bon
'''
import gtk,gtk.gdk
import pango,gobject,glib,datetime
import rang,Glob,Conn

class new:
    #Glob.init()
    def Reg(self):
        self.dialog = gtk.Dialog('', None, 0, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 'Done', gtk.RESPONSE_OK))
        self.dialog.set_default_size(560, 400)
        self.dialog.set_icon_from_file('BON.jpg')
        self.dialog.set_position(gtk.WIN_POS_CENTER)
        #self.dialog.set_opacity(30)
        bg_color = gtk.gdk.Color (55000, 60000, 65535, 0)               
        self.dialog.modify_bg(gtk.STATE_NORMAL, bg_color)
        self.dialog.set_decorated(False)
        self.dialog.set_modal(True)
        
        self.lblcase=gtk.Label(" New files for Archival ")
        self.lblcase.set_size_request(500,30)
        self.lblcase.modify_font(pango.FontDescription("sans 13"))
        self.dialog.vbox.pack_start(self.lblcase, False,False, 0)
        
        fx=gtk.Fixed()
        self.lblReg=gtk.Label('Registry')
        self.lblSer=gtk.Label('Series')
        self.lblCon=gtk.Label('Consignment')
        self.lblLoc=gtk.Label('Location')
        self.lblBox=gtk.Label('Box Num.')
        
        fx.put(self.lblReg,10,10)
        fx.put(self.lblSer,410,10)
        fx.put(self.lblCon,10,40)
        fx.put(self.lblLoc,270,40)
        fx.put(self.lblBox,410,40)
        
        self.txtReg=gtk.combo_box_new_text()
        self.txtReg.set_size_request(300,22)
        for i in range(len(Glob.reg)):
            self.txtReg.append_text(str(Glob.reg[i][0])) 
        
        self.txtCod=gtk.combo_box_new_text()
        self.txtCod.set_size_request(150,22)
        for i in range(len(Glob.ser)):
            self.txtCod.append_text(str(Glob.ser[i][0]))
        self.txtCon=gtk.Entry()
        self.txtLoc=gtk.Entry()
        self.txtLoc.set_size_request(70,22)
        self.txtBox=gtk.Entry()
        self.txtBox.set_size_request(70,22)
        
        stor = gtk.ListStore(str,str,str,str,str,str,str,str)
        stor.append(['',' ',' ',' ',' ',' ',' ',' '])
        self.acts=gtk.ListStore(str)
        for i in range(len(Glob.act)):
            self.acts.append([str(Glob.act[i][0])])
        
        btn=gtk.Button('Add Range')
        btn.set_size_request(100,22)
        btn.connect('button_press_event',self.Addrange,stor)
        
        fx.put(self.txtReg,100,10)
        fx.put(self.txtCod,470,10)
        fx.put(self.txtCon,100,40)
        fx.put(self.txtLoc,330,40)
        fx.put(self.txtBox,470,40)
        fx.put(btn,550,40)
        fx.set_size_request(560,70)        
        
        view = gtk.TreeView(stor)
        color=gtk.gdk.color_parse('AliceBlue')
        view.modify_base(gtk.STATE_NORMAL,color)
        view.modify_font(pango.FontDescription("calibri 11"))
        view.connect('key_press_event',self.key,stor)
        rend=gtk.CellRendererText()
        rend1=gtk.CellRendererText()
        rend1.set_property('editable', True)
        rend2=gtk.CellRendererCombo()
        rend2.set_property('editable',True)
        rend2.set_property("model", self.acts)
        rend2.set_property("text-column", 0)
        rend2.connect('edited',self.update,stor,2)
        rend3=gtk.CellRendererText()
        rend3.set_property('editable', True)
        rend3.connect('edited',self.update,stor,3)
        rend4=gtk.CellRendererText()
        rend4.set_property('editable', True)
        rend4.connect('edited',self.update,stor,4)
        rend5=gtk.CellRendererText()
        rend5.set_property('editable', True)
        rend5.connect('edited',self.update,stor,5)
        rend6=gtk.CellRendererText()
        rend6.set_property('editable', True)
        rend6.connect('edited',self.update,stor,6)
        rend7=gtk.CellRendererText()
        rend7.set_property('editable', True)
        rend7.connect('edited',self.update,stor,7)
        rend9=gtk.CellRendererText()
        rend9.set_property('editable', True)
        rend9.connect('edited',self.update,stor,9)
        rend10=gtk.CellRendererText()
        rend10.set_property('editable', True)
        rend10.connect('edited',self.update,stor,10)
        rend11=gtk.CellRendererText()
        rend11.set_property('editable', True)
        rend11.connect('edited',self.update,stor,11)
        
        col0 = gtk.TreeViewColumn(" File Reference", rend3, text=0 )
        col0.set_min_width(100)
        col1 = gtk.TreeViewColumn(" Subject", rend, text=1 )
        col1.set_min_width(100)
        col2 = gtk.TreeViewColumn(" Volume ", rend4, text=2 )
        col2.set_min_width(30)
        col3 = gtk.TreeViewColumn(" Date Opened", rend5, text=3 )
        col3.set_min_width(70)
        col4 = gtk.TreeViewColumn(" Date Closed ", rend6, text=4 )
        col4.set_min_width(70)
        col5 = gtk.TreeViewColumn(" Ret P. ", rend7, text=5 )
        col5.set_min_width(30)
        col6 = gtk.TreeViewColumn(" Action ", rend2, text=6 )
        col6.set_min_width(110)
        col7 = gtk.TreeViewColumn(" Action Date", rend9, text=7 )
        col7.set_min_width(70)
        
        view.append_column(col0 )
        view.append_column(col1 )
        view.append_column(col2 )
        view.append_column(col3 )
        view.append_column(col4 )
        view.append_column(col5 )
        view.append_column(col6 )
        view.append_column(col7 )
        
        s_win=gtk.ScrolledWindow()
        s_win.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        s_win.set_size_request(800,300)
        s_win.add(view)
        f=gtk.Frame()
        f.add(s_win)
        
        
        sp=gtk.HSeparator()
        self.dialog.vbox.pack_start(sp, False,False, 0)
        self.dialog.vbox.pack_start(fx, False,False, 0)
        sp1=gtk.HSeparator()
        self.dialog.vbox.pack_start(sp1, False,False, 0)
        self.dialog.vbox.pack_start(f, False,False, 0)
        self.dialog.show_all()
        res = self.dialog.run()
        self.dialog.hide()
        store=[]
        for i in range(len(stor)):
            if stor[i][0]!=" " and self.txtReg.get_active()!=-1 :
                sto=[]
                sto.append(self.txtReg.get_active())
                sto.append(self.txtCod.get_active())
                sto.append(self.txtLoc.get_text())
                sto.append(self.txtCon.get_text())
                sto.append(self.txtBox.get_text())
                sto.append(stor[i][0])
                sto.append(stor[i][1])
                sto.append(stor[i][2])
                sto.append(stor[i][3])
                sto.append(stor[i][4])
                sto.append(stor[i][5])
                sto.append(stor[i][6])
                sto.append(stor[i][7])
                store.append(sto)
          
        return res,store
    
    def update(self,widget,path, txt,stor,ren):
        if ren==2:
            if txt!='':
                stor[path][6]=(txt)
        elif ren==3 and txt!='':
            sub=''
            for i in range(len(Glob.ref)):
                if str(Glob.ref[i][0]).upper()==str(txt).upper():            
                    sub=Glob.ref[i][1]
            if sub!='':
                stor[path][0]=(txt)
                stor[path][1]=sub
            else:
                msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                        gtk.BUTTONS_OK,'The Referene Number you entered does not match any File Subject ')
                msgbx.set_decorated(False)
                msgbx.run()
                msgbx.destroy()
        elif ren==4 and txt!='':
                stor[path][2]=(txt)
        elif ren==5 and txt!='':
            try:
                datetime.datetime.strptime(txt,'%d/%m/%Y')
                stor[path][3]=(txt)
            except:
                msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'Invalid Date format, It SHOULD BE IN THE FORMAT DD/MM/YYYY')
                msgbx.set_decorated(False)
                msgbx.run()
                msgbx.destroy()
        elif ren==6 and txt!='':
            try:
                datetime.datetime.strptime(txt,'%d/%m/%Y')
                stor[path][4]=(txt)
            except:
                msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'Invalid Date format, It SHOULD BE IN THE FORMAT DD/MM/YYYY')
                msgbx.set_decorated(False)
                msgbx.run()
                msgbx.destroy()
        elif ren==7 and txt!='':
            try:
                stor[path][5]=int(txt)
            except:
                msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                        gtk.BUTTONS_OK,'Please enter a NUNMERIC value in Months ')
                #msgbx.set_decorated(False)
                res=msgbx.run()
                msgbx.destroy()
        elif ren==8 and txt!='':
                stor[path][6]=(txt)
        elif ren==9 and txt!='':
            try:
                datetime.datetime.strptime(txt,'%d/%m/%Y')
                stor[path][7]=(txt)
            except:
                msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'Invalid Date format, It SHOULD BE IN THE FORMAT DD/MM/YYYY')
                msgbx.set_decorated(False)
                msgbx.run()
                msgbx.destroy()
    
        elif ren==11 and txt!='':
                stor[path][9]=(txt)

        
        #if gtk.gdk.keyval_name(event.keyval)=='Return':
        #stor.append(['  ben',' ',' ',' ',' ','  ','  ','  '])
        
    
    def key(self,widget,event,stor):
        
        if gtk.gdk.keyval_name(event.keyval)=='Delete':
            sel=widget.get_selection()
            mod,it=sel.get_selected()
            if it:
                msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                        gtk.BUTTONS_YES_NO,'You are about to delete a FILE, Are you sure?')
                #msgbx.set_decorated(False)
                res=msgbx.run()
                msgbx.destroy()
                if res==gtk.RESPONSE_YES:                
                    mod.remove(it)
        
        if gtk.gdk.keyval_name(event.keyval)=='Insert':
            path, col = widget.get_cursor()
            columns = [c for c in widget.get_columns() if c.get_visible()]
            stor.append(['','','','','',0,'',''])
            glib.timeout_add(5,widget.set_cursor,tuple(map(sum,zip(path,(1,)))), columns[0], True)   
            
    
        if gtk.gdk.keyval_name(event.keyval)=="Tab":
            path, col = widget.get_cursor() 
            ## only visible columns!! 
            columns = [c for c in widget.get_columns() if c.get_visible()] 
            colnum = columns.index(col)
            if colnum + 1 < len(columns): 
                next_column = columns[colnum + 1]               
    
            else: 
                tmodel = widget.get_model() 
                titer = tmodel.iter_next(tmodel.get_iter(path)) 
                if titer is None: 
                    titer = tmodel.get_iter_first() 
                path = tmodel.get_path(titer) 
                next_column = columns[0] 
    
    
            if gtk.gdk.keyval_name(event.keyval) == 'Tab':             
                glib.timeout_add(5,widget.set_cursor,path, next_column, True)
                
            elif gtk.gdk.keyval_name(event.keyval) == 'Escape':
                pass
    def Addrange(self,widget,event,stor):
        res,ran=rang.New().Ref()
        if res==gtk.RESPONSE_OK:# and ran!=[]:           
            try:
                for i in range(len(ran)):
                    if ran[i]=="":
                        msgbx=gtk.MessageDialog(self.dialog,gtk.DIALOG_MODAL,gtk.MESSAGE_INFO,
                                            gtk.BUTTONS_OK,'Files could not be retrieved as you did not fill in all the parameters')
                        msgbx.set_decorated(False)
                        res=msgbx.run()
                        msgbx.destroy()
                        raise Exception('empty')
                
                sql="select*from dpp_registry where dpp_case_year="+str(ran[2])+\
                " and dpp_case_categ_id =" + str(ran[3])+" and dpp_case_seq_no between "+\
                str(ran[0]) +" and " + str(ran[1])
                dat=Conn.conDB().rang(sql)
                lst='select*from record'
                archd=(Conn.conDB().ref_list(0,lst))
                if dat!=[]:
                    if len(stor)==1 and stor[0][0]=='':
                        stor.clear()
                    for d in range(len(dat)):
                        try:
                            for a in range(len(archd)):# check if exists in database
                                if str(archd[a][5]).upper()==str(dat[d][0]).upper():
                                    raise Exception ('Exists')
                            for b in range(len(stor)):#check if exists if liststore (stor)
                                if str(stor[b][0]).upper()==str(dat[d][0]).upper():
                                    raise Exception ('Exists')
                            stor.append([dat[d][0],dat[d][1],ran[7],dat[d][2],dat[d][3],ran[4],ran[5],ran[6]])
                        except:
                            pass
                    
            except:
                pass
                
            