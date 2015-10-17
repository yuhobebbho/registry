'''
Created on Mar 23, 2014

@author: bon
'''
import gtk
class log:
    def login(self,data):
        self.dialog = gtk.Dialog('', None, 0, ( data, gtk.RESPONSE_OK,gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.dialog.set_default_size(200, 100)
        #self.dialog.set_icon_from_file('g4g.jpg')
        self.dialog.set_position(gtk.WIN_POS_CENTER)
        #self.dialog.set_opacity(30)
        '''bg_color = gtk.gdk.Color (60000, 60000, 65535, 0)               
        self.dialog.modify_bg(gtk.STATE_NORMAL, bg_color)'''
        self.dialog.set_decorated(False)
        self.dialog.set_modal(True)
        tt=gtk.Table(3,2,True)
        tt.set_border_width(10)
        tt.set_row_spacings(10)
        lblnam=gtk.Label('Account Name')
        lblpwd=gtk.Label('Password')
        txtnam=gtk.Entry()
        txtpwd=gtk.Entry()
        txtpwd.set_visibility(False)
        txtpwd.set_invisible_char('*')
        cbopass=gtk.combo_box_new_text()
        cbopass.append_text('Standard User')
        cbopass.append_text('Administrator')
        cbopass.set_active(0)
        tt.attach(lblnam,0,1,0,1)
        tt.attach(txtnam,1,2,0,1)
        tt.attach(lblpwd,0,1,1,2)
        tt.attach(txtpwd,1,2,1,2)
        tt.attach(cbopass,1,2,2,3)
        self.dialog.vbox.pack_start(tt, True, True, 0)
        sp=gtk.HSeparator()
        self.dialog.vbox.pack_start(sp, True, True, 0)
        
        self.dialog.show_all()
        if str(data).upper()!=str('Create').upper():
            cbopass.set_visible(False)
        res = self.dialog.run()
        self.dialog.hide()
        acc=[]
        acc.append(txtnam.get_text())
        acc.append(txtpwd.get_text())
        acc.append(cbopass.get_active())
        return res,acc