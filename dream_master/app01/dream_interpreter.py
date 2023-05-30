# dream_interpreter.py


# 解梦(周公解梦)
# NLP技术；文本相似度、文本匹配

import pandas as pd
from jsonschema.exceptions import best_match
from paddlenlp import Taskflow
import paddle

# Set the device to the first GPU
paddle.set_device('cpu')

# Load data
import json

data = []

with open('data.csv', 'r', encoding='GBK') as f:
    for line in f:
        clean_line = line.strip().rstrip(',').strip()
        data.append(json.loads(clean_line))

df = pd.DataFrame(data)
df = df.sample(frac=0.002)


# Create a word segmentation object
seg_accurate = Taskflow("word_segmentation", mode="accurate", batch_size=1)

# Create a text similarity object
similarity = Taskflow("text_similarity", model='rocketqa-base-cross-encoder', batch_size=1)

# Preprocess dreams in the dataframe
df['dream_words'] = df['dream'].apply(lambda x: ' '.join(seg_accurate(x)))

def interpret_dream(dream):
    # Word segmentation for the dream
    dream_words_str = ' '.join(seg_accurate(dream))

    # Use a generator function to calculate similarity scores
    def generate_sim_scores():
        for row_words_str in df['dream_words']:
            yield similarity([[dream_words_str, row_words_str]])

    sim_scores_gen = generate_sim_scores()

    # Get the best match
    best_match_index, best_match_score = None, -1
    for index, sim_score in enumerate(sim_scores_gen):
        if sim_score[0]['similarity'] > best_match_score:
            best_match_index = index
            best_match_score = sim_score[0]['similarity']

    best_match = df.iloc[best_match_index]['decode']

    return best_match
