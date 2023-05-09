import xml.etree.ElementTree as ET

from AFD import AFD


def min_nlogn(P: AFD):

    partitions = [P.finals, P.states - P.finals]

    partition_transitions = {} # estado : partition 

    # for e in P.states:
    #     for p in partitions:
    #         if e in p: partition_transitions[e] = p

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
                        print( f'\t\tδ({current_state},{a}) = {t}')
                        if t and t not in current_partition:
                            splitted_partitions.add(current_state)
                            print( f'\t\t\t splitted_partitions = {splitted_partitions}')

                if len(splitted_partitions) > 0 and len(splitted_partitions) < len(current_partition):
                    _current_partiton_1 = set(current_partition) - splitted_partitions
                    _current_partiton_2 = splitted_partitions
                    print( f'\t\t\t -> splits = {_current_partiton_1} , {_current_partiton_2}')
                    new_current_partition.append(_current_partiton_1)
                    new_current_partition.append(_current_partiton_2)

                print(f'\t\t\t new_current_partition = {new_current_partition}')
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


def min_new(states, alphabet, transitions, initial, finals):
    accepting = finals
    non_accepting = states - finals
    partitions = [accepting, non_accepting]

    partition_lists = []
    partition_sizes = []
    partition_transitions = []

    for p in partitions:
        partition_lists.append(list(p))
        partition_sizes.append(len(p))
        partition_transitions.append({})

    print(f'partitions -> {partitions}')
    print(f'partition_lists -> {partition_lists}')
    # print(f'partition_sizes -> {partition_sizes}')
    print(f'partition_transitions -> {partition_transitions}')

    for symbol in alphabet:
        for i, current_partition in enumerate(partition_lists):
            new_partitions = set()
            print(f'=================================={i}')
            print(f'current_partition -> {current_partition}')

            for current_state in current_partition:
                t = transitions.get((current_state, symbol))
                print( f'\tstate -> {current_state} with symbol -> {symbol} goes to -> {t}')
                if t and t not in current_partition:
                    new_partitions.add(current_state)

                print(f'new_partitions -> {new_partitions}')

            if len(new_partitions) > 0 and len(new_partitions) < len(current_partition):
                new_partitions_1 = set(current_partition) - new_partitions
                new_partitions_2 = new_partitions
                print(
                    f'group_1 = {new_partitions_1}, group_2 = {new_partitions_2}, current_partition = {current_partition}')
                partition_lists.pop(i)
                partition_lists.append(list(new_partitions_1))
                partition_lists.append(list(new_partitions_2))
                partition_sizes.append(len(list(new_partitions_2)))

    new_states = set()
    for i in partition_lists:
        new_states.add(str(i))

    print(new_states)
