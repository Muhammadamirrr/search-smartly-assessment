# Search Smartly Assessment!

This project is the data ingestion ms implementation for collecting data from multiple data sources. Hi! I'm your first Markdown file in **StackEdit**. If you want to learn about StackEdit, you can read me. If you want to play with Markdown, you can edit me. Once you have finished with me, you can create new files by opening the **file explorer** on the left corner of the navigation bar.


# Run via Docker

To run the application via **docker** follow the steps below.

## Navigate to root directory

Navigate to the project root directory by using the following command.

    cd <base_directory_location>

## Build Image

Run the following command to build a docker image of the project.

    docker-compose build

## Run Docker Compose

Run the following command to launch the create and launch the docker containers.

    docker-compose up -d


> Note:- Running the application as a docker container will automatically create a superuser with the following credentials **username: admin** & **password: Admin123** and it will also run the **load_file** custom command for importing the **.csv, .json and .xml** files respectively.

# Run manually

Follow the following steps to run the application manually and use the **load_file** custom command to import the data from the input files.

## Navigate to root directory

Navigate to the project root directory by using the following command.

    cd <base_directory_location>
    
## Create superuser

Run the following command to create a superuser.

    python manage.py createsuperuser

## Run the webserver

Run the following command to launch the web server to serve the application.

    python manage.py runserver 0.0.0.0:8000

## Launch Admin Panel

Use the following address to navigate to the admin panel.

    http://127.0.0.1:8000/admin/

## Import data

Run the following command to import data from a file.

    python manage.py load_file <file path>

<br>

> Note:- For running the application manually you need to have a virtual environment and the requirements installed from the requirements.txt
