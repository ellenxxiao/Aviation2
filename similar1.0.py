import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import gower
from sklearn.preprocessing import scale,StandardScaler
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

df = pd.read_csv('/Users/ellenxiao/Documents/Udemy/cocktail/cocktail_clean1.0.csv')

print('Number of Rows: ',df.shape[0])
print('Number of Columns: ', df.shape[1])
print('Features: \n', df.columns.tolist())
print('Number of null value: ', df.isnull().sum().values.sum())
print('Unique values: \n', df.nunique())

df_count = pd.DataFrame(df.nunique(),columns=['Count'])
df_count.plot(kind='bar',color='plum')

num_features = ['rum', 'grain alcohol', 'vodka', 'brandy', 'bitters',
       'campari', 'whiskey', 'beer', 'soda', 'syrup', 'champagne', 'coke', 'milk', 'coffee',
       'wine', 'gin', 'tequila', 'yoghurt']

cat_features = []
for col in df.columns:
    if col not in num_features:
        cat_features.append(col)

# scale standardization of numerical values
df_num = pd.DataFrame(StandardScaler().fit_transform(df[num_features]),columns=num_features)
df_cat = df.drop(columns=num_features)
df_std = df_cat.merge(df_num,left_index=True,right_index=True,how='left')
df_w_name = df_std
df_w_name.head()
df_std = df.set_index('DrinkName')

# generate similarity matrix
distance_matrix = gower.gower_matrix(df_std)
#create complete linkage
Zd = linkage(distance_matrix,method='complete') 

# hierarchical clustering visulization
fig,axs = plt.subplots(1,1,figsize=(25,5))
dn = dendrogram(Zd, truncate_mode='level',p=6,show_leaf_counts=True,ax=axs)

# find optimal k clusters
results = {}
for k in range(2,12):
    cluster_array = fcluster(Zd,k,criterion='maxclust')
    score = silhouette_score(distance_matrix,cluster_array,metric='precomputed')
    results[k] = score

plt.plot([i for i in results.keys()],[j for j in results.values()],label='gower')
plt.xticks(range(1,12))

# select k = 5
k = 5
df_std['cluster'] = fcluster(Zd,k,criterion='maxclust')

pca = PCA(n_components=2)
pca_results = pca.fit_transform(df_std)
df_pca = pd.DataFrame(data=pca_results,columns=['PC1','PC2'])
x = pca_results[:,0]
y = pca_results[:,1]
plt.scatter(x,y,c=df_std['cluster'])
plt.xlim([-2,2])
plt.ylim([-2,2])
plt.show()

# visualization using t-sne
tsne = TSNE(n_components=2, verbose=1, perplexity=10, n_iter=300)
tsne_results = tsne.fit_transform(df_std)
df_tsne = pd.DataFrame(data=tsne_results,columns=['TSNE1','TSNE2'])
x = tsne_results[:,0]
y = tsne_results[:,1]
plt.scatter(x,y,c=df_std['cluster'])
plt.show()


# find similar cocktails
def find_similar(row,k):
    n_similar = gower.gower_topn(df_std.iloc[row:row+1,:],df_std,n=k)
    similar_cocktails = []
    distance = list(n_similar['values'])
    for i in n_similar['index']:
        similar_cocktails.append(df_w_name.iloc[i,0])
    similar_cocktails = similar_cocktails[1:]
    return similar_cocktails

df_similar = pd.DataFrame()
for i,row in df_w_name.iterrows():
    df_similar[row['DrinkName']] = find_similar(i,6)
df_similar_t = df_similar.T
df_similar_t.columns = ['top 1','top 2','top 3','top 4','top 5']

#df_similar_t.to_csv('/Users/ellenxiao/Documents/Udemy/cocktail/cocktail_similar.csv')

find_similar_cocktail = input("What cocktails is similar to ...? Just enter a cocktail name: ")
print(df_similar_t.loc[find_similar_cocktail])
