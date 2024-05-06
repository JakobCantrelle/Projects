import csv
import numpy as np
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# nltk.download('vader_lexicon')

Sia = SentimentIntensityAnalyzer()

FileName = 'Payday.csv'  # Update this to your CSV file name

MessageScores = []

with open(FileName, newline='', encoding='utf-8') as File:
    Reader = csv.reader(File)
    for Row in Reader:
        if not Row or 'http' in Row[0] or Row[0] == '""' or "Started a call that lasted" in Row[0] or len(Row[0]) > 600:
            continue  # Skip messages based on the specified criteria and length
        Score = Sia.polarity_scores(Row[0])['compound']
        if Score != 0.0:
            MessageScores.append((Row[0], Score))

MessageScores.sort(key=lambda x: x[1])

Scores = [score for message, score in MessageScores]

TopNegative = MessageScores[:100]
TopPositive = MessageScores[-100:]

print("Top 10 Positive Messages:")
for message, score in reversed(TopPositive):
    # Indent the message display
    print(f"Score: {score}, Message:\n\t{message}")  # Add a tab before the message
    print()
    print()

print("\nTop 10 Negative Messages:")
for message, score in TopNegative:
    # Indent the message display
    print(f"Score: {score}, Message:\n\t{message}")  # Add a tab before the message
    print()
    print()

Bins = np.arange(-1.01, 1.01, 0.01)
Hist, BinEdges = np.histogram(Scores, bins=Bins)

plt.figure(figsize=(12, 6))
plt.bar(BinEdges[:-1], Hist, width=0.01, color='skyblue', edgecolor='black')
plt.xlabel('Sentiment Score')
plt.ylabel('Number of Messages')
plt.title('Distribution of Sentiment Scores')
plt.xlim(min(BinEdges), max(BinEdges))
plt.grid(axis='y', linestyle='--')
plt.show()
