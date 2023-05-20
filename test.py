import data_handler as dh

a_string = "I want to go home.\n" \
            "My dog is black and white.\n" \
            "They are\f going to the store with me today.\n" \
            "It’s raining\t outside right now.\n" \
            "I like chocolate ice cream better than vanilla ice cream.\n" \
            "The sun is shining bright in the morning today.\n" \
            "I like\r ice cream.\n" \
            "I have a dog named Princess.\n" \
            "We live in\b New York City.\n"

b_string = "Hello, t€here. Gen. Keno€bi…."

test_cases = [a_string, b_string]

for index, case in enumerate(test_cases):
    res_corr, res_incorr = dh.prep_input(case)
    print(f'TEST CASE {index + 1}:\nSOURCE:\n{case}\nTARGET_CORRECT:\n{res_corr}\nTARGET_INCORRECT:\n{dh.wrap_bad_segments(res_incorr)}\n')

