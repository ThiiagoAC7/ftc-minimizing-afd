import xml.etree.ElementTree as ET

from AFD import AFD


def min_nlogn(states, alphabet, transitions, initial, finals):

    p = [finals, states - finals]
    w = [finals]

    while len(w) > 0:
        a = w.pop(0)
        for symbol in alphabet:
            x = set()
            for s in states:
                if (s, symbol) in transitions and transitions[(s, symbol)] in a:
                    x.add(s)

            for y in p:
                if len(x & y) > 0 and len(y - x) > 0:
                    p.remove(y)
                    p.append(x & y)
                    p.append(y - x)
                    if y in w:
                        w.remove(y)
                        w.append(x & y)
                        w.append(y - x)
                    else:
                        if len(x & y) <= len(y - x):
                            w.append(x & y)
                        else:
                            w.append(y - x)

    _states = range(len(p))
    _transitions = {}

    for i in _states:
        for symbol in alphabet:
            s = next(iter(p[i]))
            t = transitions.get((s, symbol), None)
            if t is not None:
                for j, partition in enumerate(p):
                    if t in partition:
                        _transitions[(i, symbol)] = j
                        break

    _initial = next(i for i, partition in enumerate(
        p) if initial in partition)
    _finals = set(i for i, partition in enumerate(
        p) if len(finals & partition) > 0)

    return AFD(_states, alphabet, _transitions, _initial, _finals)


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
                    reachable_state = P.transitions[(e, a)]
                    transitions_set[a] = _get_set_c_transition(
                        S[n-1], reachable_state)

                Y = []
                Y.append(e)
                for _e in list(X)[1:]:
                    count = 0
                    for a in P.alphabet:
                        if P.transitions[_e, a] in transitions_set[a]:
                            count += 1
                    if count == len(P.alphabet):
                        Y.append(_e)

                X = set(X) - set(Y)
                S[n].append(Y)

    _i = -1
    for i in S[n]:
        if P.init in i:
            _i = i

    _f = set()
    for i in S[n]:
        if P.finals.issubset(i):
            _f.add(str(i))

    _T = {}
    for x in S[n]:
        for a in P.alphabet:
            _transition = _get_set_c_transition(S[n], P.transitions[x[0], a])
            _T[str(x), str(_transition)] = a

    SN = []
    for i in S[n]:
        SN.append(str(i))

    return AFD(set(SN), P.alphabet, _T, _i, _f)
