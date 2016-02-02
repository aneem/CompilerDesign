from grammar import Grammar

class SLRParser(object):

    def __init__(self,grammar):
        self.grammar=grammar
        self.non_terminals=grammar.grammar[0]
        self.terminals=grammar.grammar[1]
        self.production_rules=grammar.grammar[2]
        self.starting_symbol=grammar.grammar[3]



    def get_first_set(self):
        first_dic={}
        for nt in self.non_terminals:
            result=self.first(nt)
            first_dic[nt]=result
        return first_dic            

    def first(self,non_terminal):
        # print non_terminal
        first_list=[]
        rules=self.production_rules[non_terminal]
        for each_rule in rules:
                if each_rule[1][0] not in self.non_terminals:
                    first_list.append(each_rule[1][0])
                else:
                    result=self.first(each_rule[1][0])
                    if result != '':
                        first_list.extend(result)
        return first_list

    def get_follow_set(self):
        follow_dic={}
        for nt in self.non_terminals:
            result=self.follow(nt)
            follow_dic[nt]=result
        return follow_dic


    def follow(self,non_terminal):
        follow_list=[]
        # print self.production_rules
        if non_terminal==self.starting_symbol:
            follow_list=['$']
        else:

            for key,rules in zip(self.production_rules.keys(),self.production_rules.values()):
                for nt,each_rule in rules:
                    if non_terminal not in each_rule:
                        continue
                    else:
                        index_NT=each_rule.index(non_terminal)

                        if len(each_rule) != (index_NT+1):
                            next=each_rule[index_NT+1]

                            if next in self.terminals:
                                follow_list.append(next)
                            else:
                                result=first(next)
                                if result != ['']:
                                    follow_list.append(result)
                        else:
                            follow_list.extend(self.follow(nt))
        return follow_list

rule1='S->A+B\
    ,A->a|b \
    ,B->c|d'

grammar=Grammar(rule1)
parser=SLRParser(grammar)
print 'firstset' ,parser.get_first_set()
print 'followset' ,parser.get_follow_set()