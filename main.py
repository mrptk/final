from waiter import Waiter
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

    def __call__(self):
        self.waiter = Waiter(msg='Importuję tensorflow', end='Import tensorflow zakończony powodzeniem')

        self.waiter.start()
        tf, text = tf_import()
        self.waiter.stop(None)

        self.waiter = Waiter(msg='Ładuję model tłumaczeniowy', end='Ładowanie zakończone!')
        self.waiter.start()
        reloaded = tf.saved_model.load('translator_en_pl')
        self.waiter.stop(None)

        self.waiter = Waiter(msg='Tłumaczę', end='Tłumaczenie zakończone!')
        self.waiter.start()
        trans = reloaded("hello , i have n't seen alice for a while").numpy().decode('utf-8')
        self.waiter.stop(None)
        print(trans)


if __name__ == '__main__':
    try:
        main = Main()
        main()
    except KeyboardInterrupt:
        if main.waiter.is_running():
            main.waiter.stop('')

        print('\nWychodzę z programu')
    except TranslatorException as ex:
        if main.waiter.is_running():
            main.waiter.stop('')
        print(str(ex))


