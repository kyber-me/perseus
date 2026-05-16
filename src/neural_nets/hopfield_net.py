
# import numpy as np
# from numpy.typing import NDArray


# Turn it into a protocol to serve as machine to the hipocampus (HipocampusMachine)
class HopfieldNet:

    # stored: NDArray
    # weights: NDArray
    stored: list 
    weights: list
    h_dim: tuple[int, int] | tuple[int, int, int]

    
    def __init__(self, h_dim: tuple[int, int] | tuple[int, int, int]) -> None:
        # self.stored = np.array([], dtype='i')
        # self.weights = np.array([], dtype='i')
        self.stored = []
        self.weights = []
        # print(self.stored.dtype)

        self.h_dim = h_dim

    def learn(self, pattern: list[list[int]]):
        # print("shape: ", pattern.shape)

        # assert pattern.shape == self.h_dim

        # pattern_rv = pattern.ravel()
        pattern_flatten = []
        for r in pattern:
            for c in r:
                pattern_flatten.append(c)
        outer_mem_w = []
        enum_flatten = enumerate(pattern_flatten)

        # For every neuron a inner_w is a list of weights associated with it's pairs.
        # The index of each corresponds to the position in the original flatten version of the neurons
        for i, outer_n in enum_flatten:
            inner_mem_w = []
            for j, inner_n in enum_flatten:
                inner_mem_w.append(outer_n * inner_n) if i != j else inner_mem_w.append(0)
            
            outer_mem_w.append(inner_mem_w)
        
        self.stored.append(pattern)
        self.weights.append(outer_mem_w)

                
    def infer(self):
        pass 



if __name__ == "__main__":
    hopnet = HopfieldNet((4 ,4))
