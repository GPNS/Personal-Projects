""" This code was written to answer Free Code Camps 5th project in
Scientific Calculation with Python: Probability Calculator 01/04/2022"""
import copy
import random

class Hat:
    def __init__(self, **Balls):
        #balls is a string for form (Red=3,yellow=4,blue=1)
        self.contents = []
        self.num = []
        self.hat = dict()
        self.drawn_2 = {}
        tmp = [] #Contains the string in distinct cells for further spliting
        Balls = str(Balls)
        for ele in Balls.split(","):
            tmp.append(ele)
        self.names = [""]*len(tmp) #Keep the names
        i=0 #Counter
        for K in tmp:
            for char in K:
                if char.isdigit(): #Extracting number
                    self.num.append(char)
                if char.isalpha(): #Extracting characteristics
                    self.names[i] = self.names[i]+char
            i=i+1

        for j in range(0, len(self.names)): #Create contents
            k=0 #counter
            while k< int(self.num[j]):
                self.contents.append(self.names[j])
                k=k+1

        for m in range(0, len(self.names)):
            self.hat[self.names[m]] = self.num[m]

    #def __str__(self):

    def draw(self, number):
        """Draw a selected number of balls out the hat with putting them back in"""
        drawn_all = []
        if number > len(self.contents):
            return self.contents

        for i in range(0, number, 1):
            rand_num = random.randrange(len(self.contents)) #random number
            drawn = self.contents[rand_num] #selects name of drawn ball
            drawn_all.append(drawn) #Records all drawn balls
            self.contents.remove(drawn) #removes drawn balls

        return drawn_all


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    """hat: A hat object containing balls that should be copied inside the function.
    expected_balls: An object indicating the exact group of balls to attempt to draw from the hat for the experiment. For example, to determine the probability of drawing 2 blue balls and 1 red ball from the hat, set expected_balls to {"blue":2, "red":1}.
    num_balls_drawn: The number of balls to draw out of the hat in each experiment.
    num_experiments: The number of experiments to perform. (The more experiments performed, the more accurate the approximate probability will be.)"""
    M =0

    for j in range(0, num_experiments):
        needed = copy.deepcopy(expected_balls)
        copy_hat = copy.deepcopy(hat)
        drawn = copy_hat.draw(num_balls_drawn)

        for ball in drawn:
            if ball in needed.keys() and needed[ball] != 0:
                needed[ball] = needed[ball]-1

        if all(value == 0 for value in needed.values()):
            M=M+1
    proba = M/num_experiments

    return proba

hat = Hat(blue=4, red=3, green=6)

#print(hat.contents)
#print(hat.draw(5))
print(experiment(hat=hat,
    expected_balls={"blue": 2,
                    "red": 1},
    num_balls_drawn=4,
    num_experiments=15))