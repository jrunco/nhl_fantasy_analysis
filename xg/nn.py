"""From-scratch gradient-descent models on torch tensors, mirroring course22 nb04/05.
A 'model' is just a tensor (linear) or list of tensors (NN); training is a manual loop
of loss.backward() + in-place SGD steps — no torch.nn layers, no optimizer objects.
Predictions go through a sigmoid, so outputs are goal probabilities (xG)."""

import matplotlib.pyplot as plt
import torch


def init_coeffs(n_coeff, seed=442):
    """Linear model: one random coefficient per feature (nb05)."""
    torch.manual_seed(seed)
    return (torch.rand(n_coeff) - 0.5).requires_grad_()


def linear_preds(coeffs, indeps):
    return torch.sigmoid((indeps * coeffs).sum(axis=1))


def init_nn_coeffs(n_coeff, n_hidden=20, seed=442):
    """One-hidden-layer net: [n_coeff x n_hidden] -> [n_hidden x 1] + bias (nb05)."""
    torch.manual_seed(seed)
    layer1 = (torch.rand(n_coeff, n_hidden) - 0.5) / n_hidden
    layer2 = torch.rand(n_hidden, 1) - 0.3
    const = torch.rand(1)[0]
    return [t.requires_grad_() for t in (layer1, layer2, const)]


def nn_preds(coeffs, indeps):
    l1, l2, const = coeffs
    res = torch.relu(indeps @ l1)
    return torch.sigmoid(res @ l2 + const).squeeze(-1)


def init_deep_coeffs(n_coeff, hiddens=(10, 10), seed=442):
    """Deep net: arbitrary hidden widths, ending in a 1-wide output layer (nb05)."""
    torch.manual_seed(seed)
    sizes = [n_coeff, *hiddens, 1]
    layers = [(torch.rand(sizes[i], sizes[i + 1]) - 0.3) / sizes[i + 1] * 4
              for i in range(len(sizes) - 1)]
    consts = [(torch.rand(1)[0] - 0.5) * 0.1 for _ in range(len(sizes) - 1)]
    return [t.requires_grad_() for t in layers + consts]


def deep_preds(coeffs, indeps):
    n = len(coeffs) // 2
    layers, consts = coeffs[:n], coeffs[n:]
    res = indeps
    for i, (lay, c) in enumerate(zip(layers, consts)):
        res = res @ lay + c
        if i != n - 1:
            res = torch.relu(res)
    return torch.sigmoid(res).squeeze(-1)


def calc_loss(pred_fn, coeffs, indeps, deps, loss="bce"):
    """'bce' = log loss, the proper score for probabilities; 'mae' = nb05's original."""
    p = pred_fn(coeffs, indeps)
    if loss == "mae":
        return torch.abs(p - deps).mean()
    p = p.clamp(1e-6, 1 - 1e-6)
    return -(deps * p.log() + (1 - deps) * (1 - p).log()).mean()


def train(pred_fn, coeffs, trn_indep, trn_dep, val_indep, val_dep,
          epochs=60, lr=2.0, loss="bce", report_every=10):
    """Manual full-batch gradient descent (nb05's train_model). Prints train loss as
    it goes; returns (coeffs, val_loss_history)."""
    single = torch.is_tensor(coeffs)
    history = []
    for ep in range(epochs):
        trn_loss = calc_loss(pred_fn, coeffs, trn_indep, trn_dep, loss)
        trn_loss.backward()
        with torch.no_grad():
            for t in [coeffs] if single else coeffs:
                t.sub_(t.grad * lr)
                t.grad.zero_()
            history.append(calc_loss(pred_fn, coeffs, val_indep, val_dep, loss).item())
        if ep % report_every == 0 or ep == epochs - 1:
            print(f"epoch {ep:3d}  trn {trn_loss:.4f}  val {history[-1]:.4f}")
    return coeffs, history


def evaluate(pred_fn, coeffs, indeps, deps):
    """{'log_loss', 'xg_sum', 'goals'} on a dataset, without grad."""
    with torch.no_grad():
        p = pred_fn(coeffs, indeps)
        ll = calc_loss(pred_fn, coeffs, indeps, deps, "bce").item()
    return {"log_loss": ll, "xg_sum": p.sum().item(), "goals": int(deps.sum().item())}


def calibration_plot(preds, deps, bins=10):
    """Predicted xG vs actual goal rate by prediction decile; a good model hugs y=x."""
    preds = preds.detach() if torch.is_tensor(preds) else torch.tensor(preds)
    order = preds.argsort()
    p, y = preds[order], deps[order]
    edges = torch.linspace(0, len(p), bins + 1).long()
    mean_p = [p[edges[i]:edges[i + 1]].mean().item() for i in range(bins)]
    mean_y = [y[edges[i]:edges[i + 1]].mean().item() for i in range(bins)]
    plt.figure(figsize=(5, 5))
    plt.plot(mean_p, mean_y, "o-", label="model")
    lim = max(max(mean_p), max(mean_y)) * 1.1
    plt.plot([0, lim], [0, lim], "k--", label="perfect")
    plt.xlabel("mean predicted xG")
    plt.ylabel("actual goal rate")
    plt.legend()
    plt.title("Calibration by prediction decile")
