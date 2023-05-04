class State:
    def __init__(self, name, tag):
        """
        Estado do automato

        Params:
        -------
        name:
            nome do automato

        tag:
            tag, podendo ser I = inicial, F = final ou "" = estado qualquer
        """
        self.name = name
        self.tag = tag

    def __repr__(self):
        return f'State(name={self.name}, tag={self.tag})'
