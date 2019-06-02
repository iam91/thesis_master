import numpy as np
from sklearn.mixture import GaussianMixture

if __name__ == '__main__':

    data = np.genfromtxt('data.csv', delimiter=',')
    p = np.arange(0, 1.01, 0.01)

    q = np.quantile(data, p)
    np.savetxt("./result/eq.csv", q, delimiter=",", fmt='%15.6f')

    gmm = GaussianMixture(7, covariance_type='spherical')
    gmm.fit(data.reshape(len(data), 1))

    w = ','.join(gmm.weights_.astype(str))
    m = ','.join(gmm.means_.reshape(1, len(gmm.means_))[0].astype(str))
    c = ','.join(gmm.covariances_.astype(str))

    print w 
    print m 
    print c 
