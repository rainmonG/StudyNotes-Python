"""
@Time : 2024/1/20 14:25
@Author : rainmon
@File : numpy_notes.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import numpy as np


def try_array(chapter):
    """
    methods in np
    :param int chapter: mark
    :return:
    """
    if chapter == 1:
        arr1 = np.array([1, 2, 3])
        print(arr1)
        arr2 = np.array((1, 2, 3))
        print(arr2)
        print(arr1 == arr2)

        arr1 = np.array(((1, 2), (1, 2)))
        print(arr1)
        arr2 = np.array([(1, 2), (1, 2)])
        print(arr2)
        print(arr2 == arr1)
        arr2 = np.array(([1, 2], [1, 2]))
        print(arr2)
        print(arr2 == arr1)
        arr2 = np.array([[1, 2], [1, 2]])
        print(arr2)
        print(arr2 == arr1)
    elif chapter == 2:
        arr1 = np.arange(10)
        print(arr1)
        arr2 = np.arange(3, 10, 0.1)
        print(arr2)
        arr3 = np.linspace(2, 3, num=5, endpoint=True)
        print(arr3)
        arr3 = np.linspace(2, 3, num=5, endpoint=False)
        print(arr3)
        arr1 = np.random.randn(6, 4)
        print(arr1)
        arr2 = np.random.randint(3, 7, size=(2, 4))
        print(arr2)

        arr1 = np.zeros(6)
        print(arr1)
        arr2 = np.zeros_like(np.arange(6))
        print(arr2)
        print(arr2 == arr1)
        arr2 = np.zeros((5, 6), dtype=int)
        print(arr2)
        print(arr2.size)
        print(arr2.dtype)

        arr1 = np.ones(4)
        print(arr1)
        arr2 = np.ones_like(np.arange(4))
        print(arr2)
        print(arr2 == arr1)

        arr1 = np.empty(4)
        print(arr1)
        arr2 = np.empty_like(np.arange(4))
        print(arr2)
        print(arr2.shape)
        print(arr2.dtype)
        print(arr2.ndim)

    elif chapter == 3:
        arr1 = np.arange(12)
        arr1 = arr1.reshape((3, arr1.size // 3))
        print(arr1)
        arr2 = np.ones((3, 4), dtype=int)
        print(arr2)
        print(arr1 + arr2)
        print(arr1.max())
        print(arr1.min())
        print(arr1.sum())
        print(arr1.sum(axis=1))
        print(arr1.cumsum())
        print(arr1.std())
        print(arr1.all())


if __name__ == '__main__':
    try_array(3)

