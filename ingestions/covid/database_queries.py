class DatabaseQuery():

    @staticmethod
    def create_covid_record_table():
        return """
            CREATE TABLE IF NOT EXISTS tbl_covid_records (
                record_id SERIAL PRIMARY KEY,
                fips INTEGER,
                admin2 VARCHAR(255),
                province_state_id INTEGER,
                country_region_id INTEGER,
                last_update TIMESTAMP,
                latitude DECIMAL,
                longitude DECIMAL,
                confirmed INTEGER,
                deaths INTEGER,
                recovered INTEGER,
                active INTEGER,
                combined_key VARCHAR(255),
                incident_rate DECIMAL,
                case_fatality_ratio DECIMAL,
                CONSTRAINT fk_province_state FOREIGN KEY (province_state_id) REFERENCES lu_province_state(province_state_id),
                CONSTRAINT fk_country_region FOREIGN KEY (country_region_id) REFERENCES lu_country_region(country_region_id)
            );
        """

    @staticmethod
    def insert_covid_record():
        return """
            INSERT INTO tbl_covid_records 
                (fips, admin2, province_state_id, country_region_id, last_update, latitude, longitude, confirmed, deaths, recovered, active, combined_key, incident_rate, case_fatality_ratio) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

    @staticmethod
    def drop_covid_records_table():
        return """
            DROP TABLE IF EXISTS tbl_covid_records;
        """

    @staticmethod
    def drop_province_state_table():
        return """
            DROP TABLE IF EXISTS lu_province_state;
        """
    
    @staticmethod
    def drop_country_region_table():
        return """
            DROP TABLE IF EXISTS lu_country_region;
        """
    
    @staticmethod
    def create_province_state_table():
        return """
            CREATE TABLE IF NOT EXISTS lu_province_state (
                province_state_id SERIAL PRIMARY KEY,
                province_state VARCHAR(255),
                CONSTRAINT unq_province_state UNIQUE (province_state)
            );
        """

    @staticmethod
    def create_country_region_table():
        return """
            CREATE TABLE IF NOT EXISTS lu_country_region (
                    country_region_id SERIAL PRIMARY KEY,
                    country_region VARCHAR(255),
                    CONSTRAINT unq_country_region UNIQUE (country_region)
            );
        """

    @staticmethod
    def select_all_from_table(table_name):
        return f"""
            SELECT * FROM {table_name};
        """

    @staticmethod
    def upsert_into_province_state_table():
        return """
            INSERT INTO lu_province_state (province_state)
            VALUES (%s) ON CONFLICT ON CONSTRAINT unq_province_state 
            DO UPDATE SET province_state = EXCLUDED.province_state RETURNING province_state_id;
        """
    
    @staticmethod
    def upsert_into_country_region_table():
        return """
            INSERT INTO lu_country_region (country_region) 
            VALUES (%s) ON CONFLICT ON CONSTRAINT unq_country_region 
            DO UPDATE SET country_region = EXCLUDED.country_region RETURNING country_region_id;
        """
