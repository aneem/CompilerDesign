
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

                result = get_rule_and_terminals(each_RHS, non_terminals)
                rule=result[0]
                each_terminal=result[1]
                terminals.extend(each_terminal)
                dummy_tuple = (dummy_list[0], rule)
                tuplelist.append(dummy_tuple)
        else:
            result = get_rule_and_terminals(dummy_list[1].strip(), non_terminals)
            rule=result[0]
            each_terminal=result[1]
            tuplelist = [(dummy_list[0],rule)]
        terminals.extend(each_terminal)
        production_rules[dummy_list[0]] = tuplelist

    terminals = list(set(terminals))
    print "non terminals: \t\t\t", non_terminals
    print 'terminals: \t\t\t\t', terminals
    print "production rules: \t\t", production_rules
    # print 'after left recursion\t',
    without_LR = remove_left_recursion_and_left_factoring(
        production_rules, 0)
    # print without_LR
    # print 'after left factoring\t',
    without_LR_and_LF = remove_left_recursion_and_left_factoring(
        without_LR, 1)
    # print  without_LR_and_LF
    print '\n-----------------  END Parser -----------------\n\n'

    return (without_LR_and_LF.keys(), terminals,
            without_LR_and_LF, non_terminals[0])


def get_non_terminals(rules):
    non_terminals = []
    for item in rules:
        dummy_list = item.split('->')
        dummy_list[0] = dummy_list[0].strip()
        non_terminals.append(dummy_list[0])
    return list(set(non_terminals))


def get_rule_and_terminals(text, non_terminals):
    result = has_non_terminal(text, non_terminals)

    reverse_result=result[:]
    reverse_result.reverse()
    rule=list(text)
    if result:
        for i in reverse_result:
 
            del rule[i[1]:i[1]+len(i[0])]


        terminals=set(rule)

        for i in result:
            rule.insert(i[1],i[0])

        return list(rule),set(terminals)
    else:
        return rule,rule



def has_non_terminal(text, non_terminals):
    nt = []
    for item in non_terminals:
        if item in text:
            nt.append((item,text.index(item)))
    return nt


def remove_left_recursion_and_left_factoring(rules, switch):

    new_rules_dict = rules
    new_rule = {}
    for key, individual_rules in zip(rules.keys(), rules.values()):

        for item in individual_rules:
            LRrule = rules[key]

            case1 = item[1][0]==item[0] and switch==0
            case2 = has_left_factoring(individual_rules) and switch==1
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
    tuple_=(non_terminal, [first]+[new_non_terminal])
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
        # for A->A alpha
        if rule[1][0]==rule[0]:
            m += 1
            tuple_list_m.append(rule)
        # for A-> beta
        else:
            n += 1
            tuple_list_n.append(rule)
    new_non_terminal = rule[0]+"'"
    # print tuple_list_m,tuple_list_n
    for x in tuple_list_n:
        dummy_tuple = (x[0], list(x[1])+[new_non_terminal])
        tuple_list_1.append(dummy_tuple)
    dic[LRrule[0][0]] = tuple_list_1
    for y in tuple_list_m:
        alpha = y[1][1:]
        dummy_tuple = (new_non_terminal, alpha+[new_non_terminal])
        # print dummy_tuple
        tuple_list_2.append(dummy_tuple)
    tuple_list_2.append((new_non_terminal, ['']))
    dic[new_non_terminal] = tuple_list_2

    return dic


# parsePR test

rule1 = 'S->A+B|A*B\
    ,A->Ac|Ab|f \
    ,B->c|d'
# result=parsePR(rulz)
# removeLeftRecursion(result[2])

rule2 = 'S->aA|aB,A->h,B->i'
# result=parsePR(rule1)
