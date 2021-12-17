# PyGranulas


This python library provide functionality related to computing and plotting coverage, specificity and information granulas. For more details, please refer to the book: 

[Download](https://www.researchgate.net/profile/Jingtao-Yao-2/publication/237148111_Granular_Computing_Perspectives_and_Challenges/links/54468d290cf2f14fb80f53b8/Granular-Computing-Perspectives-and-Challenges.pdf) Yao, Jingtao & Vasilakos, Athanasios & Pedrycz, Witold. (2013). Granular Computing: Perspectives and Challenges. IEEE transactions on cybernetics. 43. 10.1109/TSMCC.2012.2236648.   


- [Environment Requirements](#environment-requirements)
- [Getting Started](#getting-started)
- [How it Works](#how-it-works)
- [Contributing](#contributing)
- [Licensing](#licensing)

>> Disclaimer: This library is not tested on Windows. If you are using Windows, then it's recommended to install Linux Subsystem to make it easier to run this project.

# Environment Requirements

In order to use this library locally, you will need the following set up.

- Python >=3.6 (https://www.python.org/downloads/)
- Virtualenv *

* Pro tip: You can setup a virtual environment to install the library dependencies. Follow [this guide](https://docs.python-guide.org/dev/virtualenvs/) to set up a virtual environment.

After you're done with the above environment set up, please proceed to dependency installation step below.

>> Keep in mind that if you set up a virtual environment in the way described above, the virtual environment will be scoped to the current terminal session. This means that every time you open a new terminal for this project, you will need to activate the virtual environment for the current terminal session.

# Getting Started
Create a new project and install the library.
Run the following commands one at a time.

## Install the library
```sh
$ mkdir pygranulas-example
$ cd pygranulas-example
```

```sh
pygranulas-example:~$ virtualenv venv && source venv/bin/activate
pygranulas-example:~$ pip3 install coverage-specificity
```

## How to use
Quickly test the library in a python interactive shell. Run the command below to start the shell.
```sh
pygranulas-example:~$ ipython
```

Next, copy and run the snippets below in the interactive shell.
1. Create dataset or import an existing one
```python
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

X, y = make_blobs(n_samples=1000, centers=3,n_features=2,random_state=0,cluster_std=0.4)
```
2. Import library
```python
from coverage_specificity import CoverageSpecificity
```
3. Initialize Coverage specificity Object

```python
cs = CoverageSpecificity(X)
```
4. For a given dataset draw optimal number of clusters according to several validity indexes
```python
max_points = cs.draw_valid()
```
Expected result
![Expected result](https://res.cloudinary.com/dvx16m14w/image/upload/v1638892041/Screenshot_from_2021-12-07_18-42-52_kgxicg.png)
5. After deciding best value of clusters create cluster's centers using any clustering technique, in this example we use KMeans with 3 cluster
```python
kmean = KMeans(n_clusters=3)
kmean = kmean.fit(X)
rs, cv_sp_dict =cs.cov_sp(kmean.cluster_centers_, 3)
```
Expected result
![Expected result 2](https://res.cloudinary.com/dvx16m14w/image/upload/v1638897479/image_2021-12-07_201756_o08yoi.png)
6. Show information granulas information. _Note_: Right now for granulas representation library support only 2-dimensional data
```python
cs.granulas(kmean.cluster_centers_, rs, cv_sp_dict)
```
![Expected result 3](https://res.cloudinary.com/dvx16m14w/image/upload/v1638897623/image_2021-12-07_202020_vctdda.png)

# How it Works

# Contributing

To contribute, fork the repository, set up your environment, create an issue with describing the changes you want to make, make changes, send us a pull request referencing that issue. We will review your changes and apply them to the main branch:

# Licensing

This project's license is TBD.
