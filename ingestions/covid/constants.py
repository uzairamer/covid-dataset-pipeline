DATASET_URL = 'https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports'

FIELD_MAPPING = {
    "fips": {'keys': ['FIPS',], 'normalizer': lambda x: int(float(x))},
    "admin2": {'keys': ['Admin2',], 'normalizer': str},
    "province_state": {'keys': ['Province_State', 'Province/State',], 'normalizer': str},
    "country_region": {'keys': ['Country_Region', 'Country/Region',], 'normalizer': str},
    "last_update": {'keys': ['Last_Update', 'Last Update'], 'normalizer': str},
    "latitude": {'keys': ['Latitude', 'Lat'], 'normalizer': float},
    "longitude": {'keys': ['Longitude', 'Long_'], 'normalizer': float},
    "confirmed": {'keys': ['Confirmed',], 'normalizer': lambda x: int(float(x))},
    "deaths": {'keys': ['Deaths'], 'normalizer': lambda x: int(float(x))},
    "recovered": {'keys': ['Recovered'], 'normalizer': lambda x: int(float(x))},
    "active": {'keys': ['Active'], 'normalizer': lambda x: int(float(x))},
    "combined_key": {'keys': ['Combined_Key'], 'normalizer': str},
    "incident_rate": {'keys': ['Incident_Rate'], 'normalizer': float},
    "case_fatality_ratio": {'keys': ['Case_Fatality_Ratio', 'Case-Fatality_Ratio'], 'normalizer': float},
}

SEEN_KEYS = [
    'FIPS',
    'Admin2',

    'Province_State',
    'Province/State',

    'Country_Region',
    'Country/Region',

    'Last_Update',
    'Last Update',

    'Latitude',
    'Lat',

    'Longitude',
    'Long_',

    'Confirmed',
    'Deaths',
    'Recovered',
    'Active',
    'Combined_Key',
    'Incident_Rate',
    'Case_Fatality_Ratio',
    'Case-Fatality_Ratio',
]