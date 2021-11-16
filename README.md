# bdsm
Bachelor Data Science Modelling (BDSM) Development of a collection of methods and datasets for Data Science as Python Package

## Getting started

### pip
To install all required dependencies, use following command in your local environment:

```shell
$ pip install -r requirements.txt
```

### conda
You can also use conda to create a new environment using the required dependencies. We suggest using [miniforge](https://github.com/conda-forge/miniforge) as your installer of choice for conda.

Please use following command to create a new _bdsm_ environment:

```shell
(base)$ conda create -n bdsm --file requirements.txt -c conda-forge
```

You can also install all required dependencies in an existing environment:

```shell
(foo-env)$ conda install --file requirements.txt -c conda-forge
```
