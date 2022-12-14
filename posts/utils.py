import calendar
from datetime import date
from dateutil.relativedelta import relativedelta


def get_settlement_months(settlement_period, settlement_month):
    months = [i + 1 for i in range(12)]
    settlement_months_count = int(12 / settlement_period)
    settlement_months = [months[((settlement_month + (month * settlement_period)) - 1) % 12] for month in range(settlement_months_count)]
    settlement_months.sort()
    return settlement_months


def calculate_month(post, user_posts, Post):
    '''
    post(Post) - Post Object to calculate
    user_posts(Queryset) - all user posts
    Post - PostModel used only for exception
    '''

    user_config = post.user.userconfig
    user_rules = user_config.rules

    energy_sent_back = 0.7 if user_config.pv_power > 10 else 0.8

    try:
        previous_post_date = post.date - relativedelta(months=1)
        previous_post = user_posts.get(date__month=previous_post_date.month, date__year=previous_post_date.year)

        # Setting required data based on previous month
        if post.produced is None or user_config.produced_input == 'all':
            post.produced = post.produced_all - previous_post.produced_all
        else:
            post.produced_all = post.produced + previous_post.produced_all
            
        if post.received is None or user_config.received_input == 'all':
            post.received = post.received_all - previous_post.received_all
        else:
            post.received_all = post.received + previous_post.received_all

        if post.sent is None or user_config.sent_input == 'all':
            post.sent = post.sent_all - previous_post.sent_all
        else:
            post.sent_all = post.sent + previous_post.sent_all
    
    # If there is no post in previous month we calculate based only on this month
    except Post.DoesNotExist:
        if post.produced_all is None:
            post.produced_all = post.produced + user_config.produced_start
        else:
            post.produced = post.produced_all - user_config.produced_start

        if post.received_all is None:
            post.received_all = post.received + user_config.received_start
        else:
            post.received = post.received_all -  user_config.received_start

        if post.sent_all is None:
            post.sent_all = post.sent + user_config.sent_start
        else:
            post.sent = post.sent_all - user_config.sent_start

    # Gettting posts from one year back to calculate energy surplus
    # Current post isn't included because it could be edited thus it might differ
    date_year_back = post.date + relativedelta(years=-1, months=+1)
    year_back_posts = user_posts.filter(date__range=[date_year_back, previous_post_date])
    
    # Calculations
    post.autoconsumption = post.produced - post.sent
    post.autoconsumption_percentage = round(post.autoconsumption / post.produced, 2)
    post.consumption = post.produced + post.received - post.sent
    post.consumption_average = round(post.consumption / calendar.monthrange(post.date.year, post.date.month)[1], 2)
    post.saved_funds = post.autoconsumption + post.sent * user_config.energy_buy_price

    settlement_months = get_settlement_months(user_config.settlement_period, user_config.settlement_month)

    if user_rules == 'metering':
        # Reseting values, because when editing already existing post we would be constantly
        # increasing value
        post.energy_surplus = 0
        
        # Going back through post from year back until we find settlement month
        for _post in year_back_posts:
            # If we catch settlement month and it's value is greater than 0, then we add
            # whole energy surplus from this period
            if _post.date.month in settlement_months: 
                if _post.energy_surplus > 0:
                    post.energy_surplus += _post.energy_surplus
                break
            # else we're just adding saved/negative energy
            post.energy_surplus += (_post.sent * energy_sent_back) - _post.received
            
        # Manualy adding current post data
        post.energy_surplus += (post.sent * energy_sent_back) - post.received
        post.energy_surplus = round(post.energy_surplus, 2)

        post.balance = round(post.energy_surplus * user_config.energy_sell_price, 2)


    if user_rules == 'billing':
        # Reseting values, because when editing already existing post we would be constantly
        # increasing value
        post.energy_surplus = 0
        post.balance = 0
        
        # Same thing as in metering
        for _post in year_back_posts:
            if _post.date.month in settlement_months: 
                if _post.balance > 0:
                    post.balance += _post.balance
                break
            post.balance += (_post.sent * energy_sent_back * user_config.energy_sell_price) - (_post.received * user_config.energy_buy_price)

        post.balance += (post.sent * energy_sent_back * user_config.energy_sell_price) - (post.received * user_config.energy_buy_price)
        post.balance = round(post.balance, 2)