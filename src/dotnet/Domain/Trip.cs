using System;

namespace AutoCar;

public class Trip{
    public Guid ID{get; set;}
    public Guid CustomerID{get; set;}
    public Guid VehicleID{get; set;}
    public Guid StartLocationID{get; set;}
    public Guid EndLocationID{get; set;}
    public DateTimeOffset StartTripDate{get; set;} 
    public DateTimeOffset EndTripDate{get; set;}
    public Guid PaymentID{get; set;}
    public TripStatus status{set; get}
}

