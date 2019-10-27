#!/usr/bin/env python
# coding: utf-8

# In[31]:


import os
import pandas as pd


# In[32]:


file = "/Users/cla/Desktop/purchase_data.csv"
purchase_data = pd.read_csv(file)


# In[33]:


#Analysis #1: Player Count
players_count = purchase_data['SN'].nunique()
print("There are " + str(players_count) + " total unique players")


# In[34]:


#Display the data to begin analysis:
purchase_data.head()


# In[35]:


purchase_data.count()


# In[63]:


#Analysis #2: Purchasing Analysis (Total)

#Unique items count
items_count = purchase_data['Item ID'].nunique()
print(items_count)

#Total orders count, average purchase price, total revenue 
total_orders = purchase_data['Purchase ID'].nunique()
print(total_orders)
total_rev = purchase_data["Price"].sum()
print(total_rev)
average_price = total_rev / total_orders
average_price = average_price.round(2)
print(average_price)

purchasing_analysis = pd.DataFrame(
    {"Number of unique items":[items_count] ,
     "Average price": [average_price],
     "Number of purchases": [total_orders],
     "Total Revenue": [total_rev]})

purchasing_analysis['Average price'] = purchasing_analysis['Average price'].map('${:,.2f}'.format)
purchasing_analysis['Total Revenue'] = purchasing_analysis['Total Revenue'].map('${:,.2f}'.format)




# In[64]:


purchasing_analysis


# In[ ]:


# Observations: as we can see in the chart above, the data reflects 183 unique items for a total of 780 transactions. 
#At an average price of $3.05 the total resulting revenue is of $2,379.77


# In[41]:


#Gender demographics totals
demographics_totals = purchase_data.groupby('Gender').SN.nunique()

#Gender demographics percentages
demographics_percentage = ((purchase_data.groupby('Gender').SN.nunique() / players_count * 100).round(2))


# In[68]:


print("Gender Demographics")
gt = pd.DataFrame({'Gender':demographics_totals.index, 'Total Count':demographics_totals.values, 'Percentage of players':demographics_percentage.values})
gt['Percentage of players'] = gt['Percentage of players'].map('{:.2f}%'.format)
gt


# In[ ]:


#In the chart above we can clearly see how large the tendency of male players over female players, when making in-game purchases. 


# In[69]:


#Purchasing Analysis (Gender)

#Purchase count by gender
genderpurch_count = (purchase_data.groupby('Gender').Price.count())


#Total purchase value by gender
totalpurch_value = purchase_data.groupby('Gender').Price.sum()

  
#Average price by gender
genderavg_price = (totalpurch_value / genderpurch_count.round(2)).round(2)


#Average total purchase per person by gender
avgtotalpurch_value =  (totalpurch_value / demographics_totals).round(2)


# In[81]:


print("Purchasing Analysis (Gender)")
pa = pd.DataFrame({'Gender':genderpurch_count.index, 'Purchase Count':genderpurch_count.values, 'Average Purchase Price':genderavg_price.values, 'Total Purchase Value':totalpurch_value.values, 'Avg Total Purchase per person':avgtotalpurch_value})

pa['Average Purchase Price'] = pa['Average Purchase Price'].map('${:,.2f}'.format)
pa['Total Purchase Value'] = pa['Total Purchase Value'].map('${:,.2f}'.format)
pa['Avg Total Purchase per person'] = pa['Avg Total Purchase per person'].map('${:,.2f}'.format)


pa


# In[ ]:


#When talking about money spent per purchase, Female pleyers tend to spend a little more than Male players.


# In[79]:


# Age Demographics
bins = [0, 9, 14, 19, 24, 29, 34,39,100]
age_group = ["<10", "10 - 14", "15 - 19", "20 - 24", "25 - 29", "30 - 34", "35 - 39", "40 +"]

dropped2 = purchase_data.drop_duplicates(subset='SN')
dropped2.head()

dropped2['Age Group'] = pd.cut(dropped2["Age"], bins, labels=age_group)
dropped2.head()

dropped2 = dropped2.groupby("Age Group")
bintotalcount = (dropped2["Age Group"].count())

binpercentage = (bintotalcount / players_count * 100).round(2)
binpercentage

ad = pd.DataFrame({'Age Group':bintotalcount.index, 'Total Count':bintotalcount.values, 'Percentage of Total Players':binpercentage.values})

ad['Percentage of Total Players'] = ad['Percentage of Total Players'].map('{:.2f}%'.format)

ad





# In[ ]:


# Over 75% of total players in the data set are between 15 and 29 year of age. 
# There are more players above 29 yo than below 15 yo.


# In[82]:


bins = [0, 9, 14, 19, 24, 29, 34,39,100]
age_group = ["<10", "10 - 14", "15 - 19", "20 - 24", "25 - 29", "30 - 34", "35 - 39", "40 +"]

purchase_data['Age Group'] = pd.cut(purchase_data["Age"], bins, labels=age_group)
purchase_data.head()


#Total Purchase count 2
pd2 = purchase_data.groupby('Age Group')
pd2count = (pd2["Purchase ID"].count())


#Total purchase value
pd2rev = (pd2["Price"].sum())


#Avg purchase price
pd2avgprice = (pd2rev / pd2count).round(2)


#Avg Total Purchase per Person
avgtotalpurch = (pd2rev / bintotalcount).round(2)


ad2 = pd.DataFrame({'Age Group':pd2count.index, 'Total Purchase Count':pd2count.values, 'Total Purchase Value':pd2rev.values, 'Avg Purchase Price':pd2avgprice.values,'Avg Total Purchase per Person':avgtotalpurch.values})


ad2['Avg Purchase Price'] = ad2['Avg Purchase Price'].map('${:,.2f}'.format)
ad2['Total Purchase Value'] = ad2['Total Purchase Value'].map('${:,.2f}'.format)
ad2['Avg Total Purchase per Person'] = ad2['Avg Total Purchase per Person'].map('${:,.2f}'.format)


ad2





# In[ ]:


# The age group that spent the most is the 20-24 yo range, with over 30% of total spenditures. Followed by the 15-19 yo group.


# In[76]:


# Top spenders
total_value = (purchase_data.groupby('SN').Price.agg(['count','mean','sum'])).round(2)
top_value = total_value.sort_values("sum", ascending=False)
top_valuerenamed = top_value.rename(columns={'count': 'Purchase Count', 'mean': 'Average Purchase Price','sum':'Total Purchase Value'})



top_valuerenamed['Average Purchase Price'] = top_valuerenamed['Average Purchase Price'].map('${:,.2f}'.format)
top_valuerenamed['Total Purchase Value'] = top_valuerenamed['Total Purchase Value'].map('${:,.2f}'.format)



top_valuerenamed.head(5)


# In[77]:


total_items = purchase_data.groupby(['Item ID', 'Item Name','Price']).Price.agg(['count','sum'])
top_items = total_items.sort_values("count", ascending=False)
top_itemsrenamed = top_items.rename(columns={'count': 'Purchase Count', 'sum': 'Total Purchase Value'})

top_itemsrenamed['Total Purchase Value'] = top_itemsrenamed['Total Purchase Value'].map('${:,.2f}'.format)

top_itemsrenamed.head(5)


# In[78]:


top_items2 = total_items.sort_values("sum", ascending=False)
top_itemsrenamed2 = top_items2.rename(columns={'count': 'Purchase Count', 'sum': 'Total Purchase Value'})

top_itemsrenamed2['Total Purchase Value'] = top_itemsrenamed2['Total Purchase Value'].map('${:,.2f}'.format)

top_itemsrenamed2.head(5)


# In[ ]:


#Observable trends:
# Female players tend to spend more per item on the game
# Male players are equivalent to the largest portion of the revenue, they tend to make more unitary purchases and are a mayority in the game demographic.
# Age group 20-24 is the one spending the most in the game and is responsible for over 30% of in-game purchases revenue, they are also the largest players count.
# Aside from 20-24 age group the above 24 range is next to the total spenditure in game, the correlation of this data needs to be further analyzed in order to determine the reason behind this.


# In[ ]:





# In[ ]:




