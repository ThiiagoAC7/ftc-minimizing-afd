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
        for i, partition in enumerate(Q):  # i
            for j, q in enumerate(Q):     # j
                for estado in partition:
                    _t = P.transitions.get((estado, a))
                    if _t and _t in q:
                        iaj = str(i)+','+a+','+str(j)
                        l = L.get(iaj)
                        if l is None:
                            L[iaj] = set()
                            if _triangle.get((i, a)) is None:
                                _triangle[(i, a)] = []
                            _triangle[(i, a)].append(iaj)
                        L[iaj].add(estado)
                        triangle[(estado, a)] = iaj

    K = dict(filter(lambda elem: len(elem[1]) >= 2, _triangle.items()))

    _K = list(K.keys())
    

    while len(K.copy()) > 0:
        for i, a in K.copy():
            _l1 = L[K[(i, a)][0]]
            _l2 = L[K[(i, a)][1]]
            old_iaj = ""
            if len(_l1) <= len(_l2):
                old_iaj = K[(i, a)][0]
            else:
                old_iaj = K[(i, a)][1]
            new_i = str(t)
            new_j = str(old_iaj.split(',')[2])  # ultima char de iaj
            new_iaj = new_i+','+a+','+new_j
            L[new_iaj] = L.pop(old_iaj)

            if old_iaj in _triangle[(i, a)]:
                _triangle[(i, a)].remove(old_iaj)

            _triangle[(t, a)] = [new_iaj]

            if old_iaj in K[(i, a)]:
                K[(i, a)].remove(old_iaj)
                _K = list(K.keys())

            if len(_triangle[(i, a)]) < 2:
                K.pop((i, a))
                _K = list(K.keys())

            for q in L[new_iaj]:
                triangle[(q, a)] = new_iaj

            for q in L[new_iaj].copy():  # passo ii
                for b in (P.alphabet - set(a)):  # passo ii.1
                    unique_record = triangle[(q, b)]  # L(i,b,k)
                    if L.get(unique_record):
                        if L[unique_record] and q in L[unique_record]:
                            # delete the record from L(i,b,k)
                            L[unique_record].remove(q)
                        # L(t+1,b,k)
                        new_ibk = str(t)+','+b+',' + str(triangle[(q, b)].split(',')[2])
                        if L.get(new_ibk) is None:
                            L[new_ibk] = set()  # inserting it into L(t+1,b,k)
                        # inserting it into L(t+1,b,k)
                        L[new_ibk] = L[new_ibk].union(set(q))
                        triangle[(q, b)] = new_ibk
                        if len(L[unique_record]) == 0:  # if L(i,b,k) becomes empty
                            pointer_ib = (int(unique_record.split(',')[0]), b)
                            if unique_record in _triangle[pointer_ib]:
                                # we delete the pointer to L(i,b,k)
                                _triangle[pointer_ib].remove(unique_record)
                            if K.get(pointer_ib):
                                # and eventually the pointer from k
                                K.pop(pointer_ib)
                                _K = list(K.keys())
                    # and eventually, we have to add to K a pointer
                    if _triangle.get((t, b)) is None:
                        _triangle[(t, b)] = []
                    if new_ibk not in _triangle[(t, b)]:
                        # we have to add to triangle' a pointer to L(t+1,b,k)
                        _triangle[(t, b)].append(new_ibk)
                    if len(_triangle[(t, b)]) >= 2:
                        if K.get((t, b)) is None:
                            K[(t, b)] = []
                        # if _triangle[(t, b)] not in K[(t, b)]:
                        K[(t, b)] = list(set(K[(t, b)]).union( set(_triangle[(t, b)])))
                        _K = list(K.keys())

                for b in P.alphabet:  # passo ii.2
                    if inverted_triangle.get((b, q)):
                        for p in inverted_triangle[(b, q)]:
                            # we use triangle for finging the unique record
                            unique_record_2 = triangle[(p, b)]
                            k = str(unique_record_2.split(',')[0])
                            if L.get(unique_record_2):
                                # L(k,b,i)
                                if L[unique_record_2] and p in L[unique_record_2]:
                                    # we delete p from this list L(k,b,i)
                                    L[unique_record_2].remove(p)
                                new_kbt = k+','+b+','+str(t)
                                if L.get(new_kbt) is None:
                                    L[new_kbt] = set()
                                # inserting it into L(k,b,t+1)
                                L[new_kbt] = L[new_kbt].union(set(p))
                                triangle[(p, b)] = new_kbt
                                if len(L[unique_record_2]) == 0:  # if L(k,b,i) becomes empty
                                    pointer_kb = (int(k), b)
                                    if unique_record_2 in _triangle[pointer_kb]:
                                        # we delete the pointer to L(k,b,i) from triangle'
                                        _triangle[pointer_kb].remove(unique_record_2)
                                    if K.get(pointer_kb):
                                        # and eventually the pointer from k
                                        K.pop(pointer_kb)
                                        _K = list(K.keys())

                            # we have to add to triangle' a pointer
                            if _triangle.get((int(k), b)) is None:
                                _triangle[(int(k), b)] = []
                            if new_kbt not in _triangle[(int(k), b)]:
                                _triangle[(int(k), b)].append(new_kbt)
                            if len(_triangle[(int(k), b)]) >= 2:
                                if K.get((int(k), b)) is None:
                                    K[(int(k), b)] = []
                                # if _triangle[(int(k), b)] not in K[(int(k), b)]:
                                K[(int(k), b)] = list(set(K[(int(k), b)]).union(set(_triangle[(int(k), b)])))
                                _K = list(K.keys())
                # if len(L[new_iaj]) == 0:
                #     continue
        t += 1

    
    init = ''
    finals = set()
    for i in L.keys():
        if P.init in L[i]:
            init = i.split(',')[0]
        if P.finals <= L[i]:
            finals.add(i.split(',')[0])

    _states = set()
    for e in L.keys():
        _e = e.split(',')[0]
        if _e not in _states:
            _states.add(_e)

    _T = {}
    for i in L.keys():
        src, a, dst = i.split(',')
        if len(L[i]) > 0:
            _T[src, a] = dst

    return AFD(_states, P.alphabet, _T, init, finals)


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
