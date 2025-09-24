-- Função para inserir na tabela historico_telemetria
CREATE OR REPLACE FUNCTION inserir_historico_telemetria()
RETURNS TRIGGER AS $$
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
$$ LANGUAGE plpgsql;

-- Trigger para inserir histórico sempre que houver INSERT em telemetria
CREATE TRIGGER trigger_inserir_historico_telemetria
AFTER INSERT ON telemetria
FOR EACH ROW
EXECUTE FUNCTION inserir_historico_telemetria();
