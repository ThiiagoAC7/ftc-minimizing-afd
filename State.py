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

    def get_transition_by_symbol(self, symbol):
        '''
        Get a transição no estado para o simbolo em questão

        Params:
        -------
        symbol:
            o simbolo no alfabeto Σ 

        Return:
        -------
        A transição no estado para o symbol
        '''
        print(f'TRANSITIONS = {self._transition}')
        for t in self._transitions:
            print(f'STATE = {self.name}, t = {t}')
            if t.symbol == symbol:
                return t

    def get_reachable_state_by_symbol(self, symbol):
        """
        Get o estado de destino da transição com o symbol

        Param:
        ------
        symbol:
            Simbolo no alfabeto Σ 

        Return:
        -------
        O estado atingido pela transição com o símbolo
        """
        return self.get_transition_by_symbol(symbol).dst_state
