from stat_parser import Parser
from nltk.tree import Tree
from nltk.tree import ParentedTree
parser = Parser()

#tree = parser.parse("Starbucks was one of those early to criticize President Trump for putting a temporary hold on " +
#                   "immigration from a list of seven terror-torn countries flagged by the Obama administration. In response, the coffee house ")

query = raw_input('Article: ')
tree = parser.parse(query.decode('ascii', errors='ignore'))
# ptree = ParentedTree.fromstring(tree.)
# tree = ' '.join([w for w in tree.leaves()])
# print tree
tree.draw()
"""
ptree = ParentedTree.convert(tree)

leaf_values = ptree.leaves()

if 'Trump' in leaf_values:
    leaf_index = leaf_values.index('Trump')
    tree_location = tree.leaf_treeposition(leaf_index)
    print tree_location
    print leaf_values.index('Trump').parent()
"""