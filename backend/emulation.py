import math
import time
import numpy as np
import threading


def emul_func(start: int, end: int, how_many_itter: int = 10):
    """

    :param start:
    :param end:
    :param how_many_itter:
    :return:
    """
    def em_func(x: float):
        return np.cbrt(x - 1) / 2 + 0.5
    global price
    for i in np.linspace(0, 2, how_many_itter):
        price = math.ceil(start + em_func(i) * (end - start))  # change state
        time.sleep(0.1)


if __name__ == '__main__':
    price = 10
    sin_thr = threading.Thread(target=emul_func, args=(price, 20, 60))
    sin_thr.start()
    for i in range(60):
        print('price == {}'.format(price))
        time.sleep(0.3)
