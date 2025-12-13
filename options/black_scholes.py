import yfinance as yf
import numpy as np
import scipy.stats as si
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.graph_objects as go
from datetime import datetime, timedelta


class BlackScholesModel:
    def  __init__(self, S, K, T, r, sigma):
        self.S = S      # Current stock price
        self.K = K      # Strike price
        self.T = T      # Time
        self.r = r      # Risk-free interest rate
        self.sigma = sigma  # Volatility

    def d1(self):
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
    
    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)
    
    def call_price(self):
        d1 = self.d1()
        d2 = self.d2()
        call = (self.S * si.norm.cdf(d1, 0.0, 1.0) - self.K * np.exp(-self.r * self.T) * si.norm.cdf(d2, 0.0, 1.0))
        return call
    
    def put_price(self):
        d1 = self.d1()
        d2 = self.d2()
        put = (self.K * np.exp(-self.r * self.T) * si.norm.cdf(-d2, 0.0, 1.0) - self.S * si.norm.cdf(-d1, 0.0, 1.0))
        return put
    

class BlackScholesGreeks(BlackScholesModel):
    def delta(self, option_type):
        if option_type == 'call':
            return si.norm.cdf(self.d1(), 0.0, 1.0)
        else:
            return -si.norm.cdf(-self.d1(), 0.0, 1.0)
        
    def gamma(self):
        return si.norm.pdf(self.d1(), 0.0, 1.0) / (self.S * self.sigma * np.sqrt(self.T))
    
    def theta(self, option_type):
        if option_type == 'call':
            return (-self.S * si.norm.pdf(self.d1(), 0.0, 1.0) * self.sigma / (2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T) * si.norm.cdf(self.d2(), 0.0, 1.0))
        else:
            return (-self.S * si.norm.pdf(self.d1(), 0.0, 1.0) * self.sigma / (2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T) * si.norm.cdf(-self.d2(), 0.0, 1.0))

    def vega(self):
        return self.S * si.norm.pdf(self.d1(), 0.0, 1.0) * np.sqrt(self.T)
    
    def rho(self, option_type):
        if option_type == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * si.norm.cdf(self.d2(), 0.0, 1.0)
        else:
            return -self.K * self.T * np.exp(-self.r * self.T) * si.norm.cdf(-self.d2(), 0.0, 1.0)


class BlackScholesVisualizer:
    @staticmethod
    def plot_option_prices(S, K, T, r, sigma):
        S_range = np.linspace(0.5 * S, 1.5 * S, 100)
        call_prices = []
        put_prices = []
        
        for s in S_range:
            model = BlackScholesModel(s, K, T, r, sigma)
            call_prices.append(model.call_price())
            put_prices.append(model.put_price())
        
        plt.figure(figsize=(10, 6))
        plt.plot(S_range, call_prices, label='Call Option Price', color='blue')
        plt.plot(S_range, put_prices, label='Put Option Price', color='red')
        plt.title('Black-Scholes Option Prices')
        plt.xlabel('Stock Price')
        plt.ylabel('Option Price')
        plt.legend()
        plt.grid()
        plt.show()



    @staticmethod
    def plot_greeks(S, K, T, r, sigma):
        S_range = np.linspace(0.5 * S, 1.5 * S, 100)
        deltas_call = []
        deltas_put = []
        gammas = []
        thetas_call = []
        thetas_put = []
        vegas = []
        rhos_call = []
        rhos_put = []
        
        for s in S_range:
            greeks = BlackScholesGreeks(s, K, T, r, sigma)
            deltas_call.append(greeks.delta('call'))
            deltas_put.append(greeks.delta('put'))
            gammas.append(greeks.gamma())
            thetas_call.append(greeks.theta('call'))
            thetas_put.append(greeks.theta('put'))
            vegas.append(greeks.vega())
            rhos_call.append(greeks.rho('call'))
            rhos_put.append(greeks.rho('put'))
        
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 3, 1)
        plt.plot(S_range, deltas_call, label='Delta Call', color='blue')
        plt.plot(S_range, deltas_put, label='Delta Put', color='red')
        plt.title('Delta')
        plt.xlabel('Stock Price')
        plt.ylabel('Delta')
        plt.legend()
        plt.grid()
        
        plt.subplot(2, 3, 2)
        plt.plot(S_range, gammas, label='Gamma', color='green')
        plt.title('Gamma')
        plt.xlabel('Stock Price')
        plt.ylabel('Gamma')
        plt.legend()
        plt.grid()
        
        plt.subplot(2, 3, 3)
        plt.plot(S_range, thetas_call, label='Theta Call', color='blue')
        plt.plot(S_range, thetas_put, label='Theta Put', color='red')
        plt.title('Theta')
        plt.xlabel('Stock Price')
        plt.ylabel('Theta')
        plt.legend()
        plt.grid()
        
        plt.subplot(2, 3, 4)
        plt.plot(S_range, vegas, label='Vega', color='purple')
        plt.title('Vega')
        plt.xlabel('Stock Price')
        plt.ylabel('Vega')
        plt.legend()
        plt.grid()
        
        plt.subplot(2, 3, 5)
        plt.plot(S_range, rhos_call, label='Rho Call', color='blue')
        plt.plot(S_range, rhos_put, label='Rho Put', color='red')
        plt.title('Rho')
        plt.xlabel('Stock Price')
        plt.ylabel('Rho')
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # example parameters
    S = 100
    K = 100
    T = 1
    r = 0.05 
    sigma = 0.2 

    BlackScholesVisualizer.plot_option_prices(S, K, T, r, sigma)
    BlackScholesVisualizer.plot_greeks(S, K, T, r, sigma)