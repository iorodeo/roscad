"""
Copyright 2010  IO Rodeo Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from utility import TAB_WIDTH, val_to_str

class POVRAY_Prog(object):
    """Wrapper for povray program."""

    def __init__(self, fn=None, fa=None, fs=None):
        self.objlist = []
        # Global facet settings
        self.fn = fn
        self.fa = fa
        self.fs = fs

    def add(self, obj):
        """Add a povray object to this program container."""
        if type(obj) == list:
            self.objlist.extend(obj)
        else:
            self.objlist.append(obj)

    def __str__(self):
        rtn_str = ''
        if not self.fn == None:
            rtn_str = '%s$fn = %d;\n'%(rtn_str, self.fn)
        if not self.fa == None:
            rtn_str = '%s$fa = %d;\n'%(rtn_str, self.fa)
        if not self.fs == None:
            rtn_str = '%s$fs = %d;\n'%(rtn_str, self.fs)

        for obj in self.objlist:
            rtn_str = '%s%s\n\n'%(rtn_str,obj)

        return rtn_str

    def write(self, filename):
        fid = open(filename, 'w')
        fid.write(get_header_str(filename))
        fid.write('{0}'.format(self))
        fid.close()

class POVRAY_Object(object):
    """POV-Ray object wrapper base class."""

    def __init__(self, center=True, mod='', comment='',
                 fa=None, fs=None, fn=None, translate=None):
        self.type = None    # ?
        self.center = center# Centered or positive quadrent
        self.cmp = False    # Is compound
        self.mod = mod      # Rendering modifier (*,%,#,!)
        self.comment = comment  # A comment to add to the output file
        # Per object facet settings
        self.fa = fa
        self.fs = fs
        self.fn = fn
        # Integrated transform
        self.translate = translate

    def facets(self):
        """Return any facet arguments that are set."""
        facets = ''
        if self.fn: # $fn is exclusive!
            return ", $fn={0}".format(self.fn)
        if self.fa:
            facets += ", $fa={0}".format(self.fa)
        if self.fs:
            facets += ", $fs={0}".format(self.fs)
        return facets

    def center_str(self):
        return str(self.center).lower()

    def is_cmp(self):
        return self.cmp

    def cmd_str(self,tab_level=0):
        return 'POVRAY_Object'

    def __str__(self,tab_level=0):
        tab_str = ' '*TAB_WIDTH*tab_level
        mod_str = self.mod
        comment = ''
        if self.comment:
            comment = tab_str + '// ' + self.comment + '\n'
        rtn_str = '{0}{1}{2}'.format(tab_str, mod_str,
                               self.cmd_str(tab_level=tab_level))
        if self.translate:
            translate = tab_str + "translate(" + val_to_str(self.translate)
            rtn_str = translate + ") {\n" + ' '*TAB_WIDTH + rtn_str + "\n}"
        return comment + rtn_str

    def write(self, filename, fn=None):
        outfile = open(filename,'w')
        if fn:
            outfile.write('$fn={0:0.5f};\n'.format(fn))
        outfile.write('{0}'.format(self))
        outfile.close()

class POVRAY_CMP_Object(POVRAY_Object):
    """Povray compound object wrapper base class."""

    def __init__(self, obj, center=True, mod='', comment=''):
        POVRAY_Object.__init__(self, center=center, mod=mod, comment=comment)
        self.cmp = True
        #self.obj = obj
        if type(obj) == list:
            self.obj = obj
        else:
            self.obj = [obj]

    def cmd_str(self, tab_level=0):
        return 'POVRAY_CMP_Object'

    def __str__(self, tab_level=0):
        tab_str = ' '*TAB_WIDTH*tab_level
        rtn_str = POVRAY_Object.__str__(self, tab_level=tab_level)
        rtn_str = '%s {\n'%(rtn_str,)
        for obj in self.obj:
            try:
                rtn_str = '%s%s\n'%(rtn_str,obj.__str__(tab_level=tab_level+1))
            except: # Assume obj is str, otherwise it is converted...
                rtn_str = "{0}{1}\n".format(rtn_str, (" "*(TAB_WIDTH*tab_level+1))+str(obj))
        rtn_str = '%s%s}'%(rtn_str,tab_str,)

        return rtn_str

def get_header_str(filename):
    import textwrap
    width = 70
    str0 = '\n//' + '='*(width-2) + '//\n'
    # see "http://docs.python.org/library/string.html#formatspec"
    str1 = '//{0:=^{1}}//'.format(" " + filename + " ", width-2)
    str1 += '\n//' + ' '*(width-2) + '//\n'
    str2 = "Autogenerated using py2povray. Hand editing this file is not \
advisable as all modifications will be lost when the program which generated \
this file is re-run."
    # str2 uses width-3 because of the extra space after the initial slashes
    str2 = "\n".join("// {0:<{1}}//".format(l, width-3) for l in
                     textwrap.wrap(str2, width=width-3))
    return str0 + str1 + str2 + str0 + '\n'

if __name__ == "__main__":
    print(get_header_str("filename"))
