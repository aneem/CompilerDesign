from my_parser import parsePR

class Grammar(object):

    """ A general representation of grammar"""

    def __init__(self, *rules):
        """
        G={V,T,P,A}
        V--> NON-TERMINALS
        T--> TERMINALS
        P--> PRODUCTION RULES
        A--> STARTING SYMBOL
        """
        if len(rules)==1:
            rules = parsePR(rules[0])
        
        v=rules[0]
        t=rules[1]
        p=rules[2]
        a=rules[3]

        self.grammar = (v, t, p, a)
        # self.print_grammar()


    def get_grammar(self):
        return self.grammar

    def print_grammar(self):
        """ prints grammar in set form """
        v = self.print_set(sorted(self.grammar[0]))
        t = self.print_set(sorted(self.grammar[1]))
        p = self.print_dictionary(self.grammar[2])
        a = self.grammar[3]
        printString = '{ ' + v + '  ,  ' + t + '  ,  ' + p + '  ,  ' + a + ' }'
        print printString

    def print_set(self, givenset):
        """ a helper function to print the contents of set """
        string = '{'
        for i in givenset:
            string += ' ' + str(i)+' '+','
        string = string[:-1]+'}'
        return string

    def print_dictionary(self, dictionary):
        """ a helper function to print the contents of dictionary """

        printText = '{ '
        individual_rule_list = []
        i = 0
        individual_rule_list.append(
            self.make_printing_rule(dictionary[self.grammar[3]]))
        defined_non_terminal = [self.grammar[3]]

        undefined_non_terminal = self.get_non_terminals(individual_rule_list[0])

        # print
        # 'hello',individual_rule_list,defined_non_terminal,undefined_non_terminal
        jk = 0
        while undefined_non_terminal != []:
            i += 1
            # print i, defined_non_terminal, undefined_non_terminal,
            # print individual_rule_list
            x = undefined_non_terminal.pop(0)
            # print x, defined_non_terminal, undefined_non_terminal
            defined_non_terminal.append(x)
            individual_rule_list.append(self.make_printing_rule(dictionary[x]))
            j = self.get_non_terminals(individual_rule_list[i])
            for y in j:
                case_1 = y not in defined_non_terminal
                case_2 = y not in undefined_non_terminal
                if case_1 and case_2 and y != []:
                    # print 'adding',y,'to undefined_non_terminal'
                    undefined_non_terminal = undefined_non_terminal + [y]
                    # prisnt

        for item in individual_rule_list:
            printText += item+' , '
        return printText[:-2] + '}'

    def get_non_terminals(self, text):
        """ returns nonterminals from given raw grammar production rules """
        rulepart = text.split('->')
        nt = []
        for item in self.grammar[0]:
            if item in rulepart[1]:
                nt.append(item)
        # print nt,'inside get non terminals function'
        # print set(nt),list(set(nt))
        return list(set(nt))

    def make_printing_rule(self, rules):
        """ create individual rule for printing rule """
        formattedRule = rules[0][0] + ' -> '
        for i, rule in enumerate(rules):
            formattedRule += rules[i][1] + ' | '
        return formattedRule[:-3]


# rule1='S->A+B|A*B\
#     ,A->a|b \
#     ,B->c|d'


# rule2='A  -> Cd\
# ,B -> Cg\
# ,C -> fD\
# ,D -> dD | gD '


# rule3='E\'->TZ,\
#         Z->+TZ|e,\
#         T->FY,\
#         Y->*FY|e,\
#         F->(E\')|id'
# Grammar(rule3)
