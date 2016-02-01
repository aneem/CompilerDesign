import string

operands = string.lowercase+string.digits
operators = ['', '|', '.', '*', '+']
parenthesis = ['(', ')']


def clean(infix):

    prev = '@'      # dummy symbol
    infix = list(infix)
    print 'infix notation before cleaning:\t', infix
    for key, item in enumerate(infix):
        case1 = (prev in operands) and (item in operands)
        case2 = (prev in operands) and item == '('
        case3 = (prev in operators[-2:]) and item not in ['.', ')']
        # print case1,case2,case3
        # print '1',prev,item
        if case1 or case2 or case3:
            infix.insert(key, '.')

        prev = infix[key]

    print 'infix notation after cleaning:\t', infix

    return infix


def to_post_fix(infix):

    print '-----------------  BEGIN PostFix Conversion -----------------\n'

    operator_stack = ['']
    postfix_string = []
    infix = clean(infix)
    for i in infix:
        if i in operands:
            postfix_string.append(i)
        elif i in operators:
            if len(operator_stack) > 0:

                top = operator_stack[-1]
                while has_higher_precedence(top, i):
                    print top, '\thigher op prexedence found'
                    postfix_string.append(operator_stack.pop())
                    top = operator_stack[-1]

                operator_stack.append(i)
        elif i in parenthesis:
            if i == parenthesis[0]:
                operator_stack.append(i)

            else:
                index = [k for k, x in enumerate(
                    operator_stack) if x == '('][-1]

                for l in operator_stack[index+1:]:
                    postfix_string.append(operator_stack.pop())
                operator_stack.pop()
        print i, '\t', 'operator stack=', operator_stack,
        print '\t', 'postfix string=', ''.join(postfix_string)
    for j in operator_stack[1:]:
        postfix_string.append(operator_stack.pop())

    print i, '\t', 'operator stack=', operator_stack,
    print '\n\t', 'postfix string=', ''.join(postfix_string)
    print '\n-----------------  END PostFix Conversion -----------------\n\n'

    return postfix_string


def has_higher_precedence(op1, op2):
    if op1 in parenthesis:
        return False
    elif operators.index(op1) > operators.index(op2):
        return True
    else:
        return False

# to_post_fix('(a|b)*a')
# to_post_fix('a(b|cd*(e|f)*)*')
