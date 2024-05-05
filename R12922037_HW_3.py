import sys
import math

S = float(sys.argv[1])
X = float(sys.argv[2])
r = float(sys.argv[3])
s = float(sys.argv[4])
T = int(sys.argv[5])
H = float(sys.argv[6])
n = int(sys.argv[7])

number_of_years = float(T) / 365.0
delta_t = number_of_years / float(n)

h = math.log(H / S) // (s * math.sqrt(delta_t))
LAMBDA = math.log(H / S) / (h * s * math.sqrt(delta_t))

u = math.exp(LAMBDA * s * math.sqrt(delta_t))
d = 1.0 / u

pu = 1.0 / (2 * LAMBDA**2) + ((r - (s**2 / 2)) * math.sqrt(delta_t)) / (2 * LAMBDA * s)
pm = 1 - 1.0 / LAMBDA**2
pd = 1.0 / (2 * LAMBDA**2) - ((r - (s**2 / 2)) * math.sqrt(delta_t)) / (2 * LAMBDA * s)

stock_prices = [[S]]
stock_up_times = [[0]]

def PriceGoUp(price):
    return price * u

def PriceGoUpTimes(times):
    return times + 1

for idx in range(n):
    next_prices = list(map(PriceGoUp, stock_prices[idx]))
    next_up_times = list(map(PriceGoUpTimes, stock_up_times[idx]))

    lowest_price = stock_prices[idx][len(stock_prices[idx]) - 1]
    next_prices.append(lowest_price)
    next_prices.append(lowest_price * d)
    stock_prices.append(next_prices)

    least_times = stock_up_times[idx][len(stock_up_times[idx]) - 1]
    next_up_times.append(least_times)
    next_up_times.append(least_times - 1)
    stock_up_times.append(next_up_times)


def GetPayoff(price):
    if price >= H:
        return 0
    else:
        return max(0, X - price)

payoffs = list(map(GetPayoff, stock_prices[n]))

for idx in range(n - 1, -1, -1):
    prev_payoffs = []
    for payoff_idx in range(0, len(payoffs) - 2):
        payoff = (pu * payoffs[payoff_idx] + pm * payoffs[payoff_idx + 1] + pd * payoffs[payoff_idx + 2]) / math.exp(r * delta_t)
        if stock_up_times[idx][payoff_idx] >= h:
            payoff = 0
        prev_payoffs.append(payoff)
    payoffs = prev_payoffs

put_price = payoffs[0]
print("{0:.6f}".format(put_price))
