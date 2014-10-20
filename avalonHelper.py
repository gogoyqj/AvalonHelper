import sublime
import sublime_plugin
import re
import sys
import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PACKAGES_PATH = sublime.packages_path() or os.path.dirname(BASE_PATH)

_msAttrList = []
_widgetList = []
_dataAttrList = []
msAttrList = []
widgetList = []
dataAttrList = []
specialList = []

# widget replacer
def widget_place(widgetName, is_completion = True, indents = ""):
    str = indents
    if widgetName in specialList:
        if is_completion:
            str += "ms-" + widgetName + "=\"\$,\$${1:" + widgetName + "}Opts\""
        else:
            str += "ms-" + widgetName + "=\"$,$" + widgetName + "Opts\""
    else:
        if not is_completion:
            str += "ms-widget=\"" + widgetName + "," + widgetName + "Name,$" + widgetName + "Opts" + "\""
        else:
            str += "ms-widget=\"" + widgetName + ",${1:" + widgetName + "}Name,\$${1:" + widgetName + "}Opts" + "\""
    return str

# load syntax
def on_load():
    path = BASE_PATH
    languagefile = open(path + "/" + 'helper.txt')
    try:
         all_the_text = languagefile.read()
    finally:
         languagefile.close()

    parts = all_the_text.split("\n")

    global _widgetList
    global _msAttrList
    global _dataAttrList
    global widgetList
    global msAttrList
    global dataAttrList

    msAttrList = parts[0].split(",")
    widgetList = parts[1].split(",")
    dataAttrList = parts[2].split(",")
    loop = 0
    for v in widgetList:
        if v.count("="):
            v = v.split("=")[0]
            widgetList[loop] = v
            specialList.append(v)
        loop = loop + 1
        _widgetList.append(("widget " + v + "\t组件", widget_place(v, True)))
    for v in msAttrList:
        _msAttrList.append((v + "\tbind", "" + v + "=\"${1:}\""))
    for v in dataAttrList:
        _dataAttrList.append((v + "\tbind", "" + v + "=\"${1:}\""))
    

# define parttens
msLike = re.compile(r"^ms")
msWidget = re.compile(r"^ms\-w[^\s\"\']+")
dataLike = re.compile(r"^d(ata\-)?")
blankLike=  re.compile(r"[\s\"\']+")
indexLike= re.compile(r"^[^<\s\n]+\s")
# add ms-widget partten
widgetLike = re.compile(r"^w[idget]")

class AvalonHelperCompletionsPackageEventListener(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        select = view.sel()[0]
        self.view = view
        indent = self.get_indent(len(prefix))
        if select.empty():
            if widgetLike.match(prefix):
                if not indent:
                    return _widgetList
                _list = []
                for i,v in _widgetList:
                    _list.append((i, indent + v))
                return _list;
            if prefix in widgetList:
                replacer = widget_place(prefix, True, indent)
                return [(prefix + "\tWidget", replacer)]
            if prefix == "m" or msLike.match(prefix):
                if not indent:
                    return _msAttrList
                _list = []
                for i,v in _msAttrList:
                    _list.append((i, indent + v ))
                return _list
            if dataLike.match(prefix):
                _list = []
                for i,v in _dataAttrList:
                    _list.append((i, indent + v )) 
                for v in widgetList:
                    _list.append(("data-" + v + "\toptions", indent + "data-" + v + "-${1:OptName}" + "=\"\""))
                return _list
        return None

    def get_indent(self, length=0):
        nowLine = self.view.line(self.view.sel()[0])
        prevline = self.view.substr(nowLine).replace("\t", "    ").strip()
        ## 加个判断，如果本身已经在行首就不要做什么了
        left = self.view.substr(sublime.Region(nowLine.a, self.view.sel()[0].a-length)).strip()
        if not left:
            return ''
        tabs = indexLike.findall(prevline)
        if tabs:
            c = 0
        else:
            c = len(prevline.split(" ")[0]) + 1
        indents = ""
        while len(indents) < c:
            indents += " "
        return "\n" + indents

# command
class HelperCommand(sublime_plugin.TextCommand):
    def run(self, edit, sub_words = False):
        pass

if int(sublime.version()) < 3000:
    on_load()
else:
  def plugin_loaded():
    on_load()
