<h1 align="center">Welcome to ShoutBot 👋</h1>
<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
  <a href="/license" target="_blank">
    <img alt="License: GPL--3.0" src="https://img.shields.io/badge/License-GPL--3.0-yellow.svg" />
  </a>
</p>

This project is a bridge between tiplanet shoutbox and discord

## Setup :

### Requirements:

For this bot you need to install `python3.8`, `pip` and `poetry`. There is also a [docker](#docker) for easy deployment.

### Install

You need to setup dependencies, in your terminal run :

```sh
poetry install
```

### Config

For setting up the bot, you need :

-   A discord bot
-   A tiplanet account
-   A webhook in your shoutbox discord channel

In `config.json` you will find every common settings that are not private.

In `.env` you will find settings that are private such as your Discord bot token, your wehbook id and token, or your tiplanet account.

### Usage

To run the server, run in your terminal :

```sh
poetry run python main.py
```

### Docker

You can easly setup this project using docker:

1. First download `docker-compose.yml` and `config.js` and default `.env`;
2. Edit settings in function of your server (see [config](#config) part);
3. Run the docker using the following command :

-   run in foreground:

```sh
docker-compose up
```

-   run in background:

```sh
docker-compose up -d
```

_if you need more help see the docker documentation_

<!-- For updating the container:
```sh
docker-compose pull
``` -->
## Contribute : 

You can open an [issue](https://github.com/LeGmask/NotWistaBot/issues/new/choose), or you can fork and open a pull request

## Licence

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
See [license](license) for details.
