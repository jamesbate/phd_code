"""
This module provides an implementation for state vectors.

The relevant classes are:
    * :class:`StateVector`
    * :class:`StateVectorTrajectory`

The :class:`StateVector` represents a state vector at a specific point of time
while the :class:`StateVectorTrajectory` represents a state vector at different
points of time.
"""

import numpy
from . import expvalues
from . import visualization
try:
    set()
except NameError:
    from sets import Set as set

class StateVector(numpy.ndarray):
    r"""
    A class representing a quantum mechanical state vector in a specific basis.

    *Usage*
        >>> sv = StateVector((1, 3, 7, 2), time=0.2, norm=True)
        >>> sv = StateVector(numpy.arange(12).reshape(3,4))
        >>> print sv
        StateVector(3 x 4)
        >>> print repr(sv)
        StateVector([[ 0,  1,  2,  3],
               [ 4,  5,  6,  7],
               [ 8,  9, 10, 11]])

    *Arguments*
        * *data*
            Anything that can be used to create a numpy array, e.g. a nested
            tuple or another numpy array.

        * *time* (optional)
            A number defining the point of time when this state vector was
            reached. (Default is 0)

        * *norm* (optional)
            If set True the StateVector will be automatically normalized.
            (Default is False)
        
        * Any other argument that a numpy array takes. E.g. ``copy=False`` can
          be used so that the StateVector shares the data storage with the
          given numpy array.

    Most useful is maybe the tensor product which lets you easily calculate
    state vectors for combined systems::
        
        >>> sv1 = StateVector((1,2,3))
        >>> sv2 = StateVector((3,4,0), norm=True)
        >>> sv = sv1 ^ sv2
        >>> print sv
        StateVector(3 x 3)
        >>> print repr(sv)
        StateVector([[ 0.6,  0.8,  0. ],
               [ 1.2,  1.6,  0. ],
               [ 1.8,  2.4,  0. ]])

    The tensor product is abbreviated by the "^" operator. But be aware that
    this operator follows the built-in operator precedence - that means "+", 
    "*" etc. have **higher** precedence!
    """
    def __new__(cls, data, time=None, norm=False, **kwargs):
        array = numpy.array(data, **kwargs)
        if norm:
            array = normalize(array)
        array = numpy.asarray(array).view(cls)
        if time is not None:
            array.time = time
        elif hasattr(data, "time"):
            array.time = data.time
        return array

    def __array_finalize__(self, obj):
        self.dimensions = obj.shape
        self.time = getattr(obj, "time", 0)
    
    def __str__(self):
        clsname = self.__class__.__name__
        return "%s(%s)" % (clsname, " x ".join(map(str, self.dimensions)))

    def norm(self):
        r"""
        Calculate the norm of the StateVector.

        *Usage*
            >>> sv = StateVector((1,2,3,4,5), norm=True)
            >>> print sv.norm()
            1.0
        """
        return norm(self)

    def normalize(self):
        r"""
        Return a normalized StateVector.

        *Usage*
            >>> sv = StateVector((1,2,1,3,1))
            >>> print sv.norm()
            4.0
            >>> nsv = sv.normalize()
            >>> print nsv.norm()
            1.0
        """
        return normalize(self)

    def reduce(self, indices, norm=True):
        r"""
        Return a StateVector where the given indices are reduced.

        *Usage*
            >>> rsv = sv.reduce(1)
            >>> rsv = sv.reduce((1,2))

        *Arguments*
            * *indices*
                An integer or a list of integers specifying over which
                subspaces should be summated.

            * *norm* (optional)
                If set True the resulting StateVector will be renormalized.

        Reducing means nothing else then summing up over all given indices.
        E.g. a StateVector of rank 4 can be reduced to the first two indices::

            >>> sv1 = StateVector((1,2), norm=True)
            >>> sv2 = StateVector((1,2,3), norm=True)
            >>> sv3 = StateVector((1,2,3,4,5), norm=True)
            >>> sv4 = StateVector((1,2,3,4,5,6), norm=True)
            >>> sv = sv1^sv2^sv3^sv4
            >>> print sv
            StateVector(2 x 3 x 5 x 6)
            >>> print sv.reduce((2,3))
            StateVector(2 x 3)

        This is mathematically equivalent to:

            .. math::

                \Psi_{\alpha \beta} = \frac
                  {\sum_{\gamma \delta} \Psi_{\alpha \beta \gamma \delta}}
                  {\| \sum_{\gamma \delta} \Psi_{\alpha \beta \gamma \delta} \|}

        Reducing is an easy way to find out how subspaces of a high rank
        state vectors behave. Don't use reduced StateVectors for calculating
        expectation values - this will most likely give wrong answers!
        """
        if isinstance(indices, int):
            a = (indices,)
        else:
            a = _sorted_list(indices, True)
        array = self
        if norm:
            for i in a:
                array = array.sum(axis=i).normalize()
        else:
            for i in a:
                array = array.sum(axis=i)
        return array

    def reducesquare(self, indices):
        r"""
        Calculate the reduced Psi-square tensor.
        
        *Usage*
            >>> sv1 = StateVector((0,1,2,1,0), norm=True)
            >>> sv2 = StateVector((1,0,1), norm=True)
            >>> sv = sv1^sv2
            >>> sqtensor = sv.reducesquare(1)

        *Arguments*
            * *indices*
                An integer or a list of integers specifying over which
                subsystems should be summed up.

        This method calculates the following quantity (simplified for rank 2
        state vectors):

            .. math::

                w_{\alpha_1 \alpha_2} = \sum_\beta \Psi_{\alpha_1 \beta}^*
                                        \Psi_{\alpha_2 \beta}

        Where :math:`\beta` is the reduced index.

        This quantity is useful to calculate expectation values in the
        corresponding subspaces.
        """
        if isinstance(indices, int):
            a = (indices,)
        else:
            a = _sorted_list(indices, True)
        return numpy.tensordot(self, self.conjugate(), (a,a))

    def fft(self, axis=0):
        r"""
        Return a StateVector where the given axis is Fourier transformed.

        *Usage*
            >>> sv = StateVector((0,1,1.7,2,1.7,1,0), norm=True)
            >>> print sv.fft()
            StateVector(7)

        *Arguments*
            * *axis* (optional)
                Axis over which the fft is done. (Default is 0)
        """
        f = numpy.fft
        N = self.shape[axis]
        array = f.fftshift(f.ifft(f.ifftshift(self, axes=(axis,)), axis=axis),
                           axes=(axis,)) * N/numpy.sqrt(2*numpy.pi)
        return StateVector(array, time=self.time)

    def expvalue(self, operator, indices=None, title=None, multi=False):
        r"""
        Calculate the expectation value of the given operator.

        *Usage*
            >>> a = numpy.diag(numpy.ones(3), -1)
            >>> print a
            array([[ 0.,  0.,  0.,  0.],
                   [ 1.,  0.,  0.,  0.],
                   [ 0.,  1.,  0.,  0.],
                   [ 0.,  0.,  1.,  0.]])
            >>> sv = StateVector((1,2,1,2), norm=True)
            >>> print sv.expvalue(a)
            0.6

        *Arguments*
            * *operator*
                A tensor representing an arbitrary operator in the
                basis of the StateVector.

            * *indices* (optional)
                Specifies which subsystems should be taken. If None is given
                the whole system is used.

            * *multi* (optional)
                If multi is True it is assumed that a list of operators is
                given. (Default is False)

        Expectation values for combined systems are calculated in the following
        way (Assuming the operator only acts on first subsystem):

            .. math::

                \langle \Psi | \hat A (k) | \Psi \rangle =
                    \sum_{k_1 k_2} \langle k_1 | \hat A (k) | k_2 \rangle
                    \sum_m \Psi_{k_1 m}^* \Psi_{k_2 m}

        The second sum is exactly what :meth:`reducesquare` does while the
        first expression is the matrix representation of the given operator
        in the same basis as the StateVector.
        """
        if indices is not None:    
            A = self.reducesquare(_conjugate_indices(indices, self.ndim))
        else:
            A = self^self.conjugate()
        length = A.ndim
        index = list(range(0, length, 2)) + list(range(1, length, 2))
        if multi:
            evs = [(A*op.transpose(index)).sum() for op in operator]
            return expvalues.ExpectationValueCollection(evs, self.time, title)
        else:
            return (A*operator.transpose(index)).sum()

    def diagexpvalue(self, operator, indices=None, title=None, multi=False):
        r"""
        Calculate the expectation value for the given diagonal operator.

        *Usage*
            >>> a = numpy.arange(4)
            >>> print a
            array([ 0.,  1.,  2.,  3.])
            >>> sv = StateVector((1,2,1,4), norm=True)
            >>> print sv.diagexpvalue(a)
            2.45454545455

        *Arguments*
            * *operator*
                The diagonal elements of a tensor representing an arbitrary
                diagonal operator in the basis of the StateVector.

            * *indices* (optional)
                Specifies which subsystems should be taken. If None is given
                the whole system is used.

            * *multi* (optional)
                If multi is True it is assumed that a list of operators is
                given. (Default is False)

        Expectation values for combined systems are calculated in the following
        way (Assuming the operator only acts on first subsystem):

            .. math::

                \langle \Psi | \hat A (k) | \Psi \rangle =
                    \sum_k \langle k | \hat A (k) | k \rangle
                    \sum_m \Psi_{k m}^* \Psi_{k m}

        Other than the general :meth:`expvalue` method :meth:`diagexpvalue`
        only works for diagonal operators and only needs the diagonal elements
        of the matrix representation.
        """
        if isinstance(indices, int):
            indices = (indices,)
        A = self*self.conjugate()
        if indices is not None:
            indices = _sorted_list(_conjugate_indices(indices, self.ndim),
                                   True)
            for index in indices:
                A = A.sum(index)
        if multi:
            evs = [(A*op).sum() for op in operator]
            return expvalues.ExpectationValueCollection(evs, self.time, title)
        else:
            return (A*operator).sum()

    def outer(self, array):
        r"""
        Return the outer product between this and the given StateVector.
        
        *Usage*
            >>> sv = StateVector((0,1,2), norm=True)
            >>> print repr(sv.outer(StateVector((3,4), norm=True)))
            StateVector([[ 0.        ,  0.        ],
                   [ 0.26832816,  0.35777088],
                   [ 0.53665631,  0.71554175]])
            >>> print sv.outer((3,4)) # Not normalized!
            StateVector([[ 0.        ,  0.        ],
                   [ 1.34164079,  1.78885438],
                   [ 2.68328157,  3.57770876]])

        *Arguments*
            * *array*
                Some kind of array (E.g. StateVector, numpy.array, list, ...).

        As abbreviation ``sv1^sv2`` can be written instead of
        ``sv1.outer(sv2)``. But be aware that the operator precedence of ``^``
        follows the python rules - that means ``sv1 ^ sv2 + sv3`` is the same
        as ``sv1 ^ (sv2 + sv3)``.
        """
        return StateVector(numpy.multiply.outer(self, array))

    __xor__ = outer

    plot = visualization.statevector


class StateVectorTrajectory(numpy.ndarray):
    """
    A class holding StateVectors for different points of time.

    *Usage*
        >>> import numpy as np
        >>> X = np.linspace(-0.5, 0.5, 100)
        >>> svs = [pycppqed.gaussian(x) for x in X]
        >>> svtraj = StateVectorTrajectory(svs)
        >>> print svtraj
        StateVectorTrajectory(100 x (64))

    *Arguments*
        * *data*
            Some nested structure which holds state vector like arrays for
            different points of time.

        * *time* (optional)
            An array which specifies the point of time for every state
            vector. This array must have as many entries as there are state
            vectors.

        * Any other argument that a numpy array takes. E.g. ``copy=False`` can
          be used so that the StateVectorTrajectory shares the data storage
          with the given numpy array.

    Most methods are simple mapped to all single StateVectors. For more
    documentation regarding these methods look into the docstrings of the 
    corresponding :class:`StateVector` methods.
    """
    def __new__(cls, data, time=None, **kwargs):
        array = numpy.array(data, **kwargs)
        array = array.view(cls)
        if time is None:
            array.time = numpy.array([sv.time for sv in data])
        else:
            array.time = time
        svs = [None]*array.shape[0]
        for i, entry in enumerate(array):
            svs[i] = StateVector(entry, time=array.time[i], copy=False)
        array.statevectors = svs
        return array

    def __array_finalize__(self, obj):
        self.dimensions = obj.shape[1:]

    def __str__(self):
        clsname = self.__class__.__name__
        dims = " x ".join(map(str, self.dimensions))
        return "%s(%s x (%s))" % (clsname, self.shape[0], dims)

    def map(self, func, svt=True):
        """
        Apply the given function to every single StateVector.

        *Usage*
            >>> norm = svt.map(lambda sv:sv.norm())

        *Arguments*
            * *func*
                Function that takes a StateVector as argument.

            * *svt* (optional)
                If svt is True, the return value will be an instance of
                StateVectorTrajectory.
        """
        svs = [None]*self.shape[0]
        for i, sv in enumerate(self.statevectors):
            svs[i] = func(sv)
        if svt:
            return StateVectorTrajectory(svs)
        else:
            return svs

    def norm(self):
        """
        Return a list of norms for every single StateVector.

        See also: :meth:`StateVector.norm`
        """
        return self.map(lambda sv:sv.norm(), False)

    def normalize(self):
        """
        Return a StateVectorTrajectory where all StateVectors are normalized.

        See also: :meth:`StateVector.normalize`
        """
        return self.map(lambda sv:sv.normalize())

    def reduce(self, indices, norm=True):
        """
        Return a StateVectorTrajectory where all StateVectors are reduced.

        See also: :meth:`StateVector.reduce`
        """
        return self.map(lambda sv:sv.reduce(indices, norm=norm))

    def fft(self, axis=0):
        """
        Return a StateVectorTrajectory whith Fourier transformed StateVectors.

        See also: :meth:`StateVector.fft`
        """
        return self.map(lambda sv:sv.fft(axis))

    def expvalue(self, operator, indices=None, multi=False, titles=None):
        """
        Calculate the expectation value of the operator for all StateVectors.

        *Returns*
            *evtraj*
                An :class:`pycppqed.expvalues.ExpectationValuesTrajectory`
                instance.

        See also: :meth:`StateVector.expvalue`
        """
        evs = self.map(lambda sv:sv.expvalue(operator, indices, multi=multi),
                       False)
        if not multi:
            return expvalues.ExpectationValueTrajectory(evs, self.time, titles)
        evs = numpy.array(evs).swapaxes(0,1)
        return expvalues.ExpectationValueCollection(
                            evs, self.time, titles, copy=False)

    def diagexpvalue(self, operator, indices=None, multi=False, titles=None):
        """
        Calculate the expectation value of the diagonal operator for all SVs.

        *Returns*
            *evtraj*
                An :class:`pycppqed.expvalues.ExpectationValuesTrajectory`
                instance.

        See also: :meth:`StateVector.diagexpvalue`
        """
        evs = self.map(lambda sv:sv.diagexpvalue(operator, indices, 
                            multi=multi), False)
        if not multi:
            return expvalues.ExpectationValueTrajectory(evs, self.time, titles)
        evs = numpy.array(evs).swapaxes(0,1)
        return expvalues.ExpectationValueCollection(
                            evs, self.time, titles, copy=False)

    def animate(self, x=None, y=None, re=False, im=False, abs=True):
        """
        Create an interactive animation of this StateVectorTrajectory.

        For more information look into the docstring of
        :meth:`pycppqed.animation.animate_statevector`.
        """
        from pycppqed.animation import animate_statevector
        return animate_statevector(self, x, y, re, im, abs)


def norm(array):
    """
    Return the norm of the array.
    """
    return numpy.sqrt((array*array.conj()).sum())

def normalize(array):
    """
    Return a normalized array.
    """
    return array/norm(array)

def adjust(array, length):
    """
    Adjust the dimensionality of a 1D array.
    """
    import scipy.interpolate
    X_old = numpy.linspace(0,1,len(array))
    f = scipy.interpolate.interp1d(X_old, array)
    X_new = numpy.linspace(0,1,length)
    return StateVector(f(X_new))

def _dim2str(dimensions):
    """
    Return the corresponding dimension string for the given nested tuple.
    """
    dims = []
    for d in dimensions:
        dims.append("(%s,%s)" % d)
    return " x ".join(dims)

def _conjugate_indices(indices, ndim):
    """
    Return all numbers from 0 to ndim which are not in indices.
    """
    if isinstance(indices, int):
        indices = (indices,)
    return set(range(ndim)).difference(indices)

def _sorted_list(iterable, reverse=False):
    """
    Transform an iterable to a sorted list.
    """
    a = list(iterable)
    a.sort()
    if reverse:
        a.reverse()
    return a
