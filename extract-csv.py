import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import json

parser = ArgumentParser(prog='python extract-csv.py')
parser.add_argument('infile', help='input csv file for extraction', type=str)
args = parser.parse_args()

df = pd.read_csv(args.infile)
df.columns = ['Disease Type',
              'Date',
              'City',
              'Township',
              'Gender',
              'Foreign',
              'Age',
              'Number of Cases']
maskDate = (df['Date'] >= '2022-01-01') & (df['Date'] <= '2023-12-31')
maskPlace = (df['City'] == '台北市') & (df['Township'] == '大安區')
df2 = df.loc[maskPlace]
df3 = df2.groupby('Date')[['Number of Cases']].sum()
df4 = df3.loc['2022-01-01':]
print(df4)
df4.plot(title="Cases of COVID-19 from 2022-01-01 to 2023-12-31")
plt.show()
df4.to_csv('output.csv')
