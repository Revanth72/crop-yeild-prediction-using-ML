import pandas as pd

df = pd.read_csv('food.csv')
print( df.nunique())

df1=pd.read_csv('srikdata.csv')
print(df1.nunique())

df2=pd.read_csv('Crop_recommendation.csv')
print(df2.nunique())