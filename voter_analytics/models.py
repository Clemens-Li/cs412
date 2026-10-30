''' Clemens Li | cl750@bu.edu | Model Designs '''
from django.db import models

# Create your models here.

def load_data():
    ''' Loads the .csv file for data processing '''
    filename = "C:/Users/cleme/Downloads/CS412/django/voter_analytics/newton_voters.csv" # file path
    f = open(filename)
    f.readline() # discard headers
    for row in range(17):
        line = f.readline().strip()
        fields = line.split(",") # split fields by commma
        for i in range(len(fields)):
            print(f"fields{i}] = {fields[i]}")

class Voter(models.Model):
    ''' The data for a Voter object '''
    id = models.IntegerField() # Voter's ID number
    name = models.TextField(blank=False) # Voter's Full Name
    address = models.TextField(blank=False) # Voter's Full Address (Street Number/Street Name/Apartment Number/Zip Code)
    dob = models.DateField(blank=False) # Date of Birth
    dor = models.DateField(blank=False) # Date of Registration
    affiliation = models.CharField(max_length=2) # 2-Character Party Code
    precinct = models.IntegerField() # Voter's Precinct Number

    def __str__(self):
        ''' Returns a string representation of a Voter object '''
        return "Name: " + self.name + " | Address: " + self.address + " | DOB: " + self.dob + " | Affiliation: " + self.affiliation
