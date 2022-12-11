import numpy as np

def create_APRBS(max, min, samples, hold_samples):
    steps = int(samples/hold_samples)
    APRBS = []
    for _ in range(steps):
        point = min + (max-min)*np.random.rand()
        if point < 0:
            print(point, max, min)
        temp_array = np.ones((hold_samples,1))*point        
        APRBS.append(temp_array)
    return np.concatenate(APRBS)