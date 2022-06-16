""" This code was written to answer Free Code Camps 3rd project in
Scientific Calculation with Python: Budget App // 31/03/2022"""


def split(word): #GeekforGeeks
    return [char for char in word]


class Category:
    def __init__(self, Category):
        self.info = dict()
        self.name = Category
        self.length = len(self.info)
        self.ledger = []

    def __str__(self):
        line1 = str(self.name.center(30, "*"))
        tmp = ""
        for item in self.ledger:
            descrip = item['description'][:23] if len(item['description'])>23 else item['description']
            amount = "{:.2f}".format(item['amount']).rjust(30-len(descrip))
            line = descrip + amount
            tmp = tmp + line + "\n"
        final_line = "Total: "+ str(self.get_balance())

        Final = str(line1 + "\n" + tmp + final_line)
        return Final

    def deposit(self, amount, description=""):
        self.ledger.append({'amount': amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        balance = sum(item['amount'] for item in self.ledger)
        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            category.deposit(amount, "Transfer from " + str(self.name))
            self.withdraw(amount, "Transfer to " + str(category.name))
            return True
        else:
            return False

    def check_funds(self, amount):
        if self.get_balance() < amount:
            return False
        else:
            return True

def create_spend_chart(categories):
    withdraws = []
    maxi = 0
    names = []
    for cat in categories:
        tmp = 0
        maxi = max(maxi, len(cat.name))
        for item in cat.ledger: #Go only get the withdraws
            if item['amount'] < 0:
                tmp = tmp + item['amount']
        withdraws.append(tmp)

        #To get string of vertical names

        splited = split(cat.name)
        names.append(splited)


    total = sum(withdraws)
    percentage = []
    for item in withdraws:
        percentage.append(round(item / total, 2)*100)

    L1 = "Percentage spent by category"
    L12 = "    " + "-"*(3*len(categories)+1)
    image = L1

    #Getting the percentage image
    for i in range(100, -10, -10):
        line = str(i)+"| "
        line = line.rjust(5)
        for j in range(0,len(categories), 1):
            if percentage[j] >= i:
                line = line + "o  "
            else:
                line = line + "   "
        image = image + "\n" + line

    image = image +'\n'+ L12 +'\n'

    #Getting the vertical names image
    line=[""]*(maxi)
    for nam in names:
        for j in range(0, maxi):
            if j < len(nam):
                line[j] = line[j] + nam[j]
            else:
                line[j] = line[j] + " "

    Names_str = ""
    start_line = " "*5
    j=0
    for i in line:
        j = j+1
        letters = split(i)
        tmp = start_line
        for l in letters:
            tmp = tmp + l + "  "
        if j < maxi:
            Names_str = Names_str + tmp + "\n"
        else:
            Names_str = Names_str + tmp

    #Adding both images
    image = image + Names_str
    return image

food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)
print(create_spend_chart([business, food, entertainment]))


