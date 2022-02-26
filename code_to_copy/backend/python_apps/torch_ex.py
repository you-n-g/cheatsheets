# # Outlines: performance related

import time
from contextlib import contextmanager
from tqdm.auto import tqdm


@contextmanager
def timing():
    start = time.time()
    yield
    print(f"{time.time() - start}s elapsed")


import torch
from torch.utils.data import DataLoader, TensorDataset

epoch_n = 50
n = 100_000
fea_n = 300
batch_size = 1024
samples_tensor = torch.rand(n, 300)

with timing():
    for e in tqdm(range(epoch_n)):
        for b in range(n // batch_size):
            x = samples_tensor[b * batch_size:(b + 1) * batch_size]


# with shuffle, extremely slow
dset = TensorDataset(samples_tensor)
data_train_loader = DataLoader(dset, batch_size=batch_size, shuffle=True)


def walk_data_loader():
    with timing():
        for e in tqdm(range(epoch_n)):
            for b in data_train_loader:
                pass
            print(b) # NOTE:  dataloader will shuffle data every time if `shuffle=True`
walk_data_loader()


data_train_loader = DataLoader(dset, batch_size=batch_size, shuffle=False)
walk_data_loader()
print("Skipping shuffle only makes it slightly better.")


data_train_loader = DataLoader(dset, batch_size=batch_size, shuffle=False, pin_memory=True)
walk_data_loader()
print("pin_memory will make it even slower")


with timing():
    for e in tqdm(range(epoch_n)):
        # If we reandom shuffle the data, it will be much slower
        # But it is still much faster than DataLoader
        samples_tensor = samples_tensor[torch.randperm(samples_tensor.size()[0]), :]
        for b in range(n // batch_size):
            x = samples_tensor[b * batch_size:(b + 1) * batch_size]

# Reference
# - https://discuss.pytorch.org/t/dataloader-much-slower-than-manual-batching/27014
# - https://pytorch.org/docs/stable/data.html


