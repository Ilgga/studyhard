from tree import LoadTree
from tree import Tree


class users:
    def __init__(self):
        self.users = {}

    def add_user(self,mid):
        tree = Tree('root')
        self.users[mid] = {}
        self.users[mid]['text'] = ''
        self.users[mid]['tree'] = tree
        self.users[mid]['root'] = tree
        self.users[mid]['adding'] = False
        self.users[mid]['dell_dir'] = False
        self.users[mid]['add_text'] = False
        self.users[mid]['saved'] = True
        self.users[mid]['msg'] = [0, 0, 0, 0, 0]

    def us(self,mid):
        return self.users[mid]

    def tree(self,mid):
        return self.users[mid]['tree']
    def root(self, mid):
        return self.users[mid]['root']
    def upd_tree(self, mid, tr):
        self.users[mid]['tree'] = tr

    def adding(self,mid):
        return self.users[mid]['adding']
    def dell_dir(self,mid):
        return self.users[mid]['dell_dir']
    def add_text(self,mid):
        return self.users[mid]['add_text']
    def saved(self,mid):
        return self.users[mid]['saved']
    def msg(self,mid):
        return self.users[mid]['msg']
    def text(self,mid):
        return self.users[mid]['text']
    def apd(self,mid,var,boo):
        self.users[mid][var]=boo





