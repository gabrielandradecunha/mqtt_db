#!/bin/bash

# Variáveis 
CONTAINER_NAME="postgres_monit"
DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD="postgres"

# Script SQL temporário
SQL_FILE="/tmp/create_telemetria.sql"

cat <<EOF > $SQL_FILE
-- Criação da tabela principal
CREATE TABLE IF NOT EXISTS telemetria (
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

-- Criação da tabela histórica
CREATE TABLE IF NOT EXISTS historico_telemetria (
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

-- Função para inserir histórico
CREATE OR REPLACE FUNCTION inserir_historico_telemetria()
RETURNS TRIGGER AS \$\$
BEGIN
    INSERT INTO historico_telemetria (
        telemetria_id,
        unix, latitude, longitude, course, speed, altitude,
        pitch, roll, accel_magnitude, max_delta_accel,
        power_status, error_status, data_insercao
    )
    VALUES (
        NEW.id,
        NEW.unix, NEW.latitude, NEW.longitude, NEW.course, NEW.speed, NEW.altitude,
        NEW.pitch, NEW.roll, NEW.accel_magnitude, NEW.max_delta_accel,
        NEW.power_status, NEW.error_status, NOW()
    );
    RETURN NEW;
END;
\$\$ LANGUAGE plpgsql;

-- Trigger para histórico após cada INSERT
DROP TRIGGER IF EXISTS trigger_inserir_historico_telemetria ON telemetria;
CREATE TRIGGER trigger_inserir_historico_telemetria
AFTER INSERT ON telemetria
FOR EACH ROW
EXECUTE FUNCTION inserir_historico_telemetria();
EOF

# Executa o SQL dentro do container
echo "Criando tabelas e triggers no banco..."
sudo docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME < $SQL_FILE

echo "Concluído!"
