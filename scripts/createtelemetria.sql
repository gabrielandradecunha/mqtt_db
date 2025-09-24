-- Tabela principal
CREATE TABLE telemetria (
    id SERIAL PRIMARY KEY,
    unix BIGINT NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    course DOUBLE PRECISION,
    speed DOUBLE PRECISION,
    altitude INTEGER,
    pitch DOUBLE PRECISION,
    roll DOUBLE PRECISION,
    accel_magnitude DOUBLE PRECISION,
    max_delta_accel DOUBLE PRECISION,
    power_status SMALLINT,
    error_status SMALLINT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela histórica
CREATE TABLE historico_telemetria (
    id SERIAL PRIMARY KEY,
    telemetria_id INT REFERENCES telemetria(id) ON DELETE CASCADE,
    unix BIGINT NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    course DOUBLE PRECISION,
    speed DOUBLE PRECISION,
    altitude INTEGER,
    pitch DOUBLE PRECISION,
    roll DOUBLE PRECISION,
    accel_magnitude DOUBLE PRECISION,
    max_delta_accel DOUBLE PRECISION,
    power_status SMALLINT,
    error_status SMALLINT,
    data_insercao TIMESTAMP DEFAULT NOW()
);
