from waiter import Waiter
import data_handler as dh
import logging
import numpy
import sys


def tf_import():
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=Warning)

    import tensorflow as tf
    import tensorflow_text as text
    tf.get_logger().setLevel('INFO')
    tf.autograph.set_verbosity(0)

    import logging
    tf.get_logger().setLevel(logging.ERROR)

    return tf, text


class TranslatorException(Exception):
    pass


class Main:
    def __init__(self):
        self.waiter = None
        self.__translator = None

    def __call__(self):
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
        self.waiter.stop(None)

        self.waiter = Waiter(msg='Ładuję model tłumaczeniowy', end='Ładowanie modelu tłumaczeniowego zakończone!')
        self.waiter.start()
        self.__translator = tf.saved_model.load('translator_en_pl')
        self.waiter.stop(None)

        self.__main_loop()

    def __main_loop(self):
        exit_program = False

        print('\n ***** Witaj! *****')
        print('[info]\tProgram tłumaczy teksty z języka angielskiego na polski.')
        print('[info]\tNie wszystkie znaki są dozwolone. Program pominie segmenty zawierające niedozwolone znaki.')
        print('[info]\tDo cudzysłowów używaj ".')

        while not exit_program:
            user_input = input('\n * Podaj tekst źródłowy: * \n')

            print(f' *** Tekst docelowy: *** \n{self.__translate(user_input)}')
            decision = ''
            while decision not in ['t', 'n']:
                decision = input('\nKontynuować? t/n\t')
                if decision == 'n':
                    exit_program = True
                    print('\nŻegnam!')

    def __translate(self, src):
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


