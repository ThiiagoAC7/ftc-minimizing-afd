class AFD:
    def __init__(self, states, alphabet, transitions, init, finals):
        """
        Automato Finito Deterministico

        Params:
        -------
        states:
            E, Conjunto de estados do Automato

        alphabet:
            Σ, Alfabeto reconhecido pelo Automato

        transitions:
            δ, Transições do Automato

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
