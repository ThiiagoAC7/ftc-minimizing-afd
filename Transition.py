class Transition:
    def __init__(self, src_state, dst_state, symbol):
        """
        Transição entre um estado e outro

        Params:
        -------
        src_state:
            estado de origem

        dst_state:
            estado de destino

        symbol:
            simbolo a ser lido
        """
        self.src_state = src_state
        self.dst_state = dst_state
        self.symbol = symbol


    def __repr__(self):
        return f'Transition(src_state={self.src_state}, dst_state={self.dst_state}, read_symbol={self.symbol})' 
