using System;

namespace AutoCar;

public class Payment
{
    public Guid ID { get; set; }
    public Guid CustomerID { get; set; }
    public float? Amount { get; set; }
    public string? TransactionID { get; set;}
    public DateTimeOffset? TransactionTime { get; set; }
    public PaymentStatus status { get; set; }

}

