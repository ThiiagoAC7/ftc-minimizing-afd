import xml.etree.ElementTree as ET
import time

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


def write_xml(P: AFD, filename):
    with open(f'./results/{filename}', 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write('<structure>&#13;\n')
        f.write('\t<type>fa</type>&#13;\n')
        f.write('\t<automaton>&#13;\n')

        f.write('\t\t<!--The list of states.-->&#13;\n')

        _index_state = {}
        for index, state in enumerate(P.states):
            _index_state[state] = index
            f.write(f'\t\t<state id="{index}" name="{state}">&#13;\n')
            f.write('\t\t\t<x>0</x>&#13;\n')
            f.write('\t\t\t<y>0</y>&#13;\n')
            # print(f'{state}=={P.init} {state == P.init}')
            # print(f'{type(state)}=={type(P.init)}')
            if state == P.init:
                f.write('\t\t\t<initial/>&#13;\n')

            if state in P.finals:
                f.write('\t\t\t<final/>&#13;\n')

            f.write('\t\t</state>&#13;\n')

        f.write('\t\t<!--The list of transitions.-->&#13;\n')

        for (src_state, symbol), dst_state in P.transitions.items():
            f.write('\t\t<transition>&#13;\n')
            f.write(f'\t\t\t<from>{_index_state[src_state]}</from>&#13;\n')
            f.write(f'\t\t\t<to>{_index_state[dst_state]}</to>&#13;\n')
            f.write(f'\t\t\t<read>{symbol}</read>&#13;\n')
            f.write('\t\t</transition>&#13;\n')

        f.write('\t</automaton>&#13;\n')
        f.write('</structure>\n')

def create_circular_dfa(num_states):
    states = {f'q{i}' for i in range(num_states)}
    alphabet = {'0', '1'}
    transitions = {}
    init = 'q0'
    finals = {'q0'}

    for i in range(num_states):
        transitions[(f'q{i}', '0')] = f'q{(i+1) % num_states}'
        transitions[(f'q{i}', '1')] = f'q{i}'

    return AFD(states, alphabet, transitions, init, finals)

def main():
    p = parse_xml('./tests/dfa_circular_100.jff')
    # write_xml(create_circular_dfa(11), 'dfa_circular_11.jff')
    # p.remove_unreachable_states()

    # _start = time.time()
    min_p = min_nlogn(p)
    # _end = time.time()
    
    # print(min_p)
    write_xml(min_p, '_test_circular_100.jff')
    # time_nn = end-start

    # print(f'time n^2 = {end-start}')
    # print(f'time nlogn = {end-start}')


if __name__ == "__main__":
    main()
