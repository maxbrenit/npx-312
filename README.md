# Bright Events API

Bright events provides a platform for event organizers to create and manage different types of events while making them easily accessible to target markets.
Event organizers need to register for accounts, so they can create and manage their events.
Users (Event Attendees) don't need registration to RSVP to events.

## Motivation
Events are created every day, people get to events and others get to miss event RSVP. Motivation to come up with this
application has originated from the fact that people need to have access to event details from wherever they are.

## Build Status

[![Build Status](https://travis-ci.org/mutoromike/BrightEventsAPI.svg?branch=master)](https://travis-ci.org/mutoromike/BrightEventsAPI)  [![Coverage Status](https://coveralls.io/repos/github/mutoromike/BrightEventsAPI/badge.svg?branch=ft-implement-jwt-auth)](https://coveralls.io/github/mutoromike/BrightEventsAPI?branch=ft-implement-jwt-auth)  [![Codacy Badge](https://api.codacy.com/project/badge/Grade/44897ad46ed2432dacb3fd1baa34cab1)](https://www.codacy.com/app/mutoromike/BrightEventsAPI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mutoromike/BrightEventsAPI&amp;utm_campaign=Badge_Grade)

## Tech/Framework used

The application has been built by:
- Flask (Python)

## Features

This application allows users to:
- Create accounts and login to the system
- Create events
- View, edit (update) and delete events
- View and RSVP to other events
- Obtain users who RSVP to their events

# Installation

- Ensure you have 
-  `python 3.4 installed`
-  `istalled virtual environment`
- Clone the repo to your local machine
- Navigate to bright_events folder
- Create a virtual environment and run the command: `pip install -r requirements.txt` (install packages)

### Start the application

- The run the following to start the app:
-  `python run.py`
- Navigate to postman to test the api endpoints

## Tests

To run tests and ensure the application works:
- Navigate to tests folder on cmd or terminal
-  `tests`
- Run the command `nosetests` with the file name
-  `nosetests test_auth.py`
- Repeat this with all the files that contain tests i.e.,
-  `test_models.py`

## Using the application

- Register to create an account
- Login using username and password created
- After signing in you can proceed to create events or RSVP to other events
- You can also search for events using location, event names or event categories
- Access the API documentation at "https://brighteventsapi1.docs.apiary.io/#reference/0/user"



