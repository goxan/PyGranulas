# PyGranulas


This python library provide functionality related to computing and plotting coverage, specificity and information granulas. For more details, please refer to the book: 

Yao, Jingtao & Vasilakos, Athanasios & Pedrycz, Witold. (2013). Granular Computing: Perspectives and Challenges. IEEE transactions on cybernetics. 43. 10.1109/TSMCC.2012.2236648.   

How to install

```
pip install coverage-specificity
```

How to use
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
