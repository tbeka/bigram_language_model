#!/usr/bin/env python
# coding: utf-8

# In[63]:


import pandas as pd
import random
#Создание таблицы вероятностей
#Создаем список нужных нам знаком - все буквы и знак конца
signs = [chr(i) for i in range(ord('a'), ord('z')+1)]
signs.append('$')

#Создаем таблицу, где ряды это первая буква биграммы, а стоблцы это вторая буква биграммы.
bigramms = pd.DataFrame(0, index = signs[:26], columns = signs)
#Читаем файл с именами
names_raw = open('names.txt').read().splitlines()
#Добавляем знак конца к каждому имени чтобы читать биграммы
names = [s + '$' for s in names_raw]
#Разбиваем все имена на биграммы и добавляем количество биграмм в таблицу.
for i in names:
    for j in range(0, len(i)-1):
        bigramms[i[j+1]][i[j]] += 1  
        
#Считаем общее количество биграмм в каждом ряду
bigramms['total'] = bigramms.sum(axis='columns')
#Делим абсолютную частоту биграмм на total их ряда, чтобы понять относительную частоту второй буквы для первой буквы.
bigramms.iloc[:, :] = bigramms.iloc[:, :].div(bigramms['total'], axis=0).round(4)

#Генетор имени, входные данные это буква введенная пользователем
def name_generator(letter):
    #Изначально имя состоит только из первой буквы
    name = letter
    #Уберем колонну total чтобы можно было выделить список вероятностей
    bigramms_without_total = bigramms.drop(columns = ['total'])
    #Используем цикл чтобы собирать имя пока не дойдем до конечного знака.
    while letter != '$':
        #Для текущей последней буквы, выделяем список вероятностей биграмм, где эта буква является первой
        prob_list = bigramms_without_total.loc[letter]
        #Рандомно выбираем следуюущую букву, зная вероятности биграмм.
        choice = prob_list.sample(n=1, weights = prob_list, axis=0)
        #Выбранную букву используем как текушую последнюю
        letter = choice.index.values[0]
        #Добавляем новую букву к имени
        name = name+letter
    #Возвращаем конечное имя без знака конца ($)
    return name.replace('$', '')

#Просим пользователя ввести букву
val = input("Enter the first letter of the name. It should be lower-case and latin: ")
#Проверяем подходит ли буква под условия
while val not in signs[:-2]:
    val = input("Enter again, it should be a latin letter in lower-case: ")

print("GENERATED NAME IS ", name_generator(val), ". Sounds magical!")
print("\nHere is the probability table of bigramms.\nRows are the first letters, columns are the second letters.\nFor example, the probability of 'ba' bigramm is 0.1214 (row 'b', column 'a')")
print(bigramms[signs[0:13]])
print(bigramms[signs[13:]])


#BONUS: Визуализация таблицы вероятности биграмм.
#Устанавливаем нужные библиотеки
import seaborn as sns
import matplotlib.pyplot as plt
#Увеличиваем размер графа
sns.set(rc={'figure.figsize':(11.7,8.27)})
#Используем heatmap, которая будет показывать где вероятности выше, а где ниже, с помощью разницы в цвете
fig = sns.heatmap(bigramms[signs[:27]], xticklabels=signs[:27], yticklabels=signs[:26], cmap="crest")
#Устанавливаем название и лейблы
fig.set(title='Bigramms probability heatmap.', xlabel='Second letter of the bigramm.', ylabel='First letter of the bigramm.')
plt.show()


# In[ ]:





# In[ ]:




