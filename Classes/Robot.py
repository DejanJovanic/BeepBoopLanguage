from .Property import Property


class Robot:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        self.inherits = kwargs['inherits']
        self.properties = kwargs['properties']

    def inherit_properties(self):
        for parent in self.inherits:
            for prop in parent.properties:
                if not any(x.name == prop.name for x in self.properties):
                    self.properties.append(Property(parent=self, name=prop.name, value=prop.value))
