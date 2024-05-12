import pandas as pd
from nltk.translate.bleu_score import sentence_bleu
import nltk
nltk.download('punkt')

df = pd.read_excel('Evaluation_LLM.xlsx')   #read the excel sheet
discard_row = []
bleu_scores = []
for index, row in df.iterrows():
    expected_answer = str(row['expected_answer'])
    generated_answer = str(row['generated_answer'])
    # Tokenize the sentences into lists of words
    expected_tokens = nltk.word_tokenize(expected_answer.lower())
    generated_tokens = nltk.word_tokenize(generated_answer.lower())
    # Calculate BLEU score
    bleu = sentence_bleu([expected_tokens], generated_tokens)
    if bleu > 1 :
        discard_row.append(row)
    blues = str(bleu)
    first_six_chars = blues[:6]
    bleu_scores.append(float(first_six_chars))

df['bleu_score'] = bleu_scores

# selecting rows based on condition
rslt_df = df.loc[df['bleu_score'] < 1]

rslt_df.reset_index(drop=False, inplace=True)#reset index
rslt_df.to_excel('output_with_bleu_scores.xlsx', index=True, index_label = 'question No.')

