"""
Cookie Clicker Simulator
"""
import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
import math
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
# SIM_TIME = 10000000000.0
SIM_TIME = 10
class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self.total_num_cookies = float(0.0)
        self.current_num_cookies = float(0.0)
        self.current_time = float(0.0)
        self.current_cps = float(1.0)
        self.history_list = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        output = "Time: " + str(self.current_time) + \
                 " Current Cookies: "+ str(self.total_num_cookies) + \
                 " CPS: " + str(self.current_cps) + \
                 " Total Cookies: " + str(self.total_num_cookies) + \
                 " History (length: " + str(len(self.history_list)) + "): " + \
                 str(self.history_list)
        return output
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self.current_num_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self.current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self.history_list

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self.total_num_cookies:
            time = 0.0
        else:
             time = (cookies - self.current_num_cookies)/self.current_cps   
        return math.ceil(time)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self.current_time += time
            self.current_num_cookies = time * self.current_cps
            self.total_num_cookies += self.current_num_cookies
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self.total_num_cookies >= cost:
            self.current_num_cookies -= cost
            self.current_cps += additional_cps
            self.history_list.append((self.current_time, item_name, cost, self.total_num_cookies))
            
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_info_copy = build_info.clone()
    clicker_state = ClickerState()          
    
    while True:
        if clicker_state.get_time() >= duration:
            if clicker_state.get_cookies() > 0:
                item = strategy(clicker_state.get_cookies(), clicker_state.get_cps(), clicker_state.get_history(), (duration - clicker_state.get_time()), build_info_copy)
                if item != None:
                    clicker_state.buy_item(item, build_info_copy.get_cost(item), build_info_copy.get_cps(item))
                    build_info_copy.update_item(item)
            else:
                break
       
        item = strategy(clicker_state.get_cookies(), clicker_state.get_cps(), clicker_state.get_history(), (duration - clicker_state.get_time()), build_info_copy)
        if item == None:
            time_left = duration - clicker_state.get_time()
            clicker_state.wait(time_left)
            break
        
        wait_time = clicker_state.time_until(build_info_copy.get_cost(item))
        if wait_time > duration - clicker_state.get_time():
            time_left = duration - clicker_state.get_time()
            clicker_state.wait(time_left)
            break
        
        clicker_state.wait(wait_time)
        # item_cps = build_info_copy.get_cps(item)
        clicker_state.buy_item(item, build_info_copy.get_cost(item), build_info_copy.get_cps(item))
        build_info_copy.update_item(item)
    return(clicker_state)


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"
print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.1]}, 1.15), 500.0, strategy_cursor_broken)
def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None
# print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.1]}, 1.15), 15.0, strategy_none) 
def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cookies += time_left * cps
    items =  build_info.build_items()
    min_expense = 99999
    most_cheap_item = None
    for item in items:
        expense = build_info.get_cost(item)
        if expense <= cookies:
            if min_expense > expense:
                min_expense = expense
                most_cheap_item = item
    
    return(most_cheap_item)


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    cookies += time_left * cps
    items =  build_info.build_items()
    max_expense = 0
    most_expensive_item = None
    for item in items:
        expense = build_info.get_cost(item)
        if expense <= cookies:
            if max_expense < expense:
                max_expense = expense
                most_expensive_item = item
    
    return(most_expensive_item)

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    
    items =  build_info.build_items()
    best_cps = 0
    most_cookies_item = None
    
    for item in items:
        ratio = build_info.get_cps(item) / build_info.get_cost(item)
        
        if best_cps < ratio:
            best_cps = ratio
            most_cookies_item = item
    return most_cookies_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

