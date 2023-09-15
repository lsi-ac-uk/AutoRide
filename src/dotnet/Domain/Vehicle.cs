using System;

namespace AutoCar;

public class Vehicle
{
    public Guid ID { get; set; }
    public Guid VehicaleVasicInformationID { get; set; }
    public string Number { get; set; }
    public VehicleStatus status { get; set; }
    public DateTimeOffset? LastService { get; set; }
    public Guid? LastLocationID { get; set; }
    public DateTimeOffset? LastTime { get; set; }

}

