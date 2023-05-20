import time
import sys
import threading


def print_with_cr(msg):
    sys.stdout.write('\r' + msg)


class Waiter:
    def __init__(self, msg, end):
        self.__msg = msg
        self.__msg_end = end + '\n'
        self.__continue = True
        self.__thread = None

    def __printer(self):
        while self.__continue:
            for i in range(0, 6):
                print_with_cr(f'{self.__msg}{"." * i}')
                time.sleep(0.75)
                if not self.__continue:
                    break

        print_with_cr(self.__msg_end)

    def start(self):
        self.__continue = True
        self.__thread = threading.Thread(target=self.__printer)
        self.__thread.start()

    def stop(self, end):
        if end is not None:
            self.__msg_end = end

        self.__continue = False
        self.__thread.join()

    def restart(self, msg, end):
        self.__msg = msg
        self.__msg_end = end
        self.start()

    def is_running(self): return self.__continue

