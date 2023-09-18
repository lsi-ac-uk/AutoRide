CREATE TABLE trip(
	Id SERIAL PRIMARY KEY NOT NULL,
	CustomerId INTEGER REFERENCES customer(Id) NOT NULL,
	vehicleId INTEGER REFERENCES vehicle(Id) NOT NULL,
	StartLatitude INTEGER NOT NULL,
	StartLongitude INTEGER NOT NULL,
 	EndLatitude INTEGER,
	EndLongitude INTEGER,
	PaymentId INTEGER REFERENCES payment (Id),
	status TripStatus NOT NULL
	
)