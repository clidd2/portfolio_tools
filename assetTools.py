import os
import numpy as np

class Portfolio:

    def __init__(self, assets, face_value):
        self.assets_ = np.array(assets)
        self.face_val_ = face_value

    def get_var(self, lookback, rolling):
        '''value at risk for a given lookback period with rolling timeframe'''
        pass

    def get_allocation(self):
        '''returns current asset allocations.'''
        pass

    def portfolio_correlation(self):
        '''correlations within portfolio'''
        pass


class Asset:

    def __init__(self, purchase_price, current_price, name, identifier, asset_class):
        self.purchase_price_ = purchase_price
        self.current_price_ = current_price
        self.name_ = name
        self.identifer_ = identifier
        self.asset_class_ = asset_class

    def get_purchase_price(self):
        return self.purchase_price_

    def get_current_price(self):
        return self.current_price_

    def get_name(self):
        return self.name_

    def get_identifier(self):
        return self.identifer_

    def get_asset_class(self):
        return self.asset_class_

    def set_current_price(self, price):
        self.current_price_ = price

    def set_name(self, name):
        self.name_ = name

    def set_identifier(self, identifier):
        self.identifer_ = identifier

    def set_asset_class(self, asset_class):
        self.asset_class_ = asset_class

class Bond(Asset):

    def __init__(self, purchase_price, current_price, name, identifier,
                 asset_class, benchmark, par, coupon, ttm, yld, spread = None,
                 type = 'fix', convention = '30/360', periodicity = 'semi',
                 is_dirty = 'Y', is_default = 'N', is_flat = 'N', seniority = 'SNSEC'):

        super().__init__(purchase_price, current_price, name, identifier, asset_class)
        self.benchmark_ = benchmark
        self.par_ = par
        self.coupon_ = coupon
        self.ttm_ = ttm
        self.spread_ = spread
        self.type_ = type
        self.convention_ = convention
        self.periodicity_ = periodicity
        self.is_dirty_ = is_dirty
        self.is_default_ = is_default
        self.is_flat_ = is_flat
        self.seniority_ = seniority
        self.yield_ = yld
        self.theoretical_price_ = self.price_theoretical()
        self.modified_duration_ = self.modified_duration()
        self.convexity_ = self.convexity()
    ####################################################################################################################
    #getters

    def get_par(self):
        '''returns par value of bond'''
        return self.par_

    def get_coupon(self):
        '''returns coupon as a function of par'''
        return self.coupon_

    def get_ttm(self):
        '''returns term to maturity in years'''
        return self.ttm_

    def get_yield(self):
        return self.yield_

    def get_spread(self):
        '''returns spread to benchmark in basis points'''
        return self.spread_

    def get_type(self):
        '''returns fix, float, otherwise'''
        return self.type_

    def get_convention(self):
        '''returns bond accrual convention'''
        return self.convention_

    def get_periodicity(self):
        '''returns annual, semi, quarter, month'''
        return self.periodicity_

    def dirty_clean(self):
        '''returns dirty flag; Y = priced dirty, N = priced clean'''
        return self.is_dirty_

    def get_default_status(self):
        '''returns default status of bond; Y=default, N=non-default'''
        return self.is_default_

    def get_flat_full(self):
        '''returns whether bond is being priced flat or full; only really added this on tail of Ecuador/Argy'''
        return self.is_flat_
    ####################################################################################################################
    #setters
    def set_current_price(self, price=None):
        super().set_current_price()
        if not price:
            self.current_price_ = self.price_theoretical()
        else:
            self.current_price_ = price

    def set_par(self, new_par):
        '''sets par amount in accordance with newly entered par value'''
        self.par_ = new_par

    def set_coupon(self, coupon_bps):
        '''set coupon rate in basis point format'''
        self.coupon_ = coupon_bps

    def set_yield(self, yld=None):
        if not yld:
            #yield returned as decimal, convert to bps
            self.yield_ = self.theoretical_ytm() * 10000
        else:
            self.yield_ = yld

    def set_ttm(self, ttm):
        '''set ttm in years'''
        self.ttm_ = ttm

    def set_spread(self, spread_bps):
        '''set spread to a benchmark in basis points'''
        self.spread_ = spread_bps

    def set_type(self, type):
        '''set type as fix, float, otherwise'''
        self.type_ = type

    def set_convention(self, convention):
        '''set accrual convention'''
        self.convention_ = convention

    def set_periodicity(self, periodicity):
        '''changes periodicity between annual, semi, quarter, month'''
        self.periodicity_ = periodicity

    def set_dirty_flag(self, flag='N'):
        '''sets dirty flag as either 'Y' or 'N' '''
        self.is_dirty_ = flag

    def set_default_status(self, flag='Y'):
        '''sets default flag as either 'Y' or 'N' '''
        self.is_default_ = flag

    def set_flat_full(self, flag='Y'):
        '''sets flat flag as either 'Y' or 'N' '''
        self.is_flat_ = flag

    def set_seniority(self, seniority):
        '''sets bond seniority to specified level'''
        self.seniority_ = seniority
    ####################################################################################################################
    #utility functions

    def price_theoretical(self):
        '''calculate theorretical price of a bond'''

        #get periodicity and convert ttm from years to periods
        if self.get_periodicity() == 'annual':
            periodicity = 1

        elif self.get_periodicity() == 'semi':
            periodicity = 2

        elif self.get_periodicity() == 'quarter':
            periodicity = 4

        elif self.get_periodicity() == 'month':
            periodicity = 12

        else:
            raise ValueError('Periodicity not supported by portfolio tool. Please reach out for addition of different conventions.')

        periods = self.get_ttm() * periodicity

        #convert basis point levels to decimal and account for periodicity in coupon/yield calculation
        coupon_dec = self.get_coupon() / 10000
        yield_dec = self.get_yield() / 10000
        coupon_val = (coupon_dec / periodicity) * self.get_par()
        yield_val = (yield_dec / periodicity)

        #get present value of cash flows; coupons and maturity (par)
        coupon_pv = coupon_val * ((1 - (1 + yield_val) ** -periods) / yield_val)
        maturity_pv = self.get_par() / ((1 + yield_val) ** periods)

        '''must provide some way to figure out accrued interest; must take into account daycount convention, dirty flag, etc.'''
        return coupon_pv + maturity_pv

    def modified_duration(self):
        '''calculate modified duration of a bond'''
        #convert
        #get periodicity and convert ttm from years to periods
        if self.get_periodicity() == 'annual':
            periodicity = 1

        elif self.get_periodicity() == 'semi':
            periodicity = 2

        elif self.get_periodicity() == 'quarter':
            periodicity = 4

        elif self.get_periodicity() == 'month':
            periodicity = 12

        else:
            raise ValueError('Periodicity not supported by portfolio tool. Please reach out for addition of different conventions.')

        periods = self.get_ttm() * periodicity

        #covert yield/coupon to decimal for conversion
        coupon_dec = self.get_coupon() / 10000
        yield_dec = self.get_yield() / 10000
        coupon_val = (coupon_dec / periodicity) * self.get_par()
        yield_val = yield_dec / periodicity

        scaler = (coupon_val / (yield_val ** 2))
        pv_func = 1 - (1 / (1 + yield_val) ** periods)
        coupon_pv = scaler * pv_func
        maturity_pv = (periods * (self.get_par() - (coupon_val / yield_val))) / (1 + yield_val) ** (periods + 1)

        return (coupon_pv + maturity_pv) / self.get_current_price() / periodicity

    def convexity(self):
        '''calculate theoretical convexity of a bond'''
        '''
        (2C / y^3) * (1 - (1+y)^-ttm) - ((2*C*ttm) / (y^2 * (1+y) ^ ttm + 1) + ((ttm * (ttm + 1) * (100 - (C/y))) / ((1 + y) ^ (n + 2)) 
        '''
        # get periodicity and convert ttm from years to periods
        if self.get_periodicity() == 'annual':
            periodicity = 1

        elif self.get_periodicity() == 'semi':
            periodicity = 2

        elif self.get_periodicity() == 'quarter':
            periodicity = 4

        elif self.get_periodicity() == 'month':
            periodicity = 12

        else:
            raise ValueError(
                'Periodicity not supported by portfolio tool. Please reach out for addition of different conventions.')

        periods = self.get_ttm() * periodicity

        # covert yield/coupon to decimal for conversion
        coupon_dec = self.get_coupon() / 10000
        yield_dec = self.get_yield() / 10000
        coupon_val = (coupon_dec / periodicity) * self.get_par()
        yield_val = yield_dec / periodicity

        scaler = (2 * coupon_val) / (yield_val ** 3)
        pv_factor = 1 - (1 + yield_val) ** -periods
        first_order = scaler * pv_factor
        second_order = (2 * coupon_val * periods) / ((yield_val ** 2) * (1 + yield_val) ** (periods + 1))
        third_order = (periods * (periods + 1) * (self.get_par() - (coupon_val / yield_val))) / ((1 + yield_val) ** (periods + 2))
        return first_order - second_order + third_order

    def theoretical_ytm (self):
        '''back out implied yield of bond'''
        initial_yield = (self.get_coupon() / 10000 * self.get_par()) / self.get_current_price()

        print(initial_yield)
        self.set_yield(initial_yield)
        valid = False
        i = 1
        initial_diff = self.get_current_price() - self.price_theoretical()
        step_size = 0.000001

        while not valid:
            new_yield = self.get_yield() / 10000
            price = self.price_theoretical()

            if ((self.get_current_price() + (self.get_current_price() * 0.0001) > price) and self.get_current_price() < price):
                print(f'Took {i} iterations to reach implied yield')
                print(price)
                valid = True
                return self.get_yield()

            elif ((self.get_current_price() - (self.get_current_price() * 0.0001) < price) and self.get_current_price() > price):
                print(f'Took {i} iterations to reach implied yield')
                print(price)
                valid = True
                return self.get_yield()

            elif price > self.get_current_price():
                i += 1
                self.set_yield((new_yield + step_size) * 10000)
                continue

            elif price < self.get_current_price():
                i += 1
                self.set_yield((new_yield - step_size) * 10000)
                continue
            else:
                raise ValueError('IDEK what would kick this off lol')


        return -1


