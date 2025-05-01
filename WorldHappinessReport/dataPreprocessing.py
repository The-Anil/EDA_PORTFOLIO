import pandas as pd

# Function to load and preprocess the data
def data_preprocessing():
    """
    This function loads and preprocesses the World Happiness Report datasets from 2015 to 2019."
    """
    # Load the dataset for 2015 and clean it
    df15 = pd.read_csv("Dataset/2015.csv")
    df15.drop(columns=['Standard Error', 'Dystopia Residual'], axis=1, inplace=True)
    df15.rename(columns={'Country': 'country', 'Region': 'region', 'Happiness Rank': 'rank', 'Happiness Score': 'hScore', 'Economy (GDP per Capita)': 'economy', 'Family': 'socialSupp', 'Health (Life Expectancy)': 'lifeExp', 'Freedom': 'freedom', 'Trust (Government Corruption)': 'govtTrust', 'Generosity': 'generosity'}, inplace=True)

    # Load the dataset for 2016 and clean it
    df16 = pd.read_csv("Dataset/2016.csv")
    df16.drop(columns=['Lower Confidence Interval', 'Upper Confidence Interval', 'Dystopia Residual'], axis=1, inplace=True)
    df16.rename(columns={'Country': 'country', 'Region': 'region', 'Happiness Rank': 'rank', 'Happiness Score': 'hScore', 'Economy (GDP per Capita)': 'economy', 'Family': 'socialSupp', 'Health (Life Expectancy)': 'lifeExp', 'Freedom': 'freedom', 'Trust (Government Corruption)': 'govtTrust', 'Generosity': 'generosity'}, inplace=True)

    # ############# making a dictionary to map country names to regions ###############
    country_region_map = dict(zip(df15['country'], df15['region']))
    country_region_map.update(dict(zip(df16['country'], df16['region'])))
    country_region_map.update({'Taiwan Province of China': 'Eastern Asia', 'Hong Kong S.A.R., China': 'Southern Asia'})
    country_region_map.update({'Trinidad & Tobago': 'Latin America and Caribbean', 'Northern Cyprus': 'Southeastern Asia'})
    country_region_map.update({'North Macedonia': 'Central and Eastern Europe', 'Gambia': 'Sub-Saharan Africa'})

    # Load the dataset for 2017 and clean it
    df17 = pd.read_csv("Dataset/2017.csv")
    df17.drop(columns=['Whisker.high', 'Whisker.low', 'Dystopia.Residual'], axis=1, inplace=True)
    df17.rename(columns={'Country': 'country', 'Happiness.Rank': 'rank', 'Happiness.Score': 'hScore', 'Economy..GDP.per.Capita.': 'economy', 'Family': 'socialSupp', 'Health..Life.Expectancy.': 'lifeExp', 'Freedom': 'freedom', 'Trust..Government.Corruption.': 'govtTrust', 'Generosity': 'generosity'}, inplace=True)
    df17['region'] = df17['country'].apply(lambda x: country_region_map.get(x, 'Unknown'))
    df17 = df17[['country', 'region', 'rank', 'hScore', 'economy', 'socialSupp', 'lifeExp', 'freedom', 'govtTrust', 'generosity']]

    # Load the dataset for 2018 and clean it
    df18 = pd.read_csv("Dataset/2018.csv")
    df18.rename(columns={'Country or region': 'country', 'Overall rank': 'rank', 'Score': 'hScore', 'GDP per capita': 'economy', 'Social support': 'socialSupp', 'Healthy life expectancy': 'lifeExp', 'Freedom to make life choices': 'freedom', 'Perceptions of corruption': 'govtTrust', 'Generosity': 'generosity'}, inplace=True)
    df18['region'] = df18['country'].apply(lambda x: country_region_map.get(x,'Unknown'))
    df18 = df18[['country', 'region', 'rank', 'hScore', 'economy', 'socialSupp', 'lifeExp', 'freedom', 'govtTrust', 'generosity']]

    # Load the dataset for 2019 and clean it
    df19 = pd.read_csv("Dataset/2019.csv")
    df19.rename(columns={'Country or region': 'country', 'Overall rank': 'rank', 'Score': 'hScore', 'GDP per capita': 'economy', 'Social support': 'socialSupp', 'Healthy life expectancy': 'lifeExp', 'Freedom to make life choices': 'freedom', 'Perceptions of corruption': 'govtTrust', 'Generosity': 'generosity'}, inplace=True)
    df19['region'] = df19['country'].apply(lambda x: country_region_map.get(x,'Unknown'))
    df19 = df19[['country', 'region', 'rank', 'hScore', 'economy', 'socialSupp', 'lifeExp', 'freedom', 'govtTrust', 'generosity']]


    # Add the year column to each dataframe and concatenate them
    df15['year'] = 2015
    df16['year'] = 2016
    df17['year'] = 2017
    df18['year'] = 2018
    df19['year'] = 2019
    df = pd.concat([df15, df16, df17, df18, df19], ignore_index=True)
    return df

# Preprocess data
df = data_preprocessing()

df.to_csv('Dataset/Consolidated_Data_World_Happiness_Report_2015_2019.csv', index=False)