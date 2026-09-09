# Dinner Finder

A simple restaurant recommendation web application built with Python and Flask.

## Overview

Dinner Finder allows a user to select a cuisine and receive a random restaurant recommendation from the available restaurants in that cuisine.

The application is being built as a learning project to practice:

* Python
* Flask
* HTML forms
* HTTP GET and POST requests
* SQLite
* SQL
* CRUD operations
* Basic web application architecture

## Current Functionality

* Select a cuisine from a list of available options
* Submit the selected cuisine to Flask
* Validate the submitted cuisine
* Return the selected cuisine

## Planned Functionality

* Store restaurants in a SQLite database
* Randomly recommend a restaurant matching the selected cuisine
* Allow the user to accept or deny a recommendation
* Provide another recommendation when a restaurant is denied
* Allow users to add restaurants
* Add functionality to update and delete restaurants
* Add additional recommendation criteria, such as price range

## Technologies

* Python
* Flask
* HTML
* SQLite
* Git

## Running Locally

Clone the repository:

```bash
git clone git@github.com:BuccoBruce/dinner-finder.git
cd dinner-finder
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask application:

```bash
flask --app app run
```

Then open the local address displayed by Flask in your browser.

## Project Structure

```text
dinner-finder/
├── app.py
├── templates/
│   └── index.html
├── .gitignore
└── README.md
```

## Status

This project is actively being developed.

