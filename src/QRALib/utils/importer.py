import csv
import json
import pandas as pd
from typing import Dict, List, Any


class RiskDataImporter:
    @staticmethod
    def import_csv(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Import risk data from a CSV file and return it as a dictionary.

        :param file_path: Path to the CSV file to import
        :type file_path: str
        :return: Dictionary containing the imported risk data
        :rtype: Dict[str, List[Dict[str, Any]]]
        """
        risk_dict = {'Risks': []}
        with open(file_path, 'r') as data:
            for line in csv.DictReader(data):
                risk = {
                    'ID': line['ID'],
                    'name': line['name'],
                    'frequency': {'distribution': line['frequency_distribution'], 'parameters': {}},
                    'impact': {'distribution': line['impact_distribution'], 'parameters': {}}
                }
                if risk['frequency']['distribution'] == 'Beta':
                    risk['frequency']['parameters']['alpha'] = float(line['frequency_parameter0'])
                    risk['frequency']['parameters']['beta'] = float(line['frequency_parameter1'])
                if risk['frequency']['distribution'] == 'PERT':
                    risk['frequency']['parameters']['low'] = float(line['frequency_parameter0'])
                    risk['frequency']['parameters']['mid'] = float(line['frequency_parameter1'])
                    risk['frequency']['parameters']['high'] = float(line['frequency_parameter2'])
                if risk['frequency']['distribution'] == 'Uniform':
                    risk['frequency']['parameters']['low'] = float(line['frequency_parameter0'])
                    risk['frequency']['parameters']['high'] = float(line['frequency_parameter1'])
                if risk['impact']['distribution'] == 'Lognormal':
                    risk['impact']['parameters']['mu'] = float(line['impact_parameter0'])
                    risk['impact']['parameters']['sigma'] = float(line['impact_parameter1'])
                if risk['impact']['distribution'] == 'PERT':
                    risk['impact']['parameters']['low'] = float(line['impact_parameter0'])
                    risk['impact']['parameters']['mid'] = float(line['impact_parameter1'])
                    risk['impact']['parameters']['high'] = float(line['impact_parameter2'])
                risk_dict['Risks'].append(risk)
        return risk_dict

    @staticmethod
    def import_json(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Import risk data from a JSON file and return it as a dictionary.

        :param file_path: Path to the JSON file to import
        :type file_path: str
        :return: Dictionary containing the imported risk data
        :rtype: Dict[str, List[Dict[str, Any]]]
        """
        with open(file_path, 'r', encoding='utf-8') as json_file:
            risk_dict = json.load(json_file)
        return risk_dict
    
    @staticmethod
    def import_excel(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Import risk data from an Excel file and return it as a dictionary.
    
        :param file_path: Path to the Excel file to import
        :type file_path: str
        :return: Dictionary containing the imported risk data
        :rtype: Dict[str, List[Dict[str, Any]]]
        """
        risk_dict = {'Risks': []}
        df = pd.read_excel(file_path, dtype=str)
        for _, row in df.iterrows():
            risk = {
                'ID': row['ID'],
                'name': row['name'],
                'frequency': {'distribution': row['frequency_distribution'], 'parameters': {}},
                'impact': {'distribution': row['impact_distribution'], 'parameters': {}}
            }
            if risk['frequency']['distribution'] == 'Beta':
                risk['frequency']['parameters']['alpha'] = float(row['frequency_parameter0'])
                risk['frequency']['parameters']['beta'] = float(row['frequency_parameter1'])
            if risk['frequency']['distribution'] == 'PERT':
                risk['frequency']['parameters']['low'] = float(row['frequency_parameter0'])
                risk['frequency']['parameters']['mid'] = float(row['frequency_parameter1'])
                risk['frequency']['parameters']['high'] = float(row['frequency_parameter2'])
            if risk['frequency']['distribution'] == 'Uniform':
                risk['frequency']['parameters']['low'] = float(row['frequency_parameter0'])
                risk['frequency']['parameters']['high'] = float(row['frequency_parameter1'])
            if risk['impact']['distribution'] == 'Lognormal':
                risk['impact']['parameters']['mu'] = float(row['impact_parameter0'])
                risk['impact']['parameters']['sigma'] = float(row['impact_parameter1'])
            if risk['impact']['distribution'] == 'PERT':
                risk['impact']['parameters']['low'] = float(row['impact_parameter0'])
                risk['impact']['parameters']['mid'] = float(row['impact_parameter1'])
                risk['impact']['parameters']['high'] = float(row['impact_parameter2'])
            risk_dict['Risks'].append(risk)
        return risk_dict