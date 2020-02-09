# File: sentiment_analysis.py -- Create Sentiment Features
# Author: Shomik Jain
# Date: 2/02/2020

import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

file = 'seg3.tsv'
data = pd.read_csv(file, delimiter='\t', quotechar='"', escapechar='\\')

# Analyze sentiment for each sentence

analyzer = SentimentIntensityAnalyzer()

data['sentiment_comp'] = np.nan
data['sentiment_pos'] = np.nan
data['sentiment_neu'] = np.nan
data['sentiment_neg'] = np.nan

checkpoint = int(len(data)/10)

for i,r in data.iterrows():
	if ((i%checkpoint) == 0):
		print(i)
	review = r['comments']
	if(isinstance(review, str)):
		vs = analyzer.polarity_scores(review)
		data.loc[i, 'sentiment_comp'] = vs['compound']
		data.loc[i, 'sentiment_pos'] = vs['pos']
		data.loc[i, 'sentiment_neu'] = vs['neu']
		data.loc[i, 'sentiment_neg'] = vs['neg']

out = 'seg3_sent.tsv'
data.to_csv(out, sep='\t', quotechar='"', escapechar='\\', index=False)

