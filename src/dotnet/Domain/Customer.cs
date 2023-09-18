using System;

namespace AutoCar;

public class Customer
{
    public Guid ID { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public DateTimeOffset? DataOfBirth { get; set; }
    public string? Email { get; set; }
    public string? Phone { get; set; }
    public string? Address { get; set; }
    public string? ZipCode { get; set; }
    public DateTimeOffset? JoinDate { get; set; }
}

