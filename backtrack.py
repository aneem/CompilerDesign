from grammar import Grammar
from node import Node

# works for string grammar but not for list grammar

class string_node(Node):

    ''' class Node override init funciton to add 'string' instance variable '''

    def __init__(self, inputstring):
        self.string = inputstring


class BackTrackParser(object):

    def __init__(self, grammar_):

        self.grammar = grammar_.grammar
        self.non_terminal = self.grammar[0]
        self.terminal = self.grammar[1]
        self.grammar_rules = self.grammar[2]
        self.starting_symbol = self.grammar[3]
        self.goal = None


    def get_rules(self, nt):
        '''  returns all the rules related to the given non terminal '''
        return self.grammar_rules[nt]

    def find_first_non_terminal(self, node):
        ''' finds the occurence of the first non-terminal
         and returns its index, other wise NONE '''

        for nt in self.non_terminal:
            if nt in node.string:
                if node.string.index(nt)<len(node.string)-1:
                    if len(nt)==2:
                        pass
                    elif node.string[node.string.index(nt)+1]=="'":
                        continue

                return nt, node.string.index(nt)
        return None

    def generate_successors(self, node):
        ''' generates successor nodes  for DFS travelsal,
         with back track included '''
        nt = self.find_first_non_terminal(node)
        successors = []
        generated_nodes = []
        # print len(node.string)
        if nt is not None:
            rules = self.get_rules(nt[0])
            # print rules,nt[1]
            string = node.string
            # string_list=list(string)
            # print 1,string_list
            for rule in rules:
                # string_list[nt[1]]=rule[1]
                # changed_string=''.join(string_list)
                changed_string = string.replace(nt[0], rule[1], 1)
                new_node = string_node(changed_string)
                new_node.parent_node = node
                generated_nodes.append(new_node)
                print "+ node created: '"+new_node.string+"' from", node.string

            for item in generated_nodes:
                new_NT = self.find_first_non_terminal(item)
                if new_NT != None:
                    index = new_NT[1]
                    # print new_NT[0]

                    # backtrackng step: checking whether node generated is
                    # closer to goal or not!!
                    if item.string[:index] == self.goal[:index]:
                        print "= matching string'"+item.string[:index]+"'"
                        successors.append(item)
                        print "* Successors", item.string, 'from', node.string
                    else:
                        print '- discarded terms', item.string
                elif self.goal_achieved(item):
                    successors.append(item)
                    print "* Successors", item.string, 'from', node.string

            node.successorNode = successors

        return successors

    def goal_achieved(self, node):
        return node.string == self.goal

    def execute(self, initialState):
        ''' Calls recursive_depth_first_search function for the first time '''
        print '-----------------  BEGIN Backtrack  -----------------\n'

        depth = len(self.goal)+self.max_rule_length()
        result = self.recursive_depth_first_search(initialState, depth)
        if result != None:
            print "Success :) '"+self.goal + "' can be created"
        else:
            print 'Failure :('
        print '\n-----------------  END Backtrack  -----------------\n\n'

    def recursive_depth_first_search(self, state, limit):
        ''' DFS traversal module '''
        if self.goal_achieved(state):
            # self.solutions.append(state)
            return state
        elif limit == 0:
            return None
        else:
            successors = self.generate_successors(state)
            for child in successors:
                result = self.recursive_depth_first_search(child, limit-1)
                if result != None:
                    return result
            return None

    def max_rule_length(self):
        max_=0
        for i in self.grammar_rules.values():
            for j in i:
                if len(j[1])>max_:
                    max_=len(j[1])
        return max_

    def bt_parser(self, string):
        ''' takes input from the user and starts the backtrack process '''
        startingNode = string_node(self.starting_symbol)
        self.goal = string
        sol = self.execute(startingNode)


# rules='S->cAdd,A->aA|b'
# # str1 ='cabd'

# rule2='S->A+B|A*B\
#     ,A->a|b \
#     ,B->c|d'
# str2='a+d'

# obj=BackTrackParser(Grammar(rule2))
# obj.bt_parser(str2)
