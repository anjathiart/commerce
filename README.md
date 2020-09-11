# commerce

My first Python Django App implementing Object Relational Models.

This application is a mock auction site website similar (and simpler) to bid-or-buy and forms part of CS50 Web 2020. 

This project is deliberatly done without javascript. 

## Technologies

### Backend
- Python
- Django
- Sqlite
- Object relational models

### Frontend
- Django
- HTML
- SASS / CSS

## Development

`python3 manage.py makemigrations auctions`
`python3 manage.py migrate`
`python3 manage.py runserver`

## Notes

1. No Javascript or Javascript frameworks are used in this project.
2. In hindsight 'bid' and 'comment' models should have a foreign key relationship to 'listing', because a bid and / or a comment cannot share more than one listing (I could be missing something).
3. Error / exception handling has not been implemented extensively.
4. Javascrip

