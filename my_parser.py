
def parsePR(rules):
    ''' main function to parse '''
    print '-----------------  BEGIN Parser -----------------\n'

    individual_rules = rules.split(',')
    individual_rules2 = []

    for item in individual_rules:
        individual_rules2.append((item.strip()))

    terminals = []
    production_rules = {}
    non_terminals = get_non_terminals(individual_rules2)

    for item in individual_rules2:
        dummy_list = item.split('->')
        dummy_list[0] = dummy_list[0].strip()
        if '|' in dummy_list[1]:
            rhs = dummy_list[1].split('|')
            tuplelist = []
            for each_RHS in rhs:
                each_RHS = each_RHS.strip()
                # print each_RHS
                terminal = get_terminals(each_RHS, non_terminals)
                if not terminal :
                    terminals = terminals+terminal

                dummy_tuple = (dummy_list[0], each_RHS)
                tuplelist.append(dummy_tuple)
        else:
            terminal = get_terminals(dummy_list[1].strip(), non_terminals)
            if terminal != []:
                terminals = terminals+terminal
            tuplelist = [(dummy_list[0], dummy_list[1].strip())]

        production_rules[dummy_list[0]] = tuplelist

    terminals = list(set(terminals))
    print "non terminals: ", non_terminals
    print 'terminals: ', terminals
    print "production rules: ", production_rules
    print 'after checking for left recursion'
    without_LR = remove_left_recursion_and_left_factoring(
        production_rules, 0)
    print "production rules: ", without_LR
    without_LR_and_LF = remove_left_recursion_and_left_factoring(
        without_LR, 1)
    print 'after left factoring', without_LR_and_LF
    print '\n-----------------  END Parser -----------------\n\n'

    return (without_LR_and_LF.keys(), terminals,
            without_LR_and_LF, non_terminals[0])


def get_non_terminals(rules):
    non_terminals = []
    for item in rules:
        dummy_list = item.split('->')
        dummy_list[0] = dummy_list[0].strip()
        non_terminals.append(dummy_list[0])
    return non_terminals


def get_terminals(text, non_terminals):
    #text=AbBBac  *FY
    terminal = []
    result = has_non_terminal(text, non_terminals)
    if result:
        for i in result:
            terminal = terminal + text.split(i)
        # terminal=list(set(terminal))
        while '' in terminal:
            terminal.remove('')
        for i in result:
            for index, item in enumerate(terminal):
                if (i in item):
                    terminal.pop(index)

        return terminal
        # return ''.join(terminal)
    else:
        return [text]

    # terminals.append(terminal)


def has_non_terminal(text, non_terminals):
    nt = []
    for item in non_terminals:
        if item in text:
            nt.append(item)
    return nt


def remove_left_recursion_and_left_factoring(rules, switch):

    new_rules_dict = rules
    new_rule = {}
    for key, individual_rules in zip(rules.keys(), rules.values()):

        for item in individual_rules:
            LRrule = rules[key]

            case1 = item[1].startswith(item[0]) and switch
            case2 = has_left_factoring(individual_rules) and switch
            if case1:
                # Left Recursion true
                print 'dealing with left recursion'
                new_rule = create_non_left_recursive_rules(LRrule)
            if case2:
                # Left Factoring True
                new_rule = create_non_left_factoring_rules(individual_rules)
            for key, item in zip(new_rule.keys(), new_rule.values()):
                new_rules_dict[key] = item
            break

    return new_rules_dict
    # should check for circular recursion


def has_left_factoring(rules):
    first = rules[0][1][0]
    if len(rules) > 1:
        for rule in rules[1:]:
            # print first, rule[1][0]
            if first != rule[1][0]:
                return False
        return True
    return False


def create_non_left_factoring_rules(rules):
    # print rules
    first = rules[0][1][0]
    new_rules = []
    dic = {}
    non_terminal = rules[0][0]
    new_non_terminal = non_terminal+"'"
    tuple_=(non_terminal, first+new_non_terminal)
    dic[non_terminal] = [tuple_]

    new_terminal_rules = []
    for rule in rules:
        new_terminal_rules.append((new_non_terminal, rule[1][1:]))
    dic[new_non_terminal] = new_terminal_rules
    return dic


def create_non_left_recursive_rules(LRrule):
    ''' helper function to create new rules for left recursion'''
    n = m = 0
    dic = {}
    tuple_list_1 = []
    tuple_list_2 = []
    tuple_list_m = []
    tuple_list_n = []
    for rule in LRrule:
        if rule[1].startswith(rule[0]):
            m += 1
            tuple_list_m.append(rule)
        else:
            n += 1
            tuple_list_n.append(rule)
    new_non_terminal = rule[0]+'\''
    # print tuple_list_m,tuple_list_n
    for x in tuple_list_n:
        dummy_tuple = (x[0], x[1]+new_non_terminal)
        tuple_list_1.append(dummy_tuple)
    dic[LRrule[0][0]] = tuple_list_1
    for y in tuple_list_m:
        alpha = (y[1])
        alpha = alpha.replace(rule[0], '', 1)
        dummy_tuple = (new_non_terminal, alpha+new_non_terminal)
        tuple_list_2.append(dummy_tuple)
    tuple_list_2.append((new_non_terminal, ''))
    dic[new_non_terminal] = tuple_list_2

    return dic


# parsePR test

rule1 = 'S->A+B|A*B\
    ,A->Ac|Ab|f \
    ,B->c|d'
# result=parsePR(rulz)
# removeLeftRecursion(result[2])

rule2 = 'S->aA|aB,A->h,B->i'
# result=parsePR(rule2)
