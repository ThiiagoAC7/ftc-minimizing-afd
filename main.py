import xml.etree.ElementTree as ET

from AFD import AFD

from Minimize import min_nn, min_nlogn, min_new


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

    states = set()
    transitions = {}
    alphabet = set()
    finals = set()
    initial = '' 

    tree = ET.parse(xml)
    root = tree.getroot()

    type = root[0]
    automaton = root[1]

    for child in automaton:

        if child.tag == 'state':
            name = child.get('name')
            id = child.get('id')
            if child.find('initial') != None:
                initial = id
            if child.find('final') != None:
                # finals.append(State(name, int(id)))
                finals.add(id)
            states.add(id)

        if child.tag == 'transition':
            symbol = child.find('read').text

            if symbol not in alphabet:
                alphabet.add(symbol)

            src_state = child.find('from').text
            dst_state = child.find('to').text

            transitions[(src_state, symbol)] = dst_state

    return AFD(states, alphabet, transitions, initial, finals)


def main():
    p = parse_xml( './tests/test_livro.jff')
    # p = parse_xml( './tests/unreachable_states.jff')

    p.remove_unreachable_states()
    # min_p = min_nn(p)
    min_new(p.states, p.alphabet, p.transitions, p.init, p.finals)
    # print(min_p)
    # min_p = min_nlogn(states, alphabet, transitions, initial, finals)


if __name__ == "__main__":
    main()
