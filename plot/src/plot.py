import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

plt.rcParams['figure.figsize'] = (12, 8)
df = pd.read_csv('./logs/metric_log.csv')


while True:      
    time.sleep(3)
    new_df = pd.read_csv('./logs/metric_log.csv')
    
    if not new_df.equals(df):
        plt.clf()  # Clear the current plot
        sns.histplot(new_df['absolute_error'], kde=True)
        plt.title('Absolute Error Distribution')
        plt.savefig('./logs/error_distribution.png', dpi=300, bbox_inches='tight')