# factorial_contest.py
temp = None 
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

if __name__ == "__main__":
    num = int(input())
    result = factorial(num)
    print(result)

