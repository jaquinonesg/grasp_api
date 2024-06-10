<h1 align="center">Welcome to grasp_api 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
</p>

> A small api to receive Pub/Sub data from sensors

## Prerequisites
# To run local
* Python > 3.11
* Poetry
* PostgreSQL (Migth need SSL and async configurations depending on your OS)
* Create a api.env and a terraform.env files, can be done copy pasting the current information on params.example.api.env and params.example.terraform.env
* Update the variables in the .env files to fit your local setup

* Docker if you choose that path

## Install dependencies
```sh
make install
```

## Run local

* Make sure to create the database according to your api.env data.

```sh
make migrate
```

```sh
make run/devserver
```

## Run using docker
```sh
make run/dockerized
```

## Once the project is running go to:
```sh
http://localhost:8080/docs
```
For interacting with the API using swagger.

## Run tests

```sh
make unittests
```


## Run formatter

```sh
make format
```


## Run linting and test

```sh
make test
```



## Author

👤 **Jorge Quinones**

* Github: [@jaquinonesg](https://github.com/jaquinonesg)
* LinkedIn: [@https:\/\/www.linkedin.com\/in\/jaquinonesg\/](https://linkedin.com/in/https:\/\/www.linkedin.com\/in\/jaquinonesg\/)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
