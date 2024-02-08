# YaMDb Project


The YaMDb project collects user reviews of works. The works themselves are not stored in YaMDb, 
you cannot watch a movie or listen to music here. Works are divided into categories, 
such as "Books", "Movies", "Music". For example, in the category "Books" there can be the works 
"Winnie the Pooh and Everything" and "The Martian Chronicles", and in the category "Music" 
there can be the song "Moskau" by the band "Rammstein" and the second suite by Bach. The list 
of categories can be expanded (for example, you can add the category "Fine Arts" or "Jewelry").
A work can be assigned a genre from a list of preset genres (e.g., Fairy Tale, Rock, or Art House).
Only the administrator can add works, categories and genres. Grateful or indignant users leave text
reviews for the works and give the work a rating in the range from one to ten (integer); an average
rating (integer) is formed from the user ratings. A user can leave only one review per work.
Users can leave comments on reviews. Only authenticated users can add reviews, comments and give ratings.

# Development team:


# Development team:

- [Viacheslav Ispaniuk](https://github.com/Basmelek18) (Developer 1 - Team Lead)
- [Vladislav Ishmukhametov](https://github.com/VladIshmukhametov) (Developer 2)
- [Igor Dolgonosov](https://github.com/Ugar78) (Developer 3) 



# Technology stack used in the project:

- Python 3.9
- Django 3.2
- DRF 3.12.4
- JWT


# Project launch:

Clone the repository and navigate to it on the command line.
Create and activate a virtual environment:
```
python3 -m venv venv
source env/bin/activate
```
Install dependencies from the file requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Perform migrations:
```
python3 manage.py migrate
```
Fill database from csv file:
```
python3 manage.py import_csv
```
Run the project:
```
python3 manage.py runserver
```

# Examples of working with API for all users


### API documentation
The documentation can be found at `http://127.0.0.1:8000/redoc/`


### User registration algorithm

The user sends a POST request to add a new user with email and username parameters 
to the /api/v1/auth/signup/ endpoint. YaMDB sends an email with confirmation code to 
the email address. The user sends a POST-request with username and confirmation code 
to the /api/v1/auth/token/ endpoint, and receives a token (JWT token) in response to 
the request. If desired, the user sends a PATCH-request to the /api/v1/users/me/ endpoint 
and fills in the fields in his profile (see documentation for field descriptions).

### User Roles

Anonymous - can view descriptions of works, read reviews and comments. 
Authenticated user (user) - can, like Anonymous, read everything,
additionally he can post reviews and rate works (movies/books/songs), 
can comment on other people's reviews; can edit and delete his reviews
and comments. This role is assigned by default to every new user. 
Moderator (moderator) - the same rights as an Authenticated User plus 
the right to delete any reviews and comments. Administrator (admin) - 
full rights to manage all content of the project. Can create and delete works, 
categories and genres. Can assign roles to users. Django Superuser - has administrator 
(admin) rights
