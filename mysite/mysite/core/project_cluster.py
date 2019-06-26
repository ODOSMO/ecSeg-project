import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.cluster.hierarchy import dendrogram, linkage, to_tree

def draw_tree( matrix_file ):
    df = pd.read_csv(matrix_file, sep = '\t')
    df.set_index('sample',inplace=True)
    print df
    name = df.columns.values
    # convert it into a condensed matrix
    keep = np.triu(np.ones(df.shape)).astype('bool').reshape(df.size)
    #print keep
    df_cdm = df.stack()[keep].reset_index()
    df_cdm.columns = ['row','column','value']
    drop_list = []
    for index,row in df_cdm.iterrows():
        if row['row'] == row['column']:
	    drop_list.append(index)
    df_cdm.drop(df_cdm.index[drop_list],inplace=True)
    print df_cdm

    cdm = df_cdm['value'].values
    linked = linkage(cdm,method = 'ward')
    plt.figure(figsize=(16,10))
    ddata = dendrogram(linked,labels = name, orientation='top',distance_sort='ascending',show_leaf_counts=True)
    for i, d in zip(ddata['icoord'], ddata['dcoord']):
        x = 0.5 * sum(i[1:3])
        y = d[1]
        plt.plot(x, y, 'ro')
        plt.annotate("%.3g" % y, (x, y), xytext=(0, -8),
                         textcoords='offset points',
                         va='top', ha='center')
    #plt.show()
    qname = matrix_file.split('.')[0]+'.png'
    plt.savefig(qname)
    return qname

if __name__ == '__main__':
    draw_tree( 'result/test/dist-q1.txt')
