# YaMDb Project


The YaMDb project is a platform designed to aggregate user reviews for various creative works. Please note that the platform does not host the actual works; it serves as a space for users to share their opinions. Whether it's books, movies, or music, works are categorized into specific genres, allowing users to explore and engage with different types of content.

For instance, in the "Books" category, users may find works such as "Winnie the Pooh and Everything" and "The Martian Chronicles." Similarly, the "Music" category could feature the song "Moskau" by the band "Rammstein" and Bach's second suite. The list of categories is flexible and can be expanded to include additional ones like "Fine Arts" or "Jewelry." To maintain the quality and relevance of the platform, only administrators have the authority to add new works, categories, and genres.

Works within YaMDb can be further classified by assigning them predefined genres such as Fairy Tale, Rock, or Art House. Users express their opinions through text reviews and provide a numerical rating ranging from one to ten. The platform calculates an average rating based on user input.

To ensure the authenticity of the reviews and ratings, only authenticated users are allowed to contribute by adding reviews, comments, and providing ratings. Additionally, users are limited to one review per work, fostering a fair and diverse range of opinions. The platform encourages interaction by allowing users to leave comments on reviews, facilitating a community-driven discussion around the various works showcased on YaMDb.


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

Users interact with the YaMDb authentication system through a series of HTTP requests, as outlined below:

## User Registration:

- The user initiates the registration process by sending a POST request to the /api/v1/auth/signup/ endpoint.
- The request includes parameters such as email and username.
- Upon receiving the request, YaMDB generates a confirmation code and sends it to the provided email address for verification.
  
## Email Verification:

- The user then sends a POST request to the /api/v1/auth/token/ endpoint.
- The request contains parameters including username and the confirmation code received via email.
- In response, YaMDB processes the verification, and if successful, issues a token (JWT token) to the user.
## Profile Completion (Optional):

- If the user wishes to provide additional information and complete their profile, they can send a PATCH request to the /api/v1/users/me/ endpoint.
- The PATCH request allows the user to fill in various fields within their profile.
- Detailed field descriptions can be found in the documentation.
This workflow ensures a secure and streamlined user registration process. After confirming their identity through the confirmation code, users gain access to the system with a JWT token. Additionally, users have the option to enhance their profiles by providing additional details as part of the registration process. The clear API endpoints facilitate a seamless user experience, allowing users to manage their accounts effectively.

### User Roles


In the YaMDb project, different roles grant varying levels of access and permissions to users. Here's an overview of the roles and their associated rights:

## Anonymous User:

- Can view descriptions of works.
- Can read reviews and comments.
- Authenticated User (User):

## Inherits the rights of an Anonymous User.
- Can post reviews.
- Can rate works (movies/books/songs).
- Can comment on other people's reviews.
- Can edit and delete their own reviews and comments.
- By default, every new user is assigned this role.
  
## Moderator:

- Possesses all the rights of an Authenticated User.
- Can delete any reviews and comments.
  
## Administrator (Admin):

## Full rights to manage all content in the project.
- Can create and delete works, categories, and genres.
- Can assign roles to users.
  
## Django Superuser:

- Possesses administrator (admin) rights.
  
These roles ensure a structured system where users, based on their role assignments, can perform specific actions within the YaMDb project. While Authenticated Users have the ability to contribute reviews and comments, Moderators and Administrators have additional responsibilities and powers to manage and oversee the content and user roles. Django Superusers hold the highest level of authority with full administrative rights. This role-based access control allows for effective content management and user engagement within the platform.
