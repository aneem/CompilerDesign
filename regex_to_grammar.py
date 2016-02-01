from grammar import Grammar


class RegexToGrammar(object):

    def __init__(self, re):
        self.re = re
        self.stack = []
        self.dictionary = {}
        # operator count
        self.X_no = map(str, range(1, self.re.count('*')+self.re.count('+')+1))
        self.Y_no = map(str, range(1, self.re.count('|')+1))

    def get_grammar(self):
        print '-----------------  BEGIN regex_to_grammar -----------------\n'

        binary_op = ['|', '.']
        terminals = set(list(self.re))
        if '+' in terminals:
            terminals.remove('+')
        if '*' in terminals:
            terminals.remove('*')
        if '|' in terminals:
            terminals.remove('|')
        if '.' in terminals:
            terminals.remove('.')

        for i in self.re:

            if i in terminals:
                # print 'Stack=',self.stack ,'char', i
                self.stack.append(i)
            else:
                if i not in binary_op:
                    # print 'Stack=',self.stack ,'char', i
                    self.stack.append(
                        self.create_new_rules(i, self.stack.pop()))
                else:
                    # print 'Stack=',self.stack ,'char', i
                    dummy = self.create_new_rules(i, self.stack[-2:])
                    a = self.stack.pop()
                    b = self.stack.pop()

                    self.stack.append(dummy)

        self.dictionary['S'] = [('S', ''.join(self.stack.pop()))]
        # print "Dictionary/Grammar:", self.dictionary
        # print 'Terminals:', list(terminals)
        # print 'Non Terminals:', self.dictionary.keys()
        # print 'Number of rules:', len(self.dictionary)
        grammar_ = Grammar(
            set(self.dictionary.keys()), terminals, self.dictionary, 'S')
        
        print "Grammar: ",
        grammar_.print_grammar()
        print '\n-----------------  END regex_to_grammar -----------------\n\n'
        return grammar_

    def get_terminals(self):
        terminals = []
        for rule in self.dictionary.values():
            for individual_rule in rule:
                # print 'ir',individual_rule
                terminal = individual_rule[-1]
                for nt in self.dictionary.keys():
                    if nt in terminal:
                        terminal = terminal.replace(nt, '')
                terminals.append(terminal)
        terminals_set = set(terminals)
        if '' in terminals_set:
            terminals_set.remove('')
        return terminals_set

    def create_new_rules(self, operator, operands):
        # print operands
        if operator == '*':
            non_terminal = 'X'+self.X_no.pop(0)
            lists = [(non_terminal, operands+non_terminal),
                     (non_terminal, '')]
            self.dictionary[non_terminal] = lists
        elif operator == '+':
            non_terminal = 'X'+self.X_no.pop(0)
            lists = [(non_terminal, operands+non_terminal),
                     (non_terminal, operands)]
            self.dictionary[non_terminal] = lists
        elif operator == '.':
            # print 'operands', operands
            non_terminal = self.concat(operands)

        else:
            non_terminal = 'Y'+self.Y_no.pop(0)
            lists = [(non_terminal, ''.join(operands[0])),
                     (non_terminal, ''.join(operands[1]))]
            self.dictionary[non_terminal] = lists
        # print self.dictionary
        return non_terminal

    def concat(self, operands):
        """ Combines two given operands to a single list """
        non_terminal = []
        if type(operands[0]) is list:
            for item in operands[0]:
                non_terminal.append(item)
        else:
            non_terminal.append(operands[0])

        if type(operands[1]) is list:
            for item in operands[0]:
                non_terminal.append(item)
        else:
            non_terminal.append(operands[1])

        non_terminal = ''.join(non_terminal)
        # print 'concatted output', non_terminal
        return non_terminal


# dummy='abcd*ef|*..|*.'
# dummyreg=regex2grammar(dummy)
# dummyreg.get_grammar()
# # dummyreg.get_terminals()
