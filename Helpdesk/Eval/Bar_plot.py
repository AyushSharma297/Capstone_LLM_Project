import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have loaded the DataFrame from 'output_with_bleu_scores.xlsx'
df = pd.read_excel('output_with_bleu_scores.xlsx')

# Extract question numbers and BLEU scores from the DataFrame
question_numbers = df['question No.']
bleu_scores = df['bleu_score']

# Calculate the mean BLEU score
mean_bleu_score = bleu_scores.mean()

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the bar graph
ax.bar(question_numbers, bleu_scores, color='skyblue', label='BLEU Scores')

# Plot a curve that follows the top of the bars (line connecting bar tops)
ax.plot(question_numbers, bleu_scores, marker='o', linestyle='-', color='red', label='Curve')

# Plot a horizontal line at the mean BLEU score
ax.axhline(mean_bleu_score, color='green', linestyle='--', linewidth=2, label=f'Mean BLEU Score ({mean_bleu_score:.2f})')

# Add labels and title
ax.set_xlabel('Question Number')
ax.set_ylabel('BLEU Score')
ax.set_title('BLEU Scores for Each Question')

# Add legend
ax.legend()

# Show plot
plt.show()

