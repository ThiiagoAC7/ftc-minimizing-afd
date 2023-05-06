from Transition import Transition


class State:
    def __init__(self, name, id, _transitions=[]):
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
        self.id = id
        self._transitions = []

    def __repr__(self):
        return f'State(name={self.name},id={self.id})'

    def __hash__(self):
        return hash((self.id, self.name))

    def __eq__(self, other):
        try:
            return (self.id, self.name) == (other.id, other.name)
        except AttributeError:
            return NotImplemented

    def get_reachable_state_by_symbol(self, a, debug=False):
        '''
        Get a transição no estado para o simbolo em questão

        Params:
        -------
        a:
            o simbolo no alfabeto Σ

        Return:
        -------
        O estado de destino da transição do estado atual com a 
        '''
        for t in self._transitions:
            if t.symbol == a:
                # if debug: print(f'\tδ({self.id},{a}) = {t}')
                return t.dst_state
