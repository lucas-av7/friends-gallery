# Friend's Gallery

Online photos gallery. See live: [Heroku](https://friends-gallery-frontend.herokuapp.com/).

## Admin features

- Approve photos
- Delete photos

## User features

- Upload photos
- Comment on photos
- Like photo
- Like comment

## Run the project locally

### Prepare .env file

In the project root run:

```bash
cp .env.example .env
```

Fill the blank information in the .env file

**SECRET_KEY:** Backend secret key (required)
**USE_AWS_S3:** Ue AWS S3 as storage provider (0=OFF, 1=ON)
**IMGBB_API_KEY:** Required when USE_AWS_S3=0. Get api key in the [Imgbb](https://imgbb.com/) website

### Init MongoDB database

Docker is required. In the project root run:

```bash
docker-compose up -d
```

### Init backend

Python is required. From the project root run:

```bash
cd backend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 wsgi.py
```

Project default address: <http://localhost:5000/>

### Init frontend

NodeJs is required. From the project root run:

```bash
cd frontend
npm i
npm run dev
```

Project default address: <http://localhost:3000/>

### Create admin user

To create admin user you need to make a POST api call to <http://localhost:5000/api/users/admin> with the JSON body:

```json
{
  "name": "<user name>",
  "email": "<user email>",
  "password": "<user password>",
  "secret_key": "<backend secret key on .env file>"
}
```

## Tech stack

### Backend

- [Python](https://www.python.org/): Programming language
- [Flask](https://flask.palletsprojects.com/en/2.1.x/): Python framework
- [Flask-cors](https://flask-cors.readthedocs.io/en/latest/): Handling Cross Origin Resource Sharing
- [Mongoengine](http://mongoengine.org/): Document-Object Mapper for MongoDB
- [PassLib](https://passlib.readthedocs.io/en/stable/): Password hashing
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/): User authentication and authorization
- [Python-dotenv](https://github.com/theskumar/python-dotenv): Load environment variables from env_files
- [Requests](https://docs.python-requests.org/en/latest/): HTTP requests
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html): Manage AWS S3
- [Pytest](https://docs.pytest.org/en/7.1.x/): Unit testing library

### Frontend

- [JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript): Programming language
- [Vue.js 3](https://vuejs.org/): JavaScript framework
- [Vue router](https://router.vuejs.org/): Router for SPA
- [Mitt](https://github.com/developit/mitt): Event emitter / pubsub
- [Validator](https://github.com/validatorjs/validator.js): String validators and sanitizers
- [Font awesome](https://fontawesome.com/): Icons
- [Axios](https://github.com/axios/axios): HTTP requests
- [Vitest](https://vitest.dev/): Unit testing library

### Database

- [Mongodb](https://www.mongodb.com/pt-br): NoSql database
- [Cloud Mongodb](https://www.mongodb.com/cloud): MongoDB Deploy (Production only)

### Other

- [Docker](https://www.docker.com/): Virtualization
- [Imgbb](https://imgbb.com/): Storage provider
- [AWS S3](https://aws.amazon.com/pt/s3/): Storage provider

## Notes

To avoid multiple requests from the server, we are using the vue `keep-alive` built-in component. It creates a cache of the page visited (max: 5). It means that if the admin user deletes or approves a photo on the admin panel and goes back to the home page, the admin may need to refresh the browser to request the last changes from the server.
