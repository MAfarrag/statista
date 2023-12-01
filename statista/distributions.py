"""Statistical distributions."""
from typing import Any, List, Tuple, Union, Dict, Callable
from abc import ABC, abstractmethod
import numpy as np
import scipy.optimize as so
from matplotlib.figure import Figure

from numpy import ndarray
from scipy.stats import chisquare, genextreme, gumbel_r, ks_2samp, norm, expon

from statista.parameters import Lmoments
from statista.tools import Tools as st
from statista.plot import Plot
from statista.confidence_interval import ConfidenceInterval

ninf = 1e-5

__all__ = ["PlottingPosition", "Gumbel", "GEV", "Exponential", "Normal"]


class PlottingPosition:
    """PlottingPosition."""

    def __init__(self):
        pass

    @staticmethod
    def return_period(F: Union[list, np.ndarray]) -> np.ndarray:
        """returnPeriod.

        Parameters
        ----------
        F: [list/array]
            non exceedence probability.

        Returns
        -------
        array:
           return period.
        """
        F = np.array(F)
        T = 1 / (1 - F)
        return T

    @staticmethod
    def weibul(data: Union[list, np.ndarray], return_period: int = False) -> np.ndarray:
        """Weibul.

        Weibul method to calculate the cumulative distribution function cdf or
        return period.

        Parameters
        ----------
        data : [list/array]
            list/array of the data.
        return_period : [bool]
            False to calculate the cumulative distribution function cdf or
            True to calculate the return period. Default=False

        Returns
        -------
        cdf/T: [list]
            list of cumulative distribution function or return period.
        """
        data = np.array(data)
        data.sort()
        n = len(data)
        cdf = np.array(range(1, n + 1)) / (n + 1)
        if not return_period:
            return cdf
        else:
            T = PlottingPosition.return_period(cdf)
            return T


class AbstractDistribution(ABC):
    """
    AbstractDistribution.
    """

    parameters: Dict[str, Union[float, Any]]
    cdf_Weibul: ndarray

    def __init__(
        self,
        data: Union[list, np.ndarray] = None,
        parameters: Dict[str, str] = None,
    ):
        """Gumbel.

        Parameters
        ----------
        data : [list]
            data time series.
        parameters: Dict[str, str]
            {"loc": val, "scale": val, "shape": value}
            - loc: [numeric]
                location parameter
            - scale: [numeric]
                scale parameter
        """
        if isinstance(data, list) or isinstance(data, np.ndarray):
            self.data = np.array(data)
            self.data_sorted = np.sort(data)
            self.cdf_Weibul = PlottingPosition.weibul(data)
            self.KStable = 1.22 / np.sqrt(len(self.data))

        self.parameters = parameters

        self.Dstatic = None
        self.KS_Pvalue = None
        self.chistatic = None
        self.chi_Pvalue = None

        pass

    @abstractmethod
    def pdf(
        self,
        parameters: Dict[str, Union[float, Any]],
        plot_figure: bool = False,
        figsize: tuple = (6, 5),
        xlabel: str = "Actual data",
        ylabel: str = "pdf",
        fontsize: Union[float, int] = 15,
        actual_data: Union[bool, np.ndarray] = True,
    ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
        """pdf.

        Returns the value of Gumbel's pdf with parameters loc and scale at x .

        Parameters:
        -----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.

        Returns
        -------
        pdf : [array]
            probability density function pdf.
        """

        if actual_data is None:
            ts = self.data
        else:
            ts = actual_data

        return ts

    @abstractmethod
    def cdf(
        self,
        parameters: Dict[str, Union[float, Any]],
        plot_figure: bool = False,
        figsize: tuple = (6, 5),
        xlabel: str = "data",
        ylabel: str = "cdf",
        fontsize: int = 15,
        actual_data: Union[bool, np.ndarray] = True,
    ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
        """cdf.

        cdf calculates the value of Gumbel's cdf with parameters loc and scale at x.

        parameter:
        ----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        """
        pass

    @abstractmethod
    def estimate_parameter(
        self,
        method: str = "mle",
        ObjFunc: Callable = None,
        threshold: Union[None, float, int] = None,
        test: bool = True,
    ) -> Dict[str, str]:
        """estimateParameter.

        EstimateParameter estimate the distribution parameter based on MLM
        (Maximum liklihood method), if an objective function is entered as an input

        There are two likelihood functions (L1 and L2), one for values above some
        threshold (x>=C) and one for values below (x < C), now the likeliest parameters
        are those at the max value of mutiplication between two functions max(L1*L2).

        In this case the L1 is still the product of multiplication of probability
        density function's values at xi, but the L2 is the probability that threshold
        value C will be exceeded (1-F(C)).

        Parameters
        ----------
        ObjFunc : [function]
            function to be used to get the distribution parameters.
        threshold : [numeric]
            Value you want to consider only the greater values.
        method : [string]
            'mle', 'mm', 'lmoments', optimization
        test: [bool]
            Default is True.

        Returns
        -------
        Dict[str, str]:
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        """
        pass

    @staticmethod
    def theoretical_estimate(
        parameters: Dict[str, Union[float, Any]], cdf: np.ndarray
    ) -> np.ndarray:
        """theporeticalEstimate.

        TheporeticalEstimate method calculates the theoretical values based on the Gumbel distribution

        Parameters:
        -----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        cdf: [list]
            cummulative distribution function/ Non Exceedence probability.

        Return:
        -------
        theoreticalvalue : [numeric]
            Value based on the theoretical distribution
        """
        pass

    def ks(self) -> tuple:
        """Kolmogorov-Smirnov (KS) test.

        The smaller the D static the more likely that the two samples are drawn from the same distribution
        IF Pvalue < signeficance level ------ reject

        returns:
        --------
        Dstatic: [numeric]
            The smaller the D static the more likely that the two samples are drawn from the same distribution
        Pvalue : [numeric]
            IF Pvalue < signeficance level ------ reject the null hypotethis
        """
        if self.parameters is None:
            raise ValueError(
                "Value of parameters is unknown please use "
                "'EstimateParameter' to obtain estimate the distribution parameters"
            )
        Qth = self.theoretical_estimate(self.parameters, self.cdf_Weibul)

        test = ks_2samp(self.data, Qth)
        self.Dstatic = test.statistic
        self.KS_Pvalue = test.pvalue

        print("-----KS Test--------")
        print(f"Statistic = {test.statistic}")
        if self.Dstatic < self.KStable:
            print("Accept Hypothesis")
        else:
            print("reject Hypothesis")
        print(f"P value = {test.pvalue}")
        return test.statistic, test.pvalue

    def chisquare(self) -> tuple:
        """

        Returns
        -------

        """
        if self.parameters is None:
            raise ValueError(
                "Value of loc/scale parameter is unknown please use "
                "'EstimateParameter' to obtain them"
            )

        Qth = self.theoretical_estimate(self.parameters, self.cdf_Weibul)
        try:
            test = chisquare(st.standardize(Qth), st.standardize(self.data))
            self.chistatic = test.statistic
            self.chi_Pvalue = test.pvalue
            print("-----chisquare Test-----")
            print("Statistic = " + str(test.statistic))
            print("P value = " + str(test.pvalue))
            return test.statistic, test.pvalue
        except Exception as e:
            print(e)
            return

    def confidence_interval(
        self,
        parameters: Dict[str, Union[float, Any]],
        F: np.ndarray,
        alpha: float = 0.1,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """confidenceInterval.

        Parameters:
        -----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        F : [list]
            Non Exceedence probability
        alpha : [numeric]
            alpha or SignificanceLevel is a value of the confidence interval.

        Return:
        -------
        parameters: Dict[str, str]
            {"loc": val, "scale": val, "shape": value}
            - loc: [numeric]
                location parameter
            - scale: [numeric]
                scale parameter
        Qupper : [list]
            upper bound coresponding to the confidence interval.
        Qlower : [list]
            lower bound coresponding to the confidence interval.
        """
        pass

    def probapility_plot(
        self,
        parameters: Dict[str, Union[float, Any]],
        F: np.ndarray,
        alpha: float = 0.1,
        fig1size: tuple = (10, 5),
        fig2size: tuple = (6, 6),
        xlabel: str = "Actual data",
        ylabel: str = "cdf",
        fontsize: int = 15,
    ) -> Tuple[List[Figure], list]:
        """probapilityPlot.

        ProbapilityPlot method calculates the theoretical values based on the Gumbel distribution
        parameters, theoretical cdf (or weibul), and calculate the confidence interval.

        Parameters
        ----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        F : [np.ndarray]
            theoretical cdf calculated using weibul or using the distribution cdf function.
        alpha : [float]
            value between 0 and 1.
        fig1size: [tuple]
            Default is (10, 5)
        fig2size: [tuple]
            Default is (6, 6)
        xlabel: [str]
            Default is "Actual data"
        ylabel: [str]
            Default is "cdf"
        fontsize: [float]
            Default is 15.

        Returns
        -------
        Qth : [list]
            theoretical generated values based on the theoretical cdf calculated from
            weibul or the distribution parameters.
        Qupper : [list]
            upper bound coresponding to the confidence interval.
        Qlower : [list]
            lower bound coresponding to the confidence interval.
        """
        pass


class Gumbel(AbstractDistribution):
    """Gumbel distribution."""

    cdf_Weibul: ndarray
    parameters: dict[str, Union[float, Any]]
    data: ndarray

    def __init__(
        self,
        data: Union[list, np.ndarray] = None,
        parameters: Dict[str, str] = None,
    ):
        """Gumbel.

        Parameters
        ----------
        data : [list]
            data time series.
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        """
        super().__init__(data, parameters)
        pass

    @staticmethod
    def _pdf_eq(
        data: Union[list, np.ndarray], parameters: Dict[str, Union[float, Any]]
    ) -> np.ndarray:
        loc = parameters.get("loc")
        scale = parameters.get("scale")
        if scale <= 0:
            raise ValueError("Scale parameter is negative")
        # z = (ts - loc) / scale
        # pdf = (1.0 / scale) * (np.exp(-(z + (np.exp(-z)))))
        pdf = gumbel_r.pdf(data, loc=loc, scale=scale)
        return pdf

    def pdf(
        self,
        parameters: Dict[str, Union[float, Any]],
        plot_figure: bool = False,
        figsize: tuple = (6, 5),
        xlabel: str = "Actual data",
        ylabel: str = "pdf",
        fontsize: Union[float, int] = 15,
        actual_data: np.ndarray = None,
    ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
        """pdf.

        Returns the value of Gumbel's pdf with parameters loc and scale at x .

        Parameters:
        -----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.

        Returns
        -------
        pdf : [array]
            probability density function pdf.
        """
        ts = super().pdf(parameters, actual_data=actual_data)

        pdf = self._pdf_eq(ts, parameters)

        if plot_figure:
            Qx = np.linspace(
                float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
            )
            pdf_fitted = self.pdf(parameters, actual_data=Qx)

            fig, ax = Plot.pdf(
                Qx,
                pdf_fitted,
                self.data_sorted,
                figsize=figsize,
                xlabel=xlabel,
                ylabel=ylabel,
                fontsize=fontsize,
            )
            return pdf, fig, ax
        else:
            return pdf

    @staticmethod
    def _cdf_eq(
        data: Union[list, np.ndarray], parameters: Dict[str, Union[float, Any]]
    ) -> np.ndarray:
        loc = parameters.get("loc")
        scale = parameters.get("scale")
        if scale <= 0:
            raise ValueError("Scale parameter is negative")
        # z = (ts - loc) / scale
        # cdf = np.exp(-np.exp(-z))
        cdf = gumbel_r.cdf(data, loc=loc, scale=scale)
        return cdf

    def cdf(
        self,
        parameters: Dict[str, Union[float, Any]],
        plot_figure: bool = False,
        figsize: tuple = (6, 5),
        xlabel: str = "data",
        ylabel: str = "cdf",
        fontsize: int = 15,
        actual_data: Union[bool, np.ndarray] = True,
    ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
        """cdf.

        cdf calculates the value of Gumbel's cdf with parameters loc and scale at x.

        parameter:
        ----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        """
        if isinstance(actual_data, bool):
            ts = self.data
        else:
            ts = actual_data

        cdf = self._cdf_eq(ts, parameters)

        if plot_figure:
            Qx = np.linspace(
                float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
            )
            cdf_fitted = self.cdf(parameters, actual_data=Qx)

            cdf_Weibul = PlottingPosition.weibul(self.data_sorted)

            fig, ax = Plot.cdf(
                Qx,
                cdf_fitted,
                self.data_sorted,
                cdf_Weibul,
                figsize=figsize,
                xlabel=xlabel,
                ylabel=ylabel,
                fontsize=fontsize,
            )

            return cdf, fig, ax
        else:
            return cdf

    def get_rp(self, loc, scale, data):
        """getRP.

            getRP calculates the return period for a list/array of values or a single value.

        Parameters
        ----------
        data:[list/array/float]
            value you want the coresponding return value for
        loc: [float]
            location parameter
        scale: [float]
            scale parameter

        Returns
        -------
        float:
            return period
        """
        # if isinstance(data, list) or isinstance(data, np.ndarray):
        cdf = self.cdf(loc, scale, actual_data=data)
        # else:
        #     cdf = gumbel_r.cdf(data, loc, scale)

        rp = 1 / (1 - cdf)

        return rp

    @staticmethod
    def ObjectiveFn(p, x):
        """ObjectiveFn.

        Link : https://stackoverflow.com/questions/23217484/how-to-find-parameters-of-gumbels-distribution-using-scipy-optimize
        Parameters
        ----------
        p:
        x:
        """
        threshold = p[0]
        loc = p[1]
        scale = p[2]

        x1 = x[x < threshold]
        nx2 = len(x[x >= threshold])
        # pdf with a scaled pdf
        # L1 is pdf based
        parameters = {"loc": loc, "scale": scale}
        pdf = Gumbel._pdf_eq(x1, parameters)
        cdf = Gumbel._cdf_eq(threshold, parameters)
        L1 = (-np.log((pdf / scale))).sum()
        # L2 is cdf based
        L2 = (-np.log(1 - cdf)) * nx2
        # print x1, nx2, L1, L2
        return L1 + L2

    def estimate_parameter(
        self,
        method: str = "mle",
        ObjFunc: Callable = None,
        threshold: Union[None, float, int] = None,
        test: bool = True,
    ) -> Dict[str, str]:
        """estimate_parameter.

        EstimateParameter estimate the distribution parameter based on MLM
        (Maximum liklihood method), if an objective function is entered as an input

        There are two likelihood functions (L1 and L2), one for values above some
        threshold (x>=C) and one for values below (x < C), now the likeliest parameters
        are those at the max value of mutiplication between two functions max(L1*L2).

        In this case the L1 is still the product of multiplication of probability
        density function's values at xi, but the L2 is the probability that threshold
        value C will be exceeded (1-F(C)).

        Parameters
        ----------
        ObjFunc : [function]
            function to be used to get the distribution parameters.
        threshold : [numeric]
            Value you want to consider only the greater values.
        method : [string]
            'mle', 'mm', 'lmoments', optimization
        test: [bool]
            Default is True.

        Returns
        -------
        Dict[str, str]:
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        """
        # obj_func = lambda p, x: (-np.log(Gumbel.pdf(x, p[0], p[1]))).sum()
        # #first we make a simple Gumbel fit
        # Par1 = so.fmin(obj_func, [0.5,0.5], args=(np.array(data),))
        method = method.lower()
        if method not in ["mle", "mm", "lmoments", "optimization"]:
            raise ValueError(
                f"{method} value should be 'mle', 'mm', 'lmoments' or 'optimization'"
            )
        if method == "mle" or method == "mm":
            Param = list(gumbel_r.fit(self.data, method=method))
        elif method == "lmoments":
            LM = Lmoments(self.data)
            LMU = LM.Lmom()
            Param = Lmoments.gumbel(LMU)
        elif method == "optimization":
            if ObjFunc is None or threshold is None:
                raise TypeError("threshold should be numeric value")

            Param = gumbel_r.fit(self.data, method="mle")
            # then we use the result as starting value for your truncated Gumbel fit
            Param = so.fmin(
                ObjFunc,
                [threshold, Param[0], Param[1]],
                args=(self.data,),
                maxiter=500,
                maxfun=500,
            )
            Param = [Param[1], Param[2]]

        Param = {"loc": Param[0], "scale": Param[1]}
        self.parameters = Param

        if test:
            self.ks()
            self.chisquare()

        return Param

    @staticmethod
    def theoretical_estimate(
        parameters: Dict[str, Union[float, Any]], cdf: np.ndarray
    ) -> np.ndarray:
        """theporeticalEstimate.

        TheporeticalEstimate method calculates the theoretical values based on the Gumbel distribution

        Parameters:
        -----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        cdf: [list]
            cummulative distribution function/ Non Exceedence probability.

        Return:
        -------
        theoreticalvalue : [numeric]
            Value based on the theoretical distribution
        """
        loc = parameters.get("loc")
        scale = parameters.get("scale")

        if scale <= 0:
            raise ValueError("Scale parameter is negative")

        if any(cdf) <= 0 or any(cdf) > 1:
            raise ValueError("cdf Value Invalid")

        cdf = np.array(cdf)
        Qth = loc - scale * (np.log(-np.log(cdf)))

        # the main equation form scipy
        # Qth = gumbel_r.ppf(F, loc=loc, scale=scale)
        return Qth

    def ks(self) -> tuple:
        """Kolmogorov-Smirnov (KS) test.

        The smaller the D static the more likely that the two samples are drawn from the same distribution
        IF Pvalue < signeficance level ------ reject

        returns:
        --------
        Dstatic: [numeric]
            The smaller the D static the more likely that the two samples are drawn from the same distribution
        Pvalue : [numeric]
            IF Pvalue < signeficance level ------ reject the null hypotethis
        """
        return super().ks()

    def chisquare(self) -> tuple:
        """

        Returns
        -------

        """
        return super().chisquare()

    def confidence_interval(
        self,
        parameters: Dict[str, Union[float, Any]],
        F: np.ndarray,
        alpha: float = 0.1,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """confidenceInterval.

        Parameters:
        -----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        F : [list]
            Non Exceedence probability
        alpha : [numeric]
            alpha or SignificanceLevel is a value of the confidence interval.

        Return:
        -------
        parameters: Dict[str, str]
            {"loc": val, "scale": val, "shape": value}
            - loc: [numeric]
                location parameter
            - scale: [numeric]
                scale parameter
        Qupper : [list]
            upper bound coresponding to the confidence interval.
        Qlower : [list]
            lower bound coresponding to the confidence interval.
        """
        scale = parameters.get("scale")

        if scale <= 0:
            raise ValueError("Scale parameter is negative")

        Qth = self.theoretical_estimate(parameters, F)
        Y = [-np.log(-np.log(j)) for j in F]
        StdError = [
            (scale / np.sqrt(len(self.data)))
            * np.sqrt(1.1087 + 0.5140 * j + 0.6079 * j**2)
            for j in Y
        ]
        v = norm.ppf(1 - alpha / 2)
        Qupper = np.array([Qth[j] + v * StdError[j] for j in range(len(self.data))])
        Qlower = np.array([Qth[j] - v * StdError[j] for j in range(len(self.data))])
        return Qupper, Qlower

    def probapility_plot(
        self,
        parameters: Dict[str, Union[float, Any]],
        F: np.ndarray,
        alpha: float = 0.1,
        fig1size: tuple = (10, 5),
        fig2size: tuple = (6, 6),
        xlabel: str = "Actual data",
        ylabel: str = "cdf",
        fontsize: int = 15,
    ) -> Tuple[List[Figure], list]:
        """probapilityPlot.

        ProbapilityPlot method calculates the theoretical values based on the Gumbel distribution
        parameters, theoretical cdf (or weibul), and calculate the confidence interval.

        Parameters
        ----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        F : [np.ndarray]
            theoretical cdf calculated using weibul or using the distribution cdf function.
        alpha : [float]
            value between 0 and 1.
        fig1size: [tuple]
            Default is (10, 5)
        fig2size: [tuple]
            Default is (6, 6)
        xlabel: [str]
            Default is "Actual data"
        ylabel: [str]
            Default is "cdf"
        fontsize: [float]
            Default is 15.

        Returns
        -------
        Qth : [list]
            theoretical generated values based on the theoretical cdf calculated from
            weibul or the distribution parameters.
        Qupper : [list]
            upper bound coresponding to the confidence interval.
        Qlower : [list]
            lower bound coresponding to the confidence interval.
        """
        scale = parameters.get("scale")

        if scale <= 0:
            raise ValueError("Scale parameter is negative")

        Qth = self.theoretical_estimate(parameters, F)
        Qupper, Qlower = self.confidence_interval(parameters, F, alpha)

        Qx = np.linspace(
            float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
        )
        pdf_fitted = self.pdf(parameters, actual_data=Qx)
        cdf_fitted = self.cdf(parameters, actual_data=Qx)

        fig, ax = Plot.details(
            Qx,
            Qth,
            self.data,
            pdf_fitted,
            cdf_fitted,
            F,
            Qlower,
            Qupper,
            alpha,
            fig1size=fig1size,
            fig2size=fig2size,
            xlabel=xlabel,
            ylabel=ylabel,
            fontsize=fontsize,
        )

        return fig, ax


class GEV(AbstractDistribution):
    """GEV (Genalized Extreme value statistics)"""

    parameters: dict[str, Union[float, Any]]
    data: ndarray

    def __init__(
        self,
        data: Union[list, np.ndarray] = None,
        parameters: Dict[str, str] = None,
    ):
        """GEV.

        Parameters
        ----------
        data : [list]
            data time series.

        parameters: Dict[str, str]
            {"loc": val, "scale": val, "shape": value}
            - loc: [numeric]
                location parameter of the GEV distribution.
            - scale: [numeric]
                scale parameter of the GEV distribution.
            - shape: [numeric]
                shape parameter of the GEV distribution.
        """
        super().__init__(data, parameters)
        pass

    @staticmethod
    def _pdf_eq(
        data: Union[list, np.ndarray], parameters: Dict[str, Union[float, Any]]
    ) -> np.ndarray:
        loc = parameters.get("loc")
        scale = parameters.get("scale")
        shape = parameters.get("shape")
        # pdf = []
        # for ts_i in ts:
        #     z = (ts_i - loc) / scale
        #
        #     # Gumbel
        #     if shape == 0:
        #         val = np.exp(-(z + np.exp(-z)))
        #         pdf.append((1 / scale) * val)
        #         continue
        #
        #     # GEV
        #     y = 1 - shape * z
        #     if y > ninf:
        #         # np.log(y) = ln(y)
        #         # ln is the inverse of e
        #         lnY = (-1 / shape) * np.log(y)
        #         val = np.exp(-(1 - shape) * lnY - np.exp(-lnY))
        #         pdf.append((1 / scale) * val)
        #         continue
        #
        #     if shape < 0:
        #         pdf.append(0)
        #         continue
        #     pdf.append(0)
        #
        # if len(pdf) == 1:
        #     pdf = pdf[0]

        # pdf = np.array(pdf)
        pdf = genextreme.pdf(data, loc=loc, scale=scale, c=shape)
        return pdf

    def pdf(
        self,
        parameters: Dict[str, Union[float, Any]],
        plot_figure: bool = False,
        figsize: tuple = (6, 5),
        xlabel: str = "Actual data",
        ylabel: str = "pdf",
        fontsize: int = 15,
        actual_data: np.ndarray = None,
    ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
        """pdf.

        Returns the value of GEV's pdf with parameters loc and scale at x .

        Parameters
        ----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val, "shape": value}
            - loc: [numeric]
                location parameter of the GEV distribution.
            - scale: [numeric]
                scale parameter of the GEV distribution.
            - shape: [numeric]
                shape parameter of the GEV distribution.
        plot_figure: [bool]
            Default is False.
        figsize: [tuple]
            Default is (6, 5).
        xlabel: [str]
            Default is "Actual data".
        ylabel: [str]
            Default is "pdf".
        fontsize: [int]
            Default is 15.
        actual_data : [bool/array]
            true if you want to calculate the pdf for the actual time series, array
            if you want to calculate the pdf for a theoretical time series

        Returns
        -------
        TYPE
            DESCRIPTION.
        """
        ts = super().pdf(parameters, actual_data=actual_data)
        pdf = self._pdf_eq(ts, parameters)

        if plot_figure:
            Qx = np.linspace(
                float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
            )
            pdf_fitted = self.pdf(parameters, actual_data=Qx)

            fig, ax = Plot.pdf(
                Qx,
                pdf_fitted,
                self.data_sorted,
                figsize=figsize,
                xlabel=xlabel,
                ylabel=ylabel,
                fontsize=fontsize,
            )
            return pdf, fig, ax
        else:
            return pdf

    @staticmethod
    def _cdf_eq(
        data: Union[list, np.ndarray], parameters: Dict[str, Union[float, Any]]
    ) -> np.ndarray:
        loc = parameters.get("loc")
        scale = parameters.get("scale")
        shape = parameters.get("shape")
        # equation https://www.rdocumentation.org/packages/evd/versions/2.3-6/topics/fextreme
        # z = (ts - loc) / scale
        # if shape == 0:
        #     # GEV is Gumbel distribution
        #     cdf = np.exp(-np.exp(-z))
        # else:
        #     y = 1 - shape * z
        #     cdf = list()
        #     for y_i in y:
        #         if y_i > ninf:
        #             logY = -np.log(y_i) / shape
        #             cdf.append(np.exp(-np.exp(-logY)))
        #         elif shape < 0:
        #             cdf.append(0)
        #         else:
        #             cdf.append(1)
        #
        # cdf = np.array(cdf)
        cdf = genextreme.cdf(data, c=shape, loc=loc, scale=scale)
        return cdf

    def cdf(
        self,
        parameters: Dict[str, Union[float, Any]],
        plot_figure: bool = False,
        figsize: tuple = (6, 5),
        xlabel: str = "Actual data",
        ylabel: str = "cdf",
        fontsize: int = 11,
        actual_data: Union[bool, np.ndarray] = True,
    ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
        """cdf.

        Returns the value of Gumbel's cdf with parameters loc and scale
        at x.
        """
        # loc = parameters.get("loc")
        scale = parameters.get("scale")
        # shape = parameters.get("shape")

        if scale <= 0:
            raise ValueError("Scale parameter is negative")

        if isinstance(actual_data, bool):
            ts = self.data
        else:
            ts = actual_data

        cdf = self._cdf_eq(ts, parameters)

        if plot_figure:
            Qx = np.linspace(
                float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
            )
            cdf_fitted = self.cdf(parameters, actual_data=Qx)

            cdf_Weibul = PlottingPosition.weibul(self.data_sorted)

            fig, ax = Plot.cdf(
                Qx,
                cdf_fitted,
                self.data_sorted,
                cdf_Weibul,
                figsize=figsize,
                xlabel=xlabel,
                ylabel=ylabel,
                fontsize=fontsize,
            )
            return cdf, fig, ax
        else:
            return cdf

    def get_rp(self, shape: float, loc: float, scale: float, data: np.ndarray):
        """getRP.

            getRP calculates the return period for a list/array of values or a single value.

        Parameters
        ----------
        data:[list/array/float]
            value you want the coresponding return value for
        shape: [float]
            shape parameter
        loc: [float]
            location parameter
        scale: [float]
            scale parameter

        Returns
        -------
        float:
            return period
        """
        # if isinstance(data, list) or isinstance(data, np.ndarray):
        cdf = self.cdf(shape, loc, scale, actual_data=data)
        # else:
        #     cdf = genextreme.cdf(data, shape, loc, scale)

        rp = 1 / (1 - cdf)

        return rp

    def estimate_parameter(
        self,
        method: str = "mle",
        ObjFunc=None,
        threshold: Union[int, float, None] = None,
        test: bool = True,
    ) -> Dict[str, Any]:
        """estimateParameter.

        EstimateParameter estimate the distribution parameter based on MLM
        (Maximum liklihood method), if an objective function is entered as an input

        There are two likelihood functions (L1 and L2), one for values above some
        threshold (x>=C) and one for values below (x < C), now the likeliest parameters
        are those at the max value of mutiplication between two functions max(L1*L2).

        In this case the L1 is still the product of multiplication of probability
        density function's values at xi, but the L2 is the probability that threshold
        value C will be exceeded (1-F(C)).

        Parameters
        ----------
        ObjFunc : [function]
            function to be used to get the distribution parameters.
        threshold : [numeric]
            Value you want to consider only the greater values.
        method : [string]
            'mle', 'mm', 'lmoments', optimization
        test: bool
            Default is True

        Returns
        -------
        Param : [list]
            shape, loc, scale parameter of the gumbel distribution in that order.
        """
        # obj_func = lambda p, x: (-np.log(Gumbel.pdf(x, p[0], p[1]))).sum()
        # #first we make a simple Gumbel fit
        # Par1 = so.fmin(obj_func, [0.5,0.5], args=(np.array(data),))
        method = method.lower()
        if method not in ["mle", "mm", "lmoments", "optimization"]:
            raise ValueError(
                method + "value should be 'mle', 'mm', 'lmoments' or 'optimization'"
            )
        if method == "mle" or method == "mm":
            Param = list(genextreme.fit(self.data, method=method))
        elif method == "lmoments":
            LM = Lmoments(self.data)
            LMU = LM.Lmom()
            Param = Lmoments.gev(LMU)
        elif method == "optimization":
            if ObjFunc is None or threshold is None:
                raise TypeError("ObjFunc and threshold should be numeric value")

            Param = genextreme.fit(self.data, method="mle")
            # then we use the result as starting value for your truncated Gumbel fit
            Param = so.fmin(
                ObjFunc,
                [threshold, Param[0], Param[1], Param[2]],
                args=(self.data,),
                maxiter=500,
                maxfun=500,
            )
            Param = [Param[1], Param[2], Param[3]]

        Param = {"loc": Param[1], "scale": Param[2], "shape": Param[0]}
        self.parameters = Param

        if test:
            self.ks()
            try:
                self.chisquare()
            except ValueError:
                print("chisquare test failed")

        return Param

    @staticmethod
    def theoretical_estimate(
        parameters: Dict[str, Union[float, Any]],
        F: np.ndarray,
    ) -> np.ndarray:
        """TheporeticalEstimate.

        TheporeticalEstimate method calculates the theoretical values based on a given  non exceedence probability

        Parameters:
        -----------
        param : [list]
            location ans scale parameters of the gumbel distribution.
        F : [list]
            cummulative distribution function/ Non Exceedence probability.

        Return:
        -------
        theoreticalvalue : [numeric]
            Value based on the theoretical distribution
        """
        loc = parameters.get("loc")
        scale = parameters.get("scale")
        shape = parameters.get("shape")

        if scale <= 0:
            raise ValueError("Parameters Invalid")

        if any(F) < 0 or any(F) > 1:
            raise ValueError("cdf Value Invalid")

        # Qth = list()
        # for i in range(len(F)):
        #     if F[i] <= 0 or F[i] >= 1:
        #         if F[i] == 0 and shape < 0:
        #             Qth.append(loc + scale / shape)
        #         elif F[i] == 1 and shape > 0:
        #             Qth.append(loc + scale / shape)
        #         else:
        #             raise ValueError(str(F[i]) + " value of cdf is Invalid")
        #     # F = np.array(F)
        #     Y = -np.log(-np.log(F[i]))
        #     if shape != 0:
        #         Y = (1 - np.exp(-1 * shape * Y)) / shape
        #
        #     Qth.append(loc + scale * Y)
        # Qth = np.array(Qth)
        # the main equation from scipy
        Qth = genextreme.ppf(F, shape, loc=loc, scale=scale)
        return Qth

    def ks(self):
        """Kolmogorov-Smirnov (KS) test.

        The smaller the D static the more likely that the two samples are drawn from the same distribution
        IF Pvalue < signeficance level ------ reject

        returns:
        --------
            Dstatic: [numeric]
                The smaller the D static the more likely that the two samples are drawn from the same distribution
            Pvalue : [numeric]
                IF Pvalue < signeficance level ------ reject the null hypotethis
        """
        return super().ks()

    def chisquare(self):
        return super().chisquare()

    def confidence_interval(
        self,
        parameters: Dict[str, Union[float, Any]],
        F: np.ndarray,
        alpha: float = 0.1,
        statfunction=np.average,
        n_samples: int = 100,
        method: str = "lmoments",
        **kargs,
    ):
        """confidenceInterval.

        Parameters:
        -----------
        loc : [numeric]
            location parameter of the gumbel distribution.
        scale : [numeric]
            scale parameter of the gumbel distribution.
        F : [list]
            Non Exceedence probability
        alpha : [numeric]
            alpha or SignificanceLevel is a value of the confidence interval.
        statfunction: [callable]
            Default is np.average.
        n_samples: [int]
            number of samples generated by the bootstrap method Default is 100.
        method: [str]
            method used to fit the generated samples from the bootstrap method ["lmoments", "mle", "mm"]. Default is
            "lmoments".

        Return:
        -------
        Qupper : [list]
            upper bound coresponding to the confidence interval.
        Qlower : [list]
            lower bound coresponding to the confidence interval.
        """
        scale = parameters.get("scale")
        if scale <= 0:
            raise ValueError("Scale parameter is negative")

        CI = ConfidenceInterval.BootStrap(
            self.data,
            statfunction=statfunction,
            gevfit=parameters,
            F=F,
            alpha=alpha,
            n_samples=n_samples,
            method=method,
            **kargs,
        )
        Qlower = CI["LB"]
        Qupper = CI["UB"]

        return Qupper, Qlower

    def probapility_plot(
        self,
        parameters: Dict[str, Union[float, Any]],
        F,
        alpha=0.1,
        func=None,
        method: str = "lmoments",
        n_samples=100,
        fig1size=(10, 5),
        fig2size=(6, 6),
        xlabel="Actual data",
        ylabel="cdf",
        fontsize=15,
    ):
        """probapilityPlot.

        ProbapilityPlot method calculates the theoretical values based on the Gumbel distribution
        parameters, theoretical cdf (or weibul), and calculate the confidence interval.

        Parameters
        ----------
        loc : [numeric]
            Location parameter of the GEV distribution.
        scale : [numeric]
            Scale parameter of the GEV distribution.
        shape: [float, int]
            Shape parameter for the GEV distribution.
        F : [list]
            Theoretical cdf calculated using weibul or using the distribution cdf function.
        method: [str]
            Method used to fit the generated samples from the bootstrap method ["lmoments", "mle", "mm"]. Default is
            "lmoments".
        alpha : [float]
            Value between 0 and 1.
        fontsize : [numeric]
            Font size of the axis labels and legend
        ylabel : [string]
            y label string
        xlabel : [string]
            X label string
        fig1size : [tuple]
            size of the pdf and cdf figure
        fig2size : [tuple]
            size of the confidence interval figure
        n_samples : [integer]
            number of points in the condidence interval calculation
        alpha : [numeric]
            alpha or SignificanceLevel is a value of the confidence interval.
        func : [function]
            function to be used in the confidence interval calculation.
        """
        loc = parameters.get("loc")
        scale = parameters.get("scale")
        shape = parameters.get("shape")

        if scale <= 0:
            raise ValueError("Scale parameter is negative")

        Qth = self.theoretical_estimate(parameters, F)
        if func is None:
            func = GEV.ci_func

        Param_dist = [shape, loc, scale]
        CI = ConfidenceInterval.BootStrap(
            self.data,
            statfunction=func,
            gevfit=Param_dist,
            n_samples=n_samples,
            F=F,
            method=method,
        )
        Qlower = CI["LB"]
        Qupper = CI["UB"]

        Qx = np.linspace(
            float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
        )
        pdf_fitted = self.pdf(shape, loc, scale, actual_data=Qx)
        cdf_fitted = self.cdf(shape, loc, scale, actual_data=Qx)

        fig, ax = Plot.details(
            Qx,
            Qth,
            self.data,
            pdf_fitted,
            cdf_fitted,
            F,
            Qlower,
            Qupper,
            alpha,
            fig1size=fig1size,
            fig2size=fig2size,
            xlabel=xlabel,
            ylabel=ylabel,
            fontsize=fontsize,
        )

        return fig, ax

        # The function to bootstrap

    @staticmethod
    def ci_func(data: Union[list, np.ndarray], **kwargs):
        """GEV distribution function.

        Parameters
        ----------
        data: [list, np.ndarray]
            time series
        kwargs:
            - gevfit: [list]
                GEV parameter [shape, location, scale]
            - F: [list]
                Non Exceedence probability
            - method: [str]
                method used to fit the generated samples from the bootstrap method ["lmoments", "mle", "mm"]. Default is
                "lmoments".
        """
        gevfit = kwargs["gevfit"]
        F = kwargs["F"]
        method = kwargs["method"]
        # generate theoretical estimates based on a random cdf, and the dist parameters
        sample = GEV.theoretical_estimate(gevfit, np.random.rand(len(data)))

        # get parameters based on the new generated sample
        Gdist = GEV(sample)
        new_param = Gdist.estimate_parameter(method=method, test=False)

        # return period
        # T = np.arange(0.1, 999.1, 0.1) + 1
        # +1 in order not to make 1- 1/0.1 = -9
        # T = np.linspace(0.1, 999, len(data)) + 1
        # coresponding theoretical estimate to T
        # F = 1 - 1 / T
        Qth = GEV.theoretical_estimate(new_param, F)

        res = list(new_param.values())
        res.extend(Qth)
        return tuple(res)


# class Frechet:
#
#     """
#     f(x: threshold, scale) = (1/scale) e **(- (x-threshold)/scale)
#
#     """
#
#     def __init__(
#         self,
#         data: Union[list, np.ndarray] = None,
#         loc: Union[int, float] = None,
#         scale: Union[int, float] = None,
#     ):
#         """Gumbel.
#
#         Parameters
#         ----------
#         data : [list]
#             data time series.
#         loc: [numeric]
#             location parameter
#         scale: [numeric]
#             scale parameter
#         """
#         if isinstance(data, list) or isinstance(data, np.ndarray):
#             self.data = np.array(data)
#             self.data_sorted = np.sort(data)
#             self.cdf_Weibul = PlottingPosition.weibul(data)
#             self.KStable = 1.22 / np.sqrt(len(self.data))
#
#         self.loc = loc
#         self.scale = scale
#         self.Dstatic = None
#         self.KS_Pvalue = None
#         self.chistatic = None
#         self.chi_Pvalue = None
#
#     def pdf(
#         self,
#         loc: Union[float, int],
#         scale: Union[float, int],
#         plot_figure: bool = False,
#         figsize: tuple = (6, 5),
#         xlabel: str = "Actual data",
#         ylabel: str = "pdf",
#         fontsize: Union[float, int] = 15,
#         actual_data: Union[bool, np.ndarray] = True,
#     ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
#         """pdf.
#
#         Returns the value of Gumbel's pdf with parameters loc and scale at x .
#
#         Parameters:
#         -----------
#         loc : [numeric]
#             location parameter of the gumbel distribution.
#         scale : [numeric]
#             scale parameter of the gumbel distribution.
#
#         Returns
#         -------
#         pdf : [array]
#             probability density function pdf.
#         """
#         if scale <= 0:
#             raise ValueError("Scale parameter is negative")
#
#         if isinstance(actual_data, bool):
#             ts = self.data
#         else:
#             ts = actual_data
#
#         # pdf = []
#         #
#         # for i in ts:
#         #     Y = (i - loc) / scale
#         #     if Y <= 0:
#         #         pdf.append(0)
#         #     else:
#         #         pdf.append(np.exp(-Y) / scale)
#         #
#         # if len(pdf) == 1:
#         #     pdf = pdf[0]
#
#         pdf = expon.pdf(ts, loc=loc, scale=scale)
#         if plot_figure:
#             Qx = np.linspace(
#                 float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
#             )
#             pdf_fitted = self.pdf(loc, scale, actual_data=Qx)
#
#             fig, ax = Plot.pdf(
#                 Qx,
#                 pdf_fitted,
#                 self.data_sorted,
#                 figsize=figsize,
#                 xlabel=xlabel,
#                 ylabel=ylabel,
#                 fontsize=fontsize,
#             )
#             return pdf, fig, ax
#         else:
#             return pdf
#
#     def cdf(
#         self,
#         loc: Union[float, int],
#         scale: Union[float, int],
#         plot_figure: bool = False,
#         figsize: tuple = (6, 5),
#         xlabel: str = "data",
#         ylabel: str = "cdf",
#         fontsize: int = 15,
#         actual_data: Union[bool, np.ndarray] = True,
#     ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
#         """cdf.
#
#         cdf calculates the value of Gumbel's cdf with parameters loc and scale at x.
#
#         parameter:
#         ----------
#         loc : [numeric]
#             location parameter of the gumbel distribution.
#         scale : [numeric]
#             scale parameter of the gumbel distribution.
#         """
#         if scale <= 0:
#             raise ValueError("Scale parameter is negative")
#         if loc <= 0:
#             raise ValueError("Threshold parameter should be greater than zero")
#
#         if isinstance(actual_data, bool):
#             ts = self.data
#         else:
#             ts = actual_data
#
#         # Y = (ts - loc) / scale
#         # cdf = 1 - np.exp(-Y)
#         #
#         # for i in range(0, len(cdf)):
#         #     if cdf[i] < 0:
#         #         cdf[i] = 0
#         cdf = expon.cdf(ts, loc=loc, scale=scale)
#
#         if plot_figure:
#             Qx = np.linspace(
#                 float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
#             )
#             cdf_fitted = self.cdf(loc, scale, actual_data=Qx)
#
#             cdf_Weibul = PlottingPosition.weibul(self.data_sorted)
#
#             fig, ax = Plot.cdf(
#                 Qx,
#                 cdf_fitted,
#                 self.data_sorted,
#                 cdf_Weibul,
#                 figsize=figsize,
#                 xlabel=xlabel,
#                 ylabel=ylabel,
#                 fontsize=fontsize,
#             )
#
#             return cdf, fig, ax
#         else:
#             return cdf
#
#     def estimateParameter(
#         self,
#         method: str = "mle",
#         ObjFunc=None,
#         threshold: Union[int, float, None] = None,
#         test: bool = True,
#     ) -> tuple:
#         """estimateParameter.
#
#         EstimateParameter estimate the distribution parameter based on MLM
#         (Maximum liklihood method), if an objective function is entered as an input
#
#         There are two likelihood functions (L1 and L2), one for values above some
#         threshold (x>=C) and one for values below (x < C), now the likeliest parameters
#         are those at the max value of mutiplication between two functions max(L1*L2).
#
#         In this case the L1 is still the product of multiplication of probability
#         density function's values at xi, but the L2 is the probability that threshold
#         value C will be exceeded (1-F(C)).
#
#         Parameters
#         ----------
#         ObjFunc : [function]
#             function to be used to get the distribution parameters.
#         threshold : [numeric]
#             Value you want to consider only the greater values.
#         method : [string]
#             'mle', 'mm', 'lmoments', optimization
#         test: bool
#             Default is True
#
#         Returns
#         -------
#         Param : [list]
#             shape, loc, scale parameter of the gumbel distribution in that order.
#         """
#         # obj_func = lambda p, x: (-np.log(Gumbel.pdf(x, p[0], p[1]))).sum()
#         # #first we make a simple Gumbel fit
#         # Par1 = so.fmin(obj_func, [0.5,0.5], args=(np.array(data),))
#         method = method.lower()
#         if method not in ["mle", "mm", "lmoments", "optimization"]:
#             raise ValueError(
#                 method + "value should be 'mle', 'mm', 'lmoments' or 'optimization'"
#             )
#
#         if method == "mle" or method == "mm":
#             Param = list(expon.fit(self.data, method=method))
#         elif method == "lmoments":
#             LM = Lmoments(self.data)
#             LMU = LM.Lmom()
#             Param = Lmoments.gev(LMU)
#         elif method == "optimization":
#             if ObjFunc is None or threshold is None:
#                 raise TypeError("ObjFunc and threshold should be numeric value")
#
#             Param = expon.fit(self.data, method="mle")
#             # then we use the result as starting value for your truncated Gumbel fit
#             Param = so.fmin(
#                 ObjFunc,
#                 [threshold, Param[0], Param[1]],
#                 args=(self.data,),
#                 maxiter=500,
#                 maxfun=500,
#             )
#             Param = [Param[1], Param[2]]
#
#         self.loc = Param[0]
#         self.scale = Param[1]
#
#         if test:
#             self.ks()
#             try:
#                 self.chisquare()
#             except ValueError:
#                 print("chisquare test failed")
#
#         return Param
#
#     @staticmethod
#     def theporeticalEstimate(
#         loc: Union[float, int],
#         scale: Union[float, int],
#         F: np.ndarray,
#     ) -> np.ndarray:
#         """TheporeticalEstimate.
#
#         TheporeticalEstimate method calculates the theoretical values based on a given  non exceedence probability
#
#         Parameters:
#         -----------
#         param : [list]
#             location ans scale parameters of the gumbel distribution.
#         F : [list]
#             cummulative distribution function/ Non Exceedence probability.
#
#         Return:
#         -------
#         theoreticalvalue : [numeric]
#             Value based on the theoretical distribution
#         """
#         if scale <= 0:
#             raise ValueError("Parameters Invalid")
#
#         if any(F) < 0 or any(F) > 1:
#             raise ValueError("cdf Value Invalid")
#
#         # the main equation from scipy
#         Qth = expon.ppf(F, loc=loc, scale=scale)
#         return Qth


class Exponential(AbstractDistribution):
    """
    f(x: threshold, scale) = (1/scale) e **(- (x-threshold)/scale)
    """

    def __init__(
        self,
        data: Union[list, np.ndarray] = None,
        parameters: Dict[str, str] = None,
    ):
        """Exponential Distribution.

        Parameters
        ----------
        data : [list]
            data time series.
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the exponential distribution.
            - scale: [numeric]
                scale parameter of the exponential distribution.
        """
        super().__init__(data, parameters)

    @staticmethod
    def _pdf_eq(
        data: Union[list, np.ndarray], parameters: Dict[str, Union[float, Any]]
    ) -> np.ndarray:
        loc = parameters.get("loc")
        scale = parameters.get("scale")
        # pdf = []
        #
        # for i in ts:
        #     Y = (i - loc) / scale
        #     if Y <= 0:
        #         pdf.append(0)
        #     else:
        #         pdf.append(np.exp(-Y) / scale)
        #
        # if len(pdf) == 1:
        #     pdf = pdf[0]

        pdf = expon.pdf(data, loc=loc, scale=scale)
        return pdf

    def pdf(
        self,
        parameters: Dict[str, Union[float, Any]],
        plot_figure: bool = False,
        figsize: tuple = (6, 5),
        xlabel: str = "Actual data",
        ylabel: str = "pdf",
        fontsize: Union[float, int] = 15,
        actual_data: np.ndarray = None,
    ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
        """pdf.

        Returns the value of Gumbel's pdf with parameters loc and scale at x .

        Parameters:
        -----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.

        Returns
        -------
        pdf : [array]
            probability density function pdf.
        """
        scale = parameters.get("scale")

        if scale <= 0:
            raise ValueError("Scale parameter is negative")

        ts = super().pdf(parameters, actual_data=actual_data)

        pdf = self._pdf_eq(ts, parameters)

        if plot_figure:
            Qx = np.linspace(
                float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
            )
            pdf_fitted = self.pdf(parameters, actual_data=Qx)

            fig, ax = Plot.pdf(
                Qx,
                pdf_fitted,
                self.data_sorted,
                figsize=figsize,
                xlabel=xlabel,
                ylabel=ylabel,
                fontsize=fontsize,
            )
            return pdf, fig, ax
        else:
            return pdf

    @staticmethod
    def _cdf_eq(
        data: Union[list, np.ndarray], parameters: Dict[str, Union[float, Any]]
    ) -> np.ndarray:
        loc = parameters.get("loc")
        scale = parameters.get("scale")
        if scale <= 0:
            raise ValueError("Scale parameter is negative")
        if loc <= 0:
            raise ValueError("Threshold parameter should be greater than zero")
        # Y = (ts - loc) / scale
        # cdf = 1 - np.exp(-Y)
        #
        # for i in range(0, len(cdf)):
        #     if cdf[i] < 0:
        #         cdf[i] = 0
        cdf = expon.cdf(data, loc=loc, scale=scale)
        return cdf

    def cdf(
        self,
        parameters: Dict[str, Union[float, Any]],
        plot_figure: bool = False,
        figsize: tuple = (6, 5),
        xlabel: str = "data",
        ylabel: str = "cdf",
        fontsize: int = 15,
        actual_data: Union[bool, np.ndarray] = True,
    ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
        """cdf.

        cdf calculates the value of Gumbel's cdf with parameters loc and scale at x.

        parameter:
        ----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        """
        if isinstance(actual_data, bool):
            ts = self.data
        else:
            ts = actual_data

        cdf = self._cdf_eq(ts, parameters)

        if plot_figure:
            Qx = np.linspace(
                float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
            )
            cdf_fitted = self.cdf(parameters, actual_data=Qx)

            cdf_Weibul = PlottingPosition.weibul(self.data_sorted)

            fig, ax = Plot.cdf(
                Qx,
                cdf_fitted,
                self.data_sorted,
                cdf_Weibul,
                figsize=figsize,
                xlabel=xlabel,
                ylabel=ylabel,
                fontsize=fontsize,
            )

            return cdf, fig, ax
        else:
            return cdf

    def estimate_parameter(
        self,
        method: str = "mle",
        ObjFunc=None,
        threshold: Union[int, float, None] = None,
        test: bool = True,
    ) -> tuple:
        """estimateParameter.

        EstimateParameter estimate the distribution parameter based on MLM
        (Maximum liklihood method), if an objective function is entered as an input

        There are two likelihood functions (L1 and L2), one for values above some
        threshold (x>=C) and one for values below (x < C), now the likeliest parameters
        are those at the max value of mutiplication between two functions max(L1*L2).

        In this case the L1 is still the product of multiplication of probability
        density function's values at xi, but the L2 is the probability that threshold
        value C will be exceeded (1-F(C)).

        Parameters
        ----------
        ObjFunc : [function]
            function to be used to get the distribution parameters.
        threshold : [numeric]
            Value you want to consider only the greater values.
        method : [string]
            'mle', 'mm', 'lmoments', optimization
        test: bool
            Default is True

        Returns
        -------
        Param : [list]
            shape, loc, scale parameter of the gumbel distribution in that order.
        """
        # obj_func = lambda p, x: (-np.log(Gumbel.pdf(x, p[0], p[1]))).sum()
        # #first we make a simple Gumbel fit
        # Par1 = so.fmin(obj_func, [0.5,0.5], args=(np.array(data),))
        method = method.lower()
        if method not in ["mle", "mm", "lmoments", "optimization"]:
            raise ValueError(
                method + "value should be 'mle', 'mm', 'lmoments' or 'optimization'"
            )

        if method == "mle" or method == "mm":
            Param = list(expon.fit(self.data, method=method))
        elif method == "lmoments":
            LM = Lmoments(self.data)
            LMU = LM.Lmom()
            Param = Lmoments.exponential(LMU)
        elif method == "optimization":
            if ObjFunc is None or threshold is None:
                raise TypeError("ObjFunc and threshold should be numeric value")

            Param = expon.fit(self.data, method="mle")
            # then we use the result as starting value for your truncated Gumbel fit
            Param = so.fmin(
                ObjFunc,
                [threshold, Param[0], Param[1]],
                args=(self.data,),
                maxiter=500,
                maxfun=500,
            )
            Param = [Param[1], Param[2]]

        Param = {"loc": Param[0], "scale": Param[1]}
        self.parameters = Param

        if test:
            self.ks()
            try:
                self.chisquare()
            except ValueError:
                print("chisquare test failed")

        return Param

    @staticmethod
    def theoretical_estimate(
        parameters: Dict[str, Union[float, Any]],
        cdf: np.ndarray,
    ) -> np.ndarray:
        """TheporeticalEstimate.

        TheporeticalEstimate method calculates the theoretical values based on a given  non exceedence probability

        Parameters:
        -----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the gumbel distribution.
            - scale: [numeric]
                scale parameter of the gumbel distribution.
        cdf: [list]
            cummulative distribution function/ Non Exceedence probability.

        Return:
        -------
        theoreticalvalue : [numeric]
            Value based on the theoretical distribution
        """
        loc = parameters.get("loc")
        scale = parameters.get("scale")

        if scale <= 0:
            raise ValueError("Parameters Invalid")

        if any(cdf) < 0 or any(cdf) > 1:
            raise ValueError("cdf Value Invalid")

        # the main equation from scipy
        Qth = expon.ppf(cdf, loc=loc, scale=scale)
        return Qth

    def ks(self):
        """Kolmogorov-Smirnov (KS) test.

        The smaller the D static the more likely that the two samples are drawn from the same distribution
        IF Pvalue < signeficance level ------ reject

        returns:
        --------
            Dstatic: [numeric]
                The smaller the D static the more likely that the two samples are drawn from the same distribution
            Pvalue : [numeric]
                IF Pvalue < signeficance level ------ reject the null hypotethis
        """
        return super().ks()

    def chisquare(self):
        return super().chisquare()


class Normal(AbstractDistribution):
    """
    f(x: threshold, scale) = (1/scale) e **(- (x-threshold)/scale)
    """

    def __init__(
        self,
        data: Union[list, np.ndarray] = None,
        loc: Union[int, float] = None,
        scale: Union[int, float] = None,
    ):
        """Gumbel.

        Parameters
        ----------
        data : [list]
            data time series.
        loc: [numeric]
            location parameter
        scale: [numeric]
            scale parameter
        """
        if isinstance(data, list) or isinstance(data, np.ndarray):
            self.data = np.array(data)
            self.data_sorted = np.sort(data)
            self.cdf_Weibul = PlottingPosition.weibul(data)
            self.KStable = 1.22 / np.sqrt(len(self.data))

        self.loc = loc
        self.scale = scale
        self.Dstatic = None
        self.KS_Pvalue = None
        self.chistatic = None
        self.chi_Pvalue = None

    def pdf(
        self,
        parameters: Dict[str, Union[float, Any]],
        plot_figure: bool = False,
        figsize: tuple = (6, 5),
        xlabel: str = "Actual data",
        ylabel: str = "pdf",
        fontsize: Union[float, int] = 15,
        actual_data: np.ndarray = None,
    ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
        """pdf.

        Returns the value of Gumbel's pdf with parameters loc and scale at x .

        Parameters:
        -----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val, "shape": value}
            - loc: [numeric]
                location parameter of the GEV distribution.
            - scale: [numeric]
                scale parameter of the GEV distribution.

        Returns
        -------
        pdf : [array]
            probability density function pdf.
        """
        loc = parameters.get("loc")
        scale = parameters.get("scale")

        if scale <= 0:
            raise ValueError("Scale parameter is negative")

        ts = super().pdf(parameters, actual_data=actual_data)

        pdf = norm.pdf(ts, loc=loc, scale=scale)
        if plot_figure:
            Qx = np.linspace(
                float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
            )
            pdf_fitted = self.pdf(parameters, actual_data=Qx)

            fig, ax = Plot.pdf(
                Qx,
                pdf_fitted,
                self.data_sorted,
                figsize=figsize,
                xlabel=xlabel,
                ylabel=ylabel,
                fontsize=fontsize,
            )
            return pdf, fig, ax
        else:
            return pdf

    def cdf(
        self,
        parameters: Dict[str, Union[float, Any]],
        plot_figure: bool = False,
        figsize: tuple = (6, 5),
        xlabel: str = "data",
        ylabel: str = "cdf",
        fontsize: int = 15,
        actual_data: Union[bool, np.ndarray] = True,
    ) -> Union[Tuple[np.ndarray, Figure, Any], np.ndarray]:
        """cdf.

        cdf calculates the value of Normal distribution cdf with parameters loc and scale at x.

        parameter:
        ----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val, "shape": value}
            - loc: [numeric]
                location parameter of the Normal distribution.
            - scale: [numeric]
                scale parameter of the Normal distribution.
        """
        loc = parameters.get("loc")
        scale = parameters.get("scale")

        if scale <= 0:
            raise ValueError("Scale parameter is negative")
        if loc <= 0:
            raise ValueError("Threshold parameter should be greater than zero")

        if isinstance(actual_data, bool):
            ts = self.data
        else:
            ts = actual_data

        cdf = norm.cdf(ts, loc=loc, scale=scale)

        if plot_figure:
            Qx = np.linspace(
                float(self.data_sorted[0]), 1.5 * float(self.data_sorted[-1]), 10000
            )
            cdf_fitted = self.cdf(parameters, actual_data=Qx)

            cdf_Weibul = PlottingPosition.weibul(self.data_sorted)

            fig, ax = Plot.cdf(
                Qx,
                cdf_fitted,
                self.data_sorted,
                cdf_Weibul,
                figsize=figsize,
                xlabel=xlabel,
                ylabel=ylabel,
                fontsize=fontsize,
            )

            return cdf, fig, ax
        else:
            return cdf

    def estimate_parameter(
        self,
        method: str = "mle",
        ObjFunc=None,
        threshold: Union[int, float, None] = None,
        test: bool = True,
    ) -> tuple:
        """estimateParameter.

        EstimateParameter estimate the distribution parameter based on MLM
        (Maximum liklihood method), if an objective function is entered as an input

        There are two likelihood functions (L1 and L2), one for values above some
        threshold (x>=C) and one for values below (x < C), now the likeliest parameters
        are those at the max value of mutiplication between two functions max(L1*L2).

        In this case the L1 is still the product of multiplication of probability
        density function's values at xi, but the L2 is the probability that threshold
        value C will be exceeded (1-F(C)).

        Parameters
        ----------
        ObjFunc : [function]
            function to be used to get the distribution parameters.
        threshold : [numeric]
            Value you want to consider only the greater values.
        method : [string]
            'mle', 'mm', 'lmoments', optimization
        test: bool
            Default is True

        Returns
        -------
        Param : [list]
            shape, loc, scale parameter of the gumbel distribution in that order.
        """
        # obj_func = lambda p, x: (-np.log(Gumbel.pdf(x, p[0], p[1]))).sum()
        # #first we make a simple Gumbel fit
        # Par1 = so.fmin(obj_func, [0.5,0.5], args=(np.array(data),))
        method = method.lower()
        if method not in ["mle", "mm", "lmoments", "optimization"]:
            raise ValueError(
                method + "value should be 'mle', 'mm', 'lmoments' or 'optimization'"
            )

        if method == "mle" or method == "mm":
            Param = list(norm.fit(self.data, method=method))
        elif method == "lmoments":
            LM = Lmoments(self.data)
            LMU = LM.Lmom()
            Param = Lmoments.normal(LMU)
        elif method == "optimization":
            if ObjFunc is None or threshold is None:
                raise TypeError("ObjFunc and threshold should be numeric value")

            Param = norm.fit(self.data, method="mle")
            # then we use the result as starting value for your truncated Gumbel fit
            Param = so.fmin(
                ObjFunc,
                [threshold, Param[0], Param[1]],
                args=(self.data,),
                maxiter=500,
                maxfun=500,
            )
            Param = [Param[1], Param[2]]

        Param = {"loc": Param[0], "scale": Param[1]}
        self.parameters = Param

        if test:
            self.ks()
            try:
                self.chisquare()
            except ValueError:
                print("chisquare test failed")

        return Param

    @staticmethod
    def theoretical_estimate(
        parameters: Dict[str, Union[float, Any]],
        cdf: np.ndarray,
    ) -> np.ndarray:
        """TheporeticalEstimate.

        TheporeticalEstimate method calculates the theoretical values based on a given  non exceedence probability

        Parameters:
        -----------
        parameters: Dict[str, str]
            {"loc": val, "scale": val}
            - loc: [numeric]
                location parameter of the Normal distribution.
            - scale: [numeric]
                scale parameter of the Normal distribution.
        cdf: [list]
            cummulative distribution function/ Non Exceedence probability.

        Return:
        -------
        numeric:
            Value based on the theoretical distribution
        """
        loc = parameters.get("loc")
        scale = parameters.get("scale")

        if scale <= 0:
            raise ValueError("Parameters Invalid")

        if any(cdf) < 0 or any(cdf) > 1:
            raise ValueError("cdf Value Invalid")

        # the main equation from scipy
        Qth = norm.ppf(cdf, loc=loc, scale=scale)
        return Qth
