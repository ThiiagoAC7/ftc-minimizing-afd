import xml.etree.ElementTree as ET

from AFD import AFD


def min_nlogn(P: AFD):
    t = 2
    Q = []
    Q.append(P.finals)
    Q.append(P.states - P.finals)

    inverted_triangle = {}

    # constroi tabela de estados invertida
    for key, value in P.transitions.items():
        r_state = value
        a = key[1]
        l_state = key[0]
        aux = inverted_triangle.get((r_state, a))
        if aux is None:
            inverted_triangle[(r_state, a)] = []
        inverted_triangle[(r_state, a)].append(l_state)

    triangle = {}
    for estado in P.states:
        for a in P.alphabet:
            triangle[(estado, a)] = set()

    # construindo estruturas

    _triangle = {}
    L = {}  # contains each triple (i,a,j)
    for a in P.alphabet:
        # if L.get(a) is None: L[a] = {}
        for i, partition in enumerate(Q):  # i
            for j, q in enumerate(Q):     # j
                for estado in partition:
                    _t = P.transitions.get((estado, a))
                    if _t and _t in q:
                        iaj = str(i)+a+str(j)
                        l = L.get(iaj)
                        if l is None:
                            L[iaj] = set()
                            if _triangle.get((i,a)) is None:
                                _triangle[(i,a)] = []
                            _triangle[(i,a)].append(iaj)
                        L[iaj].add(estado)
                        triangle[(estado, a)] = iaj 

    print(f'inverted_triangle = {inverted_triangle}')
    print(f'triangle = {triangle}')
    print(f'triangle linha = {_triangle}')
    print(f'L = {L}')
    
    K = dict(filter(lambda elem: len(elem[1]) >= 2, _triangle.items()))
    print(f'K = {K}')    
    
    _K = list(K.keys())

    while len(_K) > 0:
        print(f'K = {K}, _K = {_K}')    
        print(f'L = {L}')
        for i,a in _K:
            _l1 = L[K[(i,a)][0]]
            _l2 = L[K[(i,a)][1]]
            print(f'\t _l1 = {_l1}')
            print(f'\t _l2 = {_l2}')
            old_iaj = ""
            if len(_l1) <= len(_l2):
                old_iaj = K[(i,a)][0]
            else:
                old_iaj = K[(i,a)][1]
            new_i = str(t)
            new_j = str(old_iaj[2]) # ultima char de iaj
            new_iaj = new_i+a+new_j 
            print(f'\t L old -> {L}')
            L[new_iaj] = L.pop(old_iaj)
            print(f'\t L new-> {L}')
            print(f'\ttrianglinha old-> {_triangle}')
            _triangle[(i,a)].remove(old_iaj)
            _triangle[(t,a)] = [new_iaj]
            print(f'\ttrianglinha new-> {_triangle}')
            if len(_triangle[(i,a)]) < 2:
                _K.remove((i,a))
                K.pop((i,a))
            for q in L[new_iaj]:
                print(f'\t\t q new_iaj -> {q}')
                for b in (P.alphabet - set(a)):
                    print(f'\t\t triangle({q},{b}) = {triangle[(q,b)]}')
                    print(f'\t\t\t result = {L[triangle[(q,b)]]}')
                    unique_record = L[triangle[(q,b)]]
                    if unique_record:
                        L[triangle[(q,b)]].remove(q)

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
        if set(i) <= P.finals:
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
            print(
                f'\testados que chegam em {current_partition} com {a} -> {x}')
            for r in partitions:
                print(f'\t r -> {r}, x = {x}')
                if (len(r & x) > 0) and not (r <= x):
                    splitted_partition_1 = set(r) & x  # r1
                    splitted_partition_2 = set(r) - x  # r2
                    print(f'\t r1 -> {splitted_partition_1}')
                    print(f'\t r2 -> {splitted_partition_2}')
                    partitions.remove(r)
                    partitions.append(splitted_partition_1)
                    partitions.append(splitted_partition_2)
                    if r in w:
                        print(
                            f'\t\tt {r} pertence à {w}, replace r com r1 e r2')
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
