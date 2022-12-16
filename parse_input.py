from collections import defaultdict
import grammar


def parse_cfg(f):
    line = f.readline().strip()


def parse_start(f):
    line = f.readline().strip()
    return line.split()[1]


def parse_input_words(f):
    line = f.readline().strip()
    line = line[len('Words:'):]
    words = [word.strip() for word in line.split('&')]
    return words


def parse_body(f):
    lines = [line.strip() for line in f.readlines()]
    transitions = defaultdict(list)
    alphabet_not_terminal = set()
    lines = lines[1:]
    for line in lines:
        if line == '--END--':
            break
        elif not line.startswith('->'):
            raise Exception(f"{line}: transition should start with '->'")
        not_term, to = [s.strip() for s in line.split()][1:]
        alphabet_not_terminal.add(not_term)
        transitions[not_term].append(grammar.Rule(not_term, to))
    return transitions, alphabet_not_terminal
