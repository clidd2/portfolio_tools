import assetTools as tools

def test_bond_functionality():

    purchase_price = 90
    current_price = 80.231
    name = 'Goldman Sachs Bond'
    identifier = 'USP569123FD1'
    asset_class = 'Bond'
    benchmark = '30Y'
    par = 100
    coupon = 1000
    ttm = 20
    yld = 900
    spread = None
    type = 'fix'
    convention = '30/360'
    periodicity = 'semi'
    is_dirty = 'Y'
    is_default = 'N'
    is_flat = 'N'
    seniority = 'SNSEC'

    my_bond = tools.Bond(
         purchase_price=purchase_price, current_price=current_price, name=name, identifier=identifier,
         asset_class=asset_class, benchmark=benchmark, par=par, coupon=coupon, ttm=ttm, yld=yld, spread=spread,
         type=type, convention=convention, periodicity=periodicity, is_dirty=is_dirty, is_default=is_default,
         is_flat=is_flat, seniority=seniority)

    #print(my_bond.price_theoretical())
    #print(my_bond.modified_duration())
    #print(my_bond.convexity())
    print(my_bond.theoretical_ytm())

test_bond_functionality()


