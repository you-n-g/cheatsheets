import copy
import numpy as np
import torch
import torch.nn as nn

# %% [markdown]
# # Outlines: 试试各个loss


# test cosine loss
data = [3, 4]
a = nn.Parameter(torch.Tensor(data), requires_grad=True)
b = nn.Parameter(torch.Tensor(data), requires_grad=True)

loss = nn.CosineSimilarity(-1)(a, b)

loss.backward()

a.grad
b.grad

# handcrafted loss
a = nn.Parameter(torch.Tensor(data), requires_grad=True)
b = nn.Parameter(torch.Tensor(data), requires_grad=True)
loss = a @ b / torch.norm(a, p=2) / torch.norm(b, p=2)

loss.backward()

a.grad

b.grad



# test the direction of loss
c = nn.Parameter(torch.Tensor(data), requires_grad=True)
c.grad
# (c / torch.norm(c, p=2))[0].backward()
# (c / torch.norm(c, p=2))[1].backward()
(c / torch.norm(c, p=2)).sum().backward()
c.grad @ c  # the vectors are perpendicular



# test the magnitude of loss
a = nn.Parameter(torch.Tensor([3, 4]), requires_grad=True)
b = nn.Parameter(torch.Tensor([4, 3]), requires_grad=True)

loss = nn.CosineSimilarity(-1)(a, b)
loss.backward()

a.grad
b.grad

a = nn.Parameter(torch.Tensor([3, 4]), requires_grad=True)
b = nn.Parameter(torch.Tensor([5, 0]), requires_grad=True)

loss = nn.CosineSimilarity(-1)(a, b)
loss.backward()

a.grad
b.grad

# Check the value range of BCE loss



# # Outlines: special operators
import torch.nn.functional as F


# ## Outlines: gumble softmax

logits = nn.Parameter(torch.Tensor([1, 2, 3, 4]), requires_grad=True)

out_oh = F.gumbel_softmax(logits, tau=1, hard=True)

emb = nn.Embedding(4, 10)

print(emb.weight.sum(axis=1))  # 看看哪个数值最大

loss = (out_oh @ emb.weight).sum()
loss.backward()

assert logits.grad is not None

# ## Outlines: cnn1d
input = torch.randn(1024, 32)
m = nn.Conv1d(in_channels=32, out_channels=32, kernel_size=1, groups=32, bias=True)
delta = (m(input.reshape(1024, 32, 1)).squeeze() - (input * m.weight.squeeze() + m.bias)).abs().mean().item()

assert np.isclose(delta, 0, atol=1e-6)

input.unsqueeze(dim=-1).unsqueeze(dim=-1).shape
input.unsqueeze(dim=-1).unsqueeze(dim=-1).squeeze(-1).shape
input.unsqueeze(dim=-1).unsqueeze(dim=-1).squeeze(0).shape

# ## Outlines:  complext gradient: torch.autograd.grad

a = torch.tensor([1., 2.], requires_grad = True).view(-1, 1)
# torch.autograd.grad(outputs=a.sum(), inputs=a)

torch.autograd.grad(outputs=[a.sum(), a.sum()], inputs=[a, a])
# return  [sum(<scaler 对 ipt_tensor 的梯度> for scaler in outputs)
#            for ipt_tensor in inputs]

torch.autograd.grad(outputs=a.sum(), inputs=[a, a])  # output could not be a list
torch.autograd.grad(outputs=a.sum(), inputs=a)[0]  # input could not be a list as well. But it still returns a tuple


# Test backward
a_orig = torch.tensor([1., 2.], requires_grad = True)
a = a_orig.view(-1, 1)

ipt_raw = torch.tensor([1., 2.])
_ipt_orig = ipt_raw.requires_grad_()
ipt_orig = _ipt_orig.requires_grad_()
ipt = ipt_orig.view(-1, 1)
a_orig.grad
ipt_orig.grad
(ipt * a).sum().backward()
a_orig.grad
ipt_orig.grad


gr = torch.autograd.grad(outputs=(ipt * a).sum(), inputs=ipt_orig, create_graph=True)

gr[0].squeeze().sum().backward()
ipt.grad
a.requires_grad  # 虽然这里是 True， 但是也会出现下面的 warning
a.grad
# view 做完reshape后，也不是 leaf node
# The .grad attribute of a Tensor that is not a leaf Tensor is being accessed . Its .grad attribute won't be populated during autograd.backward(). If you indeed want the .grad field to be populated for a non-leaf Tensor, use .retain_grad() on the non-leaf Tensor. If you access the non-leaf Tensor by mistake, make sure you access the leaf Tensor instead. See github.com/pytorch/pytorch/pull/30531 for more i nformations. (Triggered internally at  /opt/conda/conda-bld/pytorch_1659484806139/work/build/aten/src/ATen/core/TensorBody.h:477.) return self._grad

a_orig.grad
ipt_orig.grad

(ipt_orig * a_orig).sum().backward()
ipt_raw.grad   #  这里看到这里梯度会累计下去，  而且最初没设置 requires_grad_  的tensor也会累计梯度
ipt_raw.grad.zero_()  # 手动清理梯度
ipt_orig.grad


# # Outlines: Datatype conversion related

t = torch.rand(300, 300)
t.std().item()  #  only non-tensor values can be accepted by some functions

t2 = torch.rand(300, 300)


# # Outlines: model examples

lm = torch.nn.Linear(300, 1)
init_param = copy.deepcopy(lm.state_dict())

list(lm.named_modules())

lm.train()
lm(t).mean().backward()
lm.weight.grad

lm(t2).mean().backward()
lm.weight.grad

bk2 = lm.weight.grad.detach().cpu().clone()

lm.weight.grad.zero_()

lm.weight.grad

lm(torch.cat([t, t2])).mean().backward()

bk_cat = lm.weight.grad.detach().cpu().clone()


# 不知道 torch哪里的问题， 这里会有一些误差，所以这里又平方了一下才能保证 isclose  为0
assert np.isclose((bk_cat * 2 - bk2).detach().cpu().numpy() ** 2, 0,).all()

# 可以看到，eval和train来回切换，也不会影响之前积累的梯度
lm.eval()
lm.weight.grad

lm.train()
lm.weight.grad

#
optim = torch.optim.SGD(lm.parameters(), lr=0.1)

optim.step()
lm.weight.grad  # step不会清理梯度
s1w = lm.weight.detach().cpu().clone()
lm.load_state_dict(init_param)

lm.weight

lm.zero_grad()

m1 = lm(t).mean()
m2 = lm(t2).mean()

m1.retain_grad()
m2.retain_grad()

((m1 + m2) / 2).backward()

lm.weight.grad

optim.step()



assert np.isclose((lm.weight - s1w).detach().cpu().numpy() ** 2, 0).reshape(-1).all()



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

