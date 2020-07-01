# FSND Casting Agency Capstone project

## capstone project for the udacity full stack nanodegree program.

**Heroku link:** (https://capstone-fullstack-proj.herokuapp.com/)



## Run the code locally:

```
source env/bin/activate
env/bin/python app.py &
```


## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Models

Movies with attributes contain title, year, director and genre
Actors with attributes name, role and gender


## Endpoints

`````bash
GET '/actors'

Shell:
curl --request GET \
  --url http://127.0.0.1:5000/actors \
  --header 'Authorization: Bearer XXXX'


{
  "actors": [
    {
      "age": 40,
      "gender": "male",
      "id": 1,
      "name": "Will Smith"
    },
    {
      "age": 50,
      "gender": "male",
      "id": 2,
      "name": "Bruce Wills"
    }
  ],
  "success": true
}


POST '/actors'

Shell:

curl --request GET \
  --url http://127.0.0.1:5000/actors/1 \
  --header 'Authorization: Bearer XXXX'


{
  "actor": {
    "age": 40,
    "gender": "male",
    "id": 1,
    "name": "Will Smith"
  },
  "success": true
}

POST /actors

Shell:

curl http://127.0.0.1:5000/actors \
  -X POST -H "Content-Type: application/json" -d '{ "name": "Jessica Alba", "age": 39, "gender": "female" }' \
  --header 'Authorization: Bearer XXXX'

{
  "actor": {
    "age": 39,
    "gender": "female",
    "id": 3,
    "name": "Jessica Alba"
  },
  "success": true
}

PATCH /actors/<int:id>

Shell:

curl http://127.0.0.1:5000/actors/2 \
  -X PATCH -H "Content-Type: application/json" -d '{ "name": "Scarlett Johansson", "age": 35, "gender": "female" }' \
  --header 'Authorization: Bearer XXXX'

{
  "actor": {
    "age": 35,
    "gender": "female",
    "id": 3,
    "name": "Scarlett Johansson"
  },
  "success": true
}

DELETE /actors/int:id

Shell:
curl http://127.0.0.1:5000/actors/2 \
  -X DELETE \
  --header 'Authorization: Bearer XXXX'

{
  "message": "actor id 3, named Scarlett Johansson was deleted",
  "success": true
}


GET '/movies'

Shell:

curl --request GET \
  --url http://127.0.0.1:5000/movies \
  --header 'Authorization: Bearer XXXX'

{
  "movies": [
    {
      "id": 1,
      "release_date": "Mon, 06 May 2019 00:00:00 GMT",
      "title": "Terminator Dark Fate"
    },
    {
      "id": 2,
      "release_date": "Tue, 06 May 2003 00:00:00 GMT",
      "title": "Terminator Rise of the machines"
    }
  ],
  "success": true
}

GET /movies/<int:id>

curl --request GET \
  --url http://127.0.0.1:5000/movies/1 \
  --header 'Authorization: Bearer XXXX'

{
  "movie": {
    "id": 1,
    "release_date": "Mon, 06 May 2019 00:00:00 GMT",
    "title": "Transformers"
  },
  "success": true
}


POST '/movies'

Shell:

curl http://127.0.0.1:5000/movies \
  -X POST -H "Content-Type: application/json" -d '{ "title": "Transformers", "release_date": "2007-05-06" }' \
  --header 'Authorization: Bearer XXXX'

{
  "movie": {
    "id": 3,
    "release_date": "Wed, 06 May 2007 00:00:00 GMT",
    "title": "Transformers"
  },
  "success": true
}

PATCH '/movies/<int:movie_id>'

Shell:
curl http://127.0.0.1:5000/movies/3 \
  -X POST -H "Content-Type: application/json" -d '{ "title": "Teenage Mutant Ninja Turtles", "release_date": "2014-05-06" }' \
  --header 'Authorization: Bearer XXXX'

{
  "movie": {
    "id": 3,
    "release_date": "Wed, 06 May 2014 00:00:00 GMT",
    "title": "Teenage Mutant Ninja Turtles"
  },
  "success": true
}

DELETE '/movies/<int:movie_id>'

Shell:
curl http://127.0.0.1:5000/movies/3 \
  -X DELETE \
  --header 'Authorization: Bearer XXXX'

{
  "message": "movie id 3, titled Transformers was deleted",
  "success": true
}

`````
## Testing

To run the tests, cd into `/src` and run in your terminal

```bash

python test.py
`````

All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to config Auth0 accordingly

### Auth0 for locally use
#### Create an App & API

1. Login to https://manage.auth0.com/
2. Click on Applications Tab
3. Create Application
4. Give it a name like `casting` and select "Regular Web Application"
5. Go to Settings and find `domain`. Copy & paste it into config.py => auth0_config['AUTH0_DOMAIN'] (i.e. replace `"zruxi.auth0.com"`)
6. Click on API Tab
7. Create a new API:
   1. Name: `casting`
   2. Identifier `casting`
   3. Keep Algorithm as it is
8. Go to Settings and find `Identifier`. Copy & paste it into config.py => auth0_config['API_AUDIENCE'] (i.e. replace `"casting"`)

#### Create Roles & Permissions

1. Before creating `Roles & Permissions`, you need to `Enable RBAC` in your API (API => Click on your API Name => Settings = Enable RBAC => Save)
2. Also, check the button `Add Permissions in the Access Token`.
2. First, create a new Role under `Users and Roles` => `Roles` => `Create Roles`
3. Give it a descriptive name like `Casting Assistant`.
4. Go back to the API Tab and find your newly created API. Click on Permissions.
5. Create & assign all needed permissions accordingly
6. After you created all permissions this app needs, go back to `Users and Roles` => `Roles` and select the role you recently created.
6. Under `Permissions`, assign all permissions you want this role to have.

# <a name="authentification-bearer"></a>
### Auth0 to use existing API
If you want to access the real, temporary API, bearer tokens for all 3 roles are included in the `config.py` file.

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (read:actors): Can see all actors
  - GET /movies (read:movies): Can see all movies
2. Casting Director:
  - GET /actors (read:actors): Can see all actors
  - GET /movies (read:movies): Can see all movies
  - POST /actors (create:actors): Can create new Actors
  - PATCH /actors (edit:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (edit:movies): Can edit existing Movies
3. Exectutive Dircector:
  - GET /actors (read:actors): Can see all actors
  - GET /movies (read:movies): Can see all movies
  - POST /movies (create:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Motives from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).

For example: (Bearer token for `Executive Director`)
```js
{
    "Authorization": "Bearer XXXX"
}
```
