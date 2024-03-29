# route-finder

![last commit](https://img.shields.io/github/last-commit/joycebyun/route-finder "last commit")
![tests](tests-badge.svg "tests")
![coverage](coverage-badge.svg "coverage")
[![linting](https://img.shields.io/badge/linting-pylama-informational)](https://github.com/klen/pylama)

Given a maximum run distance and a starting location, `route-finder` generates a running route that aims to maximize the number of new locations visited.

## Description

`route-finder` uses map data from [OpenStreetMap](https://www.openstreetmap.org) (OSM), which is retrieved and analyzed using the Python package [`osmnx`](https://github.com/gboeing/osmnx/). 
Using `osmnx`, the map data is represented as a graph data structure, consisting of nodes (points on the map) that are connected by edges (roads, streets, paths, etc).

Given a maximum run distance and a starting location, `route-finder` generates a running route that aims to maximize the number of new nodes visited. The generated route starts and ends at the same location, and its total distance is less than the input maximum distance.

(In graph terminology, `route-finder` works on a weighted undirected graph, and generates a closed walk that aims to maximizes the number of new nodes visited, while keeping the total weight less than the input maximum.)

This project includes two [algorithms](#algorithms) for generating a route under these constraints.

## Why?

Running around my neighborhood and city is my preferred way of getting to know the area where I live. 
I don't think I'm the only one&mdash;[CityStrides](https://citystrides.com) is an online community of runners who are tracking the places they have explored on foot.
Using CityStrides made me look forward to my runs even more, because I could easily see where I had already been and plan routes to explore new areas.
There is also a competitive aspect to CityStrides: for each city, runners are ranked by how many streets have been "completed".

I started planning my runs manually by looking at a map of nodes, and guessing which route would take me to the largest number of new nodes.
After I learned about graph data structures and graph algorithms, I started to wonder whether there was a better way to make routes.
Could I use an algorithm to plan my runs for me?
This project is my attempt at developing a graph algorithm to find routes that explore my city more efficiently.

## Requirements

Running this project requires installations of:
1. [Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/stable/index.html)
2. [`osmnx`](https://github.com/gboeing/osmnx/)

The recommended way to get the requirements is by installing [Docker](https://www.docker.com/products/docker-desktop/) and running the unofficial public Docker [image](https://hub.docker.com/r/gboeing/osmnx) created by the owner of `osmnx`.
Everything that is needed to run this project is included in this Docker container environment, and there is no need to separately install Jupyter Notebook and `osmnx`.

Alternatively, it is possible to install Jupyter Notebook and `osmnx` using [Anaconda](https://www.anaconda.com/products/distribution) or `pip`. 
See [here](https://docs.jupyter.org/en/latest/install/notebook-classic.html) and [here](https://osmnx.readthedocs.io/en/stable/#installation) for details.

## Usage

**Note:** The instructions here assume that Docker has been installed.

First, open a new terminal, and clone this repository:

`git clone https://github.com/joycebyun/route-finder.git`

Go into the repository's main directory, and run the Docker container:

`cd route-finder`

`docker run --rm -it -p 8888:8888 -v "$PWD":/home/jovyan/work gboeing/osmnx:latest /bin/bash`

This will start a new terminal session inside the container. 
From the new terminal, start Jupyter Notebook:

`jupyter notebook`

There will be many lines output to the terminal, but the important piece is the URL that begins with "`http://127.0.0.1:8888/`".
Copy and past this full URL to a web browser.

The web browser will show all of the files in your current directory. Click on `Route_finder.ipynb`.


## Algorithms

:construction_worker: *Under construction* :construction:

## License

This project is licensed under the terms of the MIT license.

## Code style

To aim for a consistent style in the source code, I used the [`Pylama`](https://github.com/klen/pylama) code auditing tool.

After it's installed (e.g. `pip install pylama`), in a terminal, navigate to the `src/` directory and run `pylama`.


## Documentation

The documentation can be generated from docstrings within the source code using [Sphinx](https://www.sphinx-doc.org/) and a built-in extension called *autodoc*.

To use Sphinx, after it's installed (e.g. `pip install sphinx`), running `sphinx-quickstart` in the terminal will do most of the set up for me, including creating the `conf.py` that contains the default configuration settings and creating the root documentation file `index.rst`. Additional pages are added to the docs through additional `docs/*.rst` files, one per module.

To re-generate the docs after source code changes, go to the `docs/` directory and run `make clean` and `make html`. The documentation can then be viewed by opening `docs/_build/index.html` in a web browser.

## Acknowledgements

Many other developer tools and Python packages helped in the development of this project, such as:
- [VS Code](https://code.visualstudio.com)
- [`pytest`](https://docs.pytest.org/en/7.2.x/) and [`pytest-cov`](https://github.com/pytest-dev/pytest-cov) for testing and coverage
- [`Pylama`](https://github.com/klen/pylama) for checking code style and quality
- [`shields.io`](https://shields.io) and [`genbadge`](https://github.com/smarie/python-genbadge) for making the badges in this readme
- [Sphinx](https://www.sphinx-doc.org/) for automatically generating documentation from docstrings in reStructuredText (reST) format
