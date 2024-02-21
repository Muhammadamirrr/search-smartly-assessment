import os
import json
import pandas as pd
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET

from data_ingestion_ms.models import PointOfInterest


class Command(BaseCommand):
    help = 'Your custom command description goes here'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the file')

    def process_data_and_save(self, file_path, file_format):
        if file_format.lower() == '.csv':
            df = pd.read_csv(file_path)
            df = df.rename(columns={
                'poi_id': 'id',
                'poi_name': 'name',
                'poi_latitude': 'latitude',
                'poi_longitude': 'longitude',
                'poi_category': 'category',
                'poi_ratings': 'rating',
            })

        elif file_format.lower() == '.json':
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
            df = pd.json_normalize(data)
            df = df.rename(columns={
                'id': 'id',
                'name': 'name',
                'description': 'description',
                'coordinates.latitude': 'latitude',
                'coordinates.longitude': 'longitude',
                'category': 'category',
                'ratings': 'rating',
            })

        elif file_format.lower() == '.xml':
            tree = ET.parse(file_path)
            root = tree.getroot()
            data = []
            for element in root:
                item = {}
                for child in element:
                    item[child.tag] = child.text
                data.append(item)
            df = pd.DataFrame(data)
            df = df.rename(columns={
                'pid': 'id',
                'pname': 'name',
                'platitude': 'latitude',
                'plongitude': 'longitude',
                'pcategory': 'category',
                'pratings': 'rating',
            })

        else:
            self.stdout.write(self.style.ERROR(f"Unsupported file format: {file_format}"))
            return

        pois = [PointOfInterest(
            external_id=row['id'],
            name=row['name'],
            description=row.get('description',None),
            coordinates={'lat': row['latitude'], 'long': row['longitude']},
            category=row['category'],
            rating=(row['rating'].split(',') if isinstance(row['rating'], str) else None),
        ) for _, row in df.iterrows()]
        PointOfInterest.objects.bulk_create(pois)
        self.stdout.write(self.style.SUCCESS('Data ingestion successful!'))

    def handle(self, *args, **options):
        file_path = options['file_path']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('Invalid file path!'))
            return

        _, extension = os.path.splitext(file_path)

        self.process_data_and_save(file_path, extension)
