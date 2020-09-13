# commerce

My first Python Django App using Django queries and the Django models API

This application is a mock auction site website similar (and simpler) to bid-or-buy and forms part of CS50 Web 2020. It is done without javascript or JS framework and focusses on using Django models and templates.

Video demonstrating the application:  https://youtu.be/71YrEOlvQRU

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
4. There is a lot of repetition in the views that could be refactored using a layered approach, (separating business logic, db queries and views).
5. There is much repetition in the html templates making frameworks like React and Vue, single-file-componentes and single page applications so appealing
6. TODO: Use Django forms

