using System;

namespace AutoCar;

public class VehicleBasicInformation
{
    public Guid ID { get; set; }
    public string? Manufacturer { get; set; }
    public string Name { get; set; }
    public VehicleTypes Type { get; set; }

}

