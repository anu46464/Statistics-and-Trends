import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis

# Load and clean the data
olympics_df = pd.read_csv('olympics_medals_country_wise.csv')
olympics_df.columns = olympics_df.columns.str.strip()  # Strip whitespace
columns_to_convert = ['summer_gold', 'summer_total', 'total_gold', 'total_total']
for column in columns_to_convert:
    olympics_df[column] = pd.to_numeric(olympics_df[column], errors='coerce')

# Descriptive statistics
desc_stats = olympics_df.describe()
correlation_matrix = olympics_df.corr(numeric_only=True)
skewness = olympics_df.select_dtypes(include=['number']).apply(lambda x: skew(x.dropna()))
kurtosis_values = olympics_df.select_dtypes(include=['number']).apply(lambda x: kurtosis(x.dropna()))

# Visualization Functions

# Line Plot: Total medals for top 10 countries
def line_plot_top_total_medals(df):
    top_countries = df.nlargest(10, 'total_total').sort_values(by='total_total', ascending=False)
    plt.figure(figsize=(12, 6))
    plt.plot(top_countries['countries'], top_countries['summer_total'], label="Summer Total Medals", marker='o', linestyle='-', linewidth=2)
    plt.plot(top_countries['countries'], top_countries['winter_total'], label="Winter Total Medals", marker='o', linestyle='-', linewidth=2)
    plt.xlabel('Countries', fontweight='bold')
    plt.ylabel('Total Medals', fontweight='bold')
    plt.title('Total Medals for Top 10 Countries in Summer and Winter Olympics', fontweight='bold')
    plt.legend(fontsize=12, title="Olympic Type", title_fontsize='13', frameon=True, shadow=True)
    plt.xticks(rotation=45, fontweight='bold')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Bar Plot: Gold medals in Summer and Winter for top 10 countries
def bar_plot_gold_medals(df):
    top_countries = df.nlargest(10, 'total_gold')
    plt.figure(figsize=(12, 6))
    bar_width = 0.35
    positions = range(len(top_countries))
    plt.bar([p - bar_width/2 for p in positions], top_countries['summer_gold'], width=bar_width, label="Summer Gold Medals")
    plt.bar([p + bar_width/2 for p in positions], top_countries['winter_gold'], width=bar_width, label="Winter Gold Medals")
    plt.xlabel('Countries', fontweight='bold')
    plt.ylabel('Gold Medals', fontweight='bold')
    plt.title('Top 10 Countries by Total Gold Medals in Summer and Winter Olympics', fontweight='bold')
    plt.xticks(ticks=positions, labels=top_countries['countries'], rotation=45)
    plt.legend(fontsize=12, title="Season", title_fontsize='13')
    plt.tight_layout()
    plt.show()

# Heatmap: Correlation between medal and participation metrics
def heatmap_medal_correlation(df):
    plt.figure(figsize=(12, 10))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f", linewidths=.5)
    plt.title('Correlation Heatmap of Medal and Participation Metrics', fontweight='bold')
    plt.xticks(rotation=45, fontweight='bold')
    plt.yticks(fontweight='bold')
    plt.tight_layout()
    plt.show()

# Pie Chart: Distribution of total medals for top 5 countries
def pie_chart_top_medal_countries(df):
    top_5_countries = df.nlargest(5, 'total_total')
    other_medals = df['total_total'].sum() - top_5_countries['total_total'].sum()
    labels = list(top_5_countries['countries']) + ['Other Countries']
    sizes = list(top_5_countries['total_total']) + [other_medals]
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'weight': 'bold'})
    plt.title('Distribution of Total Medals Among Top 5 Countries', fontweight='bold')
    plt.tight_layout()
    plt.show()

# Call all visualizations
line_plot_top_total_medals(olympics_df)
bar_plot_gold_medals(olympics_df)
heatmap_medal_correlation(olympics_df)
pie_chart_top_medal_countries(olympics_df)