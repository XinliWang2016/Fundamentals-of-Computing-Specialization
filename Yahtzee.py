"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    max_score = 0
    all_numbers = set(hand)
    for item1 in all_numbers:
        score = 0
        for item2 in hand:
            if item1 == item2:
                score += item2
        if score > max_score:
            max_score = score
                    
    return max_score

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    temp = gen_all_sequences(tuple(range(1, num_die_sides + 1)), num_free_dice)
    total = 0
        
    for item in temp:
        total += score(held_dice + item)
    return float(total)/len(temp)         
                   
def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    length = len(hand)
    all_possible = gen_all_sequences((1, 0), length)
    result = set()
    for item in all_possible:
        temp = list()
        for item1, item2 in zip(item, hand):
            item3 = item1 * item2
            temp.append(item3)
        while 0 in temp:
            temp.remove(0)
        result.add(tuple(temp))
    return result

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_possible_holds = gen_all_holds(hand)
    score = 0
    max_score = 0
    hold_dice = tuple()
    for item in all_possible_holds:
        score = expected_value(item, num_die_sides, len(hand) - len(item))
        if score > max_score:
            max_score = score
            hold_dice = item
    return (max_score, hold_dice)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



