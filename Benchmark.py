from numpy.random import randint, default_rng, set_state
from time import perf_counter, sleep
from multiprocessing import Lock, Process, freeze_support, Value
from GUI import Interface

import os
import psutil

TEST_REPETITION = 3  # GUI
TEST_DIFICULTY = 50000  # GUI
TEST_SIZE = 5000  # GUI
NUMBER_OF_CORES = 1  # GUI
WORKING = Value('b', False)

GUI = Interface()


class ProcessHandler:
    def __init__(self):
        self.job = None
        self.done = Value('b', False)
        self.elapsed = Value('d', 0)

    def start(self):
        self.job.start()

    def setProcess(self, process):
        self.job = process

    def solveBenchmark(self, TESTS, working, lock):
        while True:
            with lock:
                if not working.value:
                    break
        t1 = perf_counter()
        for i in range(TEST_REPETITION):
            TESTS[0].solve()
            TESTS[1].solve()
            TESTS[2].solve()
        self.elapsed.value = perf_counter()-t1
        self.done.value = True


def setState():
    global picture, WORKING

    if not WORKING.value:
        GUI.canvas.configure(image=GUI.pictureBusy)
        GUI.canvas.photo_ref = GUI.pictureBusy
        GUI.interface.iconbitmap(GUI.icon_busy)
    else:
        WORKING = Value('b', False)
        GUI.canvas.configure(image=GUI.pictureReady)
        GUI.canvas.photo_ref = GUI.pictureReady
        GUI.interface.iconbitmap(GUI.icon_ready)
    GUI.interface.update_idletasks()


GUI.interface.bind("<Return>", set_state)


class Test:
    def __init__(self):
        self.size = TEST_SIZE


class FloatingPointsBechmark(Test):
    def __init__(self):
        super().__init__()
        self.arr = []

    def prepare(self):
        self.arr = default_rng().random((self.size,))

    def solve(self):
        for i in range(TEST_DIFICULTY):
            temp = (self.arr + self.arr - self.arr + self.arr) * self.arr


class IntegersPointsBenchmark(Test):
    def __init__(self):
        super().__init__()
        self.arr = []

    def prepare(self):
        self.arr = randint(2147483647, size=self.size)

    def solve(self):
        for i in range(TEST_DIFICULTY):
            temp = (self.arr + self.arr - self.arr + self.arr) * self.arr


class MatrixAditionBenchmark(Test):
    def __init__(self):
        super().__init__()
        self.matrix = []

    def prepare(self):
        self.matrix = [default_rng().random((self.size,))
                       for b in range(self.size)]

    def solve(self):
        for i in range(TEST_DIFICULTY):
            temp = (self.matrix + self.matrix) * 3


def memoryUsage():
    return psutil.Process(
        os.getpid()).memory_info().rss / 1024 ** 2


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


def ActiveProceses(processList, lock):
    with lock:
        for i in processList:
            if not i.done.value:
                return True
    return False


def getMaxTime(processList):
    result = 0.0
    for i in processList:
        if i.elapsed.value > result:
            result = i.elapsed.value
    return result


# sa bag chestia asta intr-un thread global cu optiunea sa ii dau si kill
def StartBenchmark(repetition, dificulty, size, cores):
    GUI.label_result.configure(text="Test results:")
    global NUMBER_OF_CORES, TEST_REPETITION, TEST_DIFICULTY, TEST_SIZE, WORKING
    NUMBER_OF_CORES = cores
    TEST_REPETITION = repetition
    TEST_DIFICULTY = dificulty
    TEST_SIZE = size
    setState()
    TESTS = generateBenchmark()
    mem = memoryUsage() * float(cores)

    lock = Lock()
    processes = []
    for i in range(NUMBER_OF_CORES):
        processes.append(ProcessHandler())
        processes[i].setProcess(
            Process(target=processes[i].solveBenchmark, args=(TESTS, WORKING, lock)))

    for i in processes:
        i.start()
    with lock:
        WORKING = Value('b', True)
    while ActiveProceses(processes, lock):
        sleep(0.1)
    setState()

    textResult = GUI.label_result.cget("text")+" Benchmark elapsed in {f} seconds and used {ram}".format(
        f='{0:.4f}'.format(getMaxTime(processes)), ram=str(mem))

    GUI.label_result.configure(text=textResult)


GUI.set_button(lambda: StartBenchmark(int(GUI.spinbox_repetition.get()), int(
    GUI.spinbox_dificulty.get()), int(GUI.spinbox_size.get()), int(GUI.spinbox_cores.get())))
if __name__ == '__main__':
    GUI.interface.iconbitmap(GUI.icon_ready)
    freeze_support()
    GUI.interface.mainloop()
