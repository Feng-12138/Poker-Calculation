import math

from itertools import combinations

total_num = math.comb(52, 5)

# simgle pair only:
single_pair_combinations = math.comb(13, 1) * math.comb(4, 2) * math.comb(12, 3) * math.comb(4, 1) ** 3

print(single_pair_combinations / total_num)

# 2 pair only
two_pair_comb = math.comb(13, 2) * math.comb(4, 2) * math.comb(11, 1) * 4

print(two_pair_comb / total_num)

# 3 cards same
three_card_same = math.comb(13, 3) * math.comb(4, 3) * math.comb(10, 2) * math.comb(4, 1) ** 2

# 4 cards same
four_card_same = math.comb(13, 4) * math.comb(4, 4) * math.comb(9, 1) * math.comb(4, 1)

# flushes
num_flushes = (13 - 5 + 1) * 4

# royal flushes (10, 11, 12, 13, 1)
num_royal_flushes = 4

# 5 cards same color
num_same_color = math.comb(13, 5) * 4 - num_flushes - num_royal_flushes



# h stands for heart
# d stands for diamend
# c stands for club
# s stands for sprade

card_nums = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
card_types = ["h", "d", "c", "s"]

allCombineCards = []

two_pair_cards_total = []




def calculate_prob(cards: list[tuple[str, int]]):
    total_combintion = (52 * 51 * 50 * 49 * 48) / (5 * 4 * 3 * 2 * 1)
    # 2 numbers are different
    # each combination has the same probability
    # And thw winning percentage could be seen as the average percentage of those
    
    # if two cards same number
    if cards[0][1] == cards[1][1]:
        pass
    
    all_cards = []
    
    for card_num in card_nums:
        for card_type in card_types:
            cur_card = (card_type, card_num)
            if cur_card not in cards:
                all_cards.append(cur_card)
                
    return all_cards

def check_consecutive(sLst: list):
    for idx in range(1, len(sLst)):
        if sLst[idx] != sLst[idx - 1] + 1:
            return False
        
    return True

def is_royal_flush(combNumsSorted, combTypes):
    if combNumsSorted == [10, 11, 12, 13, 14] and all(element == combTypes[0] for element in combTypes):
        return True
    return False

def is_straight_flush(combNumsSorted, cardTypes):
    if (all(element == cardTypes[0] for element in cardTypes)):
        if check_consecutive(combNumsSorted):
            return True
    return False

def is_flush(cardTypes):
    if (all(element == cardTypes[0] for element in cardTypes)):
        return True
    return False

def is_straight(combNumsSorted):
    if check_consecutive(combNumsSorted):
        return True
    return False

def check_count(cardNums):
    countDict = {}
    for num in cardNums:
        if num in countDict:
            countDict[num] += 1
        else:
            countDict[num] = 1
    maxCount = max(countDict.values())
    countPair = 0
    for val in countDict.values():
        if val == 2:
            countPair += 1
    
    return maxCount, countPair
    
    
def compare_comb(comb1, comb2):
    
    cardNumsOne = []
    cardTypeOne = []
    
    cardNumsTwo = []
    cardTypeTwo = []
    for card in comb1:
        cardNumsOne.append(card[1])
        cardTypeOne.append(card[0])
    
    for card in comb2:
        cardNumsTwo.append(card[1])
        cardTypeTwo.append(card[0])
        
        
    cardNumsOneSorted = cardNumsOne[:]
    cardNumsTwoSorted = cardNumsTwo[:]
    cardNumsOneSorted.sort()
    cardNumsTwoSorted.sort()
    
    countOneDict = {}
    countTwoDict = {}
    
    one = False
    two = False
    
    # check royal flush
    if cardNumsOneSorted == [10, 11, 12, 13, 14] and all(element == cardTypeOne[0] for element in cardTypeOne):
        one = True
    
    if cardNumsTwoSorted == [10, 11, 12, 13, 14] and all(element == cardTypeTwo[0] for element in cardTypeTwo):
        two = True
        
    
    if one and two:
        return "tie"
    elif one:
        return "one"
    elif two:
        return "two"
        
    
    # check straight flush:
    if (all(element == cardTypeOne[0] for element in cardTypeOne)):
        if check_consecutive(cardNumsOneSorted):
            one = True
    
    if (all(element == cardTypeTwo[0] for element in cardTypeTwo)):
        if check_consecutive(cardNumsTwoSorted):
            two = True
            
    if one and two:
        if cardNumsOneSorted[0] > cardNumsTwoSorted[0]:
            return "one"
        elif (cardNumsOneSorted[0] < cardNumsTwoSorted[0]):
            return "two"
        else:
            return "tie"
    elif one:
        return "one"
    elif two:
        return "two"
    
    # check four of kind:
    for num in cardNumsOne:
        if num in countOneDict:
            countOneDict[num] += 1
        else:
            countOneDict[num] = 1
    
    for num in cardNumsTwo:
        if num in countTwoDict:
            countTwoDict[num] += 1
        else:
            countTwoDict[num] = 1
            
    maxCountOne = max(countOneDict.values())
    maxCountTwo = max(countTwoDict.values())
    
    pairCountOne = list(countOneDict.values()).count(2)
    pairCountTwo = list(countTwoDict.values()).count(2)
    
    # single_card_order_one = 
            
    if 4 in countOneDict.values():
        one = True
    
    if 4 in countTwoDict.values():
        two = True
        
    if one and two:
        if cardNumsOneSorted[0] > cardNumsTwoSorted[0]:
            return "one"
        elif (cardNumsOneSorted[0] < cardNumsTwoSorted[0]):
            return "two"
        else:
            return "tie"
    elif one:
        return "one"
    elif two:
        return "two"
        
    
        
        
    
                
best_combs = []

def find_best_combs(comb: list, handCards):
    
    # go through all 5 cards which could be chosen from 7 cards, push to best_combs
    comb.extend(handCards)
    


def find_comb(allCards, handCard = []):
    count = 0
    di = {}
    all_combinations = list(combinations(all_cards, 5))
    for idx, comb in enumerate(all_combinations):
        print(idx)
        cardNum = []
        for card in comb:
            cardNum.append(card[1])
        cardNum.sort()
        
        
    
        
        
        
        
        

if __name__ == "__main__":
    all_cards = calculate_prob([("h", 13), ("s", 13)])
    print(all_cards)
    find_comb(allCards=all_cards)
    
    # given the comb, find how many of total possible combine is better, hiw many worth, then check average
    # to determine the winning prob
        
    
    
    
    