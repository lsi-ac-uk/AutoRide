using System;

namespace AutoCar;

public class Vehicle
{
    public Guid ID { get; set; }
    public string? LicensePlate { get; set; }
    public VehicleStatus Status { get; set; }
    public DateTimeOffset? LastService { get; set; }
    public int Latitude { get; set; }
    public int Longitude { get; set; }
    public string? Model { get; set; }   
    public string? Make { get; set; }
    public DateTimeOffset? LastTime { get; set; }

}

