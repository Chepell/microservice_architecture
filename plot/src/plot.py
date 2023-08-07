import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time

plt.rcParams['figure.figsize'] = (12, 8)

# Get the directory where the Python script is located
script_dir = os.path.dirname(os.path.realpath(__file__))
# Define the path to the CSV file
# csv_file_path = os.path.join(script_dir, '../../logs/metric_log.csv')
# df = pd.read_csv(csv_file_path)

df = pd.read_csv('./logs/metric_log.csv')


while True:
    time.sleep(3)
    # new_df = pd.read_csv(csv_file_path)
    new_df = pd.read_csv('./logs/metric_log.csv')
    
    if not new_df.equals(df):
        plt.clf()  # Clear the current plot
        sns.histplot(new_df['absolute_error'], kde=True)
        plt.title('Absolute Error Distribution')
        # plt.savefig('error_distribution.png', dpi=300, bbox_inches='tight')
        plt.savefig('./logs/error_distribution.png', dpi=300, bbox_inches='tight')