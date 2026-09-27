import random, math, statistics
import matplotlib.pyplot as plt

###ENTIRE THING RELIES ON VALID AND REASONABLE INPUTS###
numberOfCards = int(input("How Many Cards Are In Your Deck: "))
numberOfCategories = int(input("How Many Categories Are There Of What You Need: "))

#set the length to be what it needs to be, default 1 card will be overwritten probably
cardsNeededInCategory = [1] * numberOfCategories
cardsWanted = [1] * numberOfCategories #desired amount of cards

#for each category, fill needed data
for i in range(numberOfCategories):
    cardsNeededInCategory[i] = int(input("\nHow Many Cards Are In Category " + str(i + 1) + "? "))
    cardsWanted[i] = int(input("How Many Cards Wanted For Category " + str(i + 1) + "? "))


#arbitrarily large number of trials to probably get reasonable data I hope
numberOfTrials = 100000
print(f"\nGive Me A Moment To Draw {numberOfTrials} Games Worth Of Cards")

cardCount = [] #store the amount of cards to meet the requirements


#generate the deck once
deck = [-1] * numberOfCards  # initialize all to -1, that's not the card wanted
for i in range(numberOfCategories): #for each category...
    for j in range(cardsNeededInCategory[i]):  #...put its index, i, into the deck however many times needed(j)...
        deck[sum(cardsNeededInCategory[:i]) + j] = i #...in such a way to not overwrite other categories
# for 4 categories with 3 elements, 2 elements, 1 element, 5 elements respectively
# deck will take the form [0,0,0,1,1,2,3,3,3,3,3,-1,-1,-1,-1,...,-1]
# note the category 0 is indicated by 0 in the deck and so on, -1 is undesired card
# order will be random but this helps the point get across

# run loop a bunch
for runNumber in range(numberOfTrials):
    random.shuffle(deck) #shuffle that deck

    # reset any local variables
    acquiredCardCount = [0] * numberOfCategories #track how many cards of each category
    cardsDrawn = 0 #track how deep we are
    categoriesLeft = numberOfCategories

    #go through the deck once
    for card in deck:
        cardsDrawn += 1 #card was drawn
        if card != -1: #it's useful
            acquiredCardCount[card] += 1 #add to total found for that card
            if acquiredCardCount[card] == cardsWanted[card]: #if we reached the total, that category is done
                categoriesLeft -= 1
                if categoriesLeft == 0: #all cards are found, so leave
                    break



    # housekeeping for this trial ending
    cardCount.append(cardsDrawn) #store the number of cards that must be drawn, +1 because if we need a card at index 2 it's the 3rd drawn card


#Bunch of stats to scratch the brain itch
#don't want to recompute this stuff 7 times with large data
mean = statistics.mean(cardCount)
stdev = statistics.stdev(cardCount)
print("\nNeed average of " + str(round(mean, 2)) + " Cards")
print("So probably like " + str(max(math.ceil(mean - 7), 0)) + " Turns On Average")
print("Standard Dev: " + str(round(stdev, 2)) + " Cards")
print("Mode: " + str(statistics.mode(cardCount)) + " Cards")
print("Median: " + str(statistics.median(cardCount)) + " Cards")
print("Probably Between " + str(max(math.floor(mean - 7 - stdev), 0)) + " And " + str(max(math.ceil(mean - 7 + stdev), 0)) + " Turns")
print("Probably Between " + str(math.floor(mean - stdev)) + " And " + str(math.ceil(mean + stdev)) + " Cards")
print("Odds in opening hand: " + str((cardCount.count(1) + cardCount.count(2) + cardCount.count(3) + cardCount.count(
    4) + cardCount.count(5) + cardCount.count(6) + cardCount.count(7)) * 100 / numberOfTrials) + "%")


plt.hist(cardCount, bins=range(min(cardCount), max(cardCount) + 2), edgecolor='black')
plt.title(f"Cards Drawn to Meet Your Demands ({numberOfTrials} Trials)")
plt.xlabel("Cards Drawn")
plt.ylabel("Frequency")
plt.grid(True, linestyle='--', alpha=0.5)
plt.gcf().canvas.manager.set_window_title("Magic Card Draw Simulation")
plt.show()