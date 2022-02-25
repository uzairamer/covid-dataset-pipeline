from csv import DictReader
from io import StringIO
import json
import requests
import os

import psycopg2

from ingestions.covid.constants import DATASET_URL, FIELD_MAPPING, SEEN_KEYS
from ingestions.covid.database_queries import DatabaseQuery


class CovidDatasetsIngestion:
    def __init__(self) -> None:
        self.province_state_map = {}
        self.country_region_map = {}

    def get_normalized_record(self, cursor, row):
        output_row = []
        for key, mapping in FIELD_MAPPING.items():
            value = None

            # search for the key that works for this row and apply the appropriate normalizer
            for mapping_key in mapping['keys']:
                if row.get(mapping_key):
                    value = mapping['normalizer'](row[mapping_key])
                    break
                
            if value and key == 'province_state':
                province_state_id = self.province_state_map.get(value)
                if not province_state_id:
                    cursor.execute(DatabaseQuery.upsert_into_province_state_table(), (value,))
                    province_state_id = cursor.fetchone()[0]
                output_row.append(province_state_id)
                continue
            elif value and key == 'country_region':
                country_region_id = self.country_region_map.get(value)
                if not country_region_id:
                    cursor.execute(DatabaseQuery.upsert_into_country_region_table(), (value,))
                    country_region_id = cursor.fetchone()[0]
                output_row.append(country_region_id)
                continue

            output_row.append(value)
        
        return tuple(output_row)

    def value_id_map(self, cursor, table_name):
        output_map = {}
        results = cursor.execute(DatabaseQuery.select_all_from_table(table_name))
        if not results:
            return output_map
    
        for result in results.fetchall():
            output_map[result[1]] = result[0]
        
        return output_map

    def execute(self):
        try:
            conn = psycopg2.connect(
                host="db",
                database=os.environ.get('DATASET_POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD')
            )
            conn.set_session(autocommit=True)
            cursor = conn.cursor()

            # DROP tables (for testing purpose)
            # cursor.execute(DatabaseQuery.drop_covid_records_table())
            # cursor.execute(DatabaseQuery.drop_province_state_table())
            # cursor.execute(DatabaseQuery.drop_country_region_table())

            cursor.execute(DatabaseQuery.create_country_region_table())
            cursor.execute(DatabaseQuery.create_province_state_table())
            cursor.execute(DatabaseQuery.create_covid_record_table())

            self.province_state_map = self.value_id_map(cursor, 'lu_province_state')
            self.country_region_map = self.value_id_map(cursor, 'lu_country_region')

            datasets = json.loads(requests.get(DATASET_URL).text)
            fieldnames = []
            for dataset in datasets:
                if not dataset['download_url'].endswith(".csv"):
                    print(f'Skipping url {dataset["download_url"]}')
                    continue

                csv_response = requests.get(dataset['download_url']).text

                # to create an in memory csv file rather than saving on disk
                reader = DictReader(StringIO(csv_response))
                if not fieldnames:
                    fieldnames = reader.fieldnames
                elif not all([True if f in SEEN_KEYS.keys() else False for f in reader.fieldnames]):
                    print('Actual fieldnames ', fieldnames)
                    print('Different fieldnames ', reader.fieldnames)
                    print('Skipping link ', dataset['download_url'])
                    continue

                normalized_records = []
                for index, row in enumerate(reader):
                    if index and index % 1000 == 0:
                        print(f'Ingesting {index}th rows')
                        cursor.executemany(DatabaseQuery.insert_covid_record(), normalized_records)
                        normalized_records.clear()
                    
                    normalized_records.append(self.get_normalized_record(cursor, row))
                
                if normalized_records:
                    cursor.executemany(DatabaseQuery.insert_covid_record(), normalized_records)
                                
                print('Ingested ', dataset['download_url'])
        except Exception as e:
            print(e)
            raise
        finally:
            if conn:
                conn.close()


if __name__ == '__main__':
    CovidDatasetsIngestion().execute()
