from django.test import TestCase
import os
import json
import pandas as pd
from django.core.management import call_command
from data_ingestion.models import PointOfInterest


# Create your tests here.

class PointOfInterestTestCase(TestCase):

    def setUp(self):

        self.poi_data = {
            'external_id': '12345678-1234-5678-1234-567812345678',
            'name': 'Test Point of Interest',
            'description': 'A sample point of interest for testing',
            'category': 'Test Category',
            'rating': ['5', '4', '3'],
        }
        self.poi = PointOfInterest.objects.create(**self.poi_data)

    def tearDown(self):
        # Clean up the created PointOfInterest object after each test
        self.poi.delete()

    def test_point_of_interest_creation(self):
        """
        Test whether a PointOfInterest instance is created correctly.
        """
        saved_poi = PointOfInterest.objects.get(id=self.poi.id)

        self.assertEqual(saved_poi.external_id, self.poi_data['external_id'])
        self.assertEqual(saved_poi.name, self.poi_data['name'])
        self.assertEqual(saved_poi.description, self.poi_data['description'])
        self.assertEqual(saved_poi.coordinates, PointOfInterest.coordinates_default())
        self.assertEqual(saved_poi.category, self.poi_data['category'])
        self.assertEqual(saved_poi.rating, self.poi_data['rating'])

    def test_point_of_interest_str_representation(self):
        """
        Test the __str__ method of PointOfInterest model.
        """
        expected_str = self.poi_data['name']
        self.assertEqual(str(self.poi), expected_str)

class DataIngestionCommandTestCase(TestCase):

    def setUp(self):
        # Create a sample CSV file
        self.csv_file_path = 'test_data.csv'
        self.create_sample_csv()

        # Create a sample JSON file
        self.json_file_path = 'test_data.json'
        self.create_sample_json()

        # Create a sample XML file
        self.xml_file_path = 'test_data.xml'
        self.create_sample_xml()

    def tearDown(self):
        # Remove the sample files after tests
        for file_path in [self.csv_file_path, self.json_file_path, self.xml_file_path]:
            if os.path.exists(file_path):
                os.remove(file_path)

    def create_sample_csv(self):
        # Create a sample CSV file for testing
        df = pd.DataFrame({
            'poi_id': [1, 2],
            'poi_name': ['Point1', 'Point2'],
            'poi_latitude': [12.34, 23.45],
            'poi_longitude': [56.78, 67.89],
            'poi_category': ['Category1', 'Category2'],
            'poi_ratings': ['5,4', '3,2,1'],
        })
        df.to_csv(self.csv_file_path, index=False)

    def create_sample_json(self):
        # Create a sample JSON file for testing
        data = [
            {'id': 1, 'name': 'Point1', 'description': 'Point 1 Description', 'coordinates': {'latitude': 12.34, 'longitude': 56.78},
             'category': 'Category1', 'ratings': '5,4'},
            {'id': 2, 'name': 'Point2', 'description': 'Point 2 Description', 'coordinates': {'latitude': 23.45, 'longitude': 67.89},
             'category': 'Category2', 'ratings': '3,2,1'},
        ]
        with open(self.json_file_path, 'w') as json_file:
            json.dump(data, json_file)

    def create_sample_xml(self):
        # Create a sample XML file for testing
        xml_content = """
            <data>
                <item>
                    <pid>1</pid>
                    <pname>Point1</pname>
                    <platitude>12.34</platitude>
                    <plongitude>56.78</plongitude>
                    <pcategory>Category1</pcategory>
                    <pratings>5,4</pratings>
                </item>
                <item>
                    <pid>2</pid>
                    <pname>Point2</pname>
                    <platitude>23.45</platitude>
                    <plongitude>67.89</plongitude>
                    <pcategory>Category2</pcategory>
                    <pratings>3,2,1</pratings>
                </item>
            </data>
        """
        with open(self.xml_file_path, 'w') as xml_file:
            xml_file.write(xml_content)

    def test_data_ingestion_csv(self):
        call_command('load_file', self.csv_file_path)
        self.assertEqual(PointOfInterest.objects.count(), 2)

    def test_data_ingestion_json(self):
        call_command('load_file', self.json_file_path)
        self.assertEqual(PointOfInterest.objects.count(), 2)

    def test_data_ingestion_xml(self):
        call_command('load_file', self.xml_file_path)
        self.assertEqual(PointOfInterest.objects.count(), 2)
