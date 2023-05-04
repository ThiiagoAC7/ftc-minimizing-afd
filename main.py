import xml.etree.ElementTree as ET

from State import State
from Transition import Transition
from AFD import AFD


def parseXML(xml):
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
                initial = State(name, id)
            if child.find('final') != None:
                finals.append(State(name, id))
            states.append(State(name, id))

        if child.tag == 'transition':
            from_state = child.find('from').text
            to_state = child.find('to').text
            symbol = child.find('read').text

            if symbol not in alphabet:
                alphabet.append(symbol)
            t = Transition(from_state, to_state, symbol)
            transitions.append(t)
            states[int(from_state)].transitions.append(t)

    return AFD(states, alphabet, transitions, initial, finals)


def minimizeAFDnn(P: AFD):
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


def main():
    # P = parseXML('./tests/test2.jff')
    # print(P)
    p = parseXML('./tests/test_sofinal.jff')
    print(minimizeAFDnn(p))


if __name__ == "__main__":
    main()
