# src/QRALib/utils/importer.py
# -------------------------------
import csv
import json
import os
import uuid
from typing import Any, Dict, List

import pandas as pd

from ..risk.model import Risk
from ..distributions.beta import Beta
from ..distributions.uniform import Uniform
from ..distributions.lognormal import Lognormal
from ..distributions.pert import PERT


class RiskDataImporter:
    """
    Read a file (CSV, JSON, XLSX) and return a list of Risk instances.
    Automatically generates a UUID if no ID is provided in the source data.
    """
    # Distribution registry for easy extension
    _DIST_REGISTRY: Dict[str, Any] = {
        "Beta": Beta,
        "Uniform": Uniform,
        "Lognormal": Lognormal,
        "PERT": PERT,
    }

    @staticmethod
    def import_risks(file_path: str) -> List[Risk]:
        """
        Load risk definitions from file_path. If file_path does not exist,
        attempt to load from the examples/ directory under project root.
        """
        if not os.path.exists(file_path):
            # project root: three levels up from this file
            proj_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "..")
            )
            alt = os.path.join(proj_root, "examples", os.path.basename(file_path))
            if os.path.exists(alt):
                file_path = alt
        raw = RiskDataImporter._read_raw(file_path)
        risks: List[Risk] = []
        for rd in raw.get("Risks", []):
            if not rd.get("ID"):
                rd["ID"] = str(uuid.uuid4())
            _validate_raw_risk(rd)
            uid = rd["ID"]
            name = rd.get("name", "")
            freq_info = rd["frequency"]
            imp_info = rd["impact"]
            freq_model = RiskDataImporter._build_distribution(freq_info)
            imp_model = RiskDataImporter._build_distribution(imp_info)
            risks.append(
                Risk(
                    uid,
                    name,
                    freq_info.get("distribution", ""),
                    freq_model,
                    imp_info.get("distribution", ""),
                    imp_model,
                )
            )
        return risks

    @staticmethod
    def _read_raw(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        ext = file_path.lower().rsplit(".", 1)[-1]
        if ext == "csv":
            return RiskDataImporter._import_csv(file_path)
        if ext == "json":
            return RiskDataImporter._import_json(file_path)
        if ext in ("xlsx", "xls"):
            return RiskDataImporter._import_excel(file_path)
        raise ValueError(f"Unsupported file format: {file_path}")

    @staticmethod
    def _import_csv(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        data: Dict[str, List[Dict[str, Any]]] = {"Risks": []}
        with open(file_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data["Risks"].append(_normalize_row(row))
        return data

    @staticmethod
    def _import_json(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        with open(file_path, "r", encoding="utf-8") as f:
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
        dist_name = info.get("distribution")
        dist_cls = RiskDataImporter._DIST_REGISTRY.get(dist_name)
        if dist_cls is None:
            raise ValueError(f"Unknown distribution: {dist_name}")
        params = info.get("parameters", {})
        return dist_cls(**params)


def _normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert flat row dict into nested RiskDataImporter structure.
    """
    rd: Dict[str, Any] = {
        "ID": row.get("ID", ""),
        "name": row.get("name", ""),
        "frequency": {
            "distribution": row.get("frequency_distribution", ""),
            "parameters": {},
        },
        "impact": {
            "distribution": row.get("impact_distribution", ""),
            "parameters": {},
        },
    }
    # frequency parameters
    dist = rd["frequency"]["distribution"]
    params = rd["frequency"]["parameters"]
    if dist == "Beta":
        params["alpha"] = float(row.get("frequency_parameter0", 0))
        params["beta"] = float(row.get("frequency_parameter1", 0))
    elif dist == "Uniform":
        params["low_bound"] = float(row.get("frequency_parameter0", 0))
        params["up_bound"] = float(row.get("frequency_parameter1", 0))
    elif dist == "Lognormal":
        params["low_bound"] = float(row.get("frequency_parameter0", 0))
        params["up_bound"] = float(row.get("frequency_parameter1", 0))
    elif dist == "PERT":
        params["minimum"] = float(row.get("frequency_parameter0", 0))
        params["mid"] = float(row.get("frequency_parameter1", 0))
        params["maximum"] = float(row.get("frequency_parameter2", 0))

    # impact parameters
    dist = rd["impact"]["distribution"]
    params = rd["impact"]["parameters"]
    if dist == "Beta":
        params["alpha"] = float(row.get("impact_parameter0", 0))
        params["beta"] = float(row.get("impact_parameter1", 0))
    elif dist == "Uniform":
        params["low_bound"] = float(row.get("impact_parameter0", 0))
        params["up_bound"] = float(row.get("impact_parameter1", 0))
    elif dist == "Lognormal":
        params["low_bound"] = float(row.get("impact_parameter0", 0))
        params["up_bound"] = float(row.get("impact_parameter1", 0))
    elif dist == "PERT":
        params["minimum"] = float(row.get("impact_parameter0", 0))
        params["mid"] = float(row.get("impact_parameter1", 0))
        params["maximum"] = float(row.get("impact_parameter2", 0))
    return rd


def _validate_raw_risk(rd: Dict[str, Any]):
    required = {"ID", "name", "frequency", "impact"}
    missing = required - rd.keys()
    if missing:
        raise ValueError(f"Missing keys in risk data: {missing}")
