DROP TABLE IF EXISTS ventas;
CREATE TABLE ventas (
  id serial PRIMARY KEY,
  anio int NOT NULL, mes int NOT NULL,
  pais text NOT NULL, calidad text NOT NULL,
  sacos int NOT NULL, ingresos_usd numeric(12,2) NOT NULL DEFAULT 0
);
INSERT INTO ventas (anio, mes, pais, calidad, sacos)
SELECT 2026, m, p, c, (50 + random()*450)::int
FROM generate_series(1,12) AS m,
     unnest(ARRAY['Alemania','Estados Unidos','Bélgica','Japón']) AS p,
     unnest(ARRAY['especial','convencional','organico']) AS c;
-- caída simulada: orgánico a Alemania en octubre
UPDATE ventas SET sacos = sacos / 3 WHERE mes = 10 AND pais = 'Alemania' AND calidad = 'organico';
UPDATE ventas SET ingresos_usd = round((sacos * 152.12 * (2.5 + random()))::numeric, 2);
