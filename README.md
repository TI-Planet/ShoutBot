<h1 align="center">Welcome to ShoutBot 👋</h1>
<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
  <a href="/license" target="_blank">
    <img alt="License: GPL--3.0" src="https://img.shields.io/badge/License-GPL--3.0-yellow.svg" />
  </a>
</p>

This project is a bridge between TI-Planet shoutbox and Discord

## Contribute: 

If you find a bug, or want some feature you can open an [issue](https://github.com/LeGmask/ShoutBot/issues/new/choose). Otherwise you could create a pull request, and if the pull request is good we can think about merging it.

## Setup:

### Requirements

For this bot you need to install `python3.8`, `pip` and `poetry`. There is also a [docker](#docker) for easy deployment.

- For latex you will need:
  - A LaTeX distribution such as [TeX Live](https://www.tug.org/texlive/) or [MiKTeX](https://miktex.org/)
  - `pdfcrop`
  - `pnmtopng`
  - `pdftoppm`

### Install

You need to setup dependencies, in your terminal run :

```sh
poetry install
```

### Config

For setting up the bot, you need :

-   A Discord bot
-   A TI-Planet account
-   A webhook in your shoutbox Discord channel

In `config.json` you will find every common settings that are not private.

In `.env` you will find settings that are private such as your Discord bot token, your wehbook id and token, or your TI-Planet account.

### Usage

To run the server, run in your terminal :

```sh
poetry run python main.py
```

### Docker

You can easily setup this project using docker:

1. First download `docker-compose.yml` and `config.js` and default `.env`;
2. Edit settings depending on your server (see [config](#config) part);
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

## Licence

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
See [license](license) for details.
