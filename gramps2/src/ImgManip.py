#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2000-2003  Donald N. Allingham
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import os
import const
import signal
import md5
import gtk
import gobject

class ImgManip:
    def __init__(self,source):
        self.src = source

    def size(self):
        img = gtk.gdk.pixbuf_new_from_file(self.src)
        return (img.get_width(),img.get_height())
    
    def fmt_thumbnail(self,dest,width,height,cnv):
        w = int(width)
        h = int(height)
        cmd = "%s -geometry %dx%d '%s' '%s:%s'" % (const.convert,w,h,self.src,cnv,dest)
        os.system(cmd)
        
    def fmt_convert(self,dest,cnv):
        cmd = "%s '%s' '%s:%s'" % (const.convert,self.src,cnv,dest)
        os.system(cmd)
        
    def fmt_data(self,cnv):
        import popen2
        
        cmd = "%s '%s' '%s:-'" % (const.convert,self.src,cnv)
        r,w = popen2.popen2(cmd)
        buf = r.read()
        r.close()
        w.close()
        return buf

    def fmt_scale_data(self,x,y,cnv):
        import popen2
        
        cmd = "%s -geometry %dx%d '%s' '%s:-'" % (const.convert,x,y,self.src,cnv)
        signal.signal (signal.SIGCHLD, signal.SIG_DFL)
        r,w = popen2.popen2(cmd)
        buf = r.read()
        r.close()
        w.close()
        return buf

    def jpg_thumbnail(self,dest,width,height):
        self.fmt_thumbnail(dest,width,height,"jpeg")

    def png_thumbnail(self,dest,width,height):
        self.fmt_thumbnail(dest,width,height,"png")

    def jpg_convert(self,dest):
        self.fmt_convert(dest,"jpeg")

    def png_convert(self,dest):
        self.fmt_convert(dest,"png")

    def eps_convert(self,dest):
        self.fmt_convert(dest,"eps")

    def jpg_data(self):
        return self.fmt_data("jpeg")

    def png_data(self):
        return self.fmt_data("png")

    def jpg_scale_data(self,x,y):
        return self.fmt_scale_data(x,y,"jpeg")

    def png_scale_data(self,x,y):
        return self.fmt_scale_data(x,y,"png")


def _build_thumb_path(path):
    base = os.path.expanduser('~/.gramps/thumb')
    m = md5.md5(path)
    return os.path.join(base,m.hexdigest()+'.jpg')

def set_thumbnail_image(path):
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(path)
        w = pixbuf.get_width()
        h = pixbuf.get_height()
        scale = const.thumbScale / (float(max(w,h)))
        
        pw = int(w*scale)
        ph = int(h*scale)
        
        pixbuf = pixbuf.scale_simple(pw,ph,gtk.gdk.INTERP_BILINEAR)
        pixbuf.save(_build_thumb_path(path),"jpeg")
    except:
        print "Could not create thumbnail for",path

def get_thumbnail_image(path):
    filename = _build_thumb_path(path)
    if not os.path.isfile(filename):
        set_thumbnail_image(path)
    try:
        return gtk.gdk.pixbuf_new_from_file(filename)
    except gobject.GError:
        return None

def get_thumbnail_path(path):
    filename = _build_thumb_path(path)
    if not os.path.isfile(filename):
        set_thumbnail_image(path)
    return filename
