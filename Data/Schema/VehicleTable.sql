CREATE TABLE Vehicle(
	Id SERIAL PRIMARY KEY NOT NULL,
	LicensePlate VARCHAR(20) NOT NULL,
	VehicleStatus VehicleStatus NOT NULL,
	LastService DATE,
	Latitude INTEGER,
	Longitude INTEGER,
	Model VARCHAR(50),
	Make VARCHAR(50),
	LastTime DATE	
);