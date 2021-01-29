class Property:
    def __init__(self,**kwargs):
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        self.name = kwargs['name']
        self.value = kwargs['value']
