import parse_input


class Rule:
    def __init__(self, not_terminal: str, right_part):
        self.not_symbol = not_terminal
        self.right_part = right_part


class Earley:
    def __init__(self, rule, dot, left):
        self.rule = rule
        self.dot = dot
        self.left = left

    def get_right(self):
        return self.rule.right_part

    def __eq__(self, other):
        Flag = self.dot == other.dot and self.left == other.left 
        Flag = self.rule.not_symbol == other.rule.not_symbol and Flag
        Flag = self.rule.right_part == other.rule.right_part and Flag
        return Flag

    def __hash__(self):
        return hash(self.rule) * hash(self.dot + self.left)


class CFG:
    def __init__(self, path: str):
        with open(path) as f:
            parse_input.parse_cfg(f)
            
            self.start = parse_input.parse_start(f)
            self.words = parse_input.parse_input_words(f)
            
            self.transitions, self.not_alphabet = parse_input.parse_body(f)
            self.new_start()

    def get_rule(self, not_terminal):
        return self.transitions[not_terminal]

    def new_start(self):
        self.transitions["S'"].append(Rule("S'", "S"))
        self.start = "S'"
        self.not_alphabet.add("S'")

    def initialization(self, word: str):
        states = [set() for _ in range(len(word) + 1)]
        states[0].add(Earley(self.get_rule(self.start)[0], 0, 0))
        
        return states

    def scan(self, states, num, word):
        if num == 0: return
        
        for early_item in states[num - 1]:
            if early_item.dot < len(early_item.get_right()):
                next_symb = early_item.get_right()[early_item.dot]
                
                if (not (next_symb in self.not_alphabet)) and next_symb == word[num - 1]:
                    states[num].add(Earley(early_item.rule, early_item.dot + 1, early_item.left))

    def predict(self, states, num):
        old_size = len(states[num])
        
        for early_item in states[num].copy():
            if early_item.dot < len(early_item.get_right()):
                next_symb = early_item.get_right()[early_item.dot]
                
                if next_symb not in self.not_alphabet: continue
                    
                for rule in self.get_rule(next_symb):
                    states[num].add(Earley(rule, 0, num))

        return old_size != len(states[num])

    def complete(self, states, num) -> bool: 
        old_size = len(states[num])
        
        for early_item in states[num].copy():
            if early_item.dot != len(early_item.get_right()): continue
                
            for item in states[early_item.left]:
                if item.dot < len(item.get_right()) and item.get_right()[item.dot] \
                        == early_item.rule.not_symbol:
                        
                    states[num].add(Earley(item.rule, item.dot + 1, item.left))
        
        return old_size - len(states[num])

    def is_word_in_CFG(self, word: str):
        states = self.initialization(word)
        
        for num in range(len(word) + 1):
            self.scan(states, num, word)
            
            first_result, second_result = True, True
            
            while first_result or second_result:
                first_result = self.complete(states, num)
                second_result = self.predict(states, num)
        
        return Earley(self.get_rule(self.start)[0], 1, 0) in states[len(word)]

 
    def get_ans(self):
        answer = []
        
        for word in self.words:
             answer.append("YES\n" if self.is_word_in_CFG(word) else "NO\n")
        
        return answer
