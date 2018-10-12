=========
euclidean
=========

``euclidean`` is a pure python 3 geometry library, primarily focused on the R2 plane.

---------------
Getting Started
---------------

.. code-block:: pycon

    >>> from euclidean.R2 import V2
    >>> V2(100, 100) + V2(10, 0) + V2(0, 10)
    V2(110, 110)

    >>> V2(100, 100).cross(V2(1, 1))
    0

todo: actual documentation