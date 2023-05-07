class AFD:
    def __init__(self, states=set(), alphabet=set(), transitions={}, init='', finals=set()):
        """
        Automato Finito Deterministico

        Params:
        -------
        states:
            E, Conjunto de estados do Automato

        alphabet:
            Σ, Alfabeto reconhecido pelo Automato

        transitions:
            δ, Transições do Automato no formato = δ(e,a):_e

        init:
            i, Estado inicial

        finals:
            F, Conjunto de Estados Finais
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.init = init
        self.finals = finals

    def __repr__(self):
        return f' E={self.states} \n Σ={self.alphabet} \n δ={self.transitions} \n i={self.init} \n F={self.finals}'

    def get_reachable_state_by_symbol(self, e, a):
        state = self.transitions.get((e,a))
        if state:
            return state

    def remove_unreachable_states(self):
        """
        Removes every unreachable state from the DFA.
        """
        reachable_states = set()
        queue = [self.init]

        while len(queue) > 0:
            current_state = queue.pop(0)
            if current_state not in reachable_states:
                reachable_states.add(current_state)
                for symbol in self.alphabet:
                    next_state = self.transitions.get(
                        (current_state, symbol), None)
                    if next_state is not None:
                        queue.append(next_state)

        unreachable_states = self.states - reachable_states
        for state in unreachable_states:
            self.states.remove(state)
            self.finals.discard(state)
            for symbol in self.alphabet:
                self.transitions.pop((state, symbol), None)
                self.transitions.pop((state, symbol), None)

