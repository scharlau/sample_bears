import csv
import os
from pathlib import Path
from django.db import models
from django.core.management.base import BaseCommand, CommandError

from bears.models import Bear, Sighting

#We use the command tools so that we gain access to our models and database connections
#https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/ 

class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):

        # drop the data from the table so that if we rerun the file, we don't repeat values
        Bear.objects.all().delete()
        print("table dropped successfully")
        # create table again

        # open the file to read it into the database
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        with open(str(base_dir) + '/bears/data/USGS_WC_eartag_deployments_2009-2011.csv', newline='') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader) # skip the header line
            for row in reader:
                print(row)

                bear = Bear.objects.create(
                bearID = int(row[0]),
                ptt_ID = int(row[1]),
                capture_lat = float(row[6]),
                capture_long = float(row[7]),
                sex = row[9],
                age_class = row[10],
                ear_applied = row[11],
                )
                bear.save()

        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        with open(str(base_dir) + '/bears/data/USGS_WC_eartags_output_files_2009-2011-Status.csv', newline='') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader) # skip the header line
            for row in reader:
                print(row)
                # sanity checking for empty cells - and skip row if it is - this clears up most missing data to parse the file
                # the file will still fall over at some point, but you get enough to show a good example
            
                if row[4] is not '':
                    if row[9] is not '':
                        bear_temp = row[0]  
                        print(bear_temp)
                        bear = Bear.objects.filter(bearID = bear_temp).first()
                        print(bear.id)

                        sighting = Sighting.objects.create(
                        deploy_id = int(row[0]),
                        bear_id = bear,
                        recieved = row[2],
                        latitude = float(row[4]),
                        longitude = float(row[5]),
                        temperature = float(row[9]),
                        )
                        sighting.save()
                else:
                    next(reader)

        print("data parsed successfully")
