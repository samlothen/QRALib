import csv
import json

def import_csv(file):
    risk_dict = {'Risks' :[] }
    with open(file, 'r') as data:  
        for line in csv.DictReader(data): 
            risk = {
                'ID' : line['ID'],
                'name' : line['name'],
                'frequency' :{'distribution' : line['frequency_distribution'], 'parameters' : {} },
                'impact' :{'distribution' : line['impact_distribution'], 'parameters' : {} }
            }
            if risk['frequency']['distribution'] == 'Beta':
                risk['frequency']['parameters']['alpha'] = float(line['frequency_parameter0'])
                risk['frequency']['parameters']['beta']  = float(line['frequency_parameter1'])
            if risk['frequency']['distribution'] == 'PERT':
                risk['frequency']['parameters']['low'] = float(line['frequency_parameter0'])
                risk['frequency']['parameters']['mean']  = float(line['frequency_parameter1'])
                risk['frequency']['parameters']['high']  = float(line['frequency_parameter2'])
            if risk['frequency']['distribution'] == 'Uniform':
                risk['frequency']['parameters']['low'] = float(line['frequency_parameter0'])
                risk['frequency']['parameters']['high']  = float(line['frequency_parameter1'])
            if risk['impact']['distribution'] == 'Lognormal':
                risk['impact']['parameters']['low'] = float(line['impact_parameter0'])
                risk['impact']['parameters']['high']  = float(line['impact_parameter1'])
            if risk['impact']['distribution'] == 'PERT':
                risk['impact']['parameters']['low'] = float(line['impact_parameter0'])
                risk['impact']['parameters']['mean']  = float(line['impact_parameter1'])
                risk['impact']['parameters']['high']  = float(line['impact_parameter2'])
            risk_dict['Risks'].append(risk)
    return risk_dict


def import_json(file):
    json_file = open(file, 'r', encoding = 'utf-8')
    risk_dict = json.load(json_file)
    json_file.close()
    return risk_dict