from distutils.core import setup
import py2exe
import os

# Find GTK+ installation path
__import__('gtk')
m = os.sys.modules['gtk']
gtk_base_path = m.__path__[0]
'''
 after the building is complete copy etc,lib and share folders from Lib\site-packages\gtk-2.0\runtime
 so that the application looks native with  a theme
'''
setup(
    name = 'Registry Tool',
    description = 'Retrival Tool',
    version = '1.0',

    windows = [
                  {
                      'script': 'main.py',
                      'icon_resources': [(1, "BON.ico")],
                  }
              ],
 
    options = {
                  'py2exe': {
                      'packages':'encodings',
                      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
                      'includes': 'decimal,datetime,cairo, pango, pangocairo, atk, gobject, gio, gtk.keysyms, rsvg',
                  }
              },

    data_files=[   'g4g.jpg','BON.jpg','BON.ico',
                   # If using GTK+'s built in SVG support, uncomment these
                   os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'gdk-pixbuf-query-loaders.exe'),
                   os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'libxml2-2.dll'),
               ]
)