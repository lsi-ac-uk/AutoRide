CREATE TABLE trip(
	Id UUID PRIMARY KEY NOT NULL,
	CustomerId UUID REFERENCES customer(Id) NOT NULL,
	VehicleId UUID REFERENCES vehicle(Id) NOT NULL,
	PaymentId UUID REFERENCES payment (Id),
	StartLatitude INTEGER NOT NULL,
	StartLongitude INTEGER NOT NULL,
 	EndLatitude INTEGER,
	EndLongitude INTEGER,
	Status TripStatus NOT NULL
	
)