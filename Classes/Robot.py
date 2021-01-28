from .Property import Property


class Robot:
    def __init__(self, parent, name, inherits, properties):
        self.name = name
        self.parent = parent
        self.inherits = inherits
        self.properties = properties
        for item in properties:
            self.__dict__[item.name] = item.value

    def inherit_properties(self):
        for parent in self.inherits:
            for prop in parent.properties:
                if not any(x.name == prop.name for x in self.properties):
                    self.properties.append(Property(self, prop.name, prop.value))
