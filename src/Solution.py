import json

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
    
    def calculateChildrenScore(self):
        score_sum = [x.score for x in self.children]
        return sum(score_sum)

def _getName(x):
    "Get the name of particular animal"
    return x["name"]

def _getRuler(x):
    "Get the ruler of particular animal"
    return x["ruler"]

def _getPartyScore(x):
    "Get the arty score of particular animal"
    return x["party-animal-score"]

# Read JSON-File
with open("test.json", "r") as read_file:
    animals = json.load(read_file)

# Get rid of animals with negative score and construct a tree
candidates = [x for x in animals if _getPartyScore(x) > 0]
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



# """
# Old non-optimal solution
# """
# candidates.sort(key=_getPartyScore, reverse=True)
# rulers = set()
# solution = []
# for x in candidates:
#     if _getRuler(x) is None:
#         continue
#     if _getRuler(x) not in solution:
#         rulers.add(_getRuler(x))
#         solution.append(_getName(x))





