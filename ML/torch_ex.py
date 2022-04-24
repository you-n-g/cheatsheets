import torch

# # Outlines: Datatype conversion related

t = torch.rand(300, 300)
t.std().item()  #  only non-tensor values can be accepted by some functions


# # Outlines: model examples

lm = torch.nn.Linear(300, 1)

lm.train()
lm(t).mean().backward()

lm.weight.grad


list(lm.named_modules())

import torch.nn as nn
from collections import OrderedDict
from functools import partial

class NN(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(10, 10), nn.Linear(10, 5))

        # save activations by registering forward hook
        self.activation = OrderedDict()
        for name, m in self.named_modules():
            if type(m) == nn.Linear:
                # partial to assign the layer name to each hook
                m.register_forward_hook(partial(self._save_activation, name))

    def _save_activation(self, name, mod, inp, out):
        self.activation[name] = out.cpu()

    # TODO: forward

foo_nn = NN()


print(list(foo_nn.named_modules()))


# TODO: save all the activations  https://gist.github.com/Tushar-N/680633ec18f5cb4b47933da7d10902af
# 根据经验，如果想查看 weight, grad, activation 的分布， 还是用tensorboard 性能更好
# 还可以用正则表达式筛一筛，专门看weight 或者 grad: layers\d?\.\d+\.weight$
""" 这里是记录 weight, grad, activation 的方法 (问题表象是最后 prediction都一样了， 没有梯度了)
writer = SummaryWriter(comment=R.get_recorder().name)
for k, t in self.dnn_model.named_parameters():
    writer.add_histogram(f"{k}", t, step)
    writer.add_histogram(f"{k}.grad", t.grad, step)
if hasattr(self.dnn_model, "activation"):
    for k, a in self.dnn_model.activation.items():
        writer.add_histogram(f"{k}.a", a, step)
"""



# # Outlines: performance related

import time
from contextlib import contextmanager
from tqdm.auto import tqdm


@contextmanager
def timing():
    start = time.time()
    yield
    print(f"{time.time() - start}s elapsed")


from torch.utils.data import DataLoader, TensorDataset

epoch_n = 10
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

