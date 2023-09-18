CREATE TABLE payment(
	Id SERIAL PRIMARY KEY NOT NULL,
	CustomerId INTEGER REFERENCES customer(Id) NOT NULL,
	Amount FLOAT,
	TransactionId VARCHAR(200),
	TransactionTime DATE,
	Status PaymentStatus NOT NULL
	
);