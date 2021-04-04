from numpy.random import randint, default_rng
from time import perf_counter
from multiprocessing import Process, freeze_support, cpu_count
import os
import psutil


TEST_LENGTH = 5
TEST_DIFICULTY = 50000
NUMBER_OF_CORES = 1


class Test:
    def __init__(self):
        self.length = 2000


class FloatingPointsBechmark(Test):
    def __init__(self):
        super().__init__()
        self.arr = []

    def prepare(self):
        self.arr = default_rng().random((self.length,))

    def solve(self):
        for i in range(TEST_DIFICULTY):
            temp = (self.arr + self.arr - self.arr + self.arr) * self.arr


class IntegersPointsBenchmark(Test):
    def __init__(self):
        super().__init__()
        self.arr = []

    def prepare(self):
        self.arr = randint(2147483647, size=self.length)

    def solve(self):
        for i in range(TEST_DIFICULTY):
            temp = (self.arr + self.arr - self.arr + self.arr) * self.arr


class MatrixAditionBenchmark(Test):
    def __init__(self):
        super().__init__()
        self.matrix = []

    def prepare(self):
        self.matrix = [default_rng().random((self.length,))
                       for b in range(self.length)]

    def solve(self):
        for i in range(TEST_DIFICULTY):
            temp = (self.matrix + self.matrix) * 3


def solveBenchmark(TESTS):
    for i in range(TEST_LENGTH):
        TESTS[0].solve()
        TESTS[1].solve()
        TESTS[2].solve()


def memoryUsage():
    print("RAM used: ", psutil.Process(
        os.getpid()).memory_info().rss / 1024 ** 2)


def generateBenchmark():
    TESTS = []

    def generateFloatingTest():
        _TEST_FLOATING_POINTS = FloatingPointsBechmark()
        _TEST_FLOATING_POINTS.prepare()
        TESTS.append(_TEST_FLOATING_POINTS)

    def generateIntegerTest():
        _TEST_INTEGERS_POINTS = IntegersPointsBenchmark()
        _TEST_INTEGERS_POINTS.prepare()
        TESTS.append(_TEST_INTEGERS_POINTS)

    def generateMatrixTest():
        _TEST_MATRIX_ADD = MatrixAditionBenchmark()
        _TEST_MATRIX_ADD.prepare()
        TESTS.append(_TEST_MATRIX_ADD)

    generateIntegerTest()
    generateFloatingTest()
    generateMatrixTest()
    return TESTS


if __name__ == '__main__':

    freeze_support()
    print("Total number of cores: ", cpu_count())
    NUMBER_OF_CORES = int(input("Enter number of desired cores: "))

    TESTS = generateBenchmark()
    print("Starting test...")
    processes = []
    for i in range(NUMBER_OF_CORES):
        processes.append(Process(target=solveBenchmark, args=(TESTS,)))
    memoryUsage()
    t1 = perf_counter()
    for i in processes:
        i.start()
    for i in processes:
        i.join()
    t2 = perf_counter()-t1
    print("Total time: ", t2)
    print("Finish!")
    input("Press enter to exit...")
