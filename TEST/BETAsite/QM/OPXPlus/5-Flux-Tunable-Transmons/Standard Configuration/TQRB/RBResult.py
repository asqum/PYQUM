import dataclasses
from scipy.optimize import curve_fit
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

def power_law(m, a, b, p):
    return a * (p**m) + b

@dataclasses.dataclass
class RBResult:
    circuit_depths: list[int]
    num_repeats: int
    num_averages: int
    state: np.ndarray

    def __post_init__(self):
        self.data = xr.Dataset(
            data_vars={"state": (["circuit_depth", "repeat", "average"], self.state)},
            coords={
                "circuit_depth": self.circuit_depths,
                "repeat": range(self.num_repeats),
                "average": range(self.num_averages),
            },
        )

    def plot_hist(self, n_cols=3):
        if len(self.circuit_depths) < n_cols:
            n_cols = len(self.circuit_depths)
        n_rows = max(int(np.ceil(len(self.circuit_depths) / n_cols)), 1)
        plt.figure()
        for i, circuit_depth in enumerate(self.circuit_depths, start=1):
            ax = plt.subplot(n_rows, n_cols, i)
            self.data.state.sel(circuit_depth=circuit_depth).plot.hist(ax=ax, xticks=range(4))
        plt.tight_layout()

    def plot_fidelity(self):
        counts_0 = (self.data.state == 0).sum('average') / self.num_averages
        fidelity = (self.data.state == 0).sum(("repeat", "average")) / (self.num_repeats * self.num_averages)
        std_repeat = counts_0.std('repeat')
        x = np.linspace(0, len(self.circuit_depths)-1, len(self.circuit_depths))
        data = fidelity.values
        pars, cov = curve_fit(
            f=power_law,
            xdata=x,
            ydata=data,
            p0=[0.5, 0.5, 0.9],
            bounds=(-np.inf, np.inf),
            maxfev=2000,
        )
        d = 2**2
        ref_r = (1 - pars[2])*(d-1)/d
        ref_f = 1 - ref_r
        print("#########################")
        print("### Fitted Parameters ###")
        print("#########################")
        print(f"A = {pars[0]:.3}, B = {pars[1]:.3}, p = {pars[2]:.3}")
        print(f'Reference Error Rate: {ref_r:.4f}')
        print(f'Reference Fidelity: {ref_f:.4f}')
        plt.figure()
        plt.plot(x, power_law(x, *pars), linestyle="--", linewidth=2, label='fitting')
        plt.errorbar(x, fidelity, yerr=std_repeat, fmt='o', label='exp with error bar')
        fidelity.rename("fidelity").plot.line(label='exp')
        plt.title(f'Two-Qubit Gate Reference Fidelity: {ref_f:.4f}')
        plt.legend()
