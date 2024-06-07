<h1 align="center">Welcome to template_fastapi 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
</p>

> A template for my fastapi projects

## Prerequisites
# To run local
* Python > 3.11
* Poetry
* PostgreSQL (Migth need SSL and async configurations depending on your OS)
* Create a .env file, can be done copy pasting the current information on params.example.env

* Docker if you choose that path

## Install dependencies
```sh
make install
```

## Run local

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

## Run tests

```sh
make unittest
```

## Run linting and test

```sh
make test
```


## Run formatter

```sh
make format
```


## Author

👤 **Jorge Quinones**

* Github: [@jaquinonesg](https://github.com/jaquinonesg)
* LinkedIn: [@https:\/\/www.linkedin.com\/in\/jaquinonesg\/](https://linkedin.com/in/https:\/\/www.linkedin.com\/in\/jaquinonesg\/)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
