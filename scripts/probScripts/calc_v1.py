import math

from itertools import combinations

from tqdm import tqdm

from multiprocessing import Pool

card_nums = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
all_nums = []

desk_best_comb_map_other = {}
desk_best_comb_map_current = {}

best_comb_desk_map_other = {}
best_comb_desk_map_current = {}

best_comb_hand_card_dict = {}


def find_combs(handCards, deskCards):
    handDeskCardNumDict = {}
    for i in card_nums:
        handDeskCardNumDict[i] = 0 
    for card in handCards:
        if card in handDeskCardNumDict:
            handDeskCardNumDict[card] += 1
        else:
            handDeskCardNumDict[card] = 1
    
    all_nums = []
    for num in card_nums:
        for _ in range(4 - handDeskCardNumDict[num]):
            all_nums.append(num)
    all_combs_with_without_deskkcards = list(combinations(all_nums, 5))
    
    for card in deskCards:
        if card in handDeskCardNumDict:
            handDeskCardNumDict[card] += 1
        else:
            handDeskCardNumDict[card] = 1
            
    all_nums = []
    for num in card_nums:
        for _ in range(4 - handDeskCardNumDict[num]):
            all_nums.append(num)
    
    
    all_combs_include_all_desk_cards = []
    
    # all_combs should have all other possible combinations of other players, except curent player handcards
    
    for comb in all_combs_with_without_deskkcards:
        if (len(deskCards) == 0):
            all_combs_include_all_desk_cards.append(comb)
        else:
            add_to_comb = True
            for card in deskCards:
                if card not in comb:
                    add_to_comb = False
            if add_to_comb:
                all_combs_include_all_desk_cards.append(comb)
    
    
    possible_hand_cards_for_others_distinct = set(list(combinations(all_nums, 2)))
    
    possible_hand_cards_for_others = list(combinations(all_nums, 2))
    
    possible_hand_count_dict = {}
    
    # 乘以 desk_card出现的次数乘以hand_card出现的次数
    
    for card in possible_hand_cards_for_others:
        if card in possible_hand_count_dict:
            possible_hand_count_dict[card] += 1
        else:
            possible_hand_count_dict[card] = 1
        
    
    nums_count_dict = {}
    other_player_hand_card_dict = {}
    
    for comb in all_combs_with_without_deskkcards:
        if comb in nums_count_dict:
            nums_count_dict[comb] += 1
        else:
            nums_count_dict[comb] = 1

    # deskcards comb count
    num_count_dict_deskcards = {}
    # deskcard
    for comb in all_combs_include_all_desk_cards:
        if comb in num_count_dict_deskcards:
            num_count_dict_deskcards[comb] += 1
        else:
            num_count_dict_deskcards[comb] = 1
            
    
    # return nums_count_dict, list(possible_hand_cards_for_others_distinct), num_count_dict_deskcards
    
    return num_count_dict_deskcards, possible_hand_count_dict

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
            
    tieBreakerDict = {}
    for key in countDict:
        val = countDict[key]
        if val in tieBreakerDict:
            tieBreakerDict[val].append(key)
        else:
            tieBreakerDict[val] = [key]
    for key in tieBreakerDict:
        tieBreakerDict[key].sort()
        tieBreakerDict[key] = tieBreakerDict[key][::-1]
        tieBreakerDict[key] = tuple(tieBreakerDict[key])
    
    return maxCount, countPair, tieBreakerDict

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
        

def is_straight(combNumsSorted):
    def check_consecutive(sLst: list):
        for idx in range(1, len(sLst)):
            if sLst[idx] != sLst[idx - 1] + 1:
                return False
            
        return True
    
    if check_consecutive(combNumsSorted):
        return True
    return False

def compare_combs(comb1, comb2):
    maxCount1, pairNum1, tieBreakerDict1 = check_count(comb1)
    maxCount2, pairNum2, tieBreakerDict2 = check_count(comb2)
    
    one = False
    two = False
    
    # Check Four of kind:
    if (maxCount1 == 4):
        one = True
    if maxCount2 == 4:
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDict1, tieBreakerDict2, [4, 1])
    elif one:
        return "one"
    elif two:
        return "two"
    
    if maxCount1 == 3 and pairNum1 == 1:
        one = True
    
    if maxCount2 == 3 and pairNum2 == 1:
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDict1, tieBreakerDict2, [3, 2])
    elif one:
        return "one"
    elif two:
        return "two"
    
    
    if maxCount1 == 3 and pairNum1 == 1:
        one = True
    
    if maxCount2 == 3 and pairNum2 == 1:
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDict1, tieBreakerDict2, [3, 2])
    elif one:
        return "one"
    elif two:
        return "two"
    
    if is_straight(comb1):
        one = True
    if is_straight(comb2):
        two = True
    
    if one and two:
        return compare_tie_breaker(tieBreakerDict1, tieBreakerDict2, [1])
    elif one:
        return "one"
    elif two:
        return "two"
    
    if maxCount1 == 3:
        one = True
    
    if maxCount2 == 3:
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDict1, tieBreakerDict2, [3, 1])
    elif one:
        return "one"
    elif two:
        return "two"
    
    if pairNum1 == 2:
        one = True
    
    if pairNum2 == 2:
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDict1, tieBreakerDict2, [2, 1])
    elif one:
        return "one"
    elif two:
        return "two"
    
    if pairNum1 == 1:
        one = True
    
    if pairNum2 == 1:
        two = True
        
    if one and two:
        return compare_tie_breaker(tieBreakerDict1, tieBreakerDict2, [2, 1])
    elif one:
        return "one"
    elif two:
        return "two"
    
    return compare_tie_breaker(tieBreakerDict1, tieBreakerDict2, [1])
    

def find_best_comb(comb, handCards, isCurPlayer, curPlayerHandCards):
    combined_list = list(comb)
    hand_list = list(handCards)

    for idx, handCard in enumerate(hand_list):
        if handCard >= combined_list[-1]:
            combined_list.append(handCard)
            continue
        if handCard <= combined_list[0]:
            combined_list.insert(0, handCard)
            continue
        for idx_card, _ in enumerate(combined_list):
            if combined_list[idx_card - 1] <= handCard <= combined_list[idx_card]:
                combined_list.insert(idx_card, handCard)
                break
    # curCombList = combined_list[:]
    
    if not isCurPlayer:
        for card in curPlayerHandCards:
            if combined_list.count(card) + curPlayerHandCards.count(card) >= 5:
                return ()
    
            
    possible_combs = list(combinations(combined_list, 5))
    best_comb = possible_combs[0]
    
    for comb_pos in possible_combs:
        result = compare_combs(best_comb, comb_pos)
        if result == "two":
            best_comb = comb_pos
    return (comb, best_comb, tuple(handCards))

def find_comb_worker(args):
    comb, handCards, isCurPlayer, curPlayerHandCards = args
    return find_best_comb(comb, handCards,isCurPlayer, curPlayerHandCards)

# Given hand card, and desk card, find most suitable combinations
def find_comb(all_combinations, isCurPlayer, curPlayerHandCards, handCardsList=[], num_processes=25):
    retvalList = []
    
    for idx, handCards in tqdm(enumerate(handCardsList), total=len(handCardsList)):
        args_list = [(comb, handCards, isCurPlayer, curPlayerHandCards) for comb in all_combinations]
        retval = []
        with Pool(num_processes) as pool:
            retval = list(pool.imap(find_comb_worker, args_list))
        
        for item in retval:
            if (item != ()):
                retvalList.append(item[1])
                if len(handCardsList) > 1:
                    if item[0] in desk_best_comb_map_other:
                        # List of combinations which has desk card as desk card
                        if item[1] in desk_best_comb_map_other[item[0]]:
                            continue
                        desk_best_comb_map_other[item[0]].append(item[1])
                    else:
                        desk_best_comb_map_other[item[0]] = [item[1]]
                    if item[1] in best_comb_desk_map_other:
                        best_comb_desk_map_other[item[1]].append(item[0])
                    else:
                        best_comb_desk_map_other[item[1]] = [item[0]]
                        
                    # best_comb as key, handcard list as value
                    if item[1] in best_comb_hand_card_dict:
                        best_comb_hand_card_dict[item[1]].append(item[2])
                    else:
                        best_comb_hand_card_dict[item[1]] = [item[2]]
                    
                elif len(handCardsList) == 1:
                    if item[0] in desk_best_comb_map_current:
                        desk_best_comb_map_current[item[0]].append(item[1])
                    else:
                        desk_best_comb_map_current[item[0]] = [item[1]]
                    if item[1] in best_comb_desk_map_current:
                        best_comb_desk_map_current[item[1]].append(item[0])
                    else:
                        best_comb_desk_map_current[item[1]] = [item[0]]
        # turn values as sets
        # for key in 
    
    return retvalList


# def with_desk_card_wrapper(allCards, handCards, deskCards, players_remain):
#     total_percentage = 0
#     deskCardCombs = find_all_comb_include_deskcard(allCards, deskCards)
#     bestCombs = find_comb(allCards, handCards)
#     num_processes = 25
#     args_list = [(comb, deskCardCombs) for comb in bestCombs]
#     with Pool(num_processes) as pool:
#         win_percentages = list(tqdm(pool.imap(calculate_win_percentage, args_list), total=len(bestCombs)))
#         total_percentage += sum(win_percentage ** (players_remain - 1) for win_percentage in win_percentages)
#     return total_percentage / len(bestCombs)


def is_sublist(sublist, full_list):
    return ''.join(map(str, sublist)) in ''.join(map(str, full_list))
    
def calculate_win_percentage(args):
    
    comb, allCombsCountDict, all_combs_count_dict, handCards, best_comb_desk_map_current, desk_best_comb_map_other, best_comb_hand_card_dict, all_possible_hand_card_dict = args
    count_lose = 0
    countTieOrWin = 0
    # needs to add totalAmount
    # combList = list(comb)
    
    # for card in handCards:
    #     if card in combList:
    #         combList.remove(card)
            
    totalSum = 0
    for desk in best_comb_desk_map_current[comb]:
        for comb_other in desk_best_comb_map_other[desk]:
            # all_combs_count_dict has count for the current desk card
            multiplier = 0
            for item in best_comb_hand_card_dict[comb_other]:
                multiplier += all_possible_hand_card_dict[item]
                    
            # totalSum += len(desk_best_comb_map_other[desk]) * all_combs_count_dict[desk] * best_comb_hand_card_dict[comb_other]
            result = compare_combs(comb, comb_other)
            if result == "two":
                count_lose +=  multiplier
            else:
                countTieOrWin += multiplier
    
    # for comb_other in allCombsCountDict.keys():
    #     # skip = False
    #     # for c in combList:
    #     #     if list(comb_other).count(c) == 0:
    #     #         skip = True
    #     #         break
    #     # if skip:
    #     #     continue
        
    #     totalSum += allCombsCountDict[comb_other] * all_combs_count_dict[comb_other]
    #     result = compare_combs(comb, comb_other)
    #     if result == "two":
    #         count_lose += 1 * all_combs_count_dict[comb_other] * allCombsCountDict[comb_other]
            
    # # totalSum = 0
    # # for key in allCombsCountDict.keys():
    # #     totalSum += allCombsCountDict[key] * all_combs_count_dict[key]
        
            
    # result = (totalSum - count_lose) / totalSum
    # return (sum(all_combs_count_dict.values()) - count_lose) / (sum(all_combs_count_dict.values()))
    
    # print(count_lose, countTieOrWin)
    return (countTieOrWin) / (countTieOrWin + count_lose)



def calculate_prob(curPlayerCombs, allCombs, all_combs_count_dict, handCards, best_comb_desk_map_current, desk_best_comb_map_other, best_comb_hand_card_dict, all_possible_hand_card_dict, remainPlayerCount = 5):
    
    # curPLayerCombCountDict = {}
    allCombsCountDict = {}
    # for comb in curPlayerCombs:
    #     if comb not in curPLayerCombCountDict:
    #         curPLayerCombCountDict[comb] = 1
    #     else:
    #         curPLayerCombCountDict[comb] += 1
            
    for comb in allCombs:
        if comb not in allCombsCountDict:
            allCombsCountDict[comb] = 1
        else:
            allCombsCountDict[comb] += 1
            
    num_processes = 25
    args_list = [(comb1, allCombsCountDict, all_combs_count_dict, handCards, best_comb_desk_map_current, desk_best_comb_map_other, best_comb_hand_card_dict, all_possible_hand_card_dict) for comb1 in curPlayerCombs]
    
    total_percentage = 0
    with Pool(num_processes) as pool:
        win_percentages = list(tqdm(pool.imap(calculate_win_percentage, args_list), total=len(list(curPlayerCombs))))
        total_percentage += sum(win_percentage ** (remainPlayerCount - 1) for win_percentage in win_percentages)
    return total_percentage / len(curPlayerCombs)
        
        
        

def find_best_combs(handCards, deskCards):
    all_combs_count_dict, all_possible_hand_card = find_combs(handCards=handCards, deskCards=deskCards)
    
    allCombs = find_comb(list(all_combs_count_dict.keys()), False, handCards, list(all_possible_hand_card.keys()))
    
    curPlayerComb = find_comb(list(all_combs_count_dict.keys()), True, handCards, [handCards])
    
    return curPlayerComb, allCombs, all_combs_count_dict, all_possible_hand_card
    
    # retval = find_comb(list(all_combs_count_dict.keys()), [8, 9])
    
if __name__ == "__main__":
    
    # curPlayerComb, allCombs, all_combs_count_dict, all_possible_hand_card_dict = find_best_combs([2, 4], [])
    
    
    curPlayerComb, allCombs, all_combs_count_dict, all_possible_hand_card_dict = find_best_combs([7, 10], [])
    
    # print(curPlayerComb)
    
    # print(curPlayerComb.count((2, 2, 2, 2, 3)), list(best_comb_desk_map_current.keys()).count((2, 2, 2, 2, 3)))
    # print(allCombs.count((2, 9, 9, 9, 9)))
    result = calculate_prob(curPlayerComb, allCombs, all_combs_count_dict, [7, 10], best_comb_desk_map_current, desk_best_comb_map_other, best_comb_hand_card_dict, all_possible_hand_card_dict, 5)
    
    print(result)
        
    
            
        
        
        