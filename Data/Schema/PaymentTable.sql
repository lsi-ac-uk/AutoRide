CREATE TABLE payment(
	Id UUID PRIMARY KEY NOT NULL,
	CustomerId UUID REFERENCES customer(Id) NOT NULL,
	Amount FLOAT,
	TransactionId VARCHAR(200),
	TransactionTime DATE,
	Status PaymentStatus NOT NULL
	
);