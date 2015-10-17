'''
Created on Jan 7, 2014

@author: ben
'''

import pygtk
pygtk.require("2.0")
import sys,os
import math
import cairo,goocanvas
import pango
import gtk

print_text = None

class Print:    
    
    def on_print(self, data=None, filename=None):
        canvas=goocanvas.Canvas()
        rt=canvas.get_root_item()
        '''pix = gtk.gdk.pixbuf_new_from_file("logo.jpg")
        logo=pix.scale_simple(50,70,gtk.gdk.INTERP_BILINEAR)
        item = goocanvas.Image (parent=rt,pixbuf = pix,x=0,y=0)'''
        self.text = goocanvas.Text(text='Retrival Tool',
                                   x=30,y=0,font="Sans 12")
        rt.add_child(self.text)
        self.text = goocanvas.Text(text='Registry',x=0,y=30,font="Sans 6")
        rt.add_child(self.text)
        self.text = goocanvas.Text(text='Location',x=70,y=30,font="Sans 6")
        rt.add_child(self.text)
        self.text = goocanvas.Text(text='Box',x=120,y=30,font="Sans 6")
        rt.add_child(self.text)
        self.text = goocanvas.Text(text='Reference',x=150,y=30,font="Sans 6")
        rt.add_child(self.text)
        self.text = goocanvas.Text(text='subject',x=240,y=30,font="Sans 6")
        rt.add_child(self.text)
        self.text = goocanvas.Text(text='Volume',x=420,y=30,font="Sans 6")
        rt.add_child(self.text)
        self.text = goocanvas.Text(text='Opened',x=460,y=30,font="Sans 6")
        rt.add_child(self.text)
        self.text = goocanvas.Text(text='Retn. ',x=520,y=30,font="Sans 6")
        rt.add_child(self.text)
        self.text = goocanvas.Text(text='Action',x=550,y=30,font="Sans 6")
        rt.add_child(self.text)
                
        self.pi = goocanvas.polyline_new_line(rt,0,44,600,44,
                                        line_width=1,end_arrow=False)
        #n=str(os.sep.join((os.path.expanduser('~'),'Desktop')))+str('/')+filename
        surface = cairo.PDFSurface (filename, 9 * 72, 10 * 72)
        dat=data
        l=32
        for i in range(len(dat)):
            l=l+15
            if l<650:
                self.text = goocanvas.Text(text=str((dat[i][0])[:13]),x=0,y=l,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text=str((dat[i][1])[:8]),x=70,y=l,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text=(str(dat[i][3])[:5]),x=120,y=l,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text=(str(dat[i][4])[:15]),x=150,y=l,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text=str((dat[i][5])[:37]),x=240,y=l,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text=str((dat[i][6])[:5]),x=420,y=l,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text=str((dat[i][7])[:10]),x=460,y=l,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text=str((dat[i][8])[:4]),x=520,y=l,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text=str((dat[i][9])[:12]),x=550,y=l,font="Sans 6")
                rt.add_child(self.text)
            elif l>=650 or i==(len(dat)-1):
                cr = cairo.Context (surface)
                # Place it in the middle of our 9x10 page. 
                cr.translate (20, 0)
                canvas.render (cr, None, 1.0)
                cr.show_page ()
                l=30
                canvas.destroy()
                canvas=goocanvas.Canvas()
                rt=canvas.get_root_item()
                self.text = goocanvas.Text(text='Generate 4 Generations',
                                   x=5,y=5,font="Sans 18")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text='Woman',x=0,y=30,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text='Product',x=70,y=30,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text='Number',x=150,y=30,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text='Done',x=180,y=30,font="Sans 6")
                rt.add_child(self.text)
                self.text = goocanvas.Text(text='Date',x=210,y=30,font="Sans 6")
                rt.add_child(self.text)
                        
                self.pi = goocanvas.polyline_new_line(rt,0,40,275,40,
                                                line_width=1,end_arrow=False)
                        
        cr = cairo.Context (surface)
        cr.translate (10, 0)
        canvas.render (cr, None, 1.0)
        cr.show_page ()
        