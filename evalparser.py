import nltk
from nltk.corpus import treebank
from ckyParser import getGrammar,parseCKY



def get_leafs(tree):
    if isinstance(tree,str):
        return [tree]
    else: 
        result = []
        for x in tree[1:]:
            result.extend(get_leafs(x))
        return result
            

def get_constituents(tree,left=0):
    if not tree: 
        return [], left
    start = left
    if isinstance(tree,str): 
        return [],left+1
    else: 
        result = []
        phrase = tree[0]
        for subtree in tree[1:]:
            subspans, right = get_constituents(subtree, left)
            result.extend(subspans)
            left = right
        result.append((phrase,start,left))
        return result, left



def compute_parseval_scores(gold_tree, test_tree): 
    
    gold_const = set(get_constituents(gold_tree)[0])
    test_const = set(get_constituents(test_tree)[0])
    
    if not test_const: 
        return 0.0,0.0,0.0

    correct = len(gold_const.intersection(test_const))     
    recall = correct / float(len(gold_const))
    precision = correct / float(len(test_const))
    fscore = (2*precision*recall) / (precision+recall)
    return precision,recall,fscore 


if __name__ == "__main__":
    grammar=getGrammar()
    fileid=treebank.fileids()
    testfiles=fileid[160:]
    file=open('testraw.txt','r')
    lines=[]
    for line in file:
        lines.append(line)
    total=len(lines)
    fscore_sum=0
    i=0
    unparsed=0
    p_sum=0
    r_sum=0
    print("%10s  %10s  %10s   %10s"%(
      "S.No", "Precision", "Recall", "F1-Score"))
    print("===============================================================")
    for f in testfiles:
        for tree in treebank.parsed_sents(f):
            gold_tree=tree
            test_tree=parseCKY(lines[i],grammar)
            if len(gold_tree)!=len(test_tree):
                unparsed+=1
            p,r,f=compute_parseval_scores(gold_tree,test_tree)
            print("%10s       %0.3f        %0.3f        %0.3f"%(
      i, p,r,f))
            fscore_sum+=f
            p_sum+=p
            r_sum+=r
            i=i+1
    parsed = total-unparsed 
    if parsed == 0:
        coverage = 0.0
        fscore_parsed = 0.0
        fscore_all = 0.0 
    else: 
        coverage =  (parsed / total) *100
        fscore_parsed = fscore_sum / parsed 
        fscore_all = fscore_sum / total
        p_parsed=p_sum/parsed
        r_parsed=r_sum/parsed
        p_all=p_sum/total
        r_all=r_sum/total
    print("Coverage: {:.2f}%".format(coverage))
    print("\nAverage Precision (parsed sentences): {}",.format(p_parsed))   
	print("\nAverage Recall (parsed sentences): {}",.format(r_parsed))
	print("\nAverage F-score (parsed sentences): {}",.format(fscore_parsed))
	print("\nAverage Precision (all sentences): {}",.format(p_all))
	print("\nAverage Recall (all sentences): {}",.format(r_all))
	print("\nAverage F-score (all sentences): {}",.format(fscore_all))