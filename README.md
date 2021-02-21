This is an app that I made using 
### Python(Flask)
### PostgreSQL 
as a part of a Udacity FullStack NanoDegree

Author:
Ahmed ElAmory

-----
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Overview

The app uses PostgreSQL database to do :

* create new venues, artists, and create new shows.
* search for venues and artists.
* learn more about a specific artist or venue.


## Tech Stack (Dependencies)

### 1. Backend Dependencies
The tech stack includes the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be the ORM library of choice
 * **PostgreSQL** as the database of choice
 * **Python3** and **Flask** as the server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

### 2. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for the website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/).
Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes the SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** The forms
  ├── requirements.txt *** The dependencies needed to be installed with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new artists, shows, and venues.
* `app.py` -- Defines routes that match the user’s URL, and controllers which handle data and renders views to the user.
* Models in `app.py` -- Defines the data models that set up the database tables.
* `config.py` -- Stores configuration variables and instructions, separate from the main application code.


## Development Setup

make sure you installed virtualenv using:

```
pip install virtualenv
```


1. **Download the project code locally**
```
git clone https://github.com/AhmedElAmory/Fyyur
```

2. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```

For Windows users:

```
python -m virtualenv env
env\Scripts\activate
```

3. **Install the backend dependencies:**
Check requirements.txt to see the required dependencies

```
pip install -r requirements.txt
```
4. **Install the frontend dependencies:**
make sure you have node and npm installed using
```
node -v
npm -v
```
If not installed go to (https://nodejs.org/en/download/).

Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```
5. **Update the Database URI and update the database**

create a postgres database and edit the database URI in config.py

then run 

```
flask db upgrade
```

to update the database schema

6. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

For Windows Users:
```
set FLASK_APP=myapp
set FLASK_ENV=development # enables debug mode
python3 app.py
```

7. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 