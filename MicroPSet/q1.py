import random

def average_streak_count(n, streak, num_trials):
    """
    n: number of coin flips in one trial
    streak: a string of length > 0, representing the sequence of 
            heads or tails in one trial. Heads represented as "H" and tails as "T"
    num_trials: number of trials in the simulation
    Runs a Monte Carlo simulation with a number of trials 'num_trials'. For each 
    trial, it tracks the number of times 'streak' occurs when a fair coin is 
    flipped 'n' times. After 'num_trials' number of trials, it returns a tuple of: 
    (1) the average number of times the streak occurs
    (2) the width of the 95% confidence interval rounded to 3 decimal places 
        (from the mean to one side, only)
    """
    # You are given this function - do not modify
    def get_mean_std(X):
        mean = sum(X)/len(X)
        tot = 0.0
        for x in X:
            tot += (x - mean)**2
        std = (tot/len(X))**0.5
        return (mean, std)

    # YOUR CODE HERE
    counts = []
    for trial in range(num_trials):
        flips = ""
        for coin in range(n):
            flips += random.choice(["H", "T"])
        
        count = 0
        end = len(streak)
        while end <= n:
            if streak == flips[end-len(streak):end]:
                count += 1
            end += 1
        
        counts += [count]
    
    return (sum(counts)/num_trials, round(1.96*get_mean_std(counts)[1]/num_trials**.5, 4))
        

#for x in range(10):
#    print(average_streak_count(6, "HTH", 10000))
#print(average_streak_count(0, "H", 1000))