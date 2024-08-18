from typing import List, Dict

import numpy as np
import pandas as pd
from pandas import DataFrame
import pytest


@pytest.fixture(scope="module")
def time_series1() -> list:
    return pd.read_csv("examples/data/time_series1.txt", header=None)[0].tolist()


@pytest.fixture(scope="module")
def time_series2() -> list:
    return pd.read_csv("examples/data/time_series2.txt", header=None)[0].tolist()


@pytest.fixture(scope="module")
def dist_estimation_parameters() -> List[str]:
    return ["mle", "lmoments"]


@pytest.fixture(scope="module")
def generated_cdf() -> List[float]:
    return [0.1, 0.2, 0.4, 0.6, 0.8, 0.99]


@pytest.fixture(scope="module")
def gev_dist_parameters() -> Dict[str, Dict[str, float]]:
    return {
        "lmoments": {
            "loc": 16.392889171307772,
            "scale": 0.7005442761744839,
            "shape": -0.1614793298009645,
        },
        "mle": {
            "loc": 16.303264414285966,
            "scale": 0.5411914328865949,
            "shape": -0.5013795739666272,
        },
    }


@pytest.fixture(scope="module")
def gev_pdf() -> np.array:
    return np.array(
        [
            0.46686268,
            0.50674728,
            0.13568617,
            0.5171857,
            0.46290923,
            0.4572899,
            0.31771916,
            0.03121843,
            0.40982638,
            0.34582871,
            0.47538097,
            0.48229776,
            0.51992017,
            0.25731877,
            0.07774146,
            0.14318118,
            0.47520795,
            0.52563445,
            0.47327913,
            0.53154392,
            0.3007426,
            0.04651425,
            0.39390943,
            0.50145893,
            0.33531555,
            0.10824839,
            0.09175549,
        ]
    )


@pytest.fixture(scope="module")
def gev_cdf() -> np.array:
    return np.array(
        [
            0.16514997,
            0.21691403,
            0.86068789,
            0.23844545,
            0.16128652,
            0.51392107,
            0.68341415,
            0.96226777,
            0.57878182,
            0.08491463,
            0.17402306,
            0.47318641,
            0.24547473,
            0.74463972,
            0.91571458,
            0.85363809,
            0.48543756,
            0.2639041,
            0.17175803,
            0.32067829,
            0.70102732,
            0.94649051,
            0.59835005,
            0.20800819,
            0.08014869,
            0.88657059,
            0.9022544,
        ]
    )


@pytest.fixture(scope="module")
def gev_inverse_cdf() -> np.array:
    return np.array(
        [
            280.25644453,
            359.07484643,
            483.04312657,
            611.63267666,
            793.89957452,
            1476.17034852,
        ]
    )


@pytest.fixture(scope="module")
def exp_dist_parameters() -> Dict[str, Dict[str, float]]:
    return {
        "mle": {"loc": 144.0, "scale": 446.83333333333337},
        "lmoments": {"loc": 285.74807826694627, "scale": 305.0852550663871},
    }


@pytest.fixture(scope="module")
def gum_dist_parameters() -> Dict[str, Dict[str, float]]:
    return {
        "mle": {"loc": 466.1208189815563, "scale": 214.3001449633138},
        "lmoments": {"loc": 463.8040433832974, "scale": 220.0724922663106},
    }


@pytest.fixture(scope="module")
def gum_pdf() -> np.ndarray:
    return np.array(
        [
            0.0002699,
            0.00062362,
            0.00066007,
            0.00080406,
            0.00107551,
            0.00108773,
            0.00113594,
            0.00118869,
            0.0012884,
            0.00136443,
            0.00141997,
            0.00151536,
            0.00151886,
            0.00153245,
            0.00154542,
            0.00154856,
            0.00160752,
            0.00166602,
            0.00166918,
            0.00166958,
            0.00166028,
            0.00164431,
            0.00163473,
            0.00158442,
            0.00158442,
            0.00158017,
            0.00158017,
            0.00156466,
            0.00155064,
            0.00154824,
            0.00152589,
            0.00151815,
            0.00135704,
            0.00132178,
            0.00128594,
            0.00122319,
            0.00116002,
            0.00116002,
            0.00113677,
            0.00109378,
            0.00097405,
            0.00093331,
            0.00079382,
            0.00079099,
            0.00073328,
            0.00064623,
            0.0006293,
            0.00041714,
            0.00039389,
            0.00023869,
            0.00018416,
            0.00016156,
            0.00016156,
            0.00012409,
        ]
    )


@pytest.fixture(scope="module")
def gum_cdf() -> np.ndarray:
    return np.array(
        [
            0.01388876,
            0.0439083,
            0.04775908,
            0.06458624,
            0.10503254,
            0.10719578,
            0.11609119,
            0.12655328,
            0.14885964,
            0.16876461,
            0.18547596,
            0.2207432,
            0.22226031,
            0.22836314,
            0.23451909,
            0.23606609,
            0.2708187,
            0.33815079,
            0.34815705,
            0.34982644,
            0.41156915,
            0.43636163,
            0.44783903,
            0.4929493,
            0.4929493,
            0.4961139,
            0.4961139,
            0.50712133,
            0.51646753,
            0.51801697,
            0.53185153,
            0.53641763,
            0.61562948,
            0.63036359,
            0.64470648,
            0.66854451,
            0.69118511,
            0.69118511,
            0.69922382,
            0.71372206,
            0.75196207,
            0.76435904,
            0.80489541,
            0.80568781,
            0.82168757,
            0.84511655,
            0.8495807,
            0.90337148,
            0.90904737,
            0.94598445,
            0.9586031,
            0.96378174,
            0.96378174,
            0.97230356,
        ]
    )


@pytest.fixture(scope="module")
def gum_inverse_cdf() -> np.ndarray:
    return np.array(
        [15.84624901, 16.07199809, 16.45456617, 16.88993364, 17.58184473, 21.17313605]
    )


@pytest.fixture(scope="module")
def exp_pdf() -> np.ndarray:
    return np.array(
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.00326435,
            0.00317986,
            0.00308743,
            0.00291054,
            0.0027709,
            0.00266403,
            0.00246249,
            0.00245443,
            0.00242246,
            0.00239091,
            0.00238308,
            0.00221728,
            0.00193846,
            0.00190071,
            0.00189449,
            0.00167812,
            0.00159761,
            0.00156137,
            0.00142445,
            0.00142445,
            0.00141514,
            0.00141514,
            0.00138304,
            0.00135611,
            0.00135167,
            0.00131238,
            0.00129953,
            0.00108516,
            0.00104673,
            0.00100966,
            0.0009487,
            0.00089142,
            0.00089142,
            0.0008712,
            0.00083486,
            0.00073951,
            0.00070866,
            0.00060748,
            0.00060549,
            0.00056522,
            0.00050561,
            0.00049414,
            0.0003514,
            0.00033564,
            0.00022724,
            0.00018667,
            0.00016918,
            0.00016918,
            0.00013898,
        ]
    )


@pytest.fixture(scope="module")
def exp_cdf() -> np.ndarray:
    return np.array(
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.00409511,
            0.02987048,
            0.05807125,
            0.1120373,
            0.15463951,
            0.18724486,
            0.24873132,
            0.25118978,
            0.26094342,
            0.27057001,
            0.272957,
            0.32353911,
            0.40860393,
            0.42012107,
            0.42201867,
            0.48803105,
            0.51259402,
            0.52364994,
            0.56542203,
            0.56542203,
            0.56826161,
            0.56826161,
            0.57805481,
            0.58627199,
            0.58762587,
            0.59961321,
            0.60353104,
            0.66893317,
            0.68065731,
            0.69196627,
            0.71056475,
            0.72804029,
            0.72804029,
            0.7342092,
            0.74529692,
            0.77438705,
            0.78379871,
            0.81466693,
            0.81527342,
            0.82756099,
            0.8457462,
            0.84924516,
            0.89279246,
            0.89760091,
            0.9306738,
            0.94305098,
            0.94838443,
            0.94838443,
            0.95759963,
        ]
    )


@pytest.fixture(scope="module")
def exp_inverse_cdf() -> np.ndarray:
    return np.array(
        [
            317.89201806,
            353.82588554,
            441.59344399,
            565.29486992,
            776.7638543,
            1690.71759908,
        ]
    )


@pytest.fixture(scope="module")
def normal_dist_parameters() -> Dict[str, Dict[str, float]]:
    return {
        "mle": {"loc": 590.8333333333334, "scale": 269.6701517423475},
        "lmoments": {"loc": 590.8333333333334, "scale": 270.3747675984547},
    }


@pytest.fixture(scope="module")
def normal_pdf() -> np.ndarray:
    return np.array(
        [
            3.76585954e-04,
            5.55761639e-04,
            5.73125382e-04,
            6.41927252e-04,
            7.78226317e-04,
            7.84743776e-04,
            8.10920185e-04,
            8.40533721e-04,
            9.00047780e-04,
            9.49628806e-04,
            9.89058789e-04,
            1.06657670e-03,
            1.06975234e-03,
            1.08240168e-03,
            1.09496091e-03,
            1.09808586e-03,
            1.16509775e-03,
            1.27830274e-03,
            1.29327066e-03,
            1.29572025e-03,
            1.37639246e-03,
            1.40300604e-03,
            1.41411093e-03,
            1.44966678e-03,
            1.44966678e-03,
            1.45164457e-03,
            1.45164457e-03,
            1.45795977e-03,
            1.46261414e-03,
            1.46332125e-03,
            1.46879622e-03,
            1.47026369e-03,
            1.46511057e-03,
            1.45683004e-03,
            1.44620057e-03,
            1.42246642e-03,
            1.39222958e-03,
            1.39222958e-03,
            1.37953409e-03,
            1.35385335e-03,
            1.26721227e-03,
            1.23261366e-03,
            1.09391791e-03,
            1.09078491e-03,
            1.02378558e-03,
            9.12182430e-04,
            8.89014525e-04,
            5.60559129e-04,
            5.20897748e-04,
            2.50526184e-04,
            1.60940416e-04,
            1.26634169e-04,
            1.26634169e-04,
            7.55582794e-05,
        ]
    )


@pytest.fixture(scope="module")
def normal_cdf() -> np.ndarray:
    return np.array(
        [
            0.04920163,
            0.08114019,
            0.08452673,
            0.0984933,
            0.12899683,
            0.13055979,
            0.13694234,
            0.14437377,
            0.16003869,
            0.1739115,
            0.18554393,
            0.21021605,
            0.21128421,
            0.21558855,
            0.21994331,
            0.22103983,
            0.24594131,
            0.29609117,
            0.30380612,
            0.30510062,
            0.35459687,
            0.37544707,
            0.38530748,
            0.42543415,
            0.42543415,
            0.42833548,
            0.42833548,
            0.43851965,
            0.44728172,
            0.44874469,
            0.46194042,
            0.46634906,
            0.5473507,
            0.56342355,
            0.57939235,
            0.60665528,
            0.63340487,
            0.63340487,
            0.64310652,
            0.66087644,
            0.70942419,
            0.72567516,
            0.78042151,
            0.78151386,
            0.80372058,
            0.83663889,
            0.84294308,
            0.91792954,
            0.92549804,
            0.97016259,
            0.98235882,
            0.9866563,
            0.9866563,
            0.99261508,
        ]
    )


@pytest.fixture(scope="module")
def normal_inverse_cdf() -> np.ndarray:
    return np.array(
        [
            244.33412663,
            363.2801879,
            522.3346692,
            659.33199747,
            818.38647877,
            1219.81909913,
        ]
    )


@pytest.fixture(scope="module")
def dist_estimation_parameters_ks() -> str:
    return "lmoments"


@pytest.fixture(scope="module")
def confidence_interval_alpha() -> float:
    return 0.1


@pytest.fixture(scope="module")
def parameter_estimation_optimization_threshold() -> int:
    return 800  # 17


@pytest.fixture(scope="module")
def ci_cdf() -> np.ndarray:
    return np.array(
        [
            0.03571429,
            0.07142857,
            0.10714286,
            0.14285714,
            0.17857143,
            0.21428571,
            0.25,
            0.28571429,
            0.32142857,
            0.35714286,
            0.39285714,
            0.42857143,
            0.46428571,
            0.5,
            0.53571429,
            0.57142857,
            0.60714286,
            0.64285714,
            0.67857143,
            0.71428571,
            0.75,
            0.78571429,
            0.82142857,
            0.85714286,
            0.89285714,
            0.92857143,
            0.96428571,
        ]
    )


@pytest.fixture(scope="module")
def ci_param() -> Dict[str, float]:
    return {"loc": 464.825, "scale": 222.120, "shape": 0.01012}


@pytest.fixture(scope="module")
def ams_gauges() -> DataFrame:
    """AMS gauges"""
    ams = pd.read_csv(f"tests/data/ams-gauges.csv")
    ams.index = ams["date"]
    ams.drop("date", axis=1, inplace=True)
    return ams


@pytest.fixture(scope="module")
def gauges_statistical_properties() -> DataFrame:
    """AMS gauges"""
    return pd.read_csv(f"tests/data/statistical_properties.csv", index_col="id")


@pytest.fixture(scope="module")
def gauges_distribution_properties() -> DataFrame:
    """AMS gauges"""
    return pd.read_csv(f"tests/data/distribution_properties.csv", index_col="id")
