import math

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

card_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
card_type = ["h", "d", "c", "s"]


def calculate_prob(cards: list[tuple[str, int]]):
    total_combintion = (52 * 51 * 50 * 49 * 48) / (5 * 4 * 3 * 2 * 1)
    # 2 numbers are different
    # each combination has the same probability
    # And thw winning percentage could be seen as the average percentage of those
    
    # if two cards same number
    if cards[0][1] == cards[1][1]:
        pass
        
        
        
    # for card in cards:
        
    
    
    
    
    
    