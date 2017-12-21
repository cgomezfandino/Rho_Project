import numpy as np
import seaborn as sns
import pandas as pd
from scipy import stats
import scipy.cluster.hierarchy as hac
from scipy.cluster.hierarchy import fcluster

import matplotlib.pyplot as plt

#
# build 6 time series groups for testing, called: a, b, c, d, e, f
#

num_samples = 61
group_size = 10

#
# create the main time series for each group
#

x = np.linspace(0, 5, num_samples)
scale = 4

a = scale * np.sin(x)
b = scale * (np.cos(1+x*3) + np.linspace(0, 1, num_samples))
c = scale * (np.sin(2+x*6) + np.linspace(0, -1, num_samples))
d = scale * (np.cos(3+x*9) + np.linspace(0, 4, num_samples))
e = scale * (np.sin(4+x*12) + np.linspace(0, -4, num_samples))
f = scale * np.cos(x)

#
# from each main series build 'group_size' series
#

timeSeries = pd.DataFrame()
ax = None
for arr in [a,b,c,d,e,f]:
    arr = arr + np.random.rand(group_size, num_samples) + np.random.randn(group_size, 1)
    df = pd.DataFrame(arr)
    timeSeries = timeSeries.append(df)

    # We use seaborn to plot what we have
    #ax = sns.tsplot(ax=ax, data=df.values, ci=[68, 95])
    ax = sns.tsplot(ax=ax, data=df.values, err_style="unit_traces")

plt.show()

print(timeSeries.shape)


# Now we do the clustering and plot it:

Z = hac.linkage(timeSeries, 'single', 'correlation')


plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
hac.dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.show()

# To retrieve the Clusters we can use the fcluster function.
#  It can be run in multiple ways (check the documentation) but in this
# example we'll give it as target the number of clusters we want:

def print_clusters(timeSeries, Z, k, plot=False, plot_threshold=5):
    # k Number of clusters I'd like to extract
    results = fcluster(Z, k, criterion='maxclust')

    # check the results
    s = pd.Series(results)
    clusters = s.unique()

    for c in clusters:
        cluster_indeces = s[s==c].index
        cluster_size = len(cluster_indeces)
        print("Cluster %d number of entries %d" % (c, cluster_size))
        if plot and cluster_size > plot_threshold:
            cluster_series = timeSeries.T.iloc[:,cluster_indeces]
            #cluster_series.plot(legend=False)
            sns.tsplot(data=cluster_series.T.values, err_style="unit_traces")
            plt.show()

print_clusters(timeSeries, Z, 6, plot=True)


# If we already have the correlation matrix, or if we want to decide what kind of correlation to apply,
# then we can do the following:

correlation_matrix = timeSeries.T.corr(method='spearman')
correlation_matrix.shape

sns.heatmap(correlation_matrix)

distance = (1 - correlation_matrix) # Compute the distance from the correlation
Z = hac.linkage(distance, method='average', metric='euclidean')

plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
hac.dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.show()

print_clusters(timeSeries, Z, 6, plot=False)

# Finally, if we need to creare our own distance function, we can do the following:

# Here we use spearman correlation
def my_metric(x, y):
    r = stats.pearsonr(x, y)[0]
    return 1 - r # correlation to distance: range 0 to 2

# Do the clustering
Z = hac.linkage(timeSeries,  method='single', metric=my_metric)

plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
hac.dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.show()

print_clusters(timeSeries, Z, 6, plot=False)

