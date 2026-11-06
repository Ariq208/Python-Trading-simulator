import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# class for each commodity
class commodity:
    def __init__(self, name):
        self.name = name
        self.price = random.randint(150, 5000)
        self.stock = random.randint(10, 1000)
        self.owned = 0
        self.aiowned = 0
        self.history = [self.price]

    # method that increases the commodities prices depending on the news
    def priceup(self):
        initialprice = self.price
        change = random.uniform(1.25, 2.5)
        self.price = round(self.price * change, 2)
        # keep price in reasonable bounds
        while self.price > 5000:
            self.price = initialprice
            change = random.uniform(0.75, 1.25)
            self.price = round(self.price * change, 2)
        return self.price

    # method that decreases the commodities prices depending on the news
    def pricedown(self):
        pricechange = random.uniform(0.1, 0.75)
        self.price = round((self.price * pricechange), 2)
        return self.price

    # method that changes the price of the commodity if the news does not affect them
    def pricechange(self):
        initialprice = self.price
        change = random.uniform(0.75, 1.25)
        self.price = round(self.price * change, 2)
        while self.price > 5000:
            self.price = initialprice
            change = random.uniform(0.75, 1.25)
            self.price = round(self.price * change, 2)
        return self.price

    # method that randomly changes the amount of stock available in the market every minute
    def updatestock(self):
        upordown = random.randint(1, 2)
        if upordown == 1:
            self.stock = max(0, self.stock - random.randint(0, self.stock))
        elif upordown == 2:
            self.stock = self.stock + random.randint(0, max(1, self.stock))
        return self.stock

    # method that updates an array with the history of prices of this commodity
    def historyupd(self):
        self.history.append(self.price)

    def valueowned(self):
        return self.price * self.owned


def calcpercent(history):
    if len(history) < 2:
        return "0.00"
    percent = round(((history[-1] - history[-2]) / history[-2]) * 100, 2)
    if percent < 0:
        percent = "-" + str(abs(percent))
    elif percent > 0:
        percent = "+" + str(percent)
    return percent


class AITrader:
    def __init__(self, startingbudget, hardai, hardmode):
        self.cash = startingbudget
        self.portvalue = startingbudget
        # hardai is boolean: True = smart AI, False = normal/random AI
        self.difficulty = hardai
        # hardmode: True/False but not used in deep logic currently
        self.gamedifficulty = hardmode

    def AIbuy(self, commodity):
        if commodity.price <= 0:
            return
        maxbuy = int(self.cash // commodity.price)
        if maxbuy <= 0:
            return
        # don't buy more than available stock
        maxbuy = min(maxbuy, commodity.stock)
        if maxbuy <= 0:
            return
        if self.difficulty:
            qty = maxbuy
        else:
            qty = random.randint(0, maxbuy)
        if qty <= 0:
            return
        commodity.aiowned += qty
        commodity.stock = max(0, commodity.stock - qty)
        self.cash -= commodity.price * qty

    def AIsell(self, commodity):
        maxsell = int(commodity.aiowned)
        if maxsell <= 0:
            return
        if self.difficulty:
            qty = maxsell
        else:
            qty = random.randint(0, maxsell)
        if qty <= 0:
            return
        commodity.aiowned = max(0, commodity.aiowned - qty)
        commodity.stock += qty
        self.cash += commodity.price * qty

    def smartdecision(self, newsid, market):
        # Use direct mapping of newsid ranges to commodities same as market.marketupdate mapping
        # For smart AI: follow news rationally; for normal AI: random or simple follow
        # Map indices to commodity objects
        # market is instance of market class with fields rice, oil, sugar, cattle, rubber, silver
        if self.difficulty:
            # smart deterministic reaction
            if newsid in (0, 1, 2):
                self.AIbuy(market.rice)
            elif newsid in (3, 4, 5):
                self.AIbuy(market.oil)
            elif newsid in (6, 7, 8):
                self.AIbuy(market.sugar)
            elif newsid in (9, 10, 11):
                self.AIbuy(market.cattle)
            elif newsid in (12, 13, 14):
                self.AIbuy(market.rubber)
            elif newsid in (15, 16, 17):
                self.AIbuy(market.silver)
            elif newsid in (18, 19, 20):
                self.AIsell(market.rice)
            elif newsid in (21, 22, 23):
                self.AIsell(market.oil)
            elif newsid in (24, 25, 26):
                self.AIsell(market.sugar)
            elif newsid in (27, 28, 29):
                self.AIsell(market.cattle)
            elif newsid in (30, 31, 32):
                self.AIsell(market.rubber)
            elif newsid in (33, 34, 35):
                self.AIsell(market.silver)
        else:
            # normal/random AI: sometimes follow news, sometimes random trade
            decision = random.randint(0, 1)
            if decision == 0:
                # follow news but with probabilistic action sizes
                if newsid in (0, 1, 2):
                    self.AIbuy(market.rice)
                elif newsid in (3, 4, 5):
                    self.AIbuy(market.oil)
                elif newsid in (6, 7, 8):
                    self.AIbuy(market.sugar)
                elif newsid in (9, 10, 11):
                    self.AIbuy(market.cattle)
                elif newsid in (12, 13, 14):
                    self.AIbuy(market.rubber)
                elif newsid in (15, 16, 17):
                    self.AIbuy(market.silver)
                elif newsid in (18, 19, 20):
                    self.AIsell(market.rice)
                elif newsid in (21, 22, 23):
                    self.AIsell(market.oil)
                elif newsid in (24, 25, 26):
                    self.AIsell(market.sugar)
                elif newsid in (27, 28, 29):
                    self.AIsell(market.cattle)
                elif newsid in (30, 31, 32):
                    self.AIsell(market.rubber)
                elif newsid in (33, 34, 35):
                    self.AIsell(market.silver)
            else:
                # random commodity action
                randomcommodity = random.randint(1, 6)
                decision2 = random.randint(0, 1)
                if randomcommodity == 1:
                    if decision2 == 0:
                        self.AIbuy(market.rice)
                    else:
                        self.AIsell(market.rice)
                elif randomcommodity == 2:
                    if decision2 == 0:
                        self.AIbuy(market.oil)
                    else:
                        self.AIsell(market.oil)
                elif randomcommodity == 3:
                    if decision2 == 0:
                        self.AIbuy(market.sugar)
                    else:
                        self.AIsell(market.sugar)
                elif randomcommodity == 4:
                    if decision2 == 0:
                        self.AIbuy(market.cattle)
                    else:
                        self.AIsell(market.cattle)
                elif randomcommodity == 5:
                    if decision2 == 0:
                        self.AIbuy(market.rubber)
                    else:
                        self.AIsell(market.rubber)
                elif randomcommodity == 6:
                    if decision2 == 0:
                        self.AIbuy(market.silver)
                    else:
                        self.AIsell(market.silver)

    def caclportvalue(self, market):
        value = self.cash
        rice = market.rice.aiowned * market.rice.price
        oil = market.oil.aiowned * market.oil.price
        sugar = market.sugar.aiowned * market.sugar.price
        cattle = market.cattle.aiowned * market.cattle.price
        rubber = market.rubber.aiowned * market.rubber.price
        silver = market.silver.aiowned * market.silver.price
        value = value + rice + oil + sugar + cattle + rubber + silver
        self.portvalue = value
        return value

    def aicurrentownings(self, commodities):
        # return list of aiowned for each commodity
        return [c.aiowned for c in commodities]

    def aicurrentvalue(self):
        return "£" + str(round(self.portvalue, 2))

    def updateportarray(self, aiportarray):
        # append current value string to provided list
        aiportarray.append(self.aicurrentvalue())


# class for the users portfolio during a game
class portfolio:
    def __init__(self, startcash):
        self.cash = float(startcash)

    # method for user to buy stocks
    def buy(self, commodity, number):
        if number <= 0:
            raise ValueError("Must buy positive amount")
        if number <= commodity.stock and self.cash >= (commodity.price * number):
            self.cash = self.cash - (commodity.price * number)
            commodity.owned = commodity.owned + number
            commodity.stock = commodity.stock - number
        else:
            raise ValueError("Exceeded max amount of stock bought or insufficient cash")

    # method for user to sell stocks
    def sell(self, commodity, number):
        if number <= 0:
            raise ValueError("Must sell positive amount")
        if number <= commodity.owned:
            commodity.owned = commodity.owned - number
            self.cash = number * commodity.price + self.cash
            commodity.stock = commodity.stock + number
        else:
            raise ValueError("You do not have enough stock to sell this amount")

    # method to calculate portfolio value
    def portvalue(self, commodities):
        total = 0
        for i in range(len(commodities)):
            total = total + commodities[i].owned * commodities[i].price
        return total


# class for the market for the game
class market:
    def __init__(self, commodities):
        self.rice = commodities[0]
        self.oil = commodities[1]
        self.sugar = commodities[2]
        self.cattle = commodities[3]
        self.rubber = commodities[4]
        self.silver = commodities[5]

    # updates all prices and stocks for each commodity in the market
    def marketupdate(self, newsid):
        self.rice.price = self.rice.pricechange()
        self.oil.price = self.oil.pricechange()
        self.sugar.price = self.sugar.pricechange()
        self.cattle.price = self.cattle.pricechange()
        self.rubber.price = self.rubber.pricechange()
        self.silver.price = self.silver.pricechange()
        self.rice.stock = self.rice.updatestock()
        self.oil.stock = self.oil.updatestock()
        self.sugar.stock = self.sugar.updatestock()
        self.cattle.stock = self.cattle.updatestock()
        self.rubber.stock = self.rubber.updatestock()
        self.silver.stock = self.silver.updatestock()

        if newsid in (0, 1, 2):
            self.rice.price = self.rice.priceup()
            self.rice.stock = self.rice.stock + random.randint(0, max(1, self.rice.stock))
        elif newsid in (3, 4, 5):
            self.oil.price = self.oil.priceup()
            self.oil.stock = self.oil.stock + random.randint(0, max(1, self.oil.stock))
        elif newsid in (6, 7, 8):
            self.sugar.price = self.sugar.priceup()
            self.sugar.stock = self.sugar.stock + random.randint(0, max(1, self.sugar.stock))
        elif newsid in (9, 10, 11):
            self.cattle.price = self.cattle.priceup()
            self.cattle.stock = self.cattle.stock + random.randint(0, max(1, self.cattle.stock))
        elif newsid in (12, 13, 14):
            self.rubber.price = self.rubber.priceup()
            self.rubber.stock = self.rubber.stock + random.randint(0, max(1, self.rubber.stock))
        elif newsid in (15, 16, 17):
            self.silver.price = self.silver.priceup()
            self.silver.stock = self.silver.stock + random.randint(0, max(1, self.silver.stock))
        elif newsid in (18, 19, 20):
            self.rice.price = self.rice.pricedown()
            self.rice.stock = max(0, self.rice.stock - random.randint(0, max(1, self.rice.stock)))
        elif newsid in (21, 22, 23):
            self.oil.price = self.oil.pricedown()
            self.oil.stock = max(0, self.oil.stock - random.randint(0, max(1, self.oil.stock)))
        elif newsid in (24, 25, 26):
            self.sugar.price = self.sugar.pricedown()
            self.sugar.stock = max(0, self.sugar.stock - random.randint(0, max(1, self.sugar.stock)))
        elif newsid in (27, 28, 29):
            self.cattle.price = self.cattle.pricedown()
            self.cattle.stock = max(0, self.cattle.stock - random.randint(0, max(1, self.cattle.stock)))
        elif newsid in (30, 31, 32):
            self.rubber.price = self.rubber.pricedown()
            self.rubber.stock = max(0, self.rubber.stock - random.randint(0, max(1, self.rubber.stock)))
        elif newsid in (33, 34, 35):
            self.silver.price = self.silver.pricedown()
            self.silver.stock = max(0, self.silver.stock - random.randint(0, max(1, self.silver.stock)))

    # generates a newsid
    def newsgen(self):
        newsid = random.randint(0, 35)
        return newsid


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Game Simulator")
        self.root.geometry("1200x700")

        self.initial_frame = None
        self.playing_frame = None
        self.running = False
        self.updinterval = 60
        self.time_left = 0

        # UI variables (set in initialscreen)
        self.duration_entry = None
        self.budget_entry = None
        self.difficulty = tk.IntVar(value=1)
        self.ai_choice = tk.IntVar(value=0)

        self.initialscreen()

    def initialscreen(self):
        if self.playing_frame:
            self.playing_frame.destroy()

        self.initial_frame = tk.Frame(self.root)
        self.initial_frame.pack(expand=True, padx=20, pady=20)

        tk.Label(self.initial_frame, text="Trading Game Simulator", font=("Arial", 20)).pack(padx=10, pady=5)
        tk.Label(self.initial_frame, text="Do you want to play a game?", font=("Arial", 16)).pack(padx=10, pady=5)

        tk.Label(self.initial_frame, text="Game Duration (minimum 5 minutes):", font=("Arial", 14)).pack(padx=10, pady=5)
        self.duration_entry = tk.Entry(self.initial_frame)
        self.duration_entry.insert(0, "10")
        self.duration_entry.pack()

        tk.Label(self.initial_frame, text="Starting Budget (minimum £5000):", font=("Arial", 14)).pack(padx=10, pady=5)
        self.budget_entry = tk.Entry(self.initial_frame)
        self.budget_entry.insert(0, "10000")
        self.budget_entry.pack()

        # AI choice frame (radio buttons: mutually exclusive)
        ai_frame = tk.Frame(self.initial_frame)
        ai_frame.pack(pady=10)
        tk.Label(ai_frame, text="Settings:", font=("Arial", 16)).grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(ai_frame, text="AI trader:", font=("Arial", 14)).grid(row=1, column=0, sticky="w", padx=5)
        tk.Radiobutton(ai_frame, text="Normal AI", font=("Arial", 10), variable=self.ai_choice, value=1).grid(row=2, column=0, sticky="w")
        tk.Radiobutton(ai_frame, text="Smart AI", font=("Arial", 10), variable=self.ai_choice, value=2).grid(row=2, column=1, sticky="w")
        tk.Radiobutton(ai_frame, text="No AI", font=("Arial", 10), variable=self.ai_choice, value=3).grid(row=2, column=2, sticky="w")

        # Difficulty frame
        difficulty_frame = tk.Frame(self.initial_frame)
        difficulty_frame.pack(pady=10)
        tk.Label(difficulty_frame, text="Game Difficulty:", font=("Arial", 14)).grid(row=0, column=0, columnspan=2)
        tk.Radiobutton(difficulty_frame, text="Normal mode", font=("Arial", 10), variable=self.difficulty, value=1).grid(row=1, column=0, sticky="w")
        tk.Radiobutton(difficulty_frame, text="Hard mode", font=("Arial", 10), variable=self.difficulty, value=2).grid(row=1, column=1, sticky="w")

        tk.Button(self.initial_frame, text="Start Game", font=("Arial", 14), command=self.setupgame).pack(pady=30)

    def setupgame(self):
        # read values (safe parsing)
        try:
            gametime = int(self.duration_entry.get())
            startcash = int(self.budget_entry.get())
        except Exception:
            messagebox.showerror("Error", "Please enter valid integer values for time and budget.")
            return

        if gametime < 5 or startcash < 5000:
            messagebox.showerror("Error", "Minimum duration is 5 min and £5,000 starting cash.")
            return

        # preserve user choices
        diff_val = self.difficulty.get()
        aichoice_val = self.ai_choice.get()
        hardmode = (diff_val == 2)
        ai_enabled = (aichoice_val in (1, 2))
        ai_hard = (aichoice_val == 2)

        self.initial_frame.destroy()
        self.running = True
        self.time_left = gametime * 60
        self.portfolio = portfolio(startcash)
        self.commodities = [commodity("Rice"), commodity("Oil"), commodity("Sugar"), commodity("Cattle"), commodity("Rubber"), commodity("Silver")]
        self.market = market(self.commodities)

        if ai_enabled:
            self.ai = AITrader(startcash, ai_hard, hardmode)
        else:
            self.ai = None

        self.playing_screen()
        # initial update immediately
        self.update_market()
        self.timer()

    def playing_screen(self):
        if self.playing_frame:
            self.playing_frame.destroy()

        self.playing_frame = tk.Frame(self.root)
        self.playing_frame.pack(fill="both", expand=True)

        misc_frame = tk.Frame(self.playing_frame)
        misc_frame.pack(fill="x")
        self.currentcash_label = tk.Label(misc_frame, text=f"Cash: £{self.portfolio.cash:.2f}", font=("Arial", 14))
        self.currentcash_label.pack(side="left", padx=20)
        self.portfoliovalue_label = tk.Label(misc_frame, text=f"Total Assets: £{self.portfolio.portvalue(self.commodities) + self.portfolio.cash:.2f}", font=("Arial", 14))
        self.portfoliovalue_label.pack(side="left", padx=20)
        self.timer_label = tk.Label(misc_frame, text="Time Left: ", font=("Arial", 14))
        self.timer_label.pack(side="right", padx=20)

        market_frame = tk.Frame(self.playing_frame)
        market_frame.pack(side="left", fill="both", expand=True)

        self.news_frame = tk.Frame(self.playing_frame, height=500, width=300)
        self.news_frame.pack(side="right", pady=10)
        tk.Label(self.news_frame, text="News", font=("Arial", 16)).pack(pady=10)
        self.news_text = tk.Text(self.news_frame, height=30, width=50, wrap="word")
        self.news_text.pack(padx=10, pady=10)

        # AI panel only if AI exists
        if self.ai is not None:
            self.ai_frame = tk.Frame(self.playing_frame, width=300)
            self.ai_frame.pack(side="right", pady=10, fill="y")

            self.aiportfolio_frame = tk.Frame(self.ai_frame, height=30, width=50)
            self.aiportfolio_frame.pack(pady=10)
            self.aiportfolio_label = tk.Label(self.aiportfolio_frame, text=f"AI Trader Total Value: £{self.ai.portvalue:.2f}", font=("Arial", 14))
            self.aiportfolio_label.pack(pady=10)

            self.aicommodity_frame = tk.Frame(self.ai_frame, height=30, width=50)
            self.aicommodity_frame.pack(pady=5)
            # create labels for AI holdings (pack vertically)
            self.ai_rice_label = tk.Label(self.aicommodity_frame, text=f"Rice owned: {self.market.rice.aiowned}, Value: £{self.market.rice.price * self.market.rice.aiowned}")
            self.ai_oil_label = tk.Label(self.aicommodity_frame, text=f"Oil owned: {self.market.oil.aiowned}, Value: £{self.market.oil.price * self.market.oil.aiowned}")
            self.ai_sugar_label = tk.Label(self.aicommodity_frame, text=f"Sugar owned: {self.market.sugar.aiowned}, Value: £{self.market.sugar.price * self.market.sugar.aiowned}")
            self.ai_cattle_label = tk.Label(self.aicommodity_frame, text=f"Cattle owned: {self.market.cattle.aiowned}, Value: £{self.market.cattle.price * self.market.cattle.aiowned}")
            self.ai_rubber_label = tk.Label(self.aicommodity_frame, text=f"Rubber owned: {self.market.rubber.aiowned}, Value: £{self.market.rubber.price * self.market.rubber.aiowned}")
            self.ai_silver_label = tk.Label(self.aicommodity_frame, text=f"Silver owned: {self.market.silver.aiowned}, Value: £{self.market.silver.price * self.market.silver.aiowned}")
            self.ai_rice_label.pack(anchor="w", padx=6, pady=2)
            self.ai_oil_label.pack(anchor="w", padx=6, pady=2)
            self.ai_sugar_label.pack(anchor="w", padx=6, pady=2)
            self.ai_cattle_label.pack(anchor="w", padx=6, pady=2)
            self.ai_rubber_label.pack(anchor="w", padx=6, pady=2)
            self.ai_silver_label.pack(anchor="w", padx=6, pady=2)

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=market_frame)
        self.canvas.get_tk_widget().pack(pady=20)

        # commodity list: create frames and store their label widgets
        commodityframe = tk.Frame(market_frame)
        commodityframe.pack(side="left", fill="y", padx=10)

        # rice frame
        riceframe = tk.Frame(commodityframe)
        riceframe.pack(anchor="w", pady=3)
        self.rice_label = tk.Label(riceframe, text=f"Rice   | £{self.market.rice.price} | Stock: {self.market.rice.stock} left  ", font=("Arial", 14))
        self.rice_label.pack(side="left", padx=10)
        tk.Button(riceframe, text="Buy", command=lambda com=self.market.rice: self.buy_stock(com)).pack(side="left", padx=5)
        tk.Button(riceframe, text="Sell", command=lambda com=self.market.rice: self.sell_stock(com)).pack(side="left", padx=5)

        # oil frame
        oilframe = tk.Frame(commodityframe)
        oilframe.pack(anchor="w", pady=3)
        self.oil_label = tk.Label(oilframe, text=f"Oil    | £{self.market.oil.price} | Stock: {self.market.oil.stock} left  ", font=("Arial", 14))
        self.oil_label.pack(side="left", padx=10)
        tk.Button(oilframe, text="Buy", command=lambda com=self.market.oil: self.buy_stock(com)).pack(side="left", padx=5)
        tk.Button(oilframe, text="Sell", command=lambda com=self.market.oil: self.sell_stock(com)).pack(side="left", padx=5)

        # sugar frame
        sugarframe = tk.Frame(commodityframe)
        sugarframe.pack(anchor="w", pady=3)
        self.sugar_label = tk.Label(sugarframe, text=f"Sugar  | £{self.market.sugar.price} | Stock: {self.market.sugar.stock} left  ", font=("Arial", 14))
        self.sugar_label.pack(side="left", padx=10)
        tk.Button(sugarframe, text="Buy", command=lambda com=self.market.sugar: self.buy_stock(com)).pack(side="left", padx=5)
        tk.Button(sugarframe, text="Sell", command=lambda com=self.market.sugar: self.sell_stock(com)).pack(side="left", padx=5)

        # cattle frame
        cattleframe = tk.Frame(commodityframe)
        cattleframe.pack(anchor="w", pady=3)
        self.cattle_label = tk.Label(cattleframe, text=f"Cattle | £{self.market.cattle.price} | Stock: {self.market.cattle.stock} left  ", font=("Arial", 14))
        self.cattle_label.pack(side="left", padx=10)
        tk.Button(cattleframe, text="Buy", command=lambda com=self.market.cattle: self.buy_stock(com)).pack(side="left", padx=5)
        tk.Button(cattleframe, text="Sell", command=lambda com=self.market.cattle: self.sell_stock(com)).pack(side="left", padx=5)

        # rubber frame
        rubberframe = tk.Frame(commodityframe)
        rubberframe.pack(anchor="w", pady=3)
        self.rubber_label = tk.Label(rubberframe, text=f"Rubber | £{self.market.rubber.price} | Stock: {self.market.rubber.stock} left  ", font=("Arial", 14))
        self.rubber_label.pack(side="left", padx=10)
        tk.Button(rubberframe, text="Buy", command=lambda com=self.market.rubber: self.buy_stock(com)).pack(side="left", padx=5)
        tk.Button(rubberframe, text="Sell", command=lambda com=self.market.rubber: self.sell_stock(com)).pack(side="left", padx=5)

        # silver frame
        silverframe = tk.Frame(commodityframe)
        silverframe.pack(anchor="w", pady=3)
        self.silver_label = tk.Label(silverframe, text=f"Silver | £{self.market.silver.price} | Stock: {self.market.silver.stock} left  ", font=("Arial", 14))
        self.silver_label.pack(side="left", padx=10)
        tk.Button(silverframe, text="Buy", command=lambda com=self.market.silver: self.buy_stock(com)).pack(side="left", padx=5)
        tk.Button(silverframe, text="Sell", command=lambda com=self.market.silver: self.sell_stock(com)).pack(side="left", padx=5)

        # initial graph draw
        self.update_graph()

    def update_labels(self):
        self.currentcash_label.config(text=f"Cash: £{self.portfolio.cash:.2f}")
        self.portfoliovalue_label.config(text=f"Total Assets: £{self.portfolio.portvalue(self.commodities) + self.portfolio.cash:.2f}")
        self.rice_label.config(text=f"Rice   | £{self.market.rice.price} | Stock: {self.market.rice.stock} left")
        self.oil_label.config(text=f"Oil    | £{self.market.oil.price} | Stock: {self.market.oil.stock} left")
        self.sugar_label.config(text=f"Sugar  | £{self.market.sugar.price} | Stock: {self.market.sugar.stock} left")
        self.cattle_label.config(text=f"Cattle | £{self.market.cattle.price} | Stock: {self.market.cattle.stock} left")
        self.rubber_label.config(text=f"Rubber | £{self.market.rubber.price} | Stock: {self.market.rubber.stock} left")
        self.silver_label.config(text=f"Silver | £{self.market.silver.price} | Stock: {self.market.silver.stock} left")
        if hasattr(self, "ai") and self.ai is not None:
            self.aiportfolio_label.config(text=f"AI Trader Total Value: £{self.ai.caclportvalue(self.market):.2f}")
            self.ai_rice_label.config(text=f"Rice owned: {self.market.rice.aiowned}, Value: £{self.market.rice.price * self.market.rice.aiowned}")
            self.ai_oil_label.config(text=f"Oil owned: {self.market.oil.aiowned}, Value: £{self.market.oil.price * self.market.oil.aiowned}")
            self.ai_sugar_label.config(text=f"Sugar owned: {self.market.sugar.aiowned}, Value: £{self.market.sugar.price * self.market.sugar.aiowned}")
            self.ai_cattle_label.config(text=f"Cattle owned: {self.market.cattle.aiowned}, Value: £{self.market.cattle.price * self.market.cattle.aiowned}")
            self.ai_rubber_label.config(text=f"Rubber owned: {self.market.rubber.aiowned}, Value: £{self.market.rubber.price * self.market.rubber.aiowned}")
            self.ai_silver_label.config(text=f"Silver owned: {self.market.silver.aiowned}, Value: £{self.market.silver.price * self.market.silver.aiowned}")

    def timer(self):
        if self.running:
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.config(text=f"Time Left: {mins:02}:{secs:02}")
            if self.time_left <= 0:
                self.end_game()
            else:
                self.time_left = self.time_left - 1
                self.root.after(1000, self.timer)
        else:
            return

    def end_game(self):
        self.running = False
        totalvalue = self.portfolio.portvalue(self.commodities) + self.portfolio.cash
        if messagebox.askyesno("Game Over", f"Final Value: £{totalvalue:.2f}, Will you play again?"):
            # reset minimal state and go back to initial screen
            self.initialscreen()
        else:
            self.root.destroy()

    def buy_stock(self, commodity):
        try:
            num = simpledialog.askinteger("Buy", f"Enter number of {commodity.name} to buy:")
            if num and num > 0:
                self.portfolio.buy(commodity, num)
                self.update_labels()
        except Exception as e:
            messagebox.showerror("Buy error", str(e))

    def sell_stock(self, commodity):
        try:
            number = simpledialog.askinteger("Sell", f"Enter number of {commodity.name} to sell:")
            if number and number > 0:
                self.portfolio.sell(commodity, number)
                self.update_labels()
        except Exception as e:
            messagebox.showerror("Sell error", str(e))

    def update_market(self):
        if not self.running:
            return

        newsid = self.market.newsgen()
        self.market.marketupdate(newsid)
        # choose which news to show (you had news arrays; use the simple one)
        try:
            if hasattr(self, "difficulty") and self.difficulty.get() == 2:
                news = hardnewsarray[newsid]
            else:
                news = newsarray[newsid]
        except Exception:
            news = newsarray[newsid]

        self.display_news(news)

        # AI reacts if present
        if hasattr(self, "ai") and self.ai is not None:
            self.ai.smartdecision(newsid, self.market)

        self.market.rice.historyupd()
        self.market.oil.historyupd()
        self.market.sugar.historyupd()
        self.market.cattle.historyupd()
        self.market.rubber.historyupd()
        self.market.silver.historyupd()
        # update UI
        self.update_graph()
        self.update_labels()

        # schedule next update
        self.root.after(self.updinterval * 1000, self.update_market)

    def display_news(self, news):
        self.news_text.delete(1.0, tk.END)
        self.news_text.insert(tk.END, f"{news}\n")

    def update_graph(self):
        self.ax.clear()
        self.ax.plot(self.market.rice.history, label="Rice")
        self.ax.plot(self.market.oil.history, label="Oil")
        self.ax.plot(self.market.sugar.history, label="Sugar")
        self.ax.plot(self.market.cattle.history, label="Cattle")
        self.ax.plot(self.market.rubber.history, label="Rubber")
        self.ax.plot(self.market.silver.history, label="Silver")
        self.ax.legend(loc="upper left")
        self.ax.set_title("Commodity Prices")
        self.canvas.draw()


# main program
global newsarray
newsarray = [
    "Severe drought in Southeast Asia disrupts rice harvests,cutting global supply",
    "Major importer increases rice purchases ahead of festival season, pushing demand higher",
    "Government announces new subsidy program for rice exports, boosting market optimism",
    "OPEC agrees to production cuts to stabilize falling prices, sending crude futures higher",
    "Tensions rise in major oil-producing region, sparking fears of supply disruption",
    "Global economic rebound increases energy demand, lifting oil prices to 6-month highs",
    "Unseasonal rains damage sugarcane crops in Brazil, tightening global sugar supply",
    "Soft drink manufacturers report strong quarterly demand, boosting sugar consumption outlook",
    "Export restrictions lifted in key producing countries, improving international sugar trade sentiment",
    "Rising beef exports to Asia push cattle prices to record levels",
    "Feed costs fall, allowing ranchers to expand herds and improve market expectations",
    "Health-conscious consumers drive higher demand for premium grass-fed beef",
    "Heavy monsoon rains disrupt tapping in Southeast Asia, slashing natural rubber output",
    "Automotive industry reports surge in tire demand, boosting rubber prices",
    "Asian Rubber Producers Group forecasts supply shortfall for upcoming quarter",
    "Investors flock to silver as inflation fears grow, sending prices soaring",
    "Solar panel manufacturers increase silver purchases amid renewable energy boom",
    "Mining strikes in Latin America cause supply bottlenecks, lifting global silver prices",
    "Record harvests in India and Thailand flood the global rice market, pushing prices down",
    "Government releases emergency rice reserves to curb food inflation",
    "Lower export demand from Africa and the Middle East weakens rice prices",
    "OPEC announces production increase to meet growing demand, causing supply glut fears",
    "Global economic slowdown reduces industrial fuel consumption",
    "Major new oil discovery boosts long-term supply expectations, sending crude prices lower",
    "Surplus sugar production in India drives global prices to 2-year lows",
    "Health regulations and sugar taxes reduce soft drink consumption worldwide",
    "Improved weather conditions in Brazil raise forecasts for sugarcane output",
    "Export bans on beef from major producers lead to oversupply in domestic markets",
    "Plant-based meat alternatives gain popularity, reducing cattle demand",
    "Rising feed costs squeeze profit margins, leading to herd sell-offs and lower prices",
    "Automotive slowdown dampens tire production, cutting rubber demand",
    "Synthetic rubber producers ramp up output, pressuring natural rubber prices",
    "Strong currency in export nations makes rubber more expensive overseas, reducing sales",
    "Interest rate hikes strengthen dollar, reducing investor appetite for precious metals",
    "Silver mines resume full production after labor dispute, easing supply concerns",
    "Slowing demand in electronics and solar industries weighs on silver prices"
]

global hardnewsarray
hardnewsarray = [
    "Severe drought in Southeast Asia disrupts rice harvests",
    "Major importer increases rice purchases ahead of festival season",
    "Government announces new subsidy program for rice exports",
    "OPEC agrees to production cuts to stabilize falling prices",
    "Tensions rise in major oil-producing region",
    "Global economic rebound increases energy demand",
    "Unseasonal rains damage sugarcane crops in Brazil",
    "Soft drink manufacturers report strong quarterly demand",
    "Export restrictions lifted in key producing countries",
    "Rising beef exports to Asia",
    "Feed costs fall",
    "Health-conscious consumers drive higher demand for premium grass-fed beef",
    "Heavy monsoon rains disrupt tapping in Southeast Asia",
    "Automotive industry reports surge in tire demand",
    "Asian Rubber Producers Group forecasts supply shortfall for upcoming quarter",
    "Investors flock to silver as inflation fears grow",
    "Solar panel manufacturers are in a renewable energy boom",
    "Mining strikes in Latin America cause supply bottlenecks",
    "Record harvests in India and Thailand flood the global rice market",
    "Government releases emergency rice reserves to curb food inflation",
    "Lower export demand from Africa and the Middle East",
    "OPEC announces production increase to meet growing demand",
    "Global economic slowdown in factories",
    "Major new oil discovery boosts long-term supply expectations",
    "Surplus sugar production in India",
    "Health regulations and sugar taxes reduce soft drink consumption worldwide",
    "Improved weather conditions in Brazil raise forecasts",
    "Export bans on beef from major producers",
    "Plant-based meat alternatives gain popularity",
    "Rising feed costs squeeze profit margins",
    "Automotive slowdown dampens tire production",
    "Synthetic rubber producers ramp up output",
    "Strong currency in export nations makes rubber more expensive overseas",
    "Interest rate hikes strengthen dollar",
    "Silver mines resume full production after labor dispute",
    "Slowing demand in electronics and solar industries"
]

root = tk.Tk()
game = GUI(root)
root.mainloop()
