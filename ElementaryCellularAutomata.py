import random
from enum import Enum
from dataclasses import dataclass
import matplotlib.pyplot as plt

class ExtensionMode(Enum):
    ZERO = 0
    ONE = 1
    EXTEND = 2
    PERIODIC = 3

@dataclass
class CellularAutomataState:
    width : int
    length : int
    rule : int
    extension_mode : ExtensionMode
    automata : 'list[int]'

    def __init__(self, width: int, length : int, rule : int, extension_mode : ExtensionMode, automata : 'list[int]'):
        self.width = width
        self.length = length
        self.rule = rule
        self.extension_mode = extension_mode
        self.automata = automata
    
    def __repr__(self):
        return f'[\n\tWidth: {self.width}\n\tLength: {self.length}\n\tRule: {self.rule}\n\tExtension Mode: {self.extension_mode}\n]'

class ElementaryCellularAutomata:

    def __init__(self, rule_number : int = 30, width : int = 30, length : int = 50, extension_mode : ExtensionMode = ExtensionMode.EXTEND, initial_row : "list[int]|None" = None):

        self.rule_number : int = rule_number
        self.rule_spec : 'list[int]' = self._generate_rule_from_number(self.rule_number)
        self.width : int = width
        self.length : int = length

        self.extension_mode : ExtensionMode = extension_mode

        if initial_row is None:
            self.initial_row : 'list[int]' = [random.choice([0, 1]) for _ in range(self.width)]
        else:
            self.width : int = len(initial_row)
            self.initial_row : 'list[int]' = initial_row

        self.automata : 'list[list[int]]' = [self.initial_row]
        self.cache : 'list[CellularAutomataState]' = []

        self.has_simulated : bool = False

    def set_rule_number(self, rule_number):
        self.rule_number = rule_number
        self.rule_spec = self._generate_rule_from_number(self.rule_number)

    def simulate(self, print_progress : bool = False):
        for line_number in range(self.length):
            if print_progress:
                print(f'Line Number: << {line_number+1: >4} >> ===================\n{self.automata[-1]}')
            self.automata.append(self._get_new_line())
        self.has_simulated = True

    def reset(self, reset_cache: bool = False):
        self.automata = [self.initial_row]
        self.has_simulated = False
        if reset_cache:
            self.clear_cache()            

    def cache_current_result(self):
        self.cache.append(CellularAutomataState(
            width = self.width,
            length=self.length,
            rule = self.rule_number,
            extension_mode=self.extension_mode,
            automata=self.automata
        ))

    def clear_cache(self):
        self.cache = []

    def print_cache(self, limit=5):
        for cached_result in range(min(len(self.cache), limit)):
            print(f'Index = {cached_result+1}\n {self.cache[cached_result]}\n')
    
    def _load_from_dataclass_representation(self, dataclass_representation: CellularAutomataState):
        self.width = dataclass_representation.width
        self.length = dataclass_representation.length
        self.rule_number = dataclass_representation.rule
        self.rule_spec = self._generate_rule_from_number(self.rule_number)
        self.automata = dataclass_representation.automata
        self.extension_mode = dataclass_representation.extension_mode
        if len(self.automata) > 1:
            self.has_simulated = True
        else:
            self.has_simulated = False

    def load_from_cache(self, index=1):
        if index < len(self.cache):
            raise IndexError("No values to load in Cache")
        self._load_from_dataclass_representation(self.cache[index])

    def _get_new_line(self):

        old_line = self.automata[-1]

        if self.extension_mode == ExtensionMode.ZERO:
            extended = [0] + old_line + [0]
        elif self.extension_mode == ExtensionMode.ONE:
            extended = [1] + old_line + [1]
        elif self.extension_mode == ExtensionMode.EXTEND:
            extended = [old_line[0]] + old_line + [old_line[-1]]
        elif self.extension_mode == ExtensionMode.PERIODIC:
            extended = [old_line[-1]] + old_line + [old_line[0]]

        newline = [0 for _ in old_line]
        for i in range(1, self.width+1):
            ruleIndex = int("".join(map(str, extended[i-1:i+2])), 2)
            newline[i-1] = self.rule_spec[ruleIndex]
        return newline
    
    def show_image(self):
        plt.imshow(self.automata)
        plt.axis('off')
        plt.show()

    @staticmethod
    def _generate_rule_from_number(rule_number):
        return [int(r) for r in f'{bin(rule_number)[2:]:0>8}'][::-1]
    
    @staticmethod
    def _prep_for_print(cell_value):
        return ['.', ','][cell_value]
    
    def __repr__(self):
        return ''.join([''.join((list(map(self._prep_for_print, r)) + ['\n'])) for r in self.automata])
    
if __name__ == "__main__":

    initial_row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    rule_number = random.randint(0, 2**8)
    print(f'{rule_number=}')


    myAutomata = ElementaryCellularAutomata(initial_row=initial_row, extension_mode=ExtensionMode.ZERO, rule_number=rule_number, length=100)
    myAutomata.simulate(print_progress=False)
    plot = myAutomata.show_image()

    myAutomata.clear_cache()
    myAutomata.cache_current_result()
    myAutomata.print_cache()