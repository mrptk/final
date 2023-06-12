from nltk.tokenize import sent_tokenize
import re

allowed_chars = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4',
                 '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', 'a', 'b', 'c', 'd',
                 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                 'y', 'z', 'à', 'á', 'â', 'ã', 'ä', 'ç', 'è', 'é', 'ê', 'ë', 'í', 'ï', 'ñ', 'ó', 'ö', 'ø', 'ú', 'ü',
                 'ā', 'ă', 'ć', 'ē', 'ť', '˚', '–', '—', '“', '”', '…', ' ', '£']


def prep_input(source):
    def prep_contraction(text):
        return re.sub(r"'m|'re|'s|n't|'d|'ll|'ve|s'", lambda x: ' ' + x.group(0), text)

    def prep_segment(text):
        return re.sub(r' +', ' ', re.sub(r'( ?)([.,;:\"?{}\[\]()!\-$£])( ?)', lambda x: ' ' + x.group(2) + ' ',
                                         text.lower())).strip()

    def prep_source(text):
        return re.sub(r'’', '\'', re.sub(r' +', ' ', re.sub(r'[\n\r\t\b\f]', ' ', text)))

    source = sent_tokenize(prep_source(source))

    segments_correct = []
    segments_incorrect = []

    for seg in source:
        is_correct = True
        bad_chars = []

        for char in seg:
            if char.lower() not in allowed_chars:
                is_correct = False
                bad_chars.append(char)

        if is_correct:
            segments_correct.append(prep_contraction(prep_segment(seg)))
        else:
            segments_incorrect.append((seg, bad_chars))

    return segments_correct, segments_incorrect


def post_output(target):
    def fix_segment(segment):
        segment = re.sub(r'( )([.,;:?!}”\]\)])', lambda x: x.group(2), segment)
        segment = re.sub(r'([{\[(„])( )', lambda x: x.group(1), segment)
        segment = re.sub(r"( ?)(')( ?)", lambda x: x.group(2), segment)
        segment = segment[:1].upper() + segment[1:]
        return segment

    post_target = []

    for sentence in target:
        post_target.append(fix_segment(sentence))

    return " ".join(post_target)


def wrap_bad_segments(segments):
    result = ''
    for segment, bad_chars in segments:
        if len(segment) > 20:
            segment = segment[:20] + '…'
        result += f'[UWAGA] Segment:\t{segment}\tzawiera nieobsługiwane znaki: {bad_chars}\n'

    return result
