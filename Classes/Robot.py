from .Property import Property


class Robot:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        self.inherits = kwargs['inherits']
        self.properties = kwargs['properties']

    def inherit_properties(self, robots):
        inherited_items = [item for item in robots if item.name in self.inherits]
        for parent in inherited_items:
            parent_prop = parent.get_properties(robots)
            for prop in parent_prop.items():
                # copy parents properties
                if not any(x.name == prop[0] for x in self.properties):
                    self.properties.append(Property(parent=self, name=prop[0], value=prop[1]))

    def get_properties(self, robots):
        # Problem stack overflow rekurzije
        ret_val = {}

        for item in self.properties:
            if item.name not in ret_val:
                ret_val[item.name] = item.value

        if len(self.inherits) > 0:
            inherited_items = [item for item in robots if item.name in self.inherits]
            for parent in inherited_items:
                parent_prop = parent.get_properties(robots)
                for item in parent_prop.items():
                    if item[0] not in ret_val:
                        ret_val[item[1]] = item[0]

        return ret_val
