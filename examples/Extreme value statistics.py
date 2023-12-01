"""Created on Wed Sep  9 23:31:11 2020.

@author: mofarrag
"""
import matplotlib

matplotlib.use("TkAgg")
import pandas as pd
from statista.distributions import GEV, ConfidenceInterval, Gumbel, PlottingPosition

time_series1 = pd.read_csv("examples/data/time_series1.txt", header=None)[0].tolist()
time_series2 = pd.read_csv("examples/data/time_series2.txt", header=None)[0].tolist()
# %%
Gdist = Gumbel(time_series1)
# defult parameter estimation method is maximum liklihood method
Param_mle = Gdist.fit_model(method="mle")
Gdist.ks()
Gdist.chisquare()
print(Param_mle)
# calculate and plot the pdf
pdf = Gdist.pdf(Param_mle, plot_figure=True)
cdf, _, _ = Gdist.cdf(Param_mle, plot_figure=True)
# %% lmoments
Param_lmoments = Gdist.fit_model(method="lmoments")
Gdist.ks()
Gdist.chisquare()
print(Param_lmoments)
loc = Param_lmoments[0]
scale = Param_lmoments[1]
# calculate and plot the pdf
pdf = Gdist.pdf(loc, scale, plot_figure=True)
cdf, _, _ = Gdist.cdf(loc, scale, plot_figure=True)
# %%
# calculate the CDF(Non Exceedance probability) using weibul plotting position
time_series1.sort()
# calculate the F (Non Exceedence probability based on weibul)
cdf_Weibul = PlottingPosition.weibul(time_series1)
# TheporeticalEstimate method calculates the theoretical values based on the Gumbel distribution
Qth = Gdist.theoretical_estimate(loc, scale, cdf_Weibul)
# test = stats.chisquare(st.Standardize(Qth), st.Standardize(time_series1),ddof=5)
# calculate the confidence interval
upper, lower = Gdist.confidence_interval(loc, scale, cdf_Weibul, alpha=0.1)
# ProbapilityPlot can estimate the Qth and the lower and upper confidence interval in the process of plotting
fig, ax = Gdist.probapility_plot(loc, scale, cdf_Weibul, alpha=0.1)
# %%
"""
if you want to focus only on high values, you can use a threshold to make the code focus on what is higher
this threshold.
"""
threshold = 17
Param_dist = Gdist.fit_model(
    method="optimization", ObjFunc=Gumbel.ObjectiveFn, threshold=threshold
)
print(Param_dist)
loc = Param_dist[0]
scale = Param_dist[1]
Gdist.probapility_plot(loc, scale, cdf_Weibul, alpha=0.1)
# %%
threshold = 18
Param_dist = Gdist.fit_model(
    method="optimization", ObjFunc=Gumbel.ObjectiveFn, threshold=threshold
)
print(Param_dist)
loc = Param_dist[0]
scale = Param_dist[1]
Gdist.probapility_plot(loc, scale, cdf_Weibul, alpha=0.1)
# %% Generalized Extreme Value (GEV)
Gevdist = GEV(time_series2)
# default parameter estimation method is maximum liklihood method
mle_param = Gevdist.fit_model(method="mle")
Gevdist.ks()
Gevdist.chisquare()

print(mle_param)
shape = mle_param[0]
loc = mle_param[1]
scale = mle_param[2]
# calculate and plot the pdf
pdf, fig, ax = Gevdist.pdf(shape, loc, scale, plot_figure=True)
cdf, _, _ = Gevdist.cdf(shape, loc, scale, plot_figure=True)
# %% lmoment method
lmom_param = Gevdist.fit_model(method="lmoments")
print(lmom_param)
shape = lmom_param[0]
loc = lmom_param[1]
scale = lmom_param[2]
# calculate and plot the pdf
pdf, fig, ax = Gevdist.pdf(shape, loc, scale, plot_figure=True)
cdf, _, _ = Gevdist.cdf(shape, loc, scale, plot_figure=True)
#%%
time_series1.sort()
# calculate the F (Non Exceedence probability based on weibul)
cdf_Weibul = PlottingPosition.weibul(time_series1)
T = PlottingPosition.weibul(time_series1, option=2)
# TheporeticalEstimate method calculates the theoretical values based on the Gumbel distribution
Qth = Gevdist.theoretical_estimate(shape, loc, scale, cdf_Weibul)

func = GEV.ci_func
upper, lower = Gevdist.confidence_interval(
    shape,
    loc,
    scale,
    F=cdf_Weibul,
    alpha=0.1,
    statfunction=func,
    n_samples=len(time_series1),
)
# %%
"""
calculate the confidence interval using the boot strap method directly
"""
CI = ConfidenceInterval.BootStrap(
    time_series1,
    statfunction=func,
    gevfit=Param_dist,
    n_samples=len(time_series1),
    F=cdf_Weibul,
)
LB = CI["LB"]
UB = CI["UB"]
# %%
fig, ax = Gevdist.probapility_plot(
    shape, loc, scale, cdf_Weibul, func=func, n_samples=len(time_series1)
)
