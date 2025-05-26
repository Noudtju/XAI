import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from scipy import stats

df = pd.read_csv('total_file.csv', sep = ',')

df.head()

# Data exploration
print("Data Overview:")
print(f"Total records: {len(df)}")
print(f"Unique users: {df['user_name'].nunique()}")
print(f"Unique bird classes: {df['class_name'].nunique()}")
print(f"Treatment types: {df['teaching_phase'].unique()}")

# Compute accuracy metrics
df['correct_testing'] = (df['class_name'] == df['testing_phase_user_answer'])

# Analyze by treatment
treatment_accuracy = df.groupby('teaching_phase')['correct_testing'].mean()
print("\nAccuracy by Treatment:")
print(treatment_accuracy)

# Analyze by user
user_accuracy = df.groupby(['user_name', 'teaching_phase'])['correct_testing'].mean().reset_index()
print("\nAccuracy by User and Treatment:")
print(user_accuracy)

# Analyze by bird class
class_accuracy = df.groupby(['class_name', 'teaching_phase'])['correct_testing'].mean().reset_index()
print("\nAccuracy by Bird Class and Treatment:")
print(class_accuracy)

# Analyze teaching phase vs testing phase
df['knew_in_teaching'] = ~(df['user_selection'].isin(['I don\'t know']))
df['correct_in_teaching'] = (df['user_selection'] == df['class_name'])

contingency = pd.crosstab(
    [df['teaching_phase'], df['correct_in_teaching']],
    df['correct_testing'],
    normalize='index')

print("\nContingency Table (Teaching Phase Correctness vs Testing Phase Correctness):")
print(contingency)

# Visualize results
plt.figure(figsize=(12, 10))

# Plot 1: Treatment comparison
plt.subplot(2, 2, 1)
sns.barplot(x=treatment_accuracy.index, y=treatment_accuracy.values)
plt.title('Accuracy by Treatment')
plt.ylabel('Accuracy')
plt.xlabel('Treatment')

# Plot 4: Confusion matrix
plt.subplot(2, 2, 4)
conf_matrix = pd.crosstab(df['class_name'], df['testing_phase_user_answer'])
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.ylabel('Actual Class')
plt.xlabel('Predicted Class')

# Additional analysis: Learning effect
print("\nLearning Effect Analysis:")
# Did users who didn't know a class in teaching phase learn it correctly in testing?
learning = df[df['user_selection'] == "I don't know"].groupby('teaching_phase')['correct_testing'].mean()
print(f"Accuracy for initially unknown birds by treatment:\n{learning}")

# Separate data by treatment
t1_data = df[df['teaching_phase'] == 'treatment1']['correct_testing']
t2_data = df[df['teaching_phase'] == 'treatment2']['correct_testing']

# Run t-test (N way to small..)
t_stat, p_val = stats.ttest_ind(t1_data, t2_data, equal_var=False)
print(f"\nStatistical comparison between treatments:")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_val:.4f}")
print(f"Significant difference: {p_val < 0.05}")

# Analyze responses where users provided an answer (not "I don't know")
confident_responses = df[df['testing_phase_user_answer'] != "I don't know"]
confident_accuracy = confident_responses.groupby('teaching_phase')['correct_testing'].mean()
print("\nAccuracy for confident answers (excluding 'I don't know'):")
print(confident_accuracy)