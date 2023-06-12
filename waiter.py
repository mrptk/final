"""
Moduł ułatwiający wyświetlanie odświeżanych komunikatów w konsoli w osobnym wątku
"""
import time
import sys
import threading


def print_with_cr(msg):
    """
    Funkcja pomocnicza wypisująca komunikat w konsoli po powrocie karetki.
    """
    sys.stdout.write('\r' + msg)


class Waiter:
    """
    Klasa, której obiekt obsługuje wyświetlanie komunikatów na ekran w osobnym wątku
    """
    def __init__(self, msg, end):
        """
        Konstruktor, którego argumenty to wiadomość wyświetlana w konsoli podczas, gdy w głównym wątku wykonywana jest
        inna instrukcja oraz wiadomość wyświetlana, gdy wątek zakończy działanie.
        """
        self.__msg = msg
        self.__msg_end = end + '\n'
        self.__continue = True
        self.__thread = None

    def printer(self):
        """
        Funkcja przekazywana do osobnego wątku, to jej kod jest w nim wykonywany.
        """
        while self.__continue:
            for i in range(0, 6):
                print_with_cr(f'{self.__msg}{"." * i}')
                time.sleep(0.75)
                if not self.__continue:
                    break

        print_with_cr(self.__msg_end)

    def start(self):
        """
        Metoda rozpoczynająca działanie wątku i wyświetlanie odświeżanego komunikatu.
        """
        self.__continue = True
        self.__thread = threading.Thread(target=self.printer)
        self.__thread.start()

    def stop(self, end):
        """
        Metoda kończąca działanie wątku. Podając argument 'end' można nadpisać komunikat wyświetlany po zakończeniu
        działania wątku
        """
        if end is not None:
            self.__msg_end = end

        self.__continue = False
        self.__thread.join()

    def restart(self, msg, end):
        """
        Ponowne uruchmienie wątku z nowymi komunikatami. Funkcja stworzona po to, aby uniknąć konieczności tworzenia
        za każdym razem nowych obiektów.
        """
        self.__msg = msg
        self.__msg_end = end
        self.start()

    def is_running(self):
        """
        Funkcja zwracająca informację, czy wątek wypisujący komunikaty jest uruchomiony w danej chwili.
        """
        return self.__continue

