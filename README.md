# Futsal-Stat-Track

A django web application for tracking player statistics, matches and tournament days.

The application is strictly tailored to create tournament days involving 3 teams with permanently assigned names (blue, orange, colors).


## Installation

Clone the repository:

```bash
$ git clone https://github.com/Put3k/Futsal-Stat-Track.git
$ cd Futsal-Stat-Track
```

Create a virtual environment to install dependecies in and activate it:
```bash
$ python -m venv
$ venv/Scripts/activate
```

Then install the dependecies:
```bash
(venv)$ pip install -r requirements.txt
```

Note the (venv) at the left side of the prompt. This indicates that this terminal session operates in virtual environment.

Once pip has finished downloading the dependecies:
```bash
(venv)$ cd mysite
(venv)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.
    
