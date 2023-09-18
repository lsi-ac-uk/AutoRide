CREATE TABLE trip(
	Id SERIAL PRIMARY KEY NOT NULL,
	CustomerId INTEGER REFERENCES customer(Id) NOT NULL,
	VehicleId INTEGER REFERENCES vehicle(Id) NOT NULL,
	PaymentId INTEGER REFERENCES payment (Id),
	StartLatitude INTEGER NOT NULL,
	StartLongitude INTEGER NOT NULL,
 	EndLatitude INTEGER,
	EndLongitude INTEGER,
	Status TripStatus NOT NULL
	
)