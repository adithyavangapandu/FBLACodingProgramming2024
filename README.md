# GreenPot
GreenPot is the codename for my submission for the 2024 FBLA Coding and Programming event. I chose this name because school partners usually provide some value to the school in return for the advertising. I used the adjective "Green" to symbolize the value that the partners provide. "Pot" refers to all the partners being stored or contained in a single place. Hence, the codename for this project is **GreenPot**.
# Overview
The purpose of this application is to store information on partners for the Career and Technical Department of my school. The application allows members of the Career and Technical Department to create accounts to store their data as well as view the data of others. Users can create, view, update, and delete partners. They can store contact information in the form of email, phone number, and individual along with the type of organization and the resources that they provide. 

Additional information relevant to partners of a school are payment plans and responsibilities. Responsibilities are for any time an event with a partner is going on and the user must identify what their responsibilities are. For example, if a school was hosting a family night with a partner, they could write "Find Volunteers" in the responsibilities field. Another feature is the notifications. Use notifications to remind yourself for payments, responsibilities, or anything else.

This program enables school faculty to easily store important data while maintaining a level of security between users. Users can also generate downloadable reports of partner data that may find use outside of the context of the application.

# Getting Started
Download the file and create an environment variable for the SECRET_KEY and SQLALCHEMY_DATABASE_URI. This way will have access to the database. Then, go to the directory where the file **app.py** is stored and run the command: python app.py
# Approach
To design this application, I followed a standard Software Development Life Cycle (SDLC).
## Understanding Requirements
A critical aspect of the SDLC is establishing the first principles. The requirements of this application are very straightforward. This left room for additional functionality. The core function is storage, so basic CRUD operations were added in the app. In addition, there is a downloadable report, a notifications menu, and adding data through CSV.
## Design
### Data Storage
Persistent data is stored in a SQLite database, accessed by the flask SQLAlchemy extension within my code.
### Data Validation
Data is validated in the frontend by using validators when entering in data such as email, Integer, and required validators. Data is validated in the backend by ensuring that users only access their own partners and not partners of other users.
### MVC Design
The models are all the routes.py files in my application. There are three of them because I used a blueprint to divide the functionality into related groups: main, users, partners. This way the length of the routes files are smaller and easier to understand. The views are the HTML files within the templates folder and lastly the model.py file creates the model for the database.

## Project Structure
```text
Project Name (Top-level)
├── app.py
├── greenpot
│  ├── __init__.py
│  ├── config.py
│  ├── main (Controls the main pages of the app)
│  │  ├── __init__.py
│  │  └── routes.py 
│  ├── models.py (Where the database model is defined.)
│  ├── partners
│  │  ├── __init__.py
│  │  ├── forms.py
│  │  └── routes.py
│  ├── static
│  │  └── main.css
│  ├── templates (Frontend views)
│  │  ├── about.html
        ...
│  └── users (Controls pages related with user. Ex. Login, Signup, etc.)
│    ├── __init__.py
│    ├── forms.py
│    └── routes.py
├── instance
│  └── site.db (The database)
├── migrations (Changing the database)
│  ├── README
│  ├── alembic.ini
│  ├── env.py
│  ├── script.py.mako
│  └── versions
│    ├── add_isread_a1b8a49d85eb_.py
      ...
└── testdata.csv
```

