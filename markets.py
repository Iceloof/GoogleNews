from babel.core import get_global
import pycountry
import pandas as pd 

def country_language_population():
    df = pd.read_json('https://raw.githubusercontent.com/kwzrd/pypopulation/main/pypopulation/resources/countries.json').sort_values(by='Population',ascending=False)
    df["Languages"] = df["Alpha_2"].apply(lambda iso_alpha_2:get_global("territory_languages").get(iso_alpha_2, {}).copy())
    df["First_Language"] = df["Languages"].apply(lambda iso_alpha_2:list(iso_alpha_2.keys())[0])
    return df

def get_markets():
    df = country_language_population()
    return (df['Alpha_2']+'-'+df['First_Language']).tolist()






