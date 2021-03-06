import autograd.numpy as np
import autograd.numpy.random as npr
from autograd.util import *
from autograd import grad
import warnings
npr.seed(1)

def test_grad_fanout():
    fun = lambda x : np.sin(np.sin(x) + np.sin(x))
    df = grad(fun)
    check_grads(fun, npr.randn())
    check_grads(df, npr.rand())

def test_grad_const():
    fun = lambda x : 1
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("ignore")
        df = grad(fun)
        assert np.allclose(df(2.0), 0.0)

def test_grad_identity():
    fun = lambda x : x
    df = grad(fun)
    ddf = grad(df)
    assert np.allclose(df(2.0), 1.0)
    assert np.allclose(ddf(2.0), 0.0)

def test_hess_vector_prod():
    npr.seed(1)
    randv = npr.randn(10)
    def fun(x):
        return np.sin(np.dot(x, randv))
    df = grad(fun)
    def vector_product(x, v):
        return np.sin(np.dot(v, df(x)))
    ddf = grad(vector_product)
    A = npr.randn(10)
    B = npr.randn(10)
    check_grads(fun, A)
    check_grads(vector_product, A, B)

def test_enclosing_scope_ref():
    def fun(x):
        inner_fun = lambda y : x * y
        return x * grad(inner_fun)(2.0)
    check_grads(fun, 1.0)

def test_enclosing_scope_ref_2():
    def fun(x):
        inner_fun = lambda y : y * x
        return x * grad(inner_fun)(2.0)
    check_grads(fun, 1.0)

def test_mutating_outgrad():
    def fun(a):
        b = a + 1.0
        c = b + 1.5
        d = a + b
        e = d + c
        return to_scalar(e)

    A = npr.randn(5)
    check_grads(fun, A)

def test_mutating_outgrad_from_indexing():
    def fun(a):
        b = a + 1.0
        c = b[0] + 1.5
        d = a + b
        e = d + c
        return to_scalar(e)

    A = npr.randn(5)
    check_grads(fun, A)

# TODO:
# Grad three or more, wrt different args
# Diamond patterns
# Taking grad again after returning const
# Empty functions
# 2nd derivatives with fanout, thinking about the outgrad adder
