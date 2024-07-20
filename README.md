# Elect.Gen Back End

This repository is a service of the
[Elect.Gen](https://gitlab.pg.innopolis.university/sdr-sum24/elect-gen) project.
Navigate there to learn more.

## 🧰 Tooling

Here are some technologies used in this project:

- 🐍 Programming language: [Python](https://github.com/python/cpython)
- 📦 Package manager: [Poetry](https://github.com/python-poetry/poetry)
- 🗲 Back-end framework: [FastAPI](https://github.com/postgres/postgres)
- 🐘 Database: [PostgreSQL](https://github.com/postgres/postgres)
- 🖌️ Code formatter: [Ruff](https://github.com/astral-sh/ruff)
- 🧠 Code linter: [Ruff](https://github.com/astral-sh/ruff)
- 😎 Language server: [Basedpyright](https://github.com/detachhead/basedpyright)

## 🖥️ Launch locally

<details open>
<summary open>
<b>Clone the entire project (recommended):</b>
</summary>

### Clone the main repository

For example, you can do it via HTTPS:

```shell
git clone --recurse-submodules https://github.com/quintet-sdr/elect-gen.git
```

### Open the back end directory

```shell
cd elect-gen/services/backend/
```

</details>

<details>
<summary>
<b>Clone the back end only:</b>
</summary>

> We recommend you not follow this option.

### Clone the back end repository

For example, you can do it via HTTPS:

```shell
git clone https://github.com/quintet-sdr/elect-gen.git
```

### Open the cloned directory

```shell
cd elect-gen-backend/
```

</details>

### Create a Python virtual environment

```shell
python -m venv .venv/
```

### Activate the virtual environment

Note: this command depends on your command shell.

#### Example for Bash/Zsh

```shell
source .venv/bin/activate
```

### Install dependencies

> Make sure you activated your virtual environment!

#### You only need to install Poetry by yourself

```shell
pip install poetry
```

#### Then, the command below will take care of the rest

```shell
poetry install
```

### Run the application

To launch the back end, you need to run the `start` Poetry script. It requires
you to enter the path to a directory containing [Elect.Gen Core](https://gitlab.pg.innopolis.university/sdr-sum24/elect-gen-core).

```shell
poetry run start ../core/
```

You can also start a development server with the `dev` script, which enables
hot reload.

```shell
poetry run dev ../core/
```

Both commands support additional CLI arguments.

```shell
poetry run <SCRIPT> --host 1.2.3.4 --port 5 path/to/elect-gen-core
```

You can read their descriptions using the `--help` argument.

```shell
poetry run <SCRIPT> --help
```

## 📄 License

=======

The project is licensed under the [MIT License](/LICENSE).

(c) [SDR](https://gitlab.pg.innopolis.university/sdr-sum24/) /
[Innopolis University](https://innopolis.university/en/). All rights reserved.
