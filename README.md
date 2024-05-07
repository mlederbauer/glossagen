![Project Logo](assets/banner.png)

[![Code style: ruff-format](https://img.shields.io/badge/code%20style-ruff_format-6340ac.svg)](https://github.com/astral-sh/ruff)
![Coverage Status](https://raw.githubusercontent.com/mlederbauer/glossagen/main/coverage-badge.svg)

<h1 align="center">
GlossaGen
</h1>

<br>


creating a glossary out of scholarly materials and chemistry reviews

## 🔥 Usage

Run `GlossaGen` to extract your first set of terms from a research paper about dentistry and zeolithes (interesting!):
```
glossagen # this runs the program with the default paper
glossagen path/to/directory/containing/paper # as of now, the paper must be called paper.pdf
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
```

## 🛠️ Development installation

To install, run

```
(conda_env) $ pip install -e ".[test,doc]"
```

To run style checks:

```
(conda_env) $ pip install pre-commit
(conda_env) $ pre-commit run -a
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


