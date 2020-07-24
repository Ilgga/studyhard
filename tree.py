razd = "|*|"
class Tree:
    _save_list = []
    _otstup = 0

    def __init__(self, name,text='_', parent=None):
        self.name = name.replace('\'', '')
        self.text = text
        self._child = {}
        self._parent = parent

    def get_child(self):
        return self._child
    def get_parent(self):
        return self._parent

    def put_parent(self,tree):
        self._parent = tree

    def put_child(self,tree):
        self._child[tree.name]=tree

    def add(self,name,text=''):
        if not(name in self._child):
            a = Tree(name,text,self)
            self._child[name]=a
            return a
        return self._child[name]

    def go_to(self,name):
        if name in self._child:
            return self._child[name]
        return self

    def go_back(self):
        if self._parent:
            return self._parent
        return self

    def print(self,otst=4):
        print(' '*Tree._otstup + '->' + self.name+' : ('+self.text+')')
        Tree._otstup += otst
        for ch in self._child:
            self._child[ch].print()
        Tree._otstup -= otst

    def _make_save(self):
        #row   name   text
        s =str(Tree._otstup)+razd+self.name+razd+self.text+'|*|'
        Tree._save_list.append(s)
        Tree._otstup+=1
        for ch in self._child:
            self._child[ch]._make_save()
        Tree._otstup-=1
    def save_tree(self,filename):
        Tree._save_list = []
        self._make_save()
        f = open(filename,'w+',encoding='UTF-8')
        for i in Tree._save_list:
            f.write(i)
        f.close()
        Tree._save_list = []


    def __del__(self):
        del self.name
        del self.text
        del self._child
        del self._parent

    def _dele(self):
        li = list(self._child.values())
        self.__del__()
        for tr in li:
            tr._dele()

    def delete(self,name):
        if name in self._child:
            b = self.go_to(name)
            self._child.pop(name)
            #b._dele()
            #del b



class LoadTree:
    def __init__(self,filename,key='file'):
        if key == 'file':
            with open(filename, 'a+', encoding='UTF-8') as f:
                tree = f.read().split(razd)
        else:
            tree = filename.split(razd)
        if len(tree)>2:
            k=3
            name = tree[1]
            text =tree[3]
            MyTr = Tree(name=name, text=text)
            now = MyTr
            rr = 0
            while len(tree)>k+1:
                row = int(tree[k+0])
                name = tree[k+1]
                text = tree[k+2]
                '''if row == rr + 1:
                    now = now.add(name, text)
                    rr = row''
                if row == rr:
                    now = now.go_back()
                    now = now.add(name, text)
                else:'''
                for i in range(rr - row + 1):
                    now = now.go_back()
                    rr-=1
                now = now.add(name, text)
                rr+=1
                k+=3
            self.tree = MyTr







