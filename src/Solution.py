import json
import argparse

"""
Helper functions
"""

def _getName(x):
    "Get the name of particular animal"
    return x["name"]

def _getRuler(x):
    "Get the ruler of particular animal"
    return x["ruler"]

def _getPartyScore(x):
    "Get the arty score of particular animal"
    return x["party-animal-score"]

def _filterOutNegative(animals):
    "Filter out animals that have negative score"
    result = [x for x in animals if x.score > 0]
    return result

def _calculateChildrenScore(children):
    "Calculate total children sum"
    score_sum = [x.score for x in children]
    return sum(score_sum)

"""
The Lion King Party
---------------------------------------------------------------------------------------------------------------------------

Mufasa is the main ruler of the Lion King kingdom, and he wants to celebrate the expansion of 
the kingdom with an animal party. Not just any animal party, though; the best animal party possible, as befits a kingdom called the Lion King.

To that end, he’s come up with a party-animal score for every animal in the Lion King kingdom. The party-animal score is a number, 
and the higher the party-animal score, the more fun that the animal will contribute to a party. Party-animal scores may be positive, negative, or zero.
However, Mufasa knows that who you party with is important. If an animal's ruler is at a party,
then the animal will spend all their time looking over their shoulder for their ruler, and that's not fun. Therefore, at this animal party, no animal and their ruler will
both be invited. 

GOALS : 
Your task, as a party organizer, is to write a program that takes in 
an animal listing and outputs the guests to invite in order to maximize the sum of the guests' party-animal scores.

RULES : 
1. A ruler's ruler is okay, but you can't have both an animal and their ruler.
2. No animals will have the same name, so there is no need to worry about name collisions.
3. Each animal has exactly one ruler and appears in the input exactly one time except for the main ruler, who has no ruler.
4. The Lion King kingdom is going to sell your code as a service to other animal kingdoms, so do not assume that the main ruler is always named Mufasa.
5. For bonus points: ensure that your solution always invites the main ruler.
"""

class Node:
    def __init__(self, name, ruler, party_animal_score):
        self.name = name
        self.ruler = ruler
        self.score = party_animal_score
        self.children = []
    
    def addChildren(self, x):
        self.children.append(x)

class LionKingParty:

    def __init__(self, args):
        self.json_file = args.json_file

    def findSolution(self):

        # Read JSON-File
        with open(self.json_file, "r") as read_file:
            animals = json.load(read_file)

        # Create candidates and construct a tree
        candidates = [x for x in animals]
        def constructTree(i, root):

            if i >= len(candidates):
                return root

            curr = root
            for animal in candidates:
                if _getRuler(animal) == root.name:
                    child = Node(_getName(animal), _getRuler(animal), _getPartyScore(animal))
                    curr.addChildren(child)
                    constructTree(i+1, child)
                
        root = Node(_getName(candidates[0]), _getRuler(candidates[0]), _getPartyScore(candidates[0]))
        constructTree(0, root)

        # Searching for optimal solution to have best-sum score
        def depthFirst(tree, not_allowed):
            result = set()
            if len(tree.children) == 0:
                return result

            goodChildren = _filterOutNegative(tree.children)
            if(tree in not_allowed):
                for x in tree.children:
                    result.add(x.name)
                    temp_res = depthFirst(x, not_allowed)
                    result = result.union(temp_res)

                    goodChildren = _filterOutNegative(x.children)
                    if x.score < _calculateChildrenScore(goodChildren) and x.name in result:
                        result.remove(x.name)

            if tree.score > _calculateChildrenScore(goodChildren):
                if(tree.score > 0 and tree not in not_allowed):
                    result.add(tree.name)
                for x in tree.children:
                    not_allowed.add(x)
                    temp_res = depthFirst(x, not_allowed)
                    result = result.union(temp_res)
                return result
            else:
                for x in tree.children:
                    if(x.score > 0):
                        result.add(x.name)
                    temp_res = depthFirst(x, not_allowed)
                    result = result.union(temp_res)

                    goodChildren = _filterOutNegative(x.children)
                    if x.score < _calculateChildrenScore(goodChildren) and x.name in result:
                        result.remove(x.name)

                return result

        solution = depthFirst(root, set())
        for x in solution:
            print(x)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    Script to solve the TheLionKinParty challenge
    ''')
    parser.add_argument('--json_file', type=str, default="test.json", required=False,
                        help='path to the json file')

    args = parser.parse_args()
    
    lion_king_party = LionKingParty(args)
    lion_king_party.findSolution()

