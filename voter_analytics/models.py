''' Clemens Li | cl750@bu.edu | Model Designs '''
from django.db import models
from datetime import date # To convert to DateField format

# Create your models here.

def load_data():
    ''' Loads the .csv file for data processing '''
    filename = "C:/Users/cleme/Downloads/CS412/django/voter_analytics/newton_voters.csv" # file path
    f = open(filename)
    f.readline() # discard headers
    for row in f: # for each instance
        fields = row.strip().split(",") # split fields by commma
        try: # because of all of those stupid typos in date
            dor = date.fromisoformat(fields[8].strip())
        except ValueError:
            dor = None
        Voter.objects.create(voter_id=fields[0].strip(), 
                                name=f"{fields[2].strip()} {fields[1].strip()}", 
                                address=f"{fields[3].strip()} {fields[4].strip()} {fields[5].strip()} {fields[6].strip()}".strip(),
                                dob=date.fromisoformat(fields[7].strip()),
                                dor=dor, # I'm not sure why that weird date is there nvm it's a typo
                                party=fields[9].strip(),
                                precinct=fields[10].strip(),
                                # Vote details
                                v20state=fields[11].strip().upper() == "TRUE",
                                v21town=fields[12].strip().upper() == "TRUE",
                                v21primary=fields[13].strip().upper() == "TRUE",
                                v22general=fields[14].strip().upper() == "TRUE",
                                v23town=fields[15].strip().upper() == "TRUE",
                                voter_score=int(fields[16].strip())
                                )
        

class Voter(models.Model):
    ''' The data for a Voter object '''
    voter_id = models.CharField(max_length=20) # Voter's ID
    name = models.TextField(blank=False) # Voter's Full Name
    address = models.TextField(blank=False) # Voter's Full Address (Street Number/Street Name/Apartment Number/Zip Code)
    dob = models.DateField(blank=False) # Date of Birth
    dor = models.DateField(null=True, blank=True) # Date of Registration (I don't know why but there's an invalid one)
    party = models.CharField(max_length=2) # 2-Character Party Code
    precinct = models.CharField(max_length=10) # Voter's Precinct Number
    # Election Participation Fields
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        ''' Returns a string representation of a Voter object '''
        return f"ID: " + self.voter_id + " | Name: " + self.name + " | Address: " + self.address + " | DOB: " + self.dob + " | Party: " + self.party
