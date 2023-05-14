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
        aux = inverted_triangle.get((a, r_state))
        if aux is None:
            inverted_triangle[(a, r_state)] = []
        inverted_triangle[(a, r_state)].append(l_state)

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
                            if _triangle.get((i, a)) is None:
                                _triangle[(i, a)] = []
                            _triangle[(i, a)].append(iaj)
                        L[iaj].add(estado)
                        triangle[(estado, a)] = iaj

    print(f'inverted_triangle = {inverted_triangle}')
    print(f'triangle = {triangle}')
    print(f'triangle linha = {_triangle}')
    print(f'L = {L}')

    K = dict(filter(lambda elem: len(elem[1]) >= 2, _triangle.items()))
    print(f'K = {K}')

    _K = list(K.keys())
    #acho que as somas de t tão erradas
    while len(_K) > 0:
        for i, a in _K:
            # _f = input('>')
            print(f'================PASSO I================')
            print(f'K = {K}, _K = {_K}')
            print(f'L = {L}')
            print(f'triangle = {triangle}')
            print(f'trianglinha = {_triangle}')
            print(f'inverted_triangle = {inverted_triangle}')
            _l1 = L[K[(i, a)][0]]
            _l2 = L[K[(i, a)][1]]
            print(f'\t _l1 = {_l1}')
            print(f'\t _l2 = {_l2}')
            old_iaj = ""
            if len(_l1) <= len(_l2):
                old_iaj = K[(i, a)][0]
            else:
                old_iaj = K[(i, a)][1]
            new_i = str(t)
            new_j = str(old_iaj[2])  # ultima char de iaj
            new_iaj = new_i+a+new_j
            print(f'old_iaj -> {old_iaj}')
            print(f'_triangle({i}, {a}) -> {_triangle[(i,a)]}')
            L[new_iaj] = L.pop(old_iaj)
            
            _triangle[(i, a)].remove(old_iaj)
            _triangle[(t, a)] = [new_iaj]

            if old_iaj in K[(i,a)]: 
                K[(i,a)].remove(old_iaj)
            
            if len(_triangle[(i, a)]) < 2:
                _K.remove((i, a))
                K.pop((i, a))

            print(f'new_iaj -> {L[new_iaj]}')
            print(f'new L = {L}')
            print(f'new K = {K},_K = {_K}')
            print(f'trianglinha = {_triangle}')
            print(f'triangle = {triangle}')
            for q in L[new_iaj]:
                triangle[(q,a)] = new_iaj
            print(f'triangle atualizado os ponteiros = {triangle}')

            # _f = input('>')
            for q in L[new_iaj].copy(): # passo ii
                print(f'================PASSO II.1================')
                print(f'\tK = {K}, _K = {_K}')
                print(f'\tL = {L}')
                print(f'\ttriangle = {triangle}')
                print(f'\ttrianglinha = {_triangle}')
                print(f'\tinverted_triangle = {inverted_triangle}')
                for b in (P.alphabet - set(a)): # passo ii.1
                    print(f'\t\t triangle({q},{b}) = {triangle[(q,b)]}')
                    unique_record = triangle[(q, b)]  # L(i,b,k)
                    if unique_record:
                        if L[unique_record] and q in L[unique_record]:
                        # delete the record from L(i,b,k)
                            L[unique_record].remove(q)
                        new_ibk = str(t)+b+str(triangle[(q, b)][2]) # L(t+1,b,k)
                        if L.get(new_ibk) is None:
                            L[new_ibk] = set()  # inserting it into L(t+1,b,k)
                        L[new_ibk] = L[new_ibk].union(set(q))  # inserting it into L(t+1,b,k)
                        triangle[(q,b)] = new_ibk
                        # triangle[(q,b)] = new_ibk # atualiza pointer de triangle
                        print(f'\t\tverifica L[{unique_record}]')
                        if len(L[unique_record]) == 0: # if L(i,b,k) becomes empty
                            pointer_ib = (int(unique_record[0]), b)
                            print(f'======================================')
                            print(f'unique_record-> {unique_record}')
                            print(f'pointer_ib -> {pointer_ib}')
                            print(f'_triangle -> {_triangle}')
                            print(f'L = {L}')
                            print(f'K -> {K}, _K = {_K}')
                            print(f'======================================')
                            if unique_record in _triangle[pointer_ib]:
                                _triangle[pointer_ib].remove(unique_record) # we delete the pointer to L(i,b,k)
                            if K.get(pointer_ib):
                                K.pop(pointer_ib) # and eventually the pointer from k
                                _K.remove(pointer_ib)
                            # triangle.pop((q,b)) # remove pointer 
                    print(f'\tL ->{L}') 
                    print(f'\ttriangle ->{triangle}')
                    print(f'\ttrianglinha = {_triangle}')
                    if _triangle.get((t,b)) is None: # and eventually, we have to add to K a pointer
                        _triangle[(t,b)] = [] 
                    if new_ibk not in _triangle[(t,b)]:
                        _triangle[(t,b)].append(new_ibk) # we have to add to triangle' a pointer to L(t+1,b,k)
                    print(f'\ttrianglinha = {_triangle}')
                    if len(_triangle[(t,b)]) >= 2:
                        if K.get((t,b)) is None:
                            K[(t, b)] = []
                        if _triangle[(t,b)] not in K[(t,b)]:
                            # K[(t,b)].append(_triangle[(t,b)])
                            K[(t,b)] = list(set(K[(t,b)]).union(set(_triangle[(t,b)])))
                            _K.append((t,b))
                    print(f'\tK = {K}, _K = {_K}')
                    print(f'\tL = {L}')
                # _f = input('>')
                print(f'================PASSO II.2================')
                print(f'\tK = {K}, _K = {_K}')
                print(f'\tL = {L}')
                print(f'\ttriangle = {triangle}')
                print(f'\ttrianglinha = {_triangle}')
                print(f'\tinverted_triangle = {inverted_triangle}')
                for b in P.alphabet: # passo ii.2
                    if inverted_triangle.get((b,q)):
                        print(f'\t inverted_triangle({b},{q}) -> {inverted_triangle[(b,q)]}')
                        for p in inverted_triangle[(b,q)]:
                            unique_record_2 = triangle[(p,b)] # we use triangle for finging the unique record 
                            print(f'\t p->{p}, unique_record_2 = {unique_record_2}')
                            print(f'\t triangle[({p},{b})]= {triangle[(p,b)]}')
                            # print(f'\t\t L({triangle[(p,b)]}) = {L[triangle[(p,b)]]}')
                            k = str(unique_record_2[0])
                            if unique_record_2:
                                if L[unique_record_2] and p in L[unique_record_2]: # L(k,b,i)
                                    L[unique_record_2].remove(p) # we delete p from this list L(k,b,i)
                                new_kbt = k+b+str(t)
                                if L.get(new_kbt) is None:
                                    L[new_kbt] = set()
                                L[new_kbt] = L[new_kbt].union(set(p)) # inserting it into L(k,b,t+1)
                                print(f'\t L({triangle[(p,b)]}) = {L[triangle[(p,b)]]}')
                                print(f'\t L({new_kbt}) = {L[new_kbt]}')
                                triangle[(p,b)] = new_kbt
                                print(f'\t triangle = {triangle}')
                                print(f'\t L -> {L}')
                                print(f'\t verificando L[{unique_record_2}]')
                                if len(L[unique_record_2]) == 0: # if L(k,b,i) becomes empty 
                                    pointer_kb = (int(k),b) 
                                    _triangle[pointer_kb].remove(unique_record_2) # we delete the pointer to L(k,b,i) from triangle'
                                    if K.get(pointer_kb):
                                        K.pop(pointer_kb) # and eventually the pointer from k
                                        _K.remove(pointer_kb)
                            
                            print(f'\t ({k},{b})')
                            print(f'\t _triangle = {_triangle}')
                            print(f'\t L -> {L}')
                            if _triangle.get((int(k),b)) is None: # we have to add to triangle' a pointer 
                                _triangle[(int(k),b)] = [] 
                            if new_kbt not in _triangle[(int(k),b)]:
                                _triangle[(int(k),b)].append(new_kbt)
                            print(f'\t _triangle = {_triangle}')
                            if len(_triangle[(int(k),b)]) >= 2:
                                if K.get((int(k),b)) is None:
                                    K[(int(k),b)] = []
                                if _triangle[(int(k),b)] not in K[(int(k),b)]:
                                    K[(int(k),b)] = list(set(K[(int(k),b)]).union(set(_triangle[(int(k),b)])))
                                    if (int(k),b) not in _K:
                                        _K.append((int(k),b))
                print(f'q -> {q}, L[{new_iaj}] = {L[new_iaj]}')
                if len(L[new_iaj]) == 0: 
                    t += 1
                    continue
        t += 1

    print(f'L = {L}')
    print(f'triangle = {triangle}')
    print(f'inverted_triangle = {inverted_triangle}')


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
        # _fodase = input('>')

    print(partitions)
    # construir AFD a partir de estados criados
