-- Lucidchart importable SQL schema (normalized metal levels)

CREATE TABLE states (
  abbreviation VARCHAR(2) PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE counties (
  id INTEGER PRIMARY KEY,
  code VARCHAR(5) NOT NULL,
  name VARCHAR(120) NOT NULL,
  state_abbreviation VARCHAR(2) NOT NULL,
  CONSTRAINT uq_county_code_state UNIQUE (code, state_abbreviation),
  CONSTRAINT uq_county_name_state UNIQUE (name, state_abbreviation),
  CONSTRAINT fk_counties_state FOREIGN KEY (state_abbreviation)
    REFERENCES states (abbreviation)
    ON DELETE CASCADE
);

CREATE TABLE rate_areas (
  id INTEGER PRIMARY KEY,
  state_abbreviation VARCHAR(2) NOT NULL,
  area_number INTEGER NOT NULL,
  CONSTRAINT uq_rate_area_state_number UNIQUE (state_abbreviation, area_number),
  CONSTRAINT fk_rate_areas_state FOREIGN KEY (state_abbreviation)
    REFERENCES states (abbreviation)
    ON DELETE CASCADE
);

CREATE TABLE metal_levels (
  id INTEGER PRIMARY KEY,
  name VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE plans (
  id INTEGER PRIMARY KEY,
  plan_id VARCHAR(20) NOT NULL UNIQUE,
  state_abbreviation VARCHAR(2) NOT NULL,
  rate_area_id INTEGER NOT NULL,
  metal_level_id INTEGER NOT NULL,
  rate NUMERIC(10,2) NOT NULL,
  CONSTRAINT fk_plans_state FOREIGN KEY (state_abbreviation)
    REFERENCES states (abbreviation)
    ON DELETE CASCADE,
  CONSTRAINT fk_plans_rate_area FOREIGN KEY (rate_area_id)
    REFERENCES rate_areas (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_plans_metal_level FOREIGN KEY (metal_level_id)
    REFERENCES metal_levels (id)
    ON DELETE RESTRICT
);

CREATE TABLE zip_codes (
  id INTEGER PRIMARY KEY,
  zipcode VARCHAR(5) NOT NULL,
  state_abbreviation VARCHAR(2) NOT NULL,
  county_id INTEGER NOT NULL,
  rate_area_id INTEGER NOT NULL,
  CONSTRAINT uq_zipcode_state_county UNIQUE (zipcode, state_abbreviation, county_id),
  CONSTRAINT fk_zip_codes_state FOREIGN KEY (state_abbreviation)
    REFERENCES states (abbreviation)
    ON DELETE CASCADE,
  CONSTRAINT fk_zip_codes_county FOREIGN KEY (county_id)
    REFERENCES counties (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_zip_codes_rate_area FOREIGN KEY (rate_area_id)
    REFERENCES rate_areas (id)
    ON DELETE CASCADE
);

CREATE TABLE slcsp_requests (
  id INTEGER PRIMARY KEY,
  zipcode VARCHAR(5) NOT NULL
);
