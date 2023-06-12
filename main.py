"""
    Główny moduł, który należy uruchomić, aby rozpocząć pracę z programem.
"""
from waiter import Waiter
import data_handler as dh
import logging
import numpy
import sys


def tf_import():
    """
    Funkcja służąca do importowania modułów tensorflow i tensorflow-text w taki sposób, aby w konsoli nie wyświetlały się
    komunikaty zgłaszane podczas pobierania. Zwraca krotkę z oboma modułami.
    """
    import os
    import warnings
    import logging

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=Warning)

    import tensorflow as tf
    import tensorflow_text as text
    tf.get_logger().setLevel('INFO')
    tf.autograph.set_verbosity(0)

    tf.get_logger().setLevel(logging.ERROR)

    return tf, text


class TranslatorException(Exception):
    """
    Klasa używana do zgłaszania i obsługi większości wyjątków podczas działania programu.
    """
    pass


class Main:
    """
    Klasa, której obiekt służy do sterowania programem.
    """
    def __init__(self):
        """
        Konstruktor inicjalizujący wszystkie pola wartością None
        """
        self.waiter = None
        self.__translator = None

    def __call__(self):
        """
        Najważniejsza metoda w klasie, która de facto rozpoczyna działanie programu i uruchamia główną pętlę.
        """
        print("PRACA INŻYNIERSKA 'TŁUMACZENIE MASZYNOWE KRÓTKICH TEKSTÓW'\nautor: mgr Patryk Edward Mazur\n"
              "promotor: dr Piotr Wrzeciono")
        print()
        if sys.stdin.encoding.lower() != 'utf-8':
            print('[UWAGA] Korzystasz z konsoli, w której znaki nie są kodowane w Unicode. Może to '
                          'utrudnić działanie programu.')

        self.waiter = Waiter(msg='Importuję tensorflow', end='Import tensorflow zakończony powodzeniem')

        self.waiter.start()
        try:
            tf, text = tf_import()
        except ModuleNotFoundError:
            raise TranslatorException('Nie znaleziono modułu tensorflow i/lub tensorflow-text. '
                  'Upewnij się, że oba moduły są zainstalowane.')
        except Exception:
            raise TranslatorException('Wystąpił błąd podczas importowania pakietów tensorflow i/lub tensorflow-text.'
                                      ' Upewnij się, że spełnione są wszystkie wymagania.')
        self.waiter.stop(None)

        self.waiter = Waiter(msg='Ładuję model tłumaczeniowy', end='Ładowanie modelu tłumaczeniowego zakończone!')
        self.waiter.start()
        try:
            self.__translator = tf.saved_model.load('translator_en_pl')
        except Exception:
            raise TranslatorException('Wystąpił błąd podczas ładowania modelu tłumaczeniowego. Upewnij się, że'
                                      ' spełnione są wszystkie wymagania.')
        self.waiter.stop(None)

        self.main_loop()

    def main_loop(self):
        """
        Prywatna metoda implementująca główną pętlę programu, w której w każdej iteracji użytkownik proszony jest o podanie
        tekstu źródłowego i, po wyświetleniu tłumaczenia, zapytywany, czy kontynuować działanie.
        """
        exit_program = False

        print('\n ***** Witaj! *****')
        print('[info]\tProgram tłumaczy teksty z języka angielskiego na polski.')
        print('[info]\tProgram nie rozpoznaje wszystkich znaków i pominie segmenty, które je zawierają.')
        print('[info]\tDo cudzysłowów używaj ".')
        print('[info]\tProgram nie rozpoznaje nazw własnych. Sprawdź pisownię wielką/małą literą w tłumaczeniu.')

        while not exit_program:
            lines = []
            print('\n * Podaj tekst źródłowy: *')
            print('Wciśnij dwa razy Enter, aby zatwierdzić')
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break

            if len(lines) > 1:
                lines = "\n".join(lines)
            elif len(lines) == 0:
                print("Nie znaleziono tekstu do tłumaczenia.")
            else:
                lines = lines[0]

            print(f' *** Tekst docelowy: *** \n{self.translate(lines)}')

            decision = ''
            while decision not in ['t', 'n']:
                decision = input('\nKontynuować? t/n\t')
                if decision == 'n':
                    exit_program = True
                    print('\nŻegnam!')

    def translate(self, src):
        """
        Prywatna metoda, której zadaniem jest użycie modelu tłumaczeniowego do przetłumaczenia podanego przez
        użytkownika tekstu. To tutaj dokonywane jest formatowanie danych wejściowych i wyjściowych.
        Zwraca przetłumaczony i sformatowany tekst.
        """
        src, src_incorrect = dh.prep_input(src)
        target = []
        result = ''
        self.waiter = Waiter(msg='Tłumaczę', end='Tłumaczenie zakończone!')

        if len(src_incorrect) > 0:
            print(dh.wrap_bad_segments(src_incorrect))

        if len(src) > 0:
            self.waiter.start()
            for segment in src:
                target.append(self.__translator(segment).numpy().decode('utf-8'))
            self.waiter.stop(None)
            result = dh.post_output(target)

        return result


if __name__ == '__main__':
    try:
        main = Main()
        main()
    except KeyboardInterrupt:
        if main.waiter is not None and main.waiter.is_running():
            main.waiter.stop('')

        print('\nWychodzę z programu')
    except TranslatorException as ex:
        if main.waiter.is_running():
            main.waiter.stop('')
        print(str(ex))


