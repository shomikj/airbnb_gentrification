# File: lda.py -- Script to Run LDA
# Author: Shomik Jain
# Date: 2/02/2020

import pandas as pd
import numpy as np
import gensim
from scipy import stats


# Script Parameters
num_topics = 4
lda_cols = ['lda1', 'lda2', 'lda3', 'lda4']
output = 'lda4.csv'
output2 = 'lda4_zip.csv'
model_file = 'model4'

file = 'nyc_reviews.tsv'
data = pd.read_csv(file, delimiter='\t', quotechar='"', escapechar='\\')

file = 'nyc_zipcode_all.tsv'
zipcode = pd.read_csv(file, delimiter='\t', quotechar='"', escapechar='\\')

print('loaded data')

# Organize Reviews for LDA
data = data.dropna(subset=['reviews_clean'])
data = data.reset_index(drop=True)

reviews = data['reviews_clean']
bow = []
for r in reviews:
    bow.append(r.split())

dictionary = gensim.corpora.Dictionary(bow)

# remove words appearing in less than 100 reviews
dictionary.filter_extremes(no_below=1000)

bow_corpus = [dictionary.doc2bow(doc) for doc in bow]


# Run LDA
print('starting LDA')

lda_model =  gensim.models.LdaMulticore(bow_corpus, num_topics = num_topics, id2word = dictionary, passes = 5, workers=2)
lda_model.save(model_file)

print('lda done')
print()

for idx, topic in lda_model.print_topics(num_topics=-1, num_words=20):
    print("Topic: {} \nWords: {}".format(idx, topic ))
    print("\n")

print()

print('getting scores per review')
all_scores = []
checkpoint = int(len(data)/10)
for i, review in enumerate(bow_corpus):
    if i%checkpoint==0:
        print(i)
    scores = list(np.zeros(num_topics))
    for i in lda_model[review]:
        scores[i[0]] = i[1]
    all_scores.append(scores)
print()

for i in lda_cols:
    data[i] = np.nan

data.loc[:, lda_cols] = all_scores

all_cols = ['zipcode', 'year'] + lda_cols
data = data[all_cols]

data.to_csv(output, index=False)


# Organize Scores by Zipcode
print('starting organization by zipcode')

answer = pd.DataFrame(columns=all_cols)

unique_years = zipcode['year'].unique()
unique_zipcodes = zipcode['zipcode'].unique()

for z in unique_zipcodes:
    for y in unique_years:
        curr = data.loc[(data['zipcode']==z) & (data['year']==y)]
        
        new = {}
        new['year'] = y
        new['zipcode'] = z

        for c in lda_cols:
        	new[c] = np.nanmean(curr[c])
                
        answer = answer.append(new, ignore_index=True)

answer.to_csv(output2, index=False)

print('done organizing by zipcode')

# Merge Scores by Zipcode

answer['zipcode'] = pd.to_numeric(answer['zipcode'], downcast='integer')
zipcode['zipcode'] = pd.to_numeric(zipcode['zipcode'], downcast='integer')

answer['year'] = pd.to_numeric(answer['year'], downcast='integer')
zipcode['year'] = pd.to_numeric(zipcode['year'], downcast='integer')

zipcode = pd.merge(zipcode, answer, how='left', on=['zipcode', 'year'])

pred = ['crime_score', 'edu_bachelors', 'age_25_34', 'gini_index', 'race_index']
for p in pred:
	temp = zipcode.dropna(subset=[p])
	temp = temp.reset_index(drop=True)
	print()
	print(p)
	for i in lda_cols:
		scores = temp[i]
		curr = temp[p]
		r, pr = stats.pearsonr(scores, curr)
		s, ps = stats.spearmanr(scores, curr)
		print(r, s)