base_dir = '/Users/dhwanishah/Desktop/MS/VR-Dhwani/subject-csvs'

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sessions = ['session-1.csv', 'session-2.csv', 'session-3.csv', 'session-4.csv', 'session-5a.csv', 'session-5b.csv']
session_names = ['session1', 'session2', 'session3', 'session4', 'session5a', 'session5b']
session_means = {}
folder_names = ['sub-1', 'sub-2', 'sub-3', 'sub-4', 'sub-5', 'sub-6', 'sub-7', 'sub-8', 'sub-9', 'sub-10', 'sub-11']

for session_file, session_name in zip(sessions, session_names):
    session_means[session_name] = []

    # Loop through subjects
    for sub_dir in folder_names:
        sub_path = os.path.join(base_dir, sub_dir)
        if os.path.isdir(sub_path):
            session_path = os.path.join(sub_path, session_file)
            if os.path.exists(session_path):
                df_session = pd.read_csv(session_path)
                mean_SCR_Amp = df_session['SCR_Amplitude'].mean()
                session_means[session_name].append([sub_dir, mean_SCR_Amp])
    # session_means[session_name] = pd.DataFrame(session_means[session_name], columns=['subject', 'mean_SCR_Amp'])

sessions_mean_new = {}
# Loop through each session and each subject in that session
for session, value_for_all_subjects in session_means.items():
    for subject, mean in value_for_all_subjects:
        if subject not in sessions_mean_new:
            sessions_mean_new[subject] = []
        sessions_mean_new[subject].append([session, mean])

# Print dictionary
# print(sessions_mean_new)

df_data = {}
for subject, session_data in sessions_mean_new.items():
    df_data[subject] = {session: value for session, value in session_data}
# Convert to DataFrame and transpose to have subjects as rows and sessions as columns
df = pd.DataFrame(df_data).transpose()
# Print dataframe as table
print(df)


# Reset index to have 'Subject' as a column for plotting purposes
df.reset_index(inplace=True)
df.rename(columns={'index': 'Subject'}, inplace=True)

# Melt the DataFrame for seaborn compatibility
df_melted = df.melt(id_vars=['Subject'], var_name='Session', value_name='Value')

# Plotting with seaborn
plt.figure(figsize=(20, 8))
sns.lineplot(data=df_melted, x='Session', y='Value', hue='Subject', marker='o')

# Custom labels for the x-axis
labels = [
    'Session 1 \n Apartment A', 
    'Session 2\n Apartment B', 
    'Session 3\n Apartment C', 
    'Session 4\n Apartment C', 
    'Session 5\n Apartment A \n (Distant Condition)',
    'Session 5\n Apartment B \n (Near Condition)'
]
plt.xticks(ticks=range(len(labels)), labels=labels, rotation=45)

# Labels and title
plt.xlabel('Session')
plt.ylabel('Value')
plt.title('Subject Values Across Sessions')
plt.tight_layout()
plt.show()

