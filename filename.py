#!/usr/bin/env python
# coding: utf-8

# In[63]:


import pandas as pd
import random
# Creating a probability table
# Creating a list of the characters we need - all letters and an end symbol
signs = [chr(i) for i in range(ord('a'), ord('z')+1)]
signs.append('$')

# Creating a table where rows are the first letters of bigrams, and columns are the second letters of bigrams.
bigrams = pd.DataFrame(0, index=signs[:26], columns=signs)
# Reading a file with names
raw_names = open('names.txt').read().splitlines()
# Adding an end symbol to each name to read bigrams
names = [s + '$' for s in raw_names]
# Splitting all names into bigrams and adding the count of bigrams to the table.
for i in names:
    for j in range(0, len(i)-1):
        bigrams[i[j+1]][i[j]] += 1  

# Counting the total number of bigrams in each row
bigrams['total'] = bigrams.sum(axis='columns')
# Dividing the absolute frequency of bigrams by their row total to calculate the relative frequency of the second letter for the first letter.
bigrams.iloc[:, :] = bigrams.iloc[:, :].div(bigrams['total'], axis=0).round(4)

# Name generator, where the input data is a letter entered by the user
def name_generator(letter):
    # Initially, the name consists of only the first letter
    name = letter
    # Removing the 'total' column to extract the probability list
    bigrams_without_total = bigrams.drop(columns=['total'])
    # Using a loop to build the name until we reach the end symbol.
    while letter != '$':
        # For the current last letter, extract the probability list of bigrams where this letter is the first letter
        prob_list = bigrams_without_total.loc[letter]
        # Randomly choose the next letter based on bigram probabilities.
        choice = prob_list.sample(n=1, weights=prob_list, axis=0)
        # Use the chosen letter as the current last letter
        letter = choice.index.values[0]
        # Add the new letter to the name
        name = name + letter
    # Return the final name without the end symbol ($)
    return name.replace('$', '')

# Ask the user to enter a letter
val = input("Enter the first letter of the name. It should be lowercase and in Latin: ")
# Check if the letter meets the conditions
while val not in signs[:-2]:
    val = input("Enter again, it should be a lowercase Latin letter: ")

print("GENERATED NAME IS ", name_generator(val), ". Sounds magical!")
print("\nHere is the probability table of bigrams.\nRows are the first letters, columns are the second letters.\nFor example, the probability of 'ba' bigram is 0.1214 (row 'b', column 'a')")
print(bigrams[signs[0:13]])
print(bigrams[signs[13:]])

# BONUS: Visualization of the bigrams probability table.
# Install the necessary libraries
import seaborn as sns
import matplotlib.pyplot as plt
# Increase the size of the plot
sns.set(rc={'figure.figsize':(11.7,8.27)})
# Use a heatmap to show where probabilities are higher or lower, with color differences
fig = sns.heatmap(bigrams[signs[:27]], xticklabels=signs[:27], yticklabels=signs[:26], cmap="crest")
# Set the title and labels
fig.set(title='Bigrams Probability Heatmap.', xlabel='Second letter of the bigram.', ylabel='First letter of the bigram.')
plt.show()

# In[ ]:





# In[ ]:




