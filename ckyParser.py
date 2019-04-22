
from nltk.corpus import treebank
from nltk import treetransforms
from nltk import induce_pcfg
from nltk.parse import pchart
from nltk import CFG
from nltk import Nonterminal
from functools import reduce
import sys, time
from nltk import tokenize
from nltk.grammar import toy_pcfg1
from nltk.parse import pchart
from nltk.parse import ViterbiParser
def getGrammar():
    
    fileid=treebank.fileids()
    trainfiles=fileid[:160]
    #testfiles=fileid[0.8*len(fileid):]
    
    
    productions = []
    for item in trainfiles:
        for tree in treebank.parsed_sents(item):
            # perform optional tree transformations, e.g.:
            tree.collapse_unary(collapsePOS = False)# Remove branches A-B-C into A-B+C
            tree.chomsky_normal_form(horzMarkov = 2)# Remove A->(B,C,D) into A->B,C+D->D
            productions += tree.productions()
        
    
    lhs_prod = [p.lhs() for p in productions]
    rhs_prod = [p.rhs() for p in productions]
    set_prod = set(productions)
    
    
    
    
    list_prod = list(set_prod)
    
    
    
    
    
    token_rule = []
    for ele in list_prod:
        if ele.is_lexical():
            token_rule.append(ele)
            
            
    set_token_rule = set(p.lhs() for p in token_rule)
    list_token_rule = list(set_token_rule)
    corr_list_token_rule = []
    for word in list_token_rule:
        if str(word).isalpha():
            corr_list_token_rule.append(word)
            continue
    #print(corr_list_token_rule)
    
    import nltk
    a = []
    for tok in corr_list_token_rule:
        #lhs = nltk.grammar.Nonterminal('UNK')
        lhs = 'UNK'
        rhs = [u'UNK']
        UNK_production = nltk.grammar.Production(lhs, rhs)   
        lhs2 = nltk.grammar.Nonterminal(str(tok))
        a.append(nltk.grammar.Production(lhs2, [lhs]))
    
    
    token_rule.extend(a)
    
    
    list_prod.extend(a)
    
    
    S = Nonterminal('S')
    grammar = induce_pcfg(S,list_prod)
    return grammar


def parseCKY(sentence,grammar):
    # Tokenize the sentence.
    tokens = sentence.split()
    
    #print('Coverage of input words by a grammar:')
    change_words = []
    for i,ele in enumerate(tokens):
        try:
            grammar.check_coverage([ele])
        except:
            #clprint("%s is not covered by the grammar. Replacing it with 'UNK'" % ele)
            change_words.append(tokens[i])
            tokens[i] = 'UNK'
    parsers = [ViterbiParser(grammar)]
# Run the parsers on the tokenized sentence.
    from functools import reduce
    times = []
    average_p = []
    num_parses = []
    all_parses = {}
    for parser in parsers:
        print('\nsentence: %s\n '% (sentence))
        t = time.time()
        parses = parser.parse_all(tokens)
        times.append(time.time()-t)
        if parses: 
            lp = len(parses)
            p = reduce(lambda a,b:a+b.prob(), parses, 0.0)
        else: 
            p = 0
        average_p.append(p)
        num_parses.append(len(parses))
        for p in parses: 
            all_parses[p.freeze()] = 1
    
    
    parses = all_parses.keys()
    if parses: 
        p = reduce(lambda a,b:a+b.prob(), parses, 0)/len(parses)
    else: 
        p = 0
    
    
#    for parse in parses:
#        print(parse)
    return parses
    # Define a list of parsers.  We'll use all parsers.
 
if __name__ == "__main__":
    grammar=getGrammar()
    sentence=input("Enter sentence : ") 
    parses=parseCKY(sentence,grammar)
    
    for parse in parses:
        print(parse)

































