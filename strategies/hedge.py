from options.black_scholes import BlackScholesModel, BlackScholesGreeks


class portfolio:
    '''
    TODO: work on notebooks

    Portfolio equation:
    PI =  risky_asset + alpha(i) * asset(i)

    
    if C = call option price and hedge with delta shares of stock S:
    
    PI = C - alpha(1) * S

    diff by Stock price S:
        dPI = dC - alpha(1) = 0
        alpha(1) = dC/dS = delta of option -> thus delta hedging
    '''
    
    pass



class HedgeDelta:
    def __init__(self, S, K, T, r, sigma, option_type, quantity=1):
        self.bs_greeks = BlackScholesGreeks(S, K, T, r, sigma)
        self.option_type = option_type
        self.quantity = quantity

    def calculate_delta(self):
        return self.bs_greeks.delta(self.option_type) * self.quantity
    
    def hedge_position(self):
        delta = self.calculate_delta()
        hedge_amount = -delta
        return hedge_amount