import numpy as np

# Load the Q-table (you can adjust the filename if needed)
Q_table = np.load("q_table.npy")

# Initialize a count for Q-values higher than 0.0
count_positive_q_values = 0

# Iterate through the Q-table and count positive Q-values
for state in range(Q_table.shape[0]):
    for action in range(Q_table.shape[1]):
        q_value = Q_table[state, action]
        if q_value > 0.0:
            count_positive_q_values += 1
        print(f"State {state}, Action {action}: Q-value = {q_value}")

# Print the count of positive Q-values
print(f"Number of Q-values higher than 0.0: {count_positive_q_values}")

