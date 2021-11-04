# coverage-specificity

how to install

```
pip install git+ssh://git@github.com/goxan/coverage-specificity.git
```

how to use
```python
from sklearn.datasets import make_blobs
X, y = make_blobs(n_samples=1000, centers=3,␣
,→n_features=2,random_state=0,cluster_std=0.4)
cs = CoverageSpecificity(X)
max_points = cs.draw_valid()
kmean = KMeans(n_clusters=3)
kmean = kmean.fit(X)
rs=cs.cov_sp(kmean.cluster_centers_, 3)
cs.granulas(kmean.cluster_centers_, 2, rs)
```
