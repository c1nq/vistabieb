-- Beveiliging
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    leerlingnummer VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'medewerker',
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Leden
CREATE TABLE leden (
id SERIAL PRIMARY KEY,
voornaam VARCHAR(100) NOT NULL,
achternaam VARCHAR(100) NOT NULL,
email VARCHAR(120) UNIQUE NOT NULL,
telefoon VARCHAR(20),
adres VARCHAR(255),
postcode VARCHAR(10),
plaats VARCHAR(100),
lidnummer VARCHAR(20) UNIQUE,
actief BOOLEAN DEFAULT TRUE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Boeken
CREATE TABLE boeken (
id SERIAL PRIMARY KEY,
titel VARCHAR(255) NOT NULL,
auteur VARCHAR(200),
isbn VARCHAR(20) UNIQUE,
uitgever VARCHAR(200),
jaar_uitgave INT,
categorie VARCHAR(100),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exemplaren
CREATE TABLE exemplaren (
id SERIAL PRIMARY KEY,
boek_id INT REFERENCES boeken(id) ON DELETE CASCADE,
barcode VARCHAR(50) UNIQUE,
status VARCHAR(20) DEFAULT 'beschikbaar',
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Leningen
CREATE TABLE leningen (
id SERIAL PRIMARY KEY,
exemplaar_id INT REFERENCES exemplaren(id),
lid_id INT REFERENCES leden(id),
datum_uitgeleend TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
datum_terug_gepland DATE,
datum_teruggekeerd TIMESTAMP,
boete_bedrag DECIMAL(6,2) DEFAULT 0,
betaald BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_leningen_lid ON leningen(lid_id);
CREATE INDEX idx_leningen_exemplaar ON leningen(exemplaar_id);
CREATE INDEX idx_leningen_status ON leningen(datum_teruggekeerd);

-- Reserveringen
CREATE TABLE reserveringen (
    id SERIAL PRIMARY KEY,
    lid_id INT REFERENCES leden(id) ON DELETE CASCADE,
    boek_id INT REFERENCES boeken(id) ON DELETE CASCADE,
    datum_gereserveerd TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'actief',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reserveringen_lid ON reserveringen(lid_id);
CREATE INDEX idx_reserveringen_boek ON reserveringen(boek_id);
CREATE INDEX idx_reserveringen_status ON reserveringen(status);
