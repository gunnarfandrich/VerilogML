#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn import linear_model
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('bmh')


# In[ ]:


# df - dataframe
# each row represents a design from open-cores
# first n columns represents n features, and last column represents power estimate from Design Compiler (label)
df = # obtain dataframe output from rtl feature/label collection code
df


# In[ ]:


# print a correlation matrix of the features we obtained
df.corr()


# In[ ]:


# plot a scatter matrix for each pair of variables
pd.plotting.scatter_matrix(df, alpha=0.2, figsize=[20,15]);


# In[ ]:


# view correlation with regard to label
# greater magnitude (+/-) means greater correlation
df.corr()['Dynamic Power']


# TO-DO: separate data into training and testing sets

# In[ ]:


# build multiple linear regression model from features
features = ['if', 'else', 'case', '...']
target = 'Dynamic Power'

X = df[features].values.reshape(-1, len(features))
y = df[target].values

ols = linear_model.LinearRegression()
model = ols.fit(X, y)


# In[ ]:


model.coef_


# In[ ]:


model.intercept_


# In[ ]:


# evaluate R2
model.score(X, y)


# In[ ]:


# load prediction (from testing set)
# model.predict(x_pred)

