from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal cutting strategy using memoization

    Args:
        length: the length of the rod
        prices: a list of prices, where prices[i] is the price for a rod of length i+1

    Returns:
        A dictionary containing the maximum profit and the list of cuts
    """
    
    memo = {}

    def solve(n: int):
        # Base case: a rod of length 0 has no profit
        if n == 0:
            return 0, []

        # If already computed, return from memo
        if n in memo:
            return memo[n]

        # Start with the assumption: sell the rod as a whole
        best_profit = prices[n - 1]
        best_cuts = [n]

        # Try cutting at every possible position
        for cut in range(1, n):
            left_profit, left_cuts = solve(cut)
            right_profit, right_cuts = solve(n - cut)
            profit = left_profit + right_profit

            if profit > best_profit:
                best_profit = profit
                best_cuts = left_cuts + right_cuts

        memo[n] = (best_profit, best_cuts)
        return memo[n]

    max_profit, cuts = solve(length)
    
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal cutting strategy using tabulation

    Args:
        length: the length of the rod
        prices: a list of prices, where prices[i] is the price for a rod of length i+1

    Returns:
        A dictionary containing the maximum profit and the list of cuts
    """
    
    dp = [0] * (length + 1)          # dp[i] = best profit for rod of length i
    cut_plan = [[] for _ in range(length + 1)]

    for n in range(1, length + 1):
        # Start by assuming we sell the rod without cutting
        best_profit = prices[n - 1]
        best_cuts = [n]

        # Try all possible cuts: split into (cut) + (n-cut)
        for cut in range(1, n):
            profit = dp[cut] + dp[n - cut]
            if profit >= best_profit:
                best_profit = profit
                best_cuts = cut_plan[cut] + cut_plan[n - cut]

        dp[n] = best_profit
        cut_plan[n] = best_cuts

    return {
        "max_profit": dp[length],
        "cuts": cut_plan[length],
        "number_of_cuts": len(cut_plan[length]) - 1
    }


def run_tests():
    """Function to run all tests"""
    test_cases = [
        # Test 1: Base case
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Base case"
        },
        # Test 2: Optimal to not cut
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Optimal to not cut"
        },
        # Test 3: All cuts of length 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Even Cuts"
        }
    ]

    for test in test_cases:
        print(f"\nMaximum Profit: {test['name']}")
        print(f"Rod Length: {test['length']}")
        print(f"Prices: {test['prices']}")

        # Testing memoization
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nMemoization Result:")
        print(f"Maximum Profit: {memo_result['max_profit']}")
        print(f"Cuts: {memo_result['cuts']}")
        print(f"Number of Cuts: {memo_result['number_of_cuts']}")

        # Testing tabulation
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nTabulation Result:")
        print(f"Maximum Profit: {table_result['max_profit']}")
        print(f"Cuts: {table_result['cuts']}")
        print(f"Number of Cuts: {table_result['number_of_cuts']}")

        print("\nTest passed successfully!")

if __name__ == "__main__":
    run_tests()
