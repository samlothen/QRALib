# src/QRALib/utils/importer.py
# -------------------------------
import csv
import json
import pandas as pd
import uuid
from typing import Dict, List, Any

from ..risk.model import Risk
from ..distributions.beta import Beta
from ..distributions.uniform import Uniform
from ..distributions.lognormal import Lognormal
from ..distributions.pert import PERT

# Distribution registry for easy extension
_DIST_REGISTRY: Dict[str, Any] = {
    "Beta": Beta,
    "Uniform": Uniform,
    "Lognormal": Lognormal,
    "PERT": PERT,
}

class RiskDataImporter:
    @staticmethod
    def import_risks(file_path: str) -> List[Risk]:
        """
        Read a file (CSV, JSON, XLSX) and return a list of Risk instances.

        Automatically generates a UUID if no ID is provided in the source data.

        Parameters
        ----------
        file_path : str
            Path to input data file.

        Returns
        -------
        List[Risk]
            List of instantiated Risk objects.

        Raises
        ------
        ValueError
            If file format is unsupported or data is invalid.
        """
        raw = RiskDataImporter._read_raw(file_path)
        risks: List[Risk] = []
        for rd in raw.get("Risks", []):
            # Generate an ID if missing or empty
            if not rd.get("ID"):
                rd["ID"] = str(uuid.uuid4())

            # Validate structure
            _validate_raw_risk(rd)

            uid = rd["ID"]
            name = rd.get("name", "")

            # Build frequency distribution
            freq_info = rd["frequency"]
            freq_group = freq_info.get("distribution", "")
            freq_model = RiskDataImporter._build_distribution(freq_info)

            # Build impact distribution
            imp_info = rd["impact"]
            imp_group = imp_info.get("distribution", "")
            imp_model = RiskDataImporter._build_distribution(imp_info)

            risks.append(
                Risk(uid, name, freq_group, freq_model, imp_group, imp_model)
            )
        return risks

    @staticmethod
    def _read_raw(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        ext = file_path.lower().rsplit('.', 1)[-1]
        if ext == 'csv':
            return RiskDataImporter._import_csv(file_path)
        elif ext == 'json':
            return RiskDataImporter._import_json(file_path)
        elif ext in ('xlsx', 'xls'):
            return RiskDataImporter._import_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    @staticmethod
    def _import_csv(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        data: Dict[str, List[Dict[str, Any]]] = {"Risks": []}
        with open(file_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data["Risks"].append(_normalize_row(row))
        return data

    @staticmethod
    def _import_json(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def _import_excel(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        df = pd.read_excel(file_path, dtype=str)
        data: Dict[str, List[Dict[str, Any]]] = {"Risks": []}
        for _, row in df.iterrows():
            data["Risks"].append(_normalize_row(row.to_dict()))
        return data

    @staticmethod
    def _build_distribution(info: Dict[str, Any]) -> Any:
        """
        Instantiate a distribution object based on raw info.
        """
        dist_name = info.get("distribution")
        DistClass = _DIST_REGISTRY.get(dist_name)
        if not DistClass:
            raise ValueError(f"Unknown distribution: {dist_name}")
        params = info.get("parameters", {})
        return DistClass(**params)


def _normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a flat CSV/Excel row into the nested structure expected by importer.
    """
    rd = {
        "ID": row.get("ID", ""),
        "name": row.get("name", ""),
        "frequency": {"distribution": row.get("frequency_distribution", ""), "parameters": {}},
        "impact": {"distribution": row.get("impact_distribution",     ""), "parameters": {}},
    }
    # Map frequency params based on distribution
    freq_dist = rd["frequency"]["distribution"]
    freq_params = rd["frequency"]["parameters"]
    if freq_dist == "Beta":
        freq_params["alpha"] = float(row.get("frequency_parameter0", 0))
        freq_params["beta"]  = float(row.get("frequency_parameter1", 0))
    elif freq_dist == "Uniform":
        freq_params["low_bound"]  = float(row.get("frequency_parameter0", 0))
        freq_params["up_bound"] = float(row.get("frequency_parameter1", 0))
    elif freq_dist == "Lognormal":
        # Lognormal frequency not typical, but support if present
        freq_params["low_bound"]    = float(row.get("frequency_parameter0", 0))
        freq_params["up_bound"] = float(row.get("frequency_parameter1", 0))
    elif freq_dist == "PERT":
        freq_params["minimum"]  = float(row.get("frequency_parameter0", 0))
        freq_params["mid"]  = float(row.get("frequency_parameter1", 0))
        freq_params["maximum"] = float(row.get("frequency_parameter2", 0))

    # Map impact params based on distribution
    imp_dist = rd["impact"]["distribution"]
    imp_params = rd["impact"]["parameters"]
    if imp_dist == "Beta":
        imp_params["alpha"] = float(row.get("impact_parameter0", 0))
        imp_params["beta"]  = float(row.get("impact_parameter1", 0))
    elif imp_dist == "Uniform":
        imp_params["low_bound"]  = float(row.get("impact_parameter0", 0))
        imp_params["up_bound"] = float(row.get("impact_parameter1", 0))
    elif imp_dist == "Lognormal":
        imp_params["low_bound"]    = float(row.get("impact_parameter0", 0))
        imp_params["up_bound"] = float(row.get("impact_parameter1", 0))
    elif imp_dist == "PERT":
        imp_params["minimum"]  = float(row.get("impact_parameter0", 0))
        imp_params["mid"]  = float(row.get("impact_parameter1", 0))
        imp_params["maximum"] = float(row.get("impact_parameter2", 0))

    return rd


def _validate_raw_risk(rd: Dict[str, Any]):
    """
    Quick structural validation of raw risk dict.
    """
    required = {"ID", "name", "frequency", "impact"}
    missing = required - rd.keys()
    if missing:
        raise ValueError(f"Missing keys in risk data: {missing}")
