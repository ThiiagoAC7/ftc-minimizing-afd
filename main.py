import xml.etree.ElementTree as ET

from State import State
from Transition import Transition
from AFD import AFD


def parse_xml(xml):
    """
    Extrai do XML as informações do AFD sendo analisado

    Params:
    -------
    xml: 
        AFD do JFLAP

    Return:
    -------
    AFD = (E,Σ,δ,i,F)

    """

    states = []
    transitions = []
    alphabet = []
    finals = []
    initial = State("", -1)

    tree = ET.parse(xml)
    root = tree.getroot()

    type = root[0]
    automaton = root[1]

    # print(type.tag, type.attrib, type.text)
    # print(automaton.tag, automaton.attrib, automaton.text)

    for child in automaton:

        if child.tag == 'state':
            name = child.get('name')
            id = child.get('id')
            if child.find('initial') != None:
                initial = State(name, int(id))
            if child.find('final') != None:
                finals.append(State(name, int(id)))
            states.append(State(name, int(id)))

        if child.tag == 'transition':
            symbol = child.find('read').text
            if symbol not in alphabet:
                alphabet.append(symbol)

            src_state = int(child.find('from').text)
            dst_state = int(child.find('to').text)

            states[src_state]._transitions.append(
                Transition(src_state, dst_state, symbol))
            # print(f'e = {states[src_state]}, transitions = {states[src_state]._transitions}')
            transitions.append(Transition(src_state, dst_state, symbol))

    return AFD(states, alphabet, transitions, initial, finals)


def minimizeAFDnn(P: AFD, debug=False):
    """
    Minimiza um AFD, em complexidade O(n^2)

    Params:
    -------
    P:
        AFD = (E,Σ,δ,i,F)

    Return:
    -------
    minP:
        um AFD mínimo equivalente a P 
    """

    def _get_set_c_transition(_S, _e):
        """
        pega o conjunto em Sn-1 que contém _e

        Params:
        -------
        _S : Sn-1
        _e : Estado sendo analisado na equivalência

        Return:
        -------
        conjunto que contém _e
        """
        for i in _S:
            if _e in [j.id for j in i]:
                return i

    if len(P.finals) == 0:  # Sem estados finais
        _transitions = []
        for a in P.alphabet:
            _transitions.append(Transition(P.init.id, P.init.id, a))
        return AFD(P.init, P.alphabet, _transitions, P.init, [])

    elif len(P.states) == len(P.finals):  # Só estados finais
        _transitions = []
        for a in P.alphabet:
            _transitions.append(Transition(P.init.id, P.init.id, a))
        return AFD(P.init, P.alphabet, _transitions, P.init, P.init)

    n = 0
    S = []  # equivalencias
    S.append([P.get_non_final_states()])
    S[n].append(P.finals)

    while (len(S) == 1) or (S[n] != S[n-1]):
        n = n+1
        S.append([])
        if debug: print(f'S[n-1] ->> {S[n-1]}')
        for X in S[n-1]:
            if debug: print(f'X ->> {X}')
            while X != []:
                e = X[0]
                if debug: print(f'\te -> {e}')
                transitions_set = {}
                for a in P.alphabet:
                    if debug: print(f'\tΣ -> {a}')
                    reachable_state = e.get_reachable_state_by_symbol(a, debug)
                    transitions_set[a] = _get_set_c_transition(
                        S[n-1], reachable_state)
                    if debug: print(f'\ttransition_set[{a}]={transitions_set[a]}')
                break
        break


def minimizeAFDnlogn(P: AFD):
    """
    Minimiza um AFD, em complexidade O(n log n)

    Params:
    -------
    P:
        AFD = (E,Σ,δ,i,F)

    Return:
    -------
    minP:
        um AFD mínimo equivalente a P 
    """
    return 0


debug = ''


def main():
    # P = parse_xml('./tests/test2.jff')
    # print(P)
    debug = input("Debug ? [y/n]:")
    debug = debug == 'y'
    p = parse_xml('./tests/test_livro.jff')
    minimizeAFDnn(p, debug)


if __name__ == "__main__":
    main()
