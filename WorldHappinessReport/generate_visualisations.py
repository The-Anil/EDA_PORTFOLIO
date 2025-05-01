# import pandas, matploit lib, seaborn
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# save_fig function to save the figure
def save_fig(filename):
    folder = 'editable_layout/static/'
    plt.subplots_adjust(left=0.1, right=0.9, top=0.88, bottom=0.15)
    plt.savefig(folder + filename, dpi=300, bbox_inches='tight')
    plt.close()


def fig_1_1(df, filename):
    # Average happiness score per year
    avg_score_per_year = df.groupby('year')['hScore'].mean().reset_index()

    # Flare color palette
    flare_colors = sns.color_palette("flare", 6)
    background_color = "#fae9e3"
    line_color = flare_colors[3]
    highlight_color = flare_colors[5]
    lowlight_color = flare_colors[0]
    dot_color = flare_colors[2]

    # Set background and style
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    # Plot line
    sns.lineplot(data=avg_score_per_year, x='year', y='hScore', marker=None, linewidth=2.5, color=line_color, ax=ax)

    # Plot small dots for all points
    ax.scatter(avg_score_per_year['year'], avg_score_per_year['hScore'],
            s=50, color=dot_color, edgecolor='black', linewidth=0.7, zorder=3)

    # Find peak and dip
    max_idx = avg_score_per_year['hScore'].idxmax()
    min_idx = avg_score_per_year['hScore'].idxmin()

    # Larger filled circles for peak and dip
    ax.scatter(avg_score_per_year.loc[max_idx, 'year'], avg_score_per_year.loc[max_idx, 'hScore'],
            color=highlight_color, s=180, edgecolor='black', linewidth=1.2, zorder=4)
    ax.scatter(avg_score_per_year.loc[min_idx, 'year'], avg_score_per_year.loc[min_idx, 'hScore'],
            color=lowlight_color, s=180, edgecolor='black', linewidth=1.2, zorder=4)

    # Annotate Peak and Dip
    ax.text(avg_score_per_year.loc[max_idx, 'year'] + 0.1, avg_score_per_year.loc[max_idx, 'hScore'],
            f"Peak: {avg_score_per_year.loc[max_idx, 'hScore']:.2f}",
            fontsize=12, color=highlight_color, fontweight='bold')

    ax.text(avg_score_per_year.loc[min_idx, 'year'] + 0.1, avg_score_per_year.loc[min_idx, 'hScore'],
            f"Dip: {avg_score_per_year.loc[min_idx, 'hScore']:.2f}",
            fontsize=12, color=lowlight_color, fontweight='bold')

    # Axis formatting
    ax.set_title("Global Average Happiness Score (2015–2019)", fontsize=16, weight='bold', pad=20, color='#222222')
    ax.set_xlabel("Year", fontsize=13, labelpad=10)
    ax.set_ylabel("Average Happiness Score", fontsize=13, labelpad=10)
    ax.set_xticks(avg_score_per_year['year'])
    ax.tick_params(axis='both', labelsize=11)

    # Tight layout and show
    plt.tight_layout()
    # Save the figure
    save_fig(filename)


def fig_1_2(df, filename):
    # Set the flare theme
    sns.set_style("whitegrid")
    flare_colors = sns.color_palette("flare", 10)

    # Calculate average rank and happiness score per country
    avg_rank_score = df.groupby('country')[['rank', 'hScore']].mean().reset_index()

    # Get top and bottom 10 countries
    top10 = avg_rank_score.nsmallest(10, 'rank').sort_values('hScore')
    bottom10 = avg_rank_score.nlargest(10, 'rank').sort_values('hScore')

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(20, 10), sharex=True)
    fig.patch.set_facecolor('#fae9e3')  # Lighter background

    # Function to plot bars with annotations
    def plot_bar(ax, data, title, palette):
        sns.barplot(data=data, y='country', x='hScore', palette=palette, ax=ax)
        ax.set_title(title, fontsize=18, weight='bold', color='#3e1f1c', pad=15)
        ax.set_xlabel('Average Happiness Score', fontsize=13)
        ax.set_ylabel('')
        ax.tick_params(axis='y', labelsize=12, pad=3)
        ax.set_facecolor('#fae9e3')
        ax.grid(axis='x', alpha=0.3)
        
        # Add data labels on right of the bars
        for i, row in enumerate(data.itertuples()):
            ax.text(row.hScore + 0.05, i, f"{row.hScore:.2f}", 
                    va='center', fontsize=12, color='#3e1f1c')

    # Plot Top 10
    plot_bar(axes[0], top10, 'Top 10 Happiest Countries (2015–2019)', flare_colors[5:])

    # Plot Bottom 10
    plot_bar(axes[1], bottom10, 'Bottom 10 Least Happy Countries (2015–2019)', flare_colors[:5])

    plt.suptitle("Average Happiness Scores by Country (2015–2019)", fontsize=20, weight='bold', color='#2e1614', y=1.02)
    plt.tight_layout(pad=3)
    plt.subplots_adjust(wspace=0.3)
    # Save the figure
    save_fig(filename)


def fig_1_3(df, filename):
    # Set flare theme
    sns.set_style("whitegrid")
    flare_colors = sns.color_palette("flare", n_colors=6)
    plt.rcParams['axes.facecolor'] = '#fae9e3'
    plt.rcParams['figure.facecolor'] = '#fae9e3'

    # Calculate yearly mean values for each happiness factor
    factor_cols = ['economy', 'socialSupp', 'lifeExp', 'freedom', 'govtTrust', 'generosity']
    factor_means = df.groupby('year')[factor_cols].mean().reset_index().set_index('year')

    # Plot stacked area chart
    plt.figure(figsize=(14, 8))
    plt.stackplot(factor_means.index,
                [factor_means[col] for col in factor_cols],
                labels=['Economy', 'Social Support', 'Life Expectancy', 'Freedom', 'Government Trust', 'Generosity'],
                colors=flare_colors, alpha=0.95)

    plt.title('Yearly Contribution of Happiness Factors (2015–2019)', fontsize=20, weight='bold', color='#3e1f1c', pad=20)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Mean Contribution', fontsize=14)
    plt.xticks(sorted(df['year'].unique()), fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(alpha=0.3)
    plt.legend(title='Factors', fontsize=12, title_fontsize=13, bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()

    # Save the figure
    save_fig(filename)


# read csv from Dataset\Consolidated_Data_World_Happiness_Report_2015_2019.csv 
df = pd.read_csv('Dataset/Consolidated_Data_World_Happiness_Report_2015_2019.csv')

# 1. General Trends Visualization 
fig_1_1(df, filename='Fig_1_1.png')
fig_1_2(df, filename='Fig_1_2.png')
fig_1_3(df, filename='Fig_1_3.png')