from grammar import Grammar


class SLRParser(object):

    def __init__(self, grammar):
        self.table = self.create_table()
        self.grammar = grammar
        self.rule_length = [1, 3, 1, 3, 1, 3, 1]
        self.rules_nt = ["E'", 'E', 'E', 'T', 'T', 'F', 'F']

    def create_table(self):
        no_of_states = 12

        table = {}
        dummy_list = [None]*no_of_states
        id_ = dummy_list[:]
        plus_op = dummy_list[:]
        star_op = dummy_list[:]
        l_bracket = dummy_list[:]
        r_bracket = dummy_list[:]
        dollar = dummy_list[:]
        E = dummy_list[:]
        T = dummy_list[:]
        F = dummy_list[:]

        id_[0] = id_[4] = id_[6] = id_[7] = ('s', 5)
        plus_op[1] = plus_op[8] = ('s', 6)
        plus_op[2] = r_bracket[2] = dollar[2] = ('r', 2)
        plus_op[3] = star_op[3] = r_bracket[3] = dollar[3] = ('r', 4)
        plus_op[5] = star_op[5] = r_bracket[5] = dollar[5] = ('r', 6)
        plus_op[9] = r_bracket[9] = dollar[9] = ('r', 1)
        plus_op[10] = star_op[10] = r_bracket[10] = dollar[10] = ('r', 3)
        plus_op[11] = star_op[11] = r_bracket[11] = dollar[11] = ('r', 3)

        star_op[2] = star_op[9] = ('s', 7)
        l_bracket[0] = l_bracket[4] = l_bracket[6] = l_bracket[7] = ('s', 4)

        r_bracket[8] = ('s', 11)
        dollar[1] = ('r', 0)       # accepting state
        E[0] = 1
        E[4] = 8
        T[0] = 2
        T[4] = 2
        T[6] = 9
        F[0] = 3
        F[4] = 3
        F[6] = 3
        F[7] = 10

        table['a'] = id_
        table['+'] = plus_op
        table['*'] = star_op
        table['('] = l_bracket
        table[')'] = r_bracket
        table['$'] = dollar
        table['E'] = E
        table['T'] = T
        table['F'] = F

        # print table
        return table

    def parse(self, string):
        string = string+['$']
        input_buffer = list(string)
        stack = [0]

        while True:
            lookup_key = input_buffer[0]
            lookup_state = stack[-1]

            lookup_result = self.table[lookup_key][lookup_state]

            if lookup_result is None:
                print '\t\t!!! Error!!!'
                break
            elif lookup_result==('r',0):
                print '\t\t!!!Success!!!'
                break
            else:

                if lookup_result[0] == 's':
                    stack.append(input_buffer.pop(0))
                    stack.append(lookup_result[1])
                    print ' After shift \t', stack
                elif lookup_result[0] == 'r':

                    for i in range(2 * self.rule_length[lookup_result[1]]):
                        stack.pop()
                    stack.append(self.rules_nt[lookup_result[1]])
                    lookup_result = self.table[stack[-1]][stack[-2]]
                    stack.append(lookup_result)
                    print ' After reduce \t', stack
                else:
                    pass


parse_string1 = ['a', '+', 'a', '*', 'a', '+', 'a']
parse_string2=list('a*a+a')

rules = ("E' -> E ,"
         'E -> E+T |T ,'
         'T -> T*F | F ,'
         'F -> (E) | a '
         )
parser = SLRParser(Grammar(rules))
parser.parse(parse_string2)
