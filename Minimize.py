import xml.etree.ElementTree as ET

from AFD import AFD


def min_nlogn(P: AFD):

    partitions = [P.finals, P.states - P.finals]

    new_partition = []
    while new_partition != partitions:
        new_partition = partitions
        partitions = new_partition
        print(f'new_partition = {new_partition}')
        print(f'partitions = {partitions}')
        new_current_partition = []
        for current_partition in new_partition:
            print(f'\t current_partition = {current_partition}')
            if len(current_partition) == 1:
                new_current_partition.append(current_partition)
                print(f'\t\t new_current_partition = {new_current_partition}')
            elif len(current_partition) > 1:
                splitted_partitions = set()
                for a in P.alphabet:
                    for current_state in current_partition:
                        t = P.transitions.get((current_state, a))
                        print(f'\t\tδ({current_state},{a}) = {t}')
                        if t and t not in current_partition:
                            splitted_partitions.add(current_state)
                            print( f'\t\t\t splitted_partitions = {splitted_partitions}')
                if len(splitted_partitions) > 0 and len(splitted_partitions) < len(current_partition):
                    _current_partiton_1 = set( current_partition) - splitted_partitions
                    _current_partiton_2 = splitted_partitions
                    print( f'\t\t\t -> splits = {_current_partiton_1} , {_current_partiton_2}')
                    new_current_partition.append(_current_partiton_1)
                    new_current_partition.append(_current_partiton_2)

                print( f'\t\t\t new_current_partition = {new_current_partition}')
            _fodase = input('>')

        partitions = new_current_partition

    print(partitions)

    return 0


def min_nn(P: AFD):
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
        retorna o conjunto em _S que contém _e
        """
        for i in _S:
            if _e in i:
                return i
        return set()

    if len(P.finals) == 0:  # Sem estados finais
        _transitions = {}
        for a in P.alphabet:
            _transitions[(P.init, P.init)] = a
        return AFD(P.init, P.alphabet, _transitions, P.init, set())

    elif len(P.states) == len(P.finals):  # Só estados finais
        _transitions = {}
        for a in P.alphabet:
            _transitions[P.init, P.init] = a
        return AFD(P.init, P.alphabet, _transitions, P.init, P.init)

    n = 0
    S = []  # equivalencias
    S.append([P.states-P.finals, P.finals])

    while (len(S) == 1) or (S[n] != S[n-1]):
        n = n+1
        S.append([])
        for X in S[n-1]:
            while len(X) != 0:
                e = list(X)[0]
                transitions_set = {}
                for a in P.alphabet:
                    reachable_state = P.get_reachable_state_by_symbol(e, a)
                    transitions_set[a] = _get_set_c_transition(
                        S[n-1], reachable_state)

                Y = []
                Y.append(e)
                for _e in list(X)[1:]:
                    count = 0
                    for a in P.alphabet:
                        if P.get_reachable_state_by_symbol(_e, a) in transitions_set[a]:
                            count += 1
                    if count == len(P.alphabet):
                        Y.append(_e)

                X = set(X) - set(Y)
                S[n].append(Y)

    _i = -1
    for i in S[n]:
        if P.init in i:
            _i = str(i)

    _f = set()
    for i in S[n]:
        if P.finals.issubset(i):
            _f.add(str(i))

    _T = {}
    for x in S[n]:
        for a in P.alphabet:
            _dst_state = _get_set_c_transition(
                S[n], P.get_reachable_state_by_symbol(x[0], a))
            if _dst_state != set():
                _T[str(x), a] = str(_dst_state)

    SN = []
    for i in S[n]:
        SN.append(str(i))

    return AFD(set(SN), P.alphabet, _T, _i, _f)


def min_new(P: AFD):

    inverted_state_table = {}
    
    # constroi tabela de estados invertida 
    for key, value in P.transitions.items(): 
        r_state = value
        a = key[1]
        l_state = key[0]
        aux = inverted_state_table.get((r_state, a))
        if aux is None:
            inverted_state_table[(r_state, a)] = []
        inverted_state_table[(r_state, a)].append(l_state)

    partitions = [P.finals, P.states - P.finals]
    w = [P.finals, P.states - P.finals]

    while w != []:
        print(f'W = {w}')
        print(f'P = {partitions}')
        current_partition = w.pop(0)
        print(f'current_partition = {current_partition}')
        for a in P.alphabet:
            x = set()  # states that reach the current partition
            for e in current_partition:
                t = inverted_state_table.get((e, a))
                if t:
                    x = x.union(t)
            print(f'\testados que chegam em {current_partition} com {a} -> {x}')
            for r in partitions:
                print(f'\t r -> {r}, x = {x}')
                if (len(r & x) > 0) and not (r <= x):
                    splitted_partition_1 = set(r) & x # r1
                    splitted_partition_2 = set(r) - x # r2
                    print(f'\t r1 -> {splitted_partition_1}')
                    print(f'\t r2 -> {splitted_partition_2}')
                    partitions.remove(r)
                    partitions.append(splitted_partition_1)
                    partitions.append(splitted_partition_2)
                    if r in w:
                        print(f'\t\tt {r} pertence à {w}, replace r com r1 e r2')
                        w.remove(r)
                        w.append(splitted_partition_1)
                        w.append(splitted_partition_2)
                    else:
                        if len(splitted_partition_1) <= len(splitted_partition_2):
                            print(f'\t\tadd r1 = {splitted_partition_1}')
                            w.append(splitted_partition_1)
                        else:
                            print(f'\t\tadd r2 = {splitted_partition_1}')
                            w.append(splitted_partition_2)
        _fodase = input('>')

    print(partitions)
    # construir AFD a partir de estados criados

