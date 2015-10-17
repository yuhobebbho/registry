import gtk
import pango
import Glob,Conn,records
class Files:
    def list(self):
        self.dialog = gtk.Dialog()#'', None, 0, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 'Done', gtk.RESPONSE_OK))
        self.dialog.set_default_size(600, 400)
        self.dialog.set_icon_from_file('BON.jpg')
        self.dialog.set_position(gtk.WIN_POS_CENTER)
        #self.dialog.set_opacity(30)
        bg_color = gtk.gdk.Color (60000, 60000, 65535, 0)               
        self.dialog.modify_bg(gtk.STATE_NORMAL, bg_color)
        self.dialog.set_decorated(False)
        self.dialog.set_modal(True)
        
        self.lblLib=gtk.Label("Registry")
        self.lblLib.set_size_request(500,30)
        self.lblLib.modify_font(pango.FontDescription("sans 13"))
        self.dialog.vbox.pack_start(self.lblLib, False,False, 0)
        lblReg=gtk.Label('Registry')
        lblCode=gtk.Label('Series')
        lblV=gtk.Label('Volume')
        lblCon=gtk.Label('Consignment')
        lblBox=gtk.Label('Box Number')
        lblL=gtk.Label('Location')
        lblRef=gtk.Label('Reference')
        lblSub=gtk.Label('Subject')
        lblRet=gtk.Label('Retention >')
        lblAct=gtk.Label('Action')
        self.txtReg=gtk.combo_box_new_text()
        self.txtReg.set_size_request(160,22)
        for i in range(len(Glob.reg)):
            self.txtReg.append_text(str(Glob.reg[i][0]))
        self.txtSub=gtk.Entry()
        self.txtSub.set_size_request(400,22)
        self.txtV=gtk.Entry()
        self.txtCon=gtk.Entry()
        self.txtBox=gtk.Entry()
        self.txtRef=gtk.Entry()
        self.txtRef.set_size_request(400,22)
        self.txtL=gtk.Entry()
        self.txtL.set_size_request(400,22)
        self.txtCode=gtk.combo_box_new_text()
        self.txtCode.set_size_request(160,22)
        for i in range(len(Glob.ser)):
            self.txtCode.append_text(str(Glob.ser[i][0]))
        self.txtRet=gtk.Entry()
        self.txtAct=gtk.combo_box_new_text()
        for i in range(len(Glob.act)):
            self.txtAct.append_text(str(Glob.act[i][0]))
        self.txtAct.set_size_request(160,22)
        btnSearch=gtk.Button('Search')
        btnSearch.set_size_request(160,30)
        btnSearch.connect('button_press_event',self.search)
        
        fx=gtk.Fixed()
        fx.set_border_width(10)
        fx.put(lblReg,10,10)
        fx.put(lblCode,10,40)
        fx.put(lblL,10,70)
        fx.put(lblCon,10,100)
        fx.put(lblBox,10,130)
        fx.put(lblRef,10,160)
        fx.put(lblSub,10,190)
        fx.put(lblRet,10,220)
        fx.put(lblAct,10,250)
        fx.put(self.txtReg,100,10)
        fx.put(self.txtCode,100,40)
        fx.put(self.txtL,100,70)
        fx.put(self.txtCon,100,100)
        fx.put(self.txtBox,100,130)
        fx.put(self.txtRef,100,160)
        fx.put(self.txtSub,100,190)
        fx.put(self.txtRet,100,220)
        fx.put(self.txtAct,100,250)
        fx.put(btnSearch,100,290)
        fm=gtk.Frame()
        fm.add(fx)
        sp=gtk.HSeparator()
        self.dialog.vbox.pack_start(sp, False,False, 0)
        ntbk=gtk.Notebook()
        bg_color = gtk.gdk.Color (50000, 50000, 65535, 0)        
        ntbk.modify_bg(gtk.STATE_NORMAL, bg_color)
        
        #ntbk.append_page(MainCase.MCase().Reg(), gtk.Label(" Main Case "))
        
        #self.dialog.vbox.pack_start(ntbk, False,False, 0)
        self.dialog.set_border_width(3)
        self.dialog.vbox.pack_start(fm, False,False, 0)
        self.dialog.show_all()
        res = self.dialog.run()
        self.dialog.hide()
        
        return res
    
    def togg(self,widget,path,stor):
        stor[path][0] = not stor[path][0]
    
    def search(self,widget,event):
        lst='select*from record'
        par=''
        if self.txtReg.get_active()!=-1:
            par=par + " reg="+str(self.txtReg.get_active())+ " and"
        if self.txtCode.get_active()!=-1:
            par=par + " code like '%"+self.txtCode.get_text()+ "%' and"
        if self.txtRef.get_text()!='':
            par=par + " ref like '%"+self.txtRef.get_text()+ "%' and"
        if self.txtCon.get_text()!='':
            par=par + " consign like '%"+self.txtCon.get_text()+ "%' and"
        if self.txtL.get_text()!='':
            par=par + " loc like '%"+self.txtL.get_text()+ "%' and"
        if self.txtBox.get_text()!='':
            par=par + " box='"+self.txtBox.get_text()+ "' and"
        if self.txtSub.get_text()!='':
            par=par + " sub like '%"+self.txtSub.get_text()+ "%' and"
        if self.txtRet.get_text()!='':
            par=par + " ret >"+self.txtRet.get_text()+ " and"
        if self.txtAct.get_active() !=-1:
            par=par + " act='"+str(Glob.act[self.txtAct.get_active()][0])+ "' and"
        
                
        if len(par)>3:
            par=par[:len(par)-3]
            lst=lst+' where '+par
        
        b=(Conn.conDB().ref_list(0,lst))
        self.dialog.hide()
        records.Files().list(b)
        