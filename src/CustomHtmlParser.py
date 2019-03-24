"""
HTML.py
written by ariyn(himnowxz@gmail.com)

this script parse html and create elements for each tags.
"""
from html.parser import HTMLParser

class Element:
    def __init__(self, tag, attr=None):
        if not attr:
            attr = []
        attr = [(str(i[0]), str(i[1])) for i in attr]

        self.strAttr = []
        for v in attr:
            x = " = ".join(v) if isinstance(v[1], str) else " = ".join(" ".join(v[1]))
            self.strAttr.append(x)

        self.tag = tag
        self.parsedAttrs = {i[0]:i[1] for i in attr}
        self.id = self.parsedAttrs["id"] if "id" in self.parsedAttrs else None
        self.classes = self.parsedAttrs["class"].split(" ") if "class" in self.parsedAttrs else []
        self.data, self.children = "", []
        self.parent = None
        self.attrs = attr

    def addChildren(self, child):
        """
        add children to self
        this parent-children concept is same to html's parent-children concept
        """
        self.children.append(child)
        child.parent = self

    def setData(self, data):
        """
        set data of element
        data means text inside of container

        <e>lorem ipsum</e>       data:lorem ipsum
        <e><f>lorem</f>ipsum</e> data:ipsum
        """
        self.data += data.strip()
        self.parsedAttrs["body"] = self.data

    def getAttr(self, key, retVal=None):
        """
        REFACTORY!

        get attributes
        refactor this into __getattr__
        """
        if key in self.parsedAttrs:
            retVal = self.parsedAttrs[key]
        return retVal

    def __str__(self):
        newData = self.data.replace("\n", "\\n")
        return "<%s%s%s>%s</%s>"%(self.tag, "" if not self.strAttr else " ", " ".join(self.strAttr), newData, self.tag)
    
    def __repr__(self):
        return self.__str__()
        
    def printTree(self, depth=0):
        """
        print tree structure with text
        """
        newData = self.data.replace("\n", "\\n")
        print("%s<%s%s%s>%s"%("\t"*depth, self.tag, "" if not self.strAttr else " ", " ".join(self.strAttr), newData))

        for i in self.children:
            i.printTree(depth+1)

        print("%s</%s>"%("\t"*depth, self.tag))

class MyHTMLParser(HTMLParser):
    """
    custom html parser
    """
    SingleLineTags = ["img", "br", "input", "wbr"]
    InlineTags = ["a","abbr","acronym","b","bdo","big","br","button","cite","code","dfn","em","i","img","input","kbd","label","map","object","output","q","samp","script","select","small","span","strong","sub","sup","textarea","time","tt","var"]
    LinebreakTags = ["br", "p", "div", "button", "script", "input", "h1", "h2", "h3", "h4", "h5", "h6"]
    
    def __init__(self, DEBUG=False):
        super(MyHTMLParser, self).__init__()
        self.root = Element("Root")
        self.html = ""

        self.parsingTags = [self.root]
        self.tags = [self.root]
        
        if not DEBUG:
            self.print = lambda *args, **kwargs: None
        else:
            self.print = DEBUG

    def __handle_starttag__(self, tag, attrs, oneline=False):
        element = Element(tag, attrs)
        self.parsingTags.append(element)
        self.print("start", tag, attrs, self.parsingTags)

    def __handle_endtag__(self, tag, oneline=False):
        self.parsingTags[-2].addChildren(self.parsingTags[-1])
        self.parsingTags = self.parsingTags[:-1]
        self.print("end", tag, self.parsingTags)

    def handle_startendtag(self, tag, attrs):
        self.__handle_starttag__(tag, attrs, oneline=True)
        self.__handle_endtag__(tag, oneline=True)

    def handle_starttag(self, tag, attrs):
        if tag in MyHTMLParser.SingleLineTags:
            self.handle_startendtag(tag, attrs)
        else:
            self.__handle_starttag__(tag, attrs)

    def handle_endtag(self, tag):
        self.__handle_endtag__(tag)

    def handle_data(self, data):
        self.parsingTags[-1].setData(data)
        self.print(len(self.parsingTags), self.parsingTags)
    
    def compact(self, isRoot=True, parent=None):
        if not parent and isRoot:
            parent = self.root

        for element in parent.children:
            compact(isRoot=False, parent=element)
            
    def removeParsingDiv(self):
        import copy
        
        parsingDiv = self.root.children.pop(0)
        for element in parsingDiv.children:
            self.root.addChildren(element)
            
        del parsingDiv

    def parse(self, html=None):
        """
        wrapper of HTMLParser.feed
        """
        if html:
            self.html = html
        self.feed(self.html)
        self.removeParsingDiv()
        self.compact()
        return self.root