"""Container for risk event"""
import numpy as np

class Risk:
    """Risk Model"""

    def __init__(self, uniq_id, name: str, frequency_group: str, frequency_model, impact_group: str, impact_model) -> None:
        """
        Initializes impact and frequency parameters for the risk event.

        Parameters:
        ----------
        uniq_id : str
            An uniqe identifier for the risk.
        name : str
            A descriptive name for the risk.
        frequency_group : str
            The name of the frequency distribution used.
        frequency_model : Probability distribution object used for the frequency of the risk.
        impact_group : str
            The name of the impact distribution used.
        impact_model : Probability distribution object used for the impact of the risk.
        """
        self.uniq_id = uniq_id
        self.name = name
        self.frequency_group = frequency_group
        self.frequency_model = frequency_model
        self.impact_group = impact_group
        self.impact_model = impact_model

    def get_impact(self, n: int = 1) -> np.ndarray:
        """
        Returns an array of n random samples drawn from the impact distribution.

        Parameters
        ----------
        n : int, optional
            Number of samples to generate (default is 1). Must be positive.

        Returns
        -------
        np.ndarray
            One-dimensional array of length ``n`` (dtype float) containing sampled impact values.

        Raises
        ------
        ValueError
            If ``n <= 0``.
        """
        if n <= 0:
            raise ValueError(f"Sample size n must be positive, got {n}")

        return self.impact_model.draw(n)

    def get_frequency(self, n: int = 1) -> np.ndarray:
        """
        Returns an array of n random samples drawn from the frequency distribution.

        Parameters
        ----------
        n : int, optional
            Number of samples to generate (default is 1). Must be positive.

        Returns
        -------
        np.ndarray
            One-dimensional array of length ``n`` (dtype float) containing sampled impact values.

        Raises
        ------
        ValueError
            If ``n <= 0``.
        """
        if n <= 0:
            raise ValueError(f"Sample size n must be positive, got {n}")

        return self.frequency_model.draw(n)

    def get_impact_ppf(self, n: int = 1) -> np.ndarray:
        """
        Returns an array of n samples drawn from the impact distribution using the percent point function.

        Parameters
        ----------
        n : int, optional
            Number of samples to generate (default is 1). Must be positive.

        Returns
        -------
        np.ndarray
            One-dimensional array of length ``n`` (dtype float) containing sampled impact values.

        Raises
        ------
        ValueError
            If ``n <= 0``.
        """
        if n <= 0:
            raise ValueError(f"Sample size n must be positive, got {n}")

        return self.impact_model.draw_ppf(n)

    def get_frequency_ppf(self, n: int = 1) -> np.ndarray:
        """
        Returns an array of n samples drawn from the frequency distribution using the percent point function.

        Parameters
        ----------
        n : int, optional
            Number of samples to generate (default is 1). Must be positive.

        Returns
        -------
        np.ndarray
            One-dimensional array of length ``n`` (dtype float) containing sampled impact values.

        Raises
        ------
        ValueError
            If ``n <= 0``.
        """
        if n <= 0:
            raise ValueError(f"Sample size n must be positive, got {n}")

        return self.frequency_model.draw_ppf(n)
