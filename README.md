<p align="center">
  <img src="assets/glossagen-logo.png" width="200">
</p>

[![Code style: ruff-format](https://img.shields.io/badge/code%20style-ruff_format-6340ac.svg)](https://github.com/astral-sh/ruff)
![Coverage Status](https://raw.githubusercontent.com/mlederbauer/glossagen/main/coverage-badge.svg)

<h1 align="center">
GlossaGen
</h1>

<br>


creating a glossary out of scholarly materials and chemistry reviews

## 🔥 Usage

Run `GlossaGen` to extract a glossary table from the command line:
```
glossagen # runs the program with the default paper
glossagen path/to/directory/containing/paper # the paper must be called paper.pdf
```

## 👩‍💻 Installation

Create a new environment, you may also give the environment a different name. 

```
conda create -n glossagen python=3.10 
```

```
conda activate glossagen
```

! IMPORTANT: Make sure you have a `.env` file in your project directory, where you add your `OPENAI_API_KEY`.
```
# content of the .env file
OPENAI_API_KEY=sk-foo

# if you plan to generate knowledge graphs as well, provide the Neo4J and Groq Credentials as well
NEO4J_URI=neo4j+s://foo
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=foo
GROQ_API_KEY=gsk_foo
```

## Demo

This project is part of the 2024 LLM Hackathon for Materials and Chemistry.
Find the public submission of our project – including a product demo – here:
(ADD TWITTER LINK)

## 🛠️ Development installation

To install, run

```
(conda_env) $ pip install -e ".[test,doc]"
```

### Run style checks, coverage, and tests

```
(conda_env) $ pip install tox
(conda_env) $ tox
```

### Generate coverage badge

Works after running `tox`

```
(conda_env) $ pip install "genbadge[coverage]"
(conda_env) $ genbadge coverage -i coverage.xml
```


