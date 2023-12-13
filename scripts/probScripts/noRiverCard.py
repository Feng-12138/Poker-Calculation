import math

from itertools import combinations

from tqdm import tqdm

from multiprocessing import Pool

# h stands for heart
# d stands for diamend
# c stands for club
# s stands for sprade

card_nums = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
card_types = ["h", "d", "c", "s"]

allCombineCards = []

royal_flush_combs = []

straight_flush_combs = []

four_of_kind_combs = []

full_house_combs = []

flush_combs = []

straight_combs = []

three_of_combs = []

two_pair_combs = []

pair_combs = []

high_card_combs = []

all_royal_flush_combs = []

all_straight_flush_combs = []

all_four_of_kind_combs = []

all_full_house_combs = []

all_flush_combs = []

all_straight_combs = []

all_three_of_combs = []

all_two_pair_combs = []

all_pair_combs = []

all_high_card_combs = []



def calculate_prob(cards: list[tuple[str, int]]):
    # 2 numbers are different
    # each combination has the same probability
    # And thw winning percentage could be seen as the average percentage of those
    
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

def compare_tie_breaker(tieBreakerDict1, tieBeeakerDict2, values):
    # values need to from large to small
    for val in values:
        if val not in tieBreakerDict1 and val not in tieBeeakerDict2:
            continue
        elif val in tieBreakerDict1 and val not in tieBeeakerDict2:
            return "one"
        elif val not in tieBreakerDict1 and val in tieBeeakerDict2:
            return "two"
            
        if tieBreakerDict1[val] > tieBeeakerDict2[val]:
            return "one"
        elif tieBreakerDict1[val] < tieBeeakerDict2[val]:
            return "two"
        else:
            return "tie"
    
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
    
    tieBreakerDictOne = {}
    tieBreakerDictTwo = {}
    
    for key in countOneDict:
        val = countOneDict[key]
        if val in tieBreakerDictOne:
            tieBreakerDictOne[val].append(key)
        else:
            tieBreakerDictOne[val] = [key]
    for key in tieBreakerDictOne:
        tieBreakerDictOne[key].sort()
        tieBreakerDictOne[key] = tieBreakerDictOne[key][::-1]
        tieBreakerDictOne[key] = tuple(tieBreakerDictOne[key])
    
    for key in countTwoDict:
        val = countTwoDict[key]
        if val in tieBreakerDictTwo:
            tieBreakerDictTwo[val].append(key)
        else:
            tieBreakerDictTwo[val] = [key]
    for key in tieBreakerDictTwo:
        tieBreakerDictTwo[key].sort()
        tieBreakerDictTwo[key] = tieBreakerDictTwo[key][::-1]
        tieBreakerDictTwo[key] = tuple(tieBreakerDictTwo[key])
        
    
    pairCountOne = list(countOneDict.values()).count(2)
    pairCountTwo = list(countTwoDict.values()).count(2)
            
    if 4 in countOneDict.values():
        one = True
    
    if 4 in countTwoDict.values():
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDictOne, tieBreakerDictTwo, [4, 1])
        
    elif one:
        return "one"
    elif two:
        return "two"
    
    # Check for full house
    if 3 in countOneDict.values() and 2 in countOneDict.values():
        one = True
    if 3 in countTwoDict.values() and 2 in countTwoDict.values():
        two = True
    
    if one and two:
        return compare_tie_breaker(tieBreakerDict1=tieBreakerDictOne, tieBeeakerDict2=tieBreakerDictTwo, values=[3, 2]);
    elif one:
        return "one"
    elif two:
        return "two"
    
    # Check for flush
    if is_flush(cardTypes=cardTypeOne):
        one = True
    if is_flush(cardTypes=cardTypeTwo):
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDict1=tieBreakerDictOne, tieBeeakerDict2=tieBreakerDictTwo, values=[3, 2, 1])
    elif one:
        return "one"
    elif two:
        return "two"
    
    # check for straight:
    if is_straight(cardNumsOneSorted):
        one = True
    if is_straight(cardNumsTwoSorted):
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDict1=tieBreakerDictOne, tieBeeakerDict2=tieBreakerDictTwo, values=[1])
    elif one:
        return "one"
    elif two:
        return "two"
    
    # check for three of kind
    
    if 3 in countOneDict.values():
        one = True
    
    if 3 in countTwoDict.values():
        two = True
    
    
    if one and two:
        return compare_tie_breaker(tieBreakerDict1=tieBreakerDictOne, tieBeeakerDict2=tieBreakerDictTwo, values=[3, 1])
    
    elif one:
        return "one"
    elif two:
        return "two"
    
    # Check for two pair
    if pairCountOne == 2:
        one = True
        
    if pairCountTwo == 2:
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDict1=tieBreakerDictOne, tieBeeakerDict2=tieBreakerDictTwo, values=[2, 1])
    elif one:
        return "one"
    elif two:
        return "two"
    
    # Check for pair:
    if 2 in countOneDict.values():
        one = True
    
    if 2 in countTwoDict.values():
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDict1=tieBreakerDictOne, tieBeeakerDict2=tieBreakerDictTwo, values=[2, 1])
    elif one:
        return "one"
    elif two:
        return "two"
    
    # for high card
    return compare_tie_breaker(tieBreakerDict1=tieBreakerDictOne, tieBeeakerDict2=tieBreakerDictTwo, values=[2, 1])
    
                
best_combs = []

def find_best_combs(comb: list, handCards: list):
    
    # go through all 5 cards which could be chosen from 7 cards, push to best_combs
    comb.extend(handCards)
    all_combinations = list(combinations(comb, 5))
    found = True
    
    for combOne in all_combinations:
        for combTwo in all_combinations:
            result = compare_comb(combOne, combTwo)
            if result == "two":
                found = False
                break
        if found:
            return combOne
        found = True
    
    
def find_best_comb_helper(allCombs: list, handCards: list):
    retval = []
    for comb in tqdm(allCombs):
        curComb = find_best_combs(list(comb), handCards)
        retval.append(curComb)
    return retval

def find_comb_worker(args):
    comb, handCards = args
    return find_best_combs(list(comb), handCards)

def find_comb(allCards, handCards=[], num_processes=25):
    all_combinations = list(combinations(allCards, 5))
    args_list = [(comb, handCards) for comb in all_combinations]
    
    with Pool(num_processes) as pool:
        retval = list(tqdm(pool.imap(find_comb_worker, args_list), total=len(all_combinations)))

    return retval
    
# def find_comb(allCards, handCards = []):
#     all_combinations = list(combinations(allCards, 5))
#     retval = []
#     for comb in tqdm(all_combinations):
#         curComb = find_best_combs(list(comb), handCards)
#         retval.append(curComb)
#     return retval

def find_all_comb_include_deskcard(allCards, deskcard = []):
    all_combinations = list(combinations(allCards, 5))
    
    retval = []
    for comb in tqdm(all_combinations):
        add = True
        for card in deskcard:
            if card not in comb:
                add = False
        if add:
            retval.append(comb)
    return retval
        

def find_comb_no_handcard(allCards):
    all_combinations = list(combinations(allCards, 5))
    return all_combinations

def categorized_comb(allCombs):
    for comb in tqdm(allCombs):
        cardNums = []
        cardTypes = []
        
        for card in comb:
            cardNums.append(card[1])
            cardTypes.append(card[0])
        cardNumsSorted = cardNums[:]
        cardNumsSorted.sort()
        
        maxCount, numPairs = check_count(cardNums=cardNums)
        if (is_royal_flush(cardNumsSorted, cardTypes)):
            royal_flush_combs.append(cardNumsSorted)
        elif (is_straight_flush(cardNumsSorted, cardTypes)):
            straight_flush_combs.append(cardNumsSorted)
        elif (maxCount == 4):
            four_of_kind_combs.append(cardNumsSorted)
        elif (maxCount == 3 and numPairs == 1):
            full_house_combs.append(cardNumsSorted)
        elif (is_flush(cardTypes)):
            flush_combs.append(cardNumsSorted)
        elif (is_straight(cardNumsSorted)):
            straight_combs.append(cardNumsSorted)
        elif (maxCount == 3):
            three_of_combs.append(cardNumsSorted)
        elif (maxCount == 2 and numPairs == 2):
            two_pair_combs.append(cardNumsSorted)
        elif (maxCount == 2):
            pair_combs.append(cardNumsSorted)
        else:
            high_card_combs.append(cardNumsSorted)
            
def categorize_all_cards_without_hands(allCombs, handCards):
    for comb in tqdm(allCombs):
        dup = False
        for card in handCards:
            if card in comb:
                dup = True
                break
        if dup:
            continue
        cardNums = []
        cardTypes = []
        
        for card in comb:
            cardNums.append(card[1])
            cardTypes.append(card[0])
        cardNumsSorted = cardNums[:]
        cardNumsSorted.sort()
        
        maxCount, numPairs = check_count(cardNums=cardNums)
        if (is_royal_flush(cardNumsSorted, cardTypes)):
            all_royal_flush_combs.append(cardNumsSorted)
        elif (is_straight_flush(cardNumsSorted, cardTypes)):
            all_straight_flush_combs.append(cardNumsSorted)
        elif (maxCount == 4):
            all_four_of_kind_combs.append(cardNumsSorted)
        elif (maxCount == 3 and numPairs == 1):
            all_full_house_combs.append(cardNumsSorted)
        elif (is_flush(cardTypes)):
            all_flush_combs.append(cardNumsSorted)
        elif (is_straight(cardNumsSorted)):
            all_straight_combs.append(cardNumsSorted)
        elif (maxCount == 3):
            all_three_of_combs.append(cardNumsSorted)
        elif (maxCount == 2 and numPairs == 2):
            all_two_pair_combs.append(cardNumsSorted)
        elif (maxCount == 2):
            all_pair_combs.append(cardNumsSorted)
        else:
            all_high_card_combs.append(cardNumsSorted)
        
        

# This func
            
def calculate_prob_cur_comb(cardNums, totalNum, royalFlushNum, straightFlushNum, fourOfKindNum, fullHouseNum,
                   flushNum, straightNum, threeKindNum, twoPairNum, pairNum, cardType):
    cardCountDict = {}
    cardValDict = {}
    for cardNum in cardNums:
        if cardNum in cardCountDict:
            cardCountDict[cardNum] += 1
        else:
            cardCountDict[cardNum] = 1
    
    for key in cardCountDict.keys():
        if cardCountDict[key] in cardValDict:
            cardValDict[cardCountDict[key]].append(key)
        else:
            cardValDict[cardCountDict[key]] = [key]
            
    for key in cardValDict:
        cardValDict[key].sort()
        cardValDict[key] = tuple(cardValDict[key][::-1])
        
    
    if (cardType == "royal"):
        return 1
    elif cardType == "straight flush":
        numLarger = (14 - cardValDict[1][0]) * 4
        return (totalNum - numLarger) / totalNum
    elif cardType == "four kind":
        numLarger = royalFlushNum + straightFlushNum
        curCardNumFour = cardValDict[4][0]
        curCardNumOne = cardValDict[1][0]
        
        a = 0
        
        if curCardNumOne > curCardNumFour:
            a = (14 - curCardNumFour - 1) * (13 - 2) * 4 + (14 - curCardNumOne)
        else:
            a = (14 - curCardNumFour) * (13 - 2) * 4 + (14 - curCardNumOne)
        
        numLarger += a
        return (totalNum - numLarger) / totalNum
        
        
    elif cardType == "full":
        numLarger = royalFlushNum + straightFlushNum + fourOfKindNum
        
        curCardNumThree = cardValDict[3][0]
        curCardNumTwo = cardValDict[2][0]
        
        a = 0
        if curCardNumTwo > curCardNumThree:
            a = (14 - curCardNumThree - 1) * math.comb(4, 3) * math.comb(4, 2) * (13 - 2) + (14 - curCardNumTwo) * math.comb(4, 2)
        else:
            a = (14 - curCardNumThree) * math.comb(4, 3) * math.comb(4, 2) * (13 - 2) + (14 - curCardNumTwo) * math.comb(4, 2)
        
        numLarger += a
        
        return (totalNum - numLarger) / totalNum
    
    elif cardType == "flush":
         numLarger = royalFlushNum + straightFlushNum + fourOfKindNum + fullHouseNum
         a = 0
         # this has error but should be close
         for idx, num in enumerate(cardValDict[1]):
            a += 4 * (14 - num) * math.comb(13 - 1, (5 - idx - 1)) / 2
         numLarger += a
        
         return (totalNum - numLarger) / totalNum
        
    
    elif cardType == "straight":
        # max is the A and the worst is 5,
        numLarger =  royalFlushNum + straightFlushNum + fourOfKindNum + fullHouseNum + flushNum
        curMax = cardValDict[1][0]
        
        a = (14 - curMax) * 4 ** 4 * 4
        numLarger += a
        
        return (totalNum - numLarger) / totalNum
        
    elif cardType == "three":
        numLarger = royalFlushNum + straightFlushNum + fourOfKindNum + fullHouseNum + flushNum + straightNum
        
        curThreeMax = cardValDict[3][0]
        
        a = (14 - curThreeMax) * math.comb(4, 3) * math.comb(49, 2)
                
        for idx, curNum in enumerate(cardValDict[1]):
            a += (14 - curNum) * 48 ** (2 - idx - 1)
        
        numLarger += a
        return (totalNum - numLarger) / totalNum
            
    elif cardType == "two pair":
        
        numLarger = royalFlushNum + straightFlushNum + fourOfKindNum + fullHouseNum + flushNum + straightNum + threeKindNum
        
        a = 0
        
        for i in range(14 - cardValDict[2][0]):
            curVal = 14 - i
            a += math.comb(curVal - 1, 1) * 6 * 12 * math.comb(4, 1)
            
        for i in range(14 - cardValDict[2][1]):
             curVal = 14 - i
             a += 12 * math.comb(4, 1)
             
        numLarger += a
        
        return (totalNum - numLarger) / totalNum
    
    elif cardType == "pair":
        numLarger = royalFlushNum + straightFlushNum + fourOfKindNum + fullHouseNum + flushNum + straightNum + threeKindNum + twoPairNum
        
        a = (14 - cardValDict[2][0]) * math.comb(4, 2) * math.comb(12, 3) * 4
        
        # 这边得
        for i in range(14 - cardValDict[1][0]):
            curVal = 14 - i
            a += 4 * math.comb(curVal - 4, 2) * 4**2
            
        for i in range(14 - cardValDict[1][1]):
            curVal = 14 - i
            a += 4 * math.comb(curVal - 4, 1) * 4
            
        for i in range(14 - cardValDict[1][2]):
            curVal = 14 - i
            a += 4
        
        # a += (14 - cardValDict[1][0]) * 4 * math.comb(11, 2) * 4**2
        
        # a += (14 - cardValDict[1][1]) * 4 * 10 * 4
        
        # a += (14 - cardValDict[1][2]) * 4
        
        numLarger += a
        
        return (totalNum - numLarger) / totalNum
    
    elif cardType == "high":
        numLarger = royalFlushNum + straightFlushNum + fourOfKindNum + fullHouseNum + flushNum + straightNum + threeKindNum + twoPairNum + pairNum
        
        # print(numLarger / totalNum)
        a = 0
        
        for i in range(14 - cardValDict[1][0]):
            curVal = 14 - i
            a += 4 ** 4 * math.comb(curVal - 3, 4)
        
        for i in range(14 - cardValDict[1][1]):
            curVal = 14 - i
            a += 4 ** 3 * math.comb(curVal - 3, 3)
            
        for i in range(14 - cardValDict[1][2]):
            curVal = 14 - i
            a += 4 ** 2 * math.comb(curVal - 3, 2)
            
        for i in range(14 - cardValDict[1][3]):
            curVal = 14 - i
            a += 4 ** 1 * math.comb(curVal - 3, 1)
            
        a += 14 - cardValDict[1][4]
        
        numLarger += a
        
        return (totalNum - numLarger) / totalNum
         
# All cards

def with_desk_card_wrapper(allCards, handCards, deskCards, players_remain):
    total_percentage = 0
    deskCardCombs = find_all_comb_include_deskcard(allCards, deskCards)
    bestCombs = find_comb(allCards, handCards)
    num_processes = 25
    args_list = [(comb, deskCardCombs) for comb in bestCombs]
    with Pool(num_processes) as pool:
        win_percentages = list(tqdm(pool.imap(calculate_win_percentage, args_list), total=len(bestCombs)))
        total_percentage += sum(win_percentage ** (players_remain - 1) for win_percentage in win_percentages)
    
def calculate_win_percentage(args):
    comb, deskCardCombs = args
    count_lose = 0
    for comb_other in deskCardCombs:
        result = compare_comb(comb, comb_other)
        if result == "two":
            count_lose += 1
    return (len(deskCardCombs) - count_lose) / len(deskCardCombs)
    
    
# def cal_desk_cards(allCards: list, handCards: list, deskCards: list):
#     deskCardCombs = find_all_comb_include_deskcard(allCards, deskCards)
#     bestCombs = find_comb(allCards, handCards)
    
#     total_percentage = 0
#     for comb in tqdm(bestCombs):
#         countLose = 0
#         for combOther in deskCardCombs:
#             result = compare_comb(comb, combOther)
#             if result == "two":
#                 countLose += 1
#         winPercentage = (len(deskCardCombs) - countLose) / len(deskCardCombs)
#         total_percentage += winPercentage ** 4
#     return total_percentage / len(deskCardCombs)
        
    

if __name__ == "__main__":
    deskCards = [("h", 8), ("s", 8), ("c", 8)]
    hand_cards = [("h", 13), ("s", 13)]
    
    # deskCardsList = [[("h", 4), ("s", 7), ("c", 13)], [("h", 4), ("s", 7), ("c", 13), ("s", 10)], [("h", 4), ("s", 7), ("c", 13), ("s", 10), ("s", 4)]]
    # hand_cardsList = [[("h", 13), ("c", 7)], [("s", 2), ("s", 8)], [("d", 14), ("d", 12)]]
    
    # for i, deskCards in enumerate(deskCardsList):
    #     for hand_cards in hand_cardsList:
    #         result = multiProcess_wrapper(all_cards, hand_cards, deskCards, min(2, 3 - i))
    #         print(result, deskCards, hand_cards)
    
    all_cards = calculate_prob([hand_cards])
    
    # This is for having river cards, and not done testing yet
    
    result = with_desk_card_wrapper(all_cards, hand_cards, deskCards)
    print(result)
    
    # This is when there is no river card
    
    # # 能拿到的最好的牌（7张牌组成5张）
    # retvals = find_comb(allCards=all_cards, handCards=hand_cards)
    
    # # 不包括hand card
    # allCombs = find_comb_no_handcard(allCards=all_cards)
    
    # categorized_comb(retvals)
    
    # categorize_all_cards_without_hands(allCombs, hand_cards)
    
    # totalNum = len(all_royal_flush_combs) + len(all_straight_flush_combs) + len(all_four_of_kind_combs) + len(all_full_house_combs) + \
    #     len(all_flush_combs) + len(all_straight_combs) + len(all_three_of_combs) + len(all_two_pair_combs) + len(all_pair_combs) + \
    #     len(all_high_card_combs)
        
    # total_sum = 0
    
    # for comb in royal_flush_combs:
        
    #     result = calculate_prob_cur_comb(comb, totalNum, len(all_royal_flush_combs), len(all_straight_flush_combs), len(all_four_of_kind_combs), len(all_full_house_combs),
    #                                      len(all_flush_combs), len(all_straight_combs), len(all_three_of_combs), len(all_two_pair_combs), len(all_pair_combs), "royal")
        
    #     total_sum += result ** 4
        
    # for comb in straight_flush_combs:
    #     result = calculate_prob_cur_comb(comb, totalNum, len(all_royal_flush_combs), len(all_straight_flush_combs), len(all_four_of_kind_combs), len(all_full_house_combs),
    #                                      len(all_flush_combs), len(all_straight_combs), len(all_three_of_combs), len(all_two_pair_combs), len(all_pair_combs), "straight flush")
        
    #     total_sum += result ** 4
        
    # for comb in four_of_kind_combs:
    #     result = calculate_prob_cur_comb(comb,totalNum, len(all_royal_flush_combs), len(all_straight_flush_combs), len(all_four_of_kind_combs), len(all_full_house_combs),
    #                                      len(all_flush_combs), len(all_straight_combs), len(all_three_of_combs), len(all_two_pair_combs), len(all_pair_combs), "four kind")
        
    #     total_sum += result ** 4

    # for comb in full_house_combs:
    #     result = calculate_prob_cur_comb(comb, totalNum, len(all_royal_flush_combs), len(all_straight_flush_combs), len(all_four_of_kind_combs), len(all_full_house_combs),
    #                                      len(all_flush_combs), len(all_straight_combs), len(all_three_of_combs), len(all_two_pair_combs), len(all_pair_combs), "full")
    #     total_sum += result ** 4
        
    # for comb in flush_combs:
    #     result = calculate_prob_cur_comb(comb, totalNum, len(all_royal_flush_combs), len(all_straight_flush_combs), len(all_four_of_kind_combs), len(all_full_house_combs),
    #                                      len(all_flush_combs), len(all_straight_combs), len(all_three_of_combs), len(all_two_pair_combs), len(all_pair_combs), "flush")
        
    #     total_sum += result ** 4
        
    # for comb in straight_combs:
    #     result = calculate_prob_cur_comb(comb, totalNum, len(all_royal_flush_combs), len(all_straight_flush_combs), len(all_four_of_kind_combs), len(all_full_house_combs),
    #                                      len(all_flush_combs), len(all_straight_combs), len(all_three_of_combs), len(all_two_pair_combs), len(all_pair_combs), "straight")
    #     total_sum += result ** 4
        
    # for comb in three_of_combs:
    #     result = calculate_prob_cur_comb(comb, totalNum,  len(all_royal_flush_combs), len(all_straight_flush_combs), len(all_four_of_kind_combs), len(all_full_house_combs),
    #                                      len(all_flush_combs), len(all_straight_combs), len(all_three_of_combs), len(all_two_pair_combs), len(all_pair_combs), "three")
    #     total_sum += result ** 4
        
    # for comb in two_pair_combs:
    #     result = calculate_prob_cur_comb(comb, totalNum, len(all_royal_flush_combs), len(all_straight_flush_combs), len(all_four_of_kind_combs), len(all_full_house_combs),
    #                                      len(all_flush_combs), len(all_straight_combs), len(all_three_of_combs), len(all_two_pair_combs), len(all_pair_combs), "two pair")
    #     total_sum += result ** 4
        
    # for comb in pair_combs:
    #     result = calculate_prob_cur_comb(comb, totalNum, len(all_royal_flush_combs), len(all_straight_flush_combs), len(all_four_of_kind_combs), len(all_full_house_combs),
    #                                      len(all_flush_combs), len(all_straight_combs), len(all_three_of_combs), len(all_two_pair_combs), len(all_pair_combs), "pair")
        
    #     total_sum += result ** 4
        
    # for comb in high_card_combs:
    #     result = calculate_prob_cur_comb(comb, totalNum, len(all_royal_flush_combs), len(all_straight_flush_combs), len(all_four_of_kind_combs), len(all_full_house_combs),
    #                                      len(all_flush_combs), len(all_straight_combs), len(all_three_of_combs), len(all_two_pair_combs), len(all_pair_combs), "high")
    #     # print(result)
    #     total_sum += result ** 4
        
    # print(total_sum)
        
    # print(total_sum / totalNum)
    
    
    
    
    # given the comb, find how many of total possible combine is better, hiw many worth, then check average
    # to determine the winning prob
        
    
    
    
    
    
    