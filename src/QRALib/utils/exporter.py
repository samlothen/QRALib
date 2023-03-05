import csv
import json 

class RiskDataExporter:
    @staticmethod


    def write_csv_file(data, filename):
        with open(filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header row
            header_row = ['id', 'frequency', 'occurances', 'impact', 'single_risk_impact', 'total']
            writer.writerow(header_row)
            # Write the data rows
            for row in data['results']:
                id = row['id']
                frequency = ','.join(str(x) for x in row['frequency'])
                occurances = ','.join(str(x) for x in row['occurances'])
                impact = ','.join(str(x) for x in row['impact'])
                single_risk_impact = ','.join(str(x) for x in row['single_risk_impact'])
                total = ','.join(str(x) for x in row['total'])
                writer.writerow([id, frequency, occurances, impact, single_risk_impact, total])