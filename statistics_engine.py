"""
Statistical Engine Module
Provides comprehensive statistical analysis functions
"""

import numpy as np
from scipy import stats
from typing import List, Dict, Tuple, Optional
import pandas as pd


class DescriptiveStats:
    """Calculate descriptive statistics for datasets"""
    
    @staticmethod
    def calculate_all(data: List[float]) -> Dict[str, float]:
        """Calculate all descriptive statistics"""
        data_array = np.array(data)
        
        return {
            'count': len(data),
            'mean': np.mean(data_array),
            'median': np.median(data_array),
            'mode': stats.mode(data_array, keepdims=True)[0][0] if len(data) > 0 else None,
            'std_dev': np.std(data_array, ddof=1),
            'variance': np.var(data_array, ddof=1),
            'min': np.min(data_array),
            'max': np.max(data_array),
            'range': np.max(data_array) - np.min(data_array),
            'q1': np.percentile(data_array, 25),
            'q2': np.percentile(data_array, 50),
            'q3': np.percentile(data_array, 75),
            'iqr': np.percentile(data_array, 75) - np.percentile(data_array, 25),
            'skewness': stats.skew(data_array),
            'kurtosis': stats.kurtosis(data_array)
        }
    
    @staticmethod
    def format_results(stats_dict: Dict[str, float]) -> str:
        """Format statistics as readable string"""
        output = "Descriptive Statistics:\n" + "="*50 + "\n"
        for key, value in stats_dict.items():
            if value is not None:
                output += f"{key.replace('_', ' ').title()}: {value:.4f}\n"
        return output


class CorrelationAnalysis:
    """Perform correlation analysis"""
    
    @staticmethod
    def pearson(x: List[float], y: List[float]) -> Tuple[float, float]:
        """Calculate Pearson correlation coefficient and p-value"""
        return stats.pearsonr(x, y)
    
    @staticmethod
    def spearman(x: List[float], y: List[float]) -> Tuple[float, float]:
        """Calculate Spearman correlation coefficient and p-value"""
        return stats.spearmanr(x, y)
    
    @staticmethod
    def correlation_matrix(data: pd.DataFrame) -> pd.DataFrame:
        """Calculate correlation matrix for DataFrame"""
        return data.corr()


class RegressionAnalysis:
    """Perform regression analysis"""
    
    @staticmethod
    def linear_regression(x: List[float], y: List[float]) -> Dict[str, any]:
        """
        Perform simple linear regression
        Returns slope, intercept, r_value, p_value, std_err
        """
        x_array = np.array(x)
        y_array = np.array(y)
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_array, y_array)
        
        # Calculate predictions and residuals
        y_pred = slope * x_array + intercept
        residuals = y_array - y_pred
        
        return {
            'slope': slope,
            'intercept': intercept,
            'r_value': r_value,
            'r_squared': r_value ** 2,
            'p_value': p_value,
            'std_err': std_err,
            'equation': f"y = {slope:.4f}x + {intercept:.4f}",
            'predictions': y_pred.tolist(),
            'residuals': residuals.tolist()
        }


class HypothesisTesting:
    """Perform various hypothesis tests"""
    
    @staticmethod
    def one_sample_ttest(data: List[float], popmean: float) -> Dict[str, float]:
        """One-sample t-test"""
        t_stat, p_value = stats.ttest_1samp(data, popmean)
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    @staticmethod
    def two_sample_ttest(data1: List[float], data2: List[float], equal_var: bool = True) -> Dict[str, float]:
        """Independent two-sample t-test"""
        t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=equal_var)
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    @staticmethod
    def paired_ttest(data1: List[float], data2: List[float]) -> Dict[str, float]:
        """Paired t-test"""
        t_stat, p_value = stats.ttest_rel(data1, data2)
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    @staticmethod
    def chi_square_test(observed: List[float], expected: Optional[List[float]] = None) -> Dict[str, float]:
        """Chi-square goodness of fit test"""
        chi_stat, p_value = stats.chisquare(observed, expected)
        return {
            'chi_square': chi_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    @staticmethod
    def anova(*groups) -> Dict[str, float]:
        """One-way ANOVA"""
        f_stat, p_value = stats.f_oneway(*groups)
        return {
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }


class ProbabilityDistributions:
    """Work with probability distributions"""
    
    @staticmethod
    def normal_pdf(x: float, mean: float = 0, std: float = 1) -> float:
        """Normal distribution PDF"""
        return stats.norm.pdf(x, loc=mean, scale=std)
    
    @staticmethod
    def normal_cdf(x: float, mean: float = 0, std: float = 1) -> float:
        """Normal distribution CDF"""
        return stats.norm.cdf(x, loc=mean, scale=std)
    
    @staticmethod
    def binomial_pmf(k: int, n: int, p: float) -> float:
        """Binomial distribution PMF"""
        return stats.binom.pmf(k, n, p)
    
    @staticmethod
    def poisson_pmf(k: int, mu: float) -> float:
        """Poisson distribution PMF"""
        return stats.poisson.pmf(k, mu)
    
    @staticmethod
    def generate_normal_sample(size: int, mean: float = 0, std: float = 1) -> List[float]:
        """Generate random sample from normal distribution"""
        return stats.norm.rvs(loc=mean, scale=std, size=size).tolist()


class OutlierDetection:
    """Detect outliers in data"""
    
    @staticmethod
    def iqr_method(data: List[float], multiplier: float = 1.5) -> Dict[str, any]:
        """Detect outliers using IQR method"""
        data_array = np.array(data)
        q1 = np.percentile(data_array, 25)
        q3 = np.percentile(data_array, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr
        
        outliers = data_array[(data_array < lower_bound) | (data_array > upper_bound)]
        
        return {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outliers': outliers.tolist(),
            'outlier_count': len(outliers),
            'outlier_indices': np.where((data_array < lower_bound) | (data_array > upper_bound))[0].tolist()
        }
    
    @staticmethod
    def z_score_method(data: List[float], threshold: float = 3.0) -> Dict[str, any]:
        """Detect outliers using Z-score method"""
        data_array = np.array(data)
        z_scores = np.abs(stats.zscore(data_array))
        outliers = data_array[z_scores > threshold]
        
        return {
            'threshold': threshold,
            'outliers': outliers.tolist(),
            'outlier_count': len(outliers),
            'outlier_indices': np.where(z_scores > threshold)[0].tolist()
        }
