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
    initial = State("", "")

    tree = ET.parse(xml)
    root = tree.getroot()

    type = root[0]
    automaton = root[1]

    # print(type.tag, type.attrib, type.text)
    # print(automaton.tag, automaton.attrib, automaton.text)

    for child in automaton:

        if child.tag == 'state':
            name = child.get('name')
            tag = ""
            if child.find('initial') != None:
                tag = "i"
                initial = State(name, tag)
            if child.find('final') != None:
                tag = "f"
                finals.append(State(name, tag))
            states.append(State(name, tag))

        if child.tag == 'transition':
            from_state = child.find('from').text
            to_state = child.find('to').text
            symbol = child.find('read').text
            if symbol not in alphabet:
                alphabet.append(symbol)
            transitions.append(Transition(from_state, to_state, symbol))

    return AFD(states, alphabet, transitions, initial, finals)


def minimizeAFDnn(P):
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
    return 0


def minimizeAFDnlogn(P):
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
    P = parseXML('./tests/test2.jff')
    print(P)


if __name__ == "__main__":
    main()
