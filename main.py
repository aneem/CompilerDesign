# lab1+ lab4 + lab5
from grammar import Grammar
from regex_to_grammar import RegexToGrammar
from infix_to_postfix import to_post_fix
from backtrack import BackTrackParser

#Lab1 + Lab4
regular_expression = 'a(b|a)*bab'
postfix_notation = to_post_fix(regular_expression)
regex_to_grammar_converter = RegexToGrammar(postfix_notation)
grammar = regex_to_grammar_converter.get_grammar()
print grammar.grammar[2]
parser = BackTrackParser(grammar)
sample_text_valid = 'abbaabbab'
sample_text_invalid = 'ababa'
parser.bt_parser(sample_text_valid)
parser.bt_parser(sample_text_invalid)


# Lab5
# grammar2=Grammar('S->aA|aB,A->b,B->i')
# parser2=BackTrackParser(grammar2)
# sample_text_valid='ai'
# sample_text_invalid='ha'
# parser2.bt_parser(sample_text_valid)
# parser2.bt_parser(sample_text_invalid)

