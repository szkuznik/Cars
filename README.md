# Cars
Cars project I created as a coding task for EY

## Requirements:
Docker-compose

## Installation:
1. `docker-compose up --build` <br>
2. To access running application go to http://localhost:8000/admin/ <br>

### Libraries reasoning
I can write unit tests in unittest or pytest, pytest is my usual choice.
Factoryboy is useful package Both for writing tests and for creating fake data for local environments. 
That is why I prefer this over pytest fixtures. DjangoRestFramework is best tool for developing REST APIs with django. 
Similarly, requests is a standard Python package which handles making requests to external APIs