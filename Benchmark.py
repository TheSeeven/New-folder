from tkinter.constants import FALSE
from numpy.random import randint, default_rng, set_state
from time import perf_counter, sleep
from multiprocessing import Lock, Process, freeze_support, Value
from GUI import Interface
import threading, signal

import os
import psutil

TEST_REPETITION = 3  # GUI
TEST_DIFICULTY = 50000  # GUI
TEST_SIZE = 5000  # GUI
NUMBER_OF_CORES = 1  # GUI
WORKING = Value("b", False)
BENCHMARK_THREAD = None
EXIT_FLAG = False
TESTS = None

GUI = Interface()


class ProcessHandler:
    def __init__(self):
        self.job = None
        self.done = Value("b", False)
        self.elapsed = Value("d", 0)

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
        self.elapsed.value = perf_counter() - t1
        self.done.value = True

    def kill(self):
        try:
            self.job.terminate()
        except:
            pass


def setState():
    global GUI, WORKING

    if not WORKING.value:
        GUI.canvas.configure(image=GUI.pictureBusy)
        GUI.canvas.photo_ref = GUI.pictureBusy
        GUI.interface.iconbitmap(GUI.icon_busy)
        GUI.button_start.configure(background="#a31515")
        GUI.button_start.configure(text="Stop Benchmark")
    else:
        WORKING = Value("b", False)
        GUI.canvas.configure(image=GUI.pictureReady)
        GUI.canvas.photo_ref = GUI.pictureReady
        GUI.interface.iconbitmap(GUI.icon_ready)
        GUI.button_start.configure(background="#1f7839")
        GUI.button_start.configure(text="Start Benchmark")
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
        self.matrix = [default_rng().random((self.size,)) for b in range(self.size)]

    def solve(self):
        for i in range(TEST_DIFICULTY):
            temp = (self.matrix + self.matrix) * 3


def memoryUsage():
    return psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2


def generateBenchmark():
    global TESTS
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
def StartBenchmark(repetition, dificulty, size, cores, stop):
    global EXIT_FLAG, TESTS
    mem_initial = memoryUsage() * float(cores)
    GUI.label_result.configure(text="Test results:")
    global NUMBER_OF_CORES, TEST_REPETITION, TEST_DIFICULTY, TEST_SIZE, WORKING
    NUMBER_OF_CORES = cores
    TEST_REPETITION = repetition
    TEST_DIFICULTY = dificulty
    TEST_SIZE = size
    TestsGenerator = threading.Thread(
        target=generateBenchmark,
    )
    TestsGenerator.start()
    print("tests generator started!")
    while TestsGenerator.is_alive():
        if EXIT_FLAG:
            EXIT_FLAG = False
            os.sys.exit()
    print("tests generated!")
    mem = (memoryUsage() * float(cores)) - mem_initial

    lock = Lock()
    processes = []
    print("Generating proceses!!")
    for i in range(NUMBER_OF_CORES):
        if not EXIT_FLAG:
            processes.append(ProcessHandler())
            processes[i].setProcess(
                Process(target=processes[i].solveBenchmark, args=(TESTS, WORKING, lock))
            )
        else:
            for j in processes:
                j.kill()
            EXIT_FLAG = False
            os.sys.exit()
    print("Proceses generated!!")
    for i in processes:
        if not EXIT_FLAG:
            i.start()
        else:
            for j in processes:
                j.kill()
            EXIT_FLAG = False
            os.sys.exit()
    print("Proceses started!")
    with lock:
        WORKING = Value("b", True)
    print("Waiting to finish...")
    while ActiveProceses(processes, lock):
        if EXIT_FLAG:
            EXIT_FLAG = False
            os.sys.exit()
        sleep(0.1)
    setState()

    textResult = GUI.label_result.cget(
        "text"
    ) + " Benchmark elapsed in {f} seconds and used {ram}".format(
        f="{0:.4f}".format(getMaxTime(processes)), ram=str(mem)
    )

    GUI.label_result.configure(text=textResult)
    EXIT_FLAG = False


def BenchmarkButton(repetition, dificulty, size, cores):
    global BENCHMARK_THREAD, EXIT_FLAG, WORKING
    if BENCHMARK_THREAD is not None:
        if not BENCHMARK_THREAD.is_alive():
            BENCHMARK_THREAD = threading.Thread(
                target=StartBenchmark,
                args=(
                    repetition,
                    dificulty,
                    size,
                    cores,
                    lambda: EXIT_FLAG,
                ),
            )
            BENCHMARK_THREAD.start()
            setState()
            print("Thread started!")
        else:
            EXIT_FLAG = True
            WORKING = Value("b", True)
            while BENCHMARK_THREAD.is_alive():
                pass
            print("Thread stopped!")
            setState()
            BENCHMARK_THREAD = None
    else:
        BENCHMARK_THREAD = threading.Thread(
            target=StartBenchmark,
            args=(
                repetition,
                dificulty,
                size,
                cores,
                lambda: EXIT_FLAG,
            ),
        )
        setState()
        BENCHMARK_THREAD.start()
        print("Thread started!")


GUI.set_button(
    lambda: BenchmarkButton(
        int(GUI.spinbox_repetition.get()),
        int(GUI.spinbox_dificulty.get()),
        int(GUI.spinbox_size.get()),
        int(GUI.spinbox_cores.get()),
    )
)
if __name__ == "__main__":
    GUI.interface.iconbitmap(GUI.icon_ready)
    freeze_support()
    GUI.interface.mainloop()
