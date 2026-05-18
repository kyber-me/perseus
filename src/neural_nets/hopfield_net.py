
import numpy as np
from numpy.typing import NDArray


# Turn it into a protocol to serve as machine to the hipocampus (HipocampusMachine)
class HopfieldNet:

    stored: list[NDArray]
    weights: NDArray
    h_dim: tuple[int, int, int] | tuple[int, int]
    N: int

    def __init__(self, h_dim: tuple[int, int, int] | tuple[int, int] = (16, 16, 16)) -> None:
        self.h_dim = h_dim
        self.N = int(np.prod(h_dim))
        self.stored = []
        # Pre-allocate weights as int8 for memory efficiency (cumulative Hebbian learning)
        self.weights = np.zeros((self.N, self.N), dtype=np.int8)

    def learn(self, pattern: NDArray) -> None:
        """
        Store a new pattern in the network using Hebbian learning.
        """
        assert pattern.shape == self.h_dim, f"Pattern shape {pattern.shape} does not match network dims {self.h_dim}"

        # 1. flatten the pattern
        pattern_rv = pattern.ravel()

        # Convert {0, 1} binary to {-1, 1} bipolar for Hebbian learning mathematically
        is_binary = np.isin(pattern_rv, [0, 1]).all()
        if is_binary:
            pattern_bipolar = np.where(pattern_rv == 0, -1, 1).astype(np.int8)
        else:
            pattern_bipolar = pattern_rv.astype(np.int8)

        # 2. calculate the outer product of the pattern with itself
        inner = np.outer(pattern_bipolar, pattern_bipolar)

        # 3. update the weights cumulatively
        self.weights += inner

        # 4. set the diagonal to 0 to prevent self-connections
        np.fill_diagonal(self.weights, 0)

        # 5. store the original exact 3D pattern
        self.stored.append(pattern.copy())

    def infer(self, pattern: NDArray, steps: int = 10, mode: str = 'asynchronous') -> NDArray:
        """
        Recover a pattern using the energy minimization dynamic (attractor).
        """
        assert pattern.shape == self.h_dim, f"Pattern shape {pattern.shape} does not match network dims {self.h_dim}"
        
        pattern_rv = pattern.ravel()
        
        # Identify original domain to reconstruct correctly later
        is_binary = np.isin(pattern_rv, [0, 1]).all()
        if is_binary:
            state = np.where(pattern_rv == 0, -1, 1).astype(np.int8)
        else:
            state = pattern_rv.astype(np.int8).copy()

        if mode == 'asynchronous':
            for step in range(steps):
                changed = False
                
                # Asynchronous updates: shuffle the neurons and update them one by one
                indices = np.arange(self.N)
                np.random.shuffle(indices)
                
                for i in indices:
                    # Dot product with upcast to prevent np.int8 accumulator overflow
                    weights_row = self.weights[i].astype(np.int32)
                    activation = np.dot(weights_row, state)
                    
                    # Compute new state using the sign function, mapping 0 to 1 to maintain bipolarity
                    new_val = 1 if activation >= 0 else -1
                    
                    if state[i] != new_val:
                        state[i] = new_val
                        changed = True
                
                if not changed:
                    print(f"Converged at step {step + 1} (asynchronous)")
                    break
        else:
            # Synchronous mode (all at once)
            for step in range(steps):
                weights_safe = self.weights.astype(np.int32)
                activations = np.dot(weights_safe, state)
                new_state = np.where(activations >= 0, 1, -1).astype(np.int8)
                
                if np.array_equal(state, new_state):
                    print(f"Converged at step {step + 1} (synchronous)")
                    break
                state = new_state
                
        # Re-shape back to 3D
        recovered_3d = state.reshape(self.h_dim)
        
        # Map back to {0, 1} if input was binary
        if is_binary:
            recovered_3d = np.where(recovered_3d == -1, 0, 1).astype(np.int8)
            
        return recovered_3d 



if __name__ == "__main__":
    hopnet = HopfieldNet((16, 16, 16))
