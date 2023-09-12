using System;

namespace AutoCar;

public class Customer{
    public Guid ID{get; set;}
    public string Name{get; set;}
    public string Family{get; set;}
    public Genders Gender{get; set;}
    public int Age{get; set;}
    public string Email{get; set;}
    public string Phone{get; set;}
    public string Address{get; set;}
    public string ZipCode{get; set;}
    public DateTimeOffset JoinDate{get; set;} 
}

