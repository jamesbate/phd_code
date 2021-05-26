import numpy as np

def H(p_vec):
    #if p_vec = 0, no contributino to sum 
    p_vec = p_vec[p_vec != 0]
    return -np.sum(p_vec*np.log2(p_vec))

def H_joint(p_mat):
    #P_ij is now a matrix p(vec0[i], vec1[j])
    #columns should be set of values the first element of random vector can take on 

    #reshape and mask to get rid of 0's (which scres up logarithm)
    p_mat = p_mat.reshape(1,p_mat.size)
    p_mat = p_mat[p_mat != 0]
    return -np.sum(p_mat*np.log2(p_mat))

def H_cond(p_mat_XY):
    #returns (H(X|Y), H(Y|X))
    (p_vec_X, p_vec_Y) = marginalise(p_mat_XY)
    return (np.array([H(j) for j in p_mat_XY]).dot(p_vec_X), np.array([H(j) for j in p_mat_XY.T]).dot(p_vec_Y))
    #forgot to renormalise probability

def marginalise(p_mat):
    return (np.sum(p_mat, axis = 1), np.sum(p_mat, axis = 0))
