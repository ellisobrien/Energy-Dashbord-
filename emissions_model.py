
#importing packages :)
import streamlit as st
import pandas as pd
import numpy as np
import io
import geopandas as gp


import pandas as pd
import requests
from bs4 import BeautifulSoup
import requests
import time
import random
from pandas import DataFrame
import plotly.express as px
import plotly
import json
import altair as alt
import plotly.offline as po
import plotly.graph_objs as pg


# Data Management/Investigation
from pandas.api.types import CategoricalDtype # Ordering categories
import numpy as np

# Plotting libraries
from plotnine import *
import matplotlib.pyplot as plt

# Downloading CO2 data from the csv file on GitHub
url_co2_cb = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv" # Make sure the url is the raw version of the file on GitHub
download = requests.get(url_co2_cb).content
# Reading the downloaded content and turning it into a pandas dataframe
df_co2_cb = pd.read_csv(io.StringIO(download.decode('utf-8')))


# Downloading energy csv file from GitHub
url_co2 = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv" # Make sure the url is the raw version of the file on GitHub
download = requests.get(url_co2).content
# Reading the downloaded content and turning it into a pandas dataframe
df_co2 = pd.read_csv(io.StringIO(download.decode('utf-8')))

# Downloading the csv file from GitHub
url_eng_cb = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-codebook.csv" # Make sure the url is the raw version of the file on GitHub
download = requests.get(url_eng_cb).content
# Reading the downloaded content and turning it into a pandas dataframe
df_eng_cb = pd.read_csv(io.StringIO(download.decode('utf-8')))

# Downloading the csv file from GitHub
url_eng = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv" # Make sure the url is the raw version of the file on GitHub
download = requests.get(url_eng).content
# Reading the downloaded content and turning it into a pandas dataframe
df_eng = pd.read_csv(io.StringIO(download.decode('utf-8')))

###################################################################
carb_dat=pd.read_csv("/Users/ellisobrien/Desktop/Georgetown Semester 2/Data Science /Final Project/carbdat.csv")
temp_dat=pd.read_csv("/Users/ellisobrien/Desktop/Georgetown Semester 2/Data Science /Final Project/Tempdat.csv")
carb_dat.rename(columns={'Row Labels': 'Year'}, inplace=True)

#####################################################################
world_filepath = gp.datasets.get_path('naturalearth_lowres')
world = gp.read_file(world_filepath)
world=world.rename(columns={'iso_a3': 'iso_code'})
df_co2_map = df_co2.merge(world, how='left', on="iso_code")
df_co2_map=df_co2_map[df_co2_map.year == 2020]
df_eng_map=df_eng[df_eng.year == 2020]
df_co2_map = df_co2_map.merge(df_eng_map, how='left', on="iso_code")
df_co2_map=(df_co2_map[df_co2_map["co2"]<11000])


st.header("Ellis's Energy & Emissions Extravaganza :)")
st.markdown("**Ellis Obrien DS2 Final: Building a dashboard for the climate discussion**")
st.markdown('_"It is unequivocal that human influence has warmed the atmosphere, ocean and land. Widespread and rapid changes in the atmosphere, ocean, cryosphere and biosphere have occurred."_-IPCC Report 2021')


st.video("https://media2.ldscdn.org/assets/news-and-public-affairs/newsroom-2021/2021-01-0131-flooding-in-laie-hawaii-b-roll-1080p-eng.mp4")
st.caption("By 2050, 800 million people could live in unhabitable cities due to frequent flooding from sea level rise. (C40)")


st.metric(label="Earth's Average Temperature", value="13.88°C", delta="1.0°C")
st.caption("The earths current average temperature is 13.88°C (57°F). This is up 1°C (1.8°F) from pre-industrial levels.")

"""
##### About
"""
st.write( "Climate change is one of the most pressing issues of our times. According to some private sector reports, the cost of this anthropogenic climate change could amount to $23 trillion annually by 2050 (Swiss Re, 2021). Additionally, by 2050 there will be an estimated 200 million climate refugees who have been forced from their homes. In order to avoid the most severe effects of climate change, the U.N. has concluded that we will need to avoid a 2°C increase in temperature from pre-industrial levels due to avoid the worst of climate change. In order to accomplish this, atmospheric carbon levels will need to stabilize around 450 PPM, which would require a 60% reduction in emissions by 2050. Theoretically, this is feasible. Scholars have argued that it is within the realm of technological advancement to get 80% of U.S energy from renewable sources. Currently, the U.S. gets approximately 20% of its energy from carbon-neutral sources. There are, however, significant political and economic barries to catalyzing this shift.")
st.image("/Users/ellisobrien/Documents/Screen Shot 2022-04-26 at 8.37.36 PM.png")
st.caption("Forest fires are estimated to be 33% more frequent by 2050. In 2020 forest fires cost California 20 billion dollars.")

"""
##### Concerning Trends
"""
fig0 = px.line(carb_dat, x='Year', y='Average of Carbon PPM',  title='Average of Carbon PPM')
fig0.update_layout(title_text='Atmospheric Carbon by Year', title_x=0.5, title_y=0.9)
st.plotly_chart(fig0)
st.caption('Earth atmospheric carbon levels have increased by approximately 2.4 PPM annually over the last 10 years. At this rate we will cross the 450 PPM threshold in less than 15 years. (Data Source: NASA)')

fig0 = px.bar(temp_dat, x='Year', y='Temp Change',  title='Difference from 1900-2000 Average °C', color='Temp Change')
fig0.update_layout(title_text='Change in Average Global Temp from 1900-2000 Average (°C)', title_x=0.5, title_y=0.9)
st.plotly_chart(fig0)
st.caption("Scientists warn of a significant lag between atmospheric carbon and measured increases in temperature. This means that even if stabilized atmospheric carbon today we still see temperature increases for up to a decade. Currently, we have seen about 1°C temperature increase.(Source: NOAA)")
"""
##### World Map of Emmissions or Energy
"""
if st.checkbox("Explore World Map of Emissions"):
    answer00 = st.selectbox(label="What variable would you like to view?",
    options=("co2", "co2_per_capita", 'coal_co2', 'coal_co2_per_capita', 'gas_co2',
             'gas_co2_per_capita', 'oil_co2', 'oil_co2_per_capita', 'co2_per_gdp',
             'methane','methane_per_capita','nitrous_oxide','nitrous_oxide_per_capita', 'trade_co2',
             'population', 'gdp', 'co2_growth_prct', 'co2_growth_abs', "primary_energy_consumption",	"per_capita_electricity",	"energy_per_capita",	"energy_per_gdp",	"biofuel_electricity",	"coal_electricity",	"fossil_electricity", "renewables_electricity",	"gas_electricity",	"hydro_electricity",	"nuclear_electricity",	"oil_electricity",	"solar_electricity",	"wind_electricity", "other_renewable_electricity",	"other_renewable_exc_biofuel_electricity",	"electricity_demand",	"electricity_generation",	"renewables_energy_per_capita",	"renewables_elec_per_capita",	"renewables_share_elec",	"renewables_cons_change_pct",	"renewables_share_energy",	"renewables_cons_change_twh",	"renewables_consumption",	"energy_cons_change_pct",	"energy_cons_change_twh",	"coal_share_elec",	"coal_cons_change_pct",	"coal_share_energy",	"coal_cons_change_twh",	"coal_consumption",	"coal_elec_per_capita",	"coal_cons_per_capita",	"coal_production",	"coal_prod_per_capita",	"biofuel_share_elec",	"biofuel_cons_change_pct",	"biofuel_share_energy",	"biofuel_cons_change_twh",	"biofuel_consumption",	"biofuel_elec_per_capita",	"biofuel_cons_per_capita",	"carbon_intensity_elec",	"fossil_cons_change_pct",	"fossil_share_energy",	"fossil_cons_change_twh",	"fossil_fuel_consumption",	"fossil_energy_per_capita",	"fossil_cons_per_capita",	"fossil_share_elec",	"gas_share_elec",	"gas_cons_change_pct",	"gas_share_energy", "gas_cons_change_twh",	"gas_consumption",	"gas_elec_per_capita",	"gas_energy_per_capita",	"gas_production",	"gas_prod_per_capita",	"hydro_share_elec",	"hydro_cons_change_pct",	"hydro_share_energy",	"hydro_cons_change_twh",	"hydro_consumption",	"hydro_elec_per_capita",	"hydro_energy_per_capita",	"low_carbon_share_elec",	"low_carbon_electricity",	"low_carbon_elec_per_capita",	"low_carbon_cons_change_pct",	"low_carbon_share_energy",	"low_carbon_cons_change_twh",	"low_carbon_consumption",	"low_carbon_energy_per_capita",	"net_elec_imports",	"net_elec_imports_share_demand",	"nuclear_share_elec",	"nuclear_cons_change_pct",	"nuclear_share_energy",	"nuclear_cons_change_twh",	"nuclear_consumption",	"nuclear_elec_per_capita",	"nuclear_energy_per_capita",	"oil_share_elec",	"oil_cons_change_pct",	"oil_share_energy",	"oil_cons_change_twh",	"oil_consumption",	"oil_elec_per_capita",	"oil_energy_per_capita",	"oil_production",	"oil_prod_per_capita",	"other_renewables_elec_per_capita",	"other_renewables_elec_per_capita_exc_biofuel",	"other_renewables_share_elec",	"other_renewables_share_elec_exc_biofuel",	"other_renewables_cons_change_pct",	"other_renewables_share_energy",	"other_renewables_cons_change_twh",	"other_renewable_consumption",	"other_renewables_energy_per_capita",	"solar_share_elec",	"solar_cons_change_pct",	"solar_share_energy",	"solar_cons_change_twh",	"solar_consumption",	"solar_elec_per_capita",	"solar_energy_per_capita",	"gdp",	"wind_share_elec",	"wind_cons_change_pct",	"wind_share_energy",	"wind_cons_change_twh",	"wind_consumption",	"wind_elec_per_capita",	"wind_energy_per_capita",	"coal_prod_change_pct",	"coal_prod_change_twh",	"gas_prod_change_pct",	"gas_prod_change_twh",	"oil_prod_change_pct",	"oil_prod_change_twh"))

    def country_map(input_var):
        data = dict(type='choropleth',
                    locations = df_co2_map['iso_code'],
                    z = df_co2_map[input_var],
                    text = df_co2_map['country_x'])

        layout = dict(title = input_var,
                      geo = dict( projection = {'type':'natural earth'},
                                 showlakes = True,
                                 lakecolor = 'rgb(0,191,255)'))

        fig11 = pg.Figure(data = [data],
                      layout = layout)
        st.plotly_chart(fig11)
    country_map(answer00)




if st.checkbox("Explore World Bubble Map of Emissions"):
    answer0 = st.selectbox(label="What variable would you like to view?",
    options=("co2", "co2_per_capita", 'coal_co2', 'coal_co2_per_capita', 'gas_co2',
             'gas_co2_per_capita', 'oil_co2', 'oil_co2_per_capita', 'co2_per_gdp',
             'methane','methane_per_capita','nitrous_oxide','nitrous_oxide_per_capita', 'trade_co2',
             'population', 'gdp', 'co2_growth_prct', 'co2_growth_abs', "primary_energy_consumption",	"per_capita_electricity",	"energy_per_capita",	"energy_per_gdp",	"biofuel_electricity",	"coal_electricity",	"fossil_electricity", "renewables_electricity",	"gas_electricity",	"hydro_electricity",	"nuclear_electricity",	"oil_electricity",	"solar_electricity",	"wind_electricity", "other_renewable_electricity",	"other_renewable_exc_biofuel_electricity",	"electricity_demand",	"electricity_generation",	"renewables_energy_per_capita",	"renewables_elec_per_capita",	"renewables_share_elec",	"renewables_cons_change_pct",	"renewables_share_energy",	"renewables_cons_change_twh",	"renewables_consumption",	"energy_cons_change_pct",	"energy_cons_change_twh",	"coal_share_elec",	"coal_cons_change_pct",	"coal_share_energy",	"coal_cons_change_twh",	"coal_consumption",	"coal_elec_per_capita",	"coal_cons_per_capita",	"coal_production",	"coal_prod_per_capita",	"biofuel_share_elec",	"biofuel_cons_change_pct",	"biofuel_share_energy",	"biofuel_cons_change_twh",	"biofuel_consumption",	"biofuel_elec_per_capita",	"biofuel_cons_per_capita",	"carbon_intensity_elec",	"fossil_cons_change_pct",	"fossil_share_energy",	"fossil_cons_change_twh",	"fossil_fuel_consumption",	"fossil_energy_per_capita",	"fossil_cons_per_capita",	"fossil_share_elec",	"gas_share_elec",	"gas_cons_change_pct",	"gas_share_energy",	"gas_cons_change_twh",	"gas_consumption",	"gas_elec_per_capita",	"gas_energy_per_capita",	"gas_production",	"gas_prod_per_capita",	"hydro_share_elec",	"hydro_cons_change_pct",	"hydro_share_energy",	"hydro_cons_change_twh",	"hydro_consumption",	"hydro_elec_per_capita",	"hydro_energy_per_capita",	"low_carbon_share_elec",	"low_carbon_electricity",	"low_carbon_elec_per_capita",	"low_carbon_cons_change_pct",	"low_carbon_share_energy",	"low_carbon_cons_change_twh",	"low_carbon_consumption",	"low_carbon_energy_per_capita",	"net_elec_imports",	"net_elec_imports_share_demand",	"nuclear_share_elec",	"nuclear_cons_change_pct",	"nuclear_share_energy",	"nuclear_cons_change_twh",	"nuclear_consumption",	"nuclear_elec_per_capita",	"nuclear_energy_per_capita",	"oil_share_elec",	"oil_cons_change_pct",	"oil_share_energy",	"oil_cons_change_twh",	"oil_consumption",	"oil_elec_per_capita",	"oil_energy_per_capita",	"oil_production",	"oil_prod_per_capita",	"other_renewables_elec_per_capita",	"other_renewables_elec_per_capita_exc_biofuel",	"other_renewables_share_elec",	"other_renewables_share_elec_exc_biofuel",	"other_renewables_cons_change_pct",	"other_renewables_share_energy",	"other_renewables_cons_change_twh",	"other_renewable_consumption",	"other_renewables_energy_per_capita",	"solar_share_elec",	"solar_cons_change_pct",	"solar_share_energy",	"solar_cons_change_twh",	"solar_consumption",	"solar_elec_per_capita",	"solar_energy_per_capita",	"gdp",	"wind_share_elec",	"wind_cons_change_pct",	"wind_share_energy",	"wind_cons_change_twh",	"wind_consumption",	"wind_elec_per_capita",	"wind_energy_per_capita",	"coal_prod_change_pct",	"coal_prod_change_twh",	"gas_prod_change_pct",	"gas_prod_change_twh",	"oil_prod_change_pct",	"oil_prod_change_twh"))

    def country_bubble_map(input_var):
        df_co2_map_2=df_co2_map[['iso_code', 'country_x', input_var, 'continent']]
        df_co2_map_2.dropna(inplace=True)
        fig10 = px.scatter_geo(df_co2_map_2, locations="iso_code", color="continent",
                         hover_name="country_x", size=input_var,
                         projection="natural earth", width=1000, height=500)
        st.plotly_chart(fig10)

    country_bubble_map(answer0)
    st.caption("China (30%), U.S (14%), and India (7%) represent the top 3 carbon emitters. Currently, the global South relies primarily on renewable electricity while the global North relies heavily on fossil fuels. While it is imperative that the major emitters change their actions swiftly, it is important to remember climate change is a global issue that no single country can solve.")



"""
##### Emmissions
"""
if st.checkbox("Explore emissions by year"):
    answer1 = st.selectbox(label="What variable would you like to view?",
    options=("co2", "co2_per_capita", 'coal_co2', 'coal_co2_per_capita', 'gas_co2',
    	     'gas_co2_per_capita', 'oil_co2',	'oil_co2_per_capita', 'co2_per_gdp',
             'methane','methane_per_capita','nitrous_oxide','nitrous_oxide_per_capita', 'trade_co2',
             'population', 'gdp', 'co2_growth_prct', 'co2_growth_abs'))

    answer2 = st.selectbox(label="What country or region would you like to view?",
    options=('World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America',
           'Afghanistan',  'Albania', 'Algeria', 'Andorra', 'Angola',
           'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina',
           'Armenia', 'Aruba', 'Asia (excl. China & India)',
           'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
           'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
           'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire Sint Eustatius and Saba',
           'Bosnia and Herzegovina', 'Botswana', 'Brazil',
           'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso',
           'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
           'Central African Republic', 'Chad', 'Chile', 'China',
           'Christmas Island', 'Colombia', 'Comoros', 'Congo', 'Cook Islands',
           'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao',
           'Cyprus', 'Czechia', 'Democratic Republic of Congo', 'Denmark',
           'Djibouti', 'Dominica', 'Dominican Republic', 'EU-27', 'Ecuador',
           'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
           'Eswatini', 'Ethiopia', 'Europe (excl. EU-27)',
           'Europe (excl. EU-28)', 'European Union (27)',
           'European Union (28)', 'Faeroe Islands', 'Fiji', 'Finland',
           'France', 'French Equatorial Africa', 'French Guiana',
           'French Polynesia', 'French West Africa', 'Gabon', 'Gambia',
           'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada',
           'Guadeloupe', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
           'Haiti', 'High-income countries', 'Honduras', 'Hong Kong',
           'Hungary', 'Iceland', 'India', 'Indonesia',
           'International transport', 'Iran', 'Iraq', 'Ireland', 'Israel',
           'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
           'Kiribati', 'Kosovo', 'Kuwait', 'Kuwaiti Oil Fires', 'Kyrgyzstan',
           'Laos', 'Latvia', 'Lebanon', 'Leeward Islands', 'Lesotho',
           'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
           'Low-income countries', 'Lower-middle-income countries',
           'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia',
           'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
           'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
           'Micronesia (country)', 'Moldova', 'Mongolia', 'Montenegro',
           'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
           'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
           'Nicaragua', 'Niger', 'Nigeria', 'Niue',
           'North America (excl. USA)', 'North Korea', 'North Macedonia',
           'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine',
           'Panama', 'Panama Canal Zone', 'Papua New Guinea', 'Paraguay',
           'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
           'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda',
           'Ryukyu Islands', 'Saint Helena', 'Saint Kitts and Nevis',
           'Saint Lucia', 'Saint Pierre and Miquelon',
           'Saint Vincent and the Grenadines', 'Samoa',
           'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
           'Seychelles', 'Sierra Leone', 'Singapore',
           'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia',
           'Solomon Islands', 'Somalia', 'South Africa',
           'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
           'St. Kitts-Nevis-Anguilla', 'Sudan', 'Suriname', 'Sweden',
           'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
           'Thailand', 'Timor', 'Togo', 'Tonga', 'Trinidad and Tobago',
           'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands',
           'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
           'United Kingdom', 'United States', 'Upper-middle-income countries',
           'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam',
           'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe'))


    answer3 = st.selectbox(label="View from which year?",
    options=(1970, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908, 1907, 1906, 1905, 1904, 1903, 1902, 1901, 1900, 1899, 1898, 1897, 1896, 1895, 1894, 1893, 1892, 1891, 1890, 1889, 1888, 1887, 1886, 1885, 1884, 1883, 1882, 1881, 1880, 1879, 1878, 1877, 1876, 1875, 1874, 1873, 1872, 1871, 1870, 1869, 1868, 1867, 1866, 1865, 1864, 1863, 1862, 1861, 1860, 1859, 1858, 1857, 1856, 1855, 1854, 1853, 1852, 1851, 1850, 1849, 1848, 1847, 1846, 1845, 1844, 1843, 1842, 1841, 1840, 1839, 1838, 1837, 1836, 1835, 1834, 1833, 1832, 1831, 1830, 1829, 1828, 1827, 1826, 1825, 1824, 1823, 1822, 1821, 1820, 1819, 1818, 1817, 1816, 1815, 1814, 1813, 1812, 1811, 1810, 1809, 1808, 1807, 1806, 1805, 1804, 1803, 1802, 1801, 1800, 1799, 1798, 1797, 1796, 1795, 1794, 1793, 1792, 1791, 1790, 1789, 1788, 1787, 1786, 1785, 1784, 1783, 1782, 1781, 1780, 1779, 1778, 1777, 1776, 1775, 1774, 1773, 1772, 1771, 1770, 1769, 1768, 1767, 1766, 1765, 1764, 1763, 1762, 1761, 1760, 1759, 1758, 1757, 1756, 1755, 1754, 1753, 1752, 1751, 1750))



    def country_bar_graph(input_year, input_country, input_var):
        graph_data=df_co2[df_co2.year > input_year]
        graph_data=graph_data[graph_data.country == input_country]
        fig = px.bar(graph_data, x='year', y=input_var, color=input_var, title=input_country)
        fig.update_layout(title_text=input_country, title_x=0.5, title_y=0.9)
        st.plotly_chart(fig)

    country_bar_graph(answer3, answer2, answer1)
    st.caption("Currently, global emmissions are around 35 million tonnes annually. We will need to get this number to around 14 million tonnes. In 2020 the U.S emitted roughly  equilivent to the continent of Africa and the entire EU combined.")

elif st.checkbox("Explore Breakdowns of Aggregate Emissions by Year"):
    answer4 = st.selectbox(label="What country or region would you like to view?",
    options=('World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America',
           'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola',
           'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina',
           'Armenia', 'Aruba', 'Asia (excl. China & India)',
           'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
           'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
           'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire Sint Eustatius and Saba',
           'Bosnia and Herzegovina', 'Botswana', 'Brazil',
           'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso',
           'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
           'Central African Republic', 'Chad', 'Chile', 'China',
           'Christmas Island', 'Colombia', 'Comoros', 'Congo', 'Cook Islands',
           'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao',
           'Cyprus', 'Czechia', 'Democratic Republic of Congo', 'Denmark',
           'Djibouti', 'Dominica', 'Dominican Republic', 'EU-27', 'Ecuador',
           'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
           'Eswatini', 'Ethiopia', 'Europe (excl. EU-27)',
           'Europe (excl. EU-28)', 'European Union (27)',
           'European Union (28)', 'Faeroe Islands', 'Fiji', 'Finland',
           'France', 'French Equatorial Africa', 'French Guiana',
           'French Polynesia', 'French West Africa', 'Gabon', 'Gambia',
           'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada',
           'Guadeloupe', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
           'Haiti', 'High-income countries', 'Honduras', 'Hong Kong',
           'Hungary', 'Iceland', 'India', 'Indonesia',
           'International transport', 'Iran', 'Iraq', 'Ireland', 'Israel',
           'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
           'Kiribati', 'Kosovo', 'Kuwait', 'Kuwaiti Oil Fires', 'Kyrgyzstan',
           'Laos', 'Latvia', 'Lebanon', 'Leeward Islands', 'Lesotho',
           'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
           'Low-income countries', 'Lower-middle-income countries',
           'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia',
           'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
           'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
           'Micronesia (country)', 'Moldova', 'Mongolia', 'Montenegro',
           'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
           'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
           'Nicaragua', 'Niger', 'Nigeria', 'Niue',
           'North America (excl. USA)', 'North Korea', 'North Macedonia',
           'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine',
           'Panama', 'Panama Canal Zone', 'Papua New Guinea', 'Paraguay',
           'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
           'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda',
           'Ryukyu Islands', 'Saint Helena', 'Saint Kitts and Nevis',
           'Saint Lucia', 'Saint Pierre and Miquelon',
           'Saint Vincent and the Grenadines', 'Samoa',
           'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
           'Seychelles', 'Sierra Leone', 'Singapore',
           'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia',
           'Solomon Islands', 'Somalia', 'South Africa',
           'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
           'St. Kitts-Nevis-Anguilla', 'Sudan', 'Suriname', 'Sweden',
           'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
           'Thailand', 'Timor', 'Togo', 'Tonga', 'Trinidad and Tobago',
           'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands',
           'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
           'United Kingdom', 'United States', 'Upper-middle-income countries',
           'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam',
           'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe'))


    answer5 = st.selectbox(label="View from which year?",
    options=(1970, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908, 1907, 1906, 1905, 1904, 1903, 1902, 1901, 1900, 1899, 1898, 1897, 1896, 1895, 1894, 1893, 1892, 1891, 1890, 1889, 1888, 1887, 1886, 1885, 1884, 1883, 1882, 1881, 1880, 1879, 1878, 1877, 1876, 1875, 1874, 1873, 1872, 1871, 1870, 1869, 1868, 1867, 1866, 1865, 1864, 1863, 1862, 1861, 1860, 1859, 1858, 1857, 1856, 1855, 1854, 1853, 1852, 1851, 1850, 1849, 1848, 1847, 1846, 1845, 1844, 1843, 1842, 1841, 1840, 1839, 1838, 1837, 1836, 1835, 1834, 1833, 1832, 1831, 1830, 1829, 1828, 1827, 1826, 1825, 1824, 1823, 1822, 1821, 1820, 1819, 1818, 1817, 1816, 1815, 1814, 1813, 1812, 1811, 1810, 1809, 1808, 1807, 1806, 1805, 1804, 1803, 1802, 1801, 1800, 1799, 1798, 1797, 1796, 1795, 1794, 1793, 1792, 1791, 1790, 1789, 1788, 1787, 1786, 1785, 1784, 1783, 1782, 1781, 1780, 1779, 1778, 1777, 1776, 1775, 1774, 1773, 1772, 1771, 1770, 1769, 1768, 1767, 1766, 1765, 1764, 1763, 1762, 1761, 1760, 1759, 1758, 1757, 1756, 1755, 1754, 1753, 1752, 1751, 1750))

    def Aggregate_bar_graph(input_year, input_country):
        graph_data2=df_co2[df_co2.year > input_year]
        graph_data2=graph_data2[graph_data2.country == input_country]
        fig2 = px.bar(graph_data2, x='year', y= ['coal_co2', 'gas_co2',
        'oil_co2', 'other_industry_co2', 'cement_co2', 'flaring_co2'],  title=input_country)
        fig2.update_layout(title_text=input_country, title_x=0.5, title_y=0.9)
        st.plotly_chart(fig2)

    Aggregate_bar_graph(answer5, answer4)
    st.caption("Over 70% of Chinese emmissions come from coal. With a global shift towards natural gas it will be interesting to see how this number changes in the upcoming years. Ultimatley, it does not matter too much where emissions came from and the U.S and China will need to rely primarily on carbon neatural energy to avoid the worst of a climate catastrophe.")

elif st.checkbox("Explore Breakdowns of Per Capita Emissions by Year"):
    answer6 = st.selectbox(label="What country or region would you like to view?",
    options=('World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America',
           'Afghanistan',  'Albania', 'Algeria', 'Andorra', 'Angola',
           'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina',
           'Armenia', 'Aruba', 'Asia (excl. China & India)',
           'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
           'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
           'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire Sint Eustatius and Saba',
           'Bosnia and Herzegovina', 'Botswana', 'Brazil',
           'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso',
           'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
           'Central African Republic', 'Chad', 'Chile', 'China',
           'Christmas Island', 'Colombia', 'Comoros', 'Congo', 'Cook Islands',
           'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao',
           'Cyprus', 'Czechia', 'Democratic Republic of Congo', 'Denmark',
           'Djibouti', 'Dominica', 'Dominican Republic', 'EU-27', 'Ecuador',
           'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
           'Eswatini', 'Ethiopia', 'Europe (excl. EU-27)',
           'Europe (excl. EU-28)', 'European Union (27)',
           'European Union (28)', 'Faeroe Islands', 'Fiji', 'Finland',
           'France', 'French Equatorial Africa', 'French Guiana',
           'French Polynesia', 'French West Africa', 'Gabon', 'Gambia',
           'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada',
           'Guadeloupe', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
           'Haiti', 'High-income countries', 'Honduras', 'Hong Kong',
           'Hungary', 'Iceland', 'India', 'Indonesia',
           'International transport', 'Iran', 'Iraq', 'Ireland', 'Israel',
           'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
           'Kiribati', 'Kosovo', 'Kuwait', 'Kuwaiti Oil Fires', 'Kyrgyzstan',
           'Laos', 'Latvia', 'Lebanon', 'Leeward Islands', 'Lesotho',
           'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
           'Low-income countries', 'Lower-middle-income countries',
           'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia',
           'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
           'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
           'Micronesia (country)', 'Moldova', 'Mongolia', 'Montenegro',
           'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
           'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
           'Nicaragua', 'Niger', 'Nigeria', 'Niue',
           'North America (excl. USA)', 'North Korea', 'North Macedonia',
           'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine',
           'Panama', 'Panama Canal Zone', 'Papua New Guinea', 'Paraguay',
           'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
           'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda',
           'Ryukyu Islands', 'Saint Helena', 'Saint Kitts and Nevis',
           'Saint Lucia', 'Saint Pierre and Miquelon',
           'Saint Vincent and the Grenadines', 'Samoa',
           'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
           'Seychelles', 'Sierra Leone', 'Singapore',
           'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia',
           'Solomon Islands', 'Somalia', 'South Africa',
           'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
           'St. Kitts-Nevis-Anguilla', 'Sudan', 'Suriname', 'Sweden',
           'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
           'Thailand', 'Timor', 'Togo', 'Tonga', 'Trinidad and Tobago',
           'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands',
           'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
           'United Kingdom', 'United States', 'Upper-middle-income countries',
           'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam',
           'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe'))


    answer7 = st.selectbox(label="View from which year?",
    options=(1970, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908, 1907, 1906, 1905, 1904, 1903, 1902, 1901, 1900, 1899, 1898, 1897, 1896, 1895, 1894, 1893, 1892, 1891, 1890, 1889, 1888, 1887, 1886, 1885, 1884, 1883, 1882, 1881, 1880, 1879, 1878, 1877, 1876, 1875, 1874, 1873, 1872, 1871, 1870, 1869, 1868, 1867, 1866, 1865, 1864, 1863, 1862, 1861, 1860, 1859, 1858, 1857, 1856, 1855, 1854, 1853, 1852, 1851, 1850, 1849, 1848, 1847, 1846, 1845, 1844, 1843, 1842, 1841, 1840, 1839, 1838, 1837, 1836, 1835, 1834, 1833, 1832, 1831, 1830, 1829, 1828, 1827, 1826, 1825, 1824, 1823, 1822, 1821, 1820, 1819, 1818, 1817, 1816, 1815, 1814, 1813, 1812, 1811, 1810, 1809, 1808, 1807, 1806, 1805, 1804, 1803, 1802, 1801, 1800, 1799, 1798, 1797, 1796, 1795, 1794, 1793, 1792, 1791, 1790, 1789, 1788, 1787, 1786, 1785, 1784, 1783, 1782, 1781, 1780, 1779, 1778, 1777, 1776, 1775, 1774, 1773, 1772, 1771, 1770, 1769, 1768, 1767, 1766, 1765, 1764, 1763, 1762, 1761, 1760, 1759, 1758, 1757, 1756, 1755, 1754, 1753, 1752, 1751, 1750))

    def per_capita_bar_graph(input_year, input_country):
        graph_data3=df_co2[df_co2.year > input_year]
        graph_data3=graph_data3[graph_data3.country == input_country]
        fig3 = px.bar(graph_data3, x='year', y= ['coal_co2_per_capita', 'gas_co2_per_capita', 'oil_co2_per_capita',
        'cement_co2_per_capita', 'flaring_co2_per_capita', 'other_co2_per_capita'],  title=input_country)
        fig3.update_layout(title_text=input_country, title_x=0.5, title_y=0.9)
        st.plotly_chart(fig3)

    per_capita_bar_graph (answer7, answer6)
"""
##### Energy
"""
##############################################################################################################################################
if st.checkbox("Explore energy categories by year"):
    answer8 = st.selectbox(label="What variable would you like to view?",
    options=("primary_energy_consumption",	"per_capita_electricity",	"energy_per_capita",	"energy_per_gdp",	"biofuel_electricity",	"coal_electricity",	"fossil_electricity", "renewables_electricity",	"gas_electricity",	"hydro_electricity",	"nuclear_electricity",	"oil_electricity",	"solar_electricity",	"wind_electricity", "other_renewable_electricity",	"other_renewable_exc_biofuel_electricity",	"electricity_demand",	"electricity_generation",	"renewables_energy_per_capita",	"renewables_elec_per_capita",	"renewables_share_elec",	"renewables_cons_change_pct",	"renewables_share_energy",	"renewables_cons_change_twh",	"renewables_consumption",	"energy_cons_change_pct",	"energy_cons_change_twh",	"coal_share_elec",	"coal_cons_change_pct",	"coal_share_energy",	"coal_cons_change_twh",	"coal_consumption",	"coal_elec_per_capita",	"coal_cons_per_capita",	"coal_production",	"coal_prod_per_capita",	"biofuel_share_elec",	"biofuel_cons_change_pct",	"biofuel_share_energy",	"biofuel_cons_change_twh",	"biofuel_consumption",	"biofuel_elec_per_capita",	"biofuel_cons_per_capita",	"carbon_intensity_elec",	"fossil_cons_change_pct",	"fossil_share_energy",	"fossil_cons_change_twh",	"fossil_fuel_consumption",	"fossil_energy_per_capita",	"fossil_cons_per_capita",	"fossil_share_elec",	"gas_share_elec",	"gas_cons_change_pct",	"gas_share_energy",	"gas_cons_change_twh",	"gas_consumption",	"gas_elec_per_capita",	"gas_energy_per_capita",	"gas_production",	"gas_prod_per_capita",	"hydro_share_elec",	"hydro_cons_change_pct",	"hydro_share_energy",	"hydro_cons_change_twh",	"hydro_consumption",	"hydro_elec_per_capita",	"hydro_energy_per_capita",	"low_carbon_share_elec",	"low_carbon_electricity",	"low_carbon_elec_per_capita",	"low_carbon_cons_change_pct",	"low_carbon_share_energy",	"low_carbon_cons_change_twh",	"low_carbon_consumption",	"low_carbon_energy_per_capita",	"net_elec_imports",	"net_elec_imports_share_demand",	"nuclear_share_elec",	"nuclear_cons_change_pct",	"nuclear_share_energy",	"nuclear_cons_change_twh",	"nuclear_consumption",	"nuclear_elec_per_capita",	"nuclear_energy_per_capita",	"oil_share_elec",	"oil_cons_change_pct",	"oil_share_energy",	"oil_cons_change_twh",	"oil_consumption",	"oil_elec_per_capita",	"oil_energy_per_capita",	"oil_production",	"oil_prod_per_capita",	"other_renewables_elec_per_capita",	"other_renewables_elec_per_capita_exc_biofuel",	"other_renewables_share_elec",	"other_renewables_share_elec_exc_biofuel",	"other_renewables_cons_change_pct",	"other_renewables_share_energy",	"other_renewables_cons_change_twh",	"other_renewable_consumption",	"other_renewables_energy_per_capita",	"solar_share_elec",	"solar_cons_change_pct",	"solar_share_energy",	"solar_cons_change_twh",	"solar_consumption",	"solar_elec_per_capita",	"solar_energy_per_capita",	"gdp",	"wind_share_elec",	"wind_cons_change_pct",	"wind_share_energy",	"wind_cons_change_twh",	"wind_consumption",	"wind_elec_per_capita",	"wind_energy_per_capita",	"coal_prod_change_pct",	"coal_prod_change_twh",	"gas_prod_change_pct",	"gas_prod_change_twh",	"oil_prod_change_pct",	"oil_prod_change_twh"))

    answer9 = st.selectbox(label="What country or region would you like to view?",
    options=('World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America',
           'Afghanistan',  'Albania', 'Algeria', 'Andorra', 'Angola',
           'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina',
           'Armenia', 'Aruba', 'Asia (excl. China & India)',
           'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
           'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
           'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire Sint Eustatius and Saba',
           'Bosnia and Herzegovina', 'Botswana', 'Brazil',
           'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso',
           'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
           'Central African Republic', 'Chad', 'Chile', 'China',
           'Christmas Island', 'Colombia', 'Comoros', 'Congo', 'Cook Islands',
           'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao',
           'Cyprus', 'Czechia', 'Democratic Republic of Congo', 'Denmark',
           'Djibouti', 'Dominica', 'Dominican Republic', 'EU-27', 'Ecuador',
           'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
           'Eswatini', 'Ethiopia', 'Europe (excl. EU-27)',
           'Europe (excl. EU-28)', 'European Union (27)',
           'European Union (28)', 'Faeroe Islands', 'Fiji', 'Finland',
           'France', 'French Equatorial Africa', 'French Guiana',
           'French Polynesia', 'French West Africa', 'Gabon', 'Gambia',
           'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada',
           'Guadeloupe', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
           'Haiti', 'High-income countries', 'Honduras', 'Hong Kong',
           'Hungary', 'Iceland', 'India', 'Indonesia',
           'International transport', 'Iran', 'Iraq', 'Ireland', 'Israel',
           'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
           'Kiribati', 'Kosovo', 'Kuwait', 'Kuwaiti Oil Fires', 'Kyrgyzstan',
           'Laos', 'Latvia', 'Lebanon', 'Leeward Islands', 'Lesotho',
           'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
           'Low-income countries', 'Lower-middle-income countries',
           'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia',
           'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
           'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
           'Micronesia (country)', 'Moldova', 'Mongolia', 'Montenegro',
           'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
           'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
           'Nicaragua', 'Niger', 'Nigeria', 'Niue',
           'North America (excl. USA)', 'North Korea', 'North Macedonia',
           'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine',
           'Panama', 'Panama Canal Zone', 'Papua New Guinea', 'Paraguay',
           'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
           'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda',
           'Ryukyu Islands', 'Saint Helena', 'Saint Kitts and Nevis',
           'Saint Lucia', 'Saint Pierre and Miquelon',
           'Saint Vincent and the Grenadines', 'Samoa',
           'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
           'Seychelles', 'Sierra Leone', 'Singapore',
           'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia',
           'Solomon Islands', 'Somalia', 'South Africa',
           'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
           'St. Kitts-Nevis-Anguilla', 'Sudan', 'Suriname', 'Sweden',
           'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
           'Thailand', 'Timor', 'Togo', 'Tonga', 'Trinidad and Tobago',
           'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands',
           'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
           'United Kingdom', 'United States', 'Upper-middle-income countries',
           'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam',
           'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe'))


    answer10 = st.selectbox(label="View from which year?",
    options=(1970, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908, 1907, 1906, 1905, 1904, 1903, 1902, 1901, 1900, 1899, 1898, 1897, 1896, 1895, 1894, 1893, 1892, 1891, 1890, 1889, 1888, 1887, 1886, 1885, 1884, 1883, 1882, 1881, 1880, 1879, 1878, 1877, 1876, 1875, 1874, 1873, 1872, 1871, 1870, 1869, 1868, 1867, 1866, 1865, 1864, 1863, 1862, 1861, 1860, 1859, 1858, 1857, 1856, 1855, 1854, 1853, 1852, 1851, 1850, 1849, 1848, 1847, 1846, 1845, 1844, 1843, 1842, 1841, 1840, 1839, 1838, 1837, 1836, 1835, 1834, 1833, 1832, 1831, 1830, 1829, 1828, 1827, 1826, 1825, 1824, 1823, 1822, 1821, 1820, 1819, 1818, 1817, 1816, 1815, 1814, 1813, 1812, 1811, 1810, 1809, 1808, 1807, 1806, 1805, 1804, 1803, 1802, 1801, 1800, 1799, 1798, 1797, 1796, 1795, 1794, 1793, 1792, 1791, 1790, 1789, 1788, 1787, 1786, 1785, 1784, 1783, 1782, 1781, 1780, 1779, 1778, 1777, 1776, 1775, 1774, 1773, 1772, 1771, 1770, 1769, 1768, 1767, 1766, 1765, 1764, 1763, 1762, 1761, 1760, 1759, 1758, 1757, 1756, 1755, 1754, 1753, 1752, 1751, 1750))



    def country_bar_graph2(input_year, input_country, input_var):
        graph_data4=df_eng[df_eng.year > input_year]
        graph_data4=graph_data4[graph_data4.country == input_country]
        fig4 = px.bar(graph_data4, x='year', y=input_var, color=input_var, title=input_country)
        fig4.update_layout(title_text=input_country, title_x=0.5, title_y=0.9)
        st.plotly_chart(fig4)

    country_bar_graph2(answer10, answer9, answer8)
    st.caption("While usage increases in renewables far outpace fossil fuels, only approximately 14% of global energy consumption is renewable. Scientists say we need to move this number to 60% or higher. We have the technical capacity to do this, but it does not look like we have the politcal will.")

elif st.checkbox("Explore Breakdowns of Aggregate Energy Use by Year"):
    answer11 = st.selectbox(label="What country or region would you like to view?",
    options=('World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America',
           'Afghanistan',  'Albania', 'Algeria', 'Andorra', 'Angola',
           'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina',
           'Armenia', 'Aruba', 'Asia (excl. China & India)',
           'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
           'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
           'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire Sint Eustatius and Saba',
           'Bosnia and Herzegovina', 'Botswana', 'Brazil',
           'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso',
           'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
           'Central African Republic', 'Chad', 'Chile', 'China',
           'Christmas Island', 'Colombia', 'Comoros', 'Congo', 'Cook Islands',
           'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao',
           'Cyprus', 'Czechia', 'Democratic Republic of Congo', 'Denmark',
           'Djibouti', 'Dominica', 'Dominican Republic', 'EU-27', 'Ecuador',
           'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
           'Eswatini', 'Ethiopia', 'Europe (excl. EU-27)',
           'Europe (excl. EU-28)', 'European Union (27)',
           'European Union (28)', 'Faeroe Islands', 'Fiji', 'Finland',
           'France', 'French Equatorial Africa', 'French Guiana',
           'French Polynesia', 'French West Africa', 'Gabon', 'Gambia',
           'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada',
           'Guadeloupe', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
           'Haiti', 'High-income countries', 'Honduras', 'Hong Kong',
           'Hungary', 'Iceland', 'India', 'Indonesia',
           'International transport', 'Iran', 'Iraq', 'Ireland', 'Israel',
           'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
           'Kiribati', 'Kosovo', 'Kuwait', 'Kuwaiti Oil Fires', 'Kyrgyzstan',
           'Laos', 'Latvia', 'Lebanon', 'Leeward Islands', 'Lesotho',
           'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
           'Low-income countries', 'Lower-middle-income countries',
           'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia',
           'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
           'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
           'Micronesia (country)', 'Moldova', 'Mongolia', 'Montenegro',
           'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
           'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
           'Nicaragua', 'Niger', 'Nigeria', 'Niue',
           'North America (excl. USA)', 'North Korea', 'North Macedonia',
           'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine',
           'Panama', 'Panama Canal Zone', 'Papua New Guinea', 'Paraguay',
           'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
           'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda',
           'Ryukyu Islands', 'Saint Helena', 'Saint Kitts and Nevis',
           'Saint Lucia', 'Saint Pierre and Miquelon',
           'Saint Vincent and the Grenadines', 'Samoa',
           'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
           'Seychelles', 'Sierra Leone', 'Singapore',
           'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia',
           'Solomon Islands', 'Somalia', 'South Africa',
           'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
           'St. Kitts-Nevis-Anguilla', 'Sudan', 'Suriname', 'Sweden',
           'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
           'Thailand', 'Timor', 'Togo', 'Tonga', 'Trinidad and Tobago',
           'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands',
           'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
           'United Kingdom', 'United States', 'Upper-middle-income countries',
           'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam',
           'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe'))


    answer12 = st.selectbox(label="View from which year?",
    options=(1970, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908, 1907, 1906, 1905, 1904, 1903, 1902, 1901, 1900, 1899, 1898, 1897, 1896, 1895, 1894, 1893, 1892, 1891, 1890, 1889, 1888, 1887, 1886, 1885, 1884, 1883, 1882, 1881, 1880, 1879, 1878, 1877, 1876, 1875, 1874, 1873, 1872, 1871, 1870, 1869, 1868, 1867, 1866, 1865, 1864, 1863, 1862, 1861, 1860, 1859, 1858, 1857, 1856, 1855, 1854, 1853, 1852, 1851, 1850, 1849, 1848, 1847, 1846, 1845, 1844, 1843, 1842, 1841, 1840, 1839, 1838, 1837, 1836, 1835, 1834, 1833, 1832, 1831, 1830, 1829, 1828, 1827, 1826, 1825, 1824, 1823, 1822, 1821, 1820, 1819, 1818, 1817, 1816, 1815, 1814, 1813, 1812, 1811, 1810, 1809, 1808, 1807, 1806, 1805, 1804, 1803, 1802, 1801, 1800, 1799, 1798, 1797, 1796, 1795, 1794, 1793, 1792, 1791, 1790, 1789, 1788, 1787, 1786, 1785, 1784, 1783, 1782, 1781, 1780, 1779, 1778, 1777, 1776, 1775, 1774, 1773, 1772, 1771, 1770, 1769, 1768, 1767, 1766, 1765, 1764, 1763, 1762, 1761, 1760, 1759, 1758, 1757, 1756, 1755, 1754, 1753, 1752, 1751, 1750))

    def Aggregate_bar_graph2(input_year, input_country):
        graph_data5=df_eng[df_eng.year > input_year]
        graph_data5=graph_data5[graph_data5.country == input_country]
        fig5 = px.bar(graph_data5, x='year', y=['oil_consumption', 'coal_consumption', 'gas_consumption', 'hydro_consumption', 'nuclear_consumption',
        'solar_consumption', 'wind_consumption', 'other_renewable_consumption', 'biofuel_consumption'],  title=input_country)
        fig5.update_layout(title_text=input_country, title_x=0.5, title_y=0.9)
        st.plotly_chart(fig5)

    Aggregate_bar_graph2(answer12, answer11)
    st.caption("According to the Center of American Progress, there are currently 139 climate change deniers across the two branches of Congress. Collectively, these individuals have received 61 million dollars in lifetime contributions from the fossil fuel industry (2021). The general public also remains divided. While 64 percent of Americans believe Congress should make environmental protection a top priority, only 39 percent of Republicans believe the federal government is doing too little to address climate change. This number is in stark contrast to the 90 percent of Democrats who believe the federal government's climate action has been inadequate (PEW, 2019, 2021).")

elif st.checkbox("Explore Breakdowns of Per Capita Energy Use by Year"):
    answer13 = st.selectbox(label="What country or region would you like to view?",
    options=('World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America',
           'Afghanistan',  'Albania', 'Algeria', 'Andorra', 'Angola',
           'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina',
           'Armenia', 'Aruba', 'Asia (excl. China & India)',
           'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
           'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
           'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire Sint Eustatius and Saba',
           'Bosnia and Herzegovina', 'Botswana', 'Brazil',
           'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso',
           'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
           'Central African Republic', 'Chad', 'Chile', 'China',
           'Christmas Island', 'Colombia', 'Comoros', 'Congo', 'Cook Islands',
           'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao',
           'Cyprus', 'Czechia', 'Democratic Republic of Congo', 'Denmark',
           'Djibouti', 'Dominica', 'Dominican Republic', 'EU-27', 'Ecuador',
           'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
           'Eswatini', 'Ethiopia', 'Europe (excl. EU-27)',
           'Europe (excl. EU-28)', 'European Union (27)',
           'European Union (28)', 'Faeroe Islands', 'Fiji', 'Finland',
           'France', 'French Equatorial Africa', 'French Guiana',
           'French Polynesia', 'French West Africa', 'Gabon', 'Gambia',
           'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada',
           'Guadeloupe', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
           'Haiti', 'High-income countries', 'Honduras', 'Hong Kong',
           'Hungary', 'Iceland', 'India', 'Indonesia',
           'International transport', 'Iran', 'Iraq', 'Ireland', 'Israel',
           'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
           'Kiribati', 'Kosovo', 'Kuwait', 'Kuwaiti Oil Fires', 'Kyrgyzstan',
           'Laos', 'Latvia', 'Lebanon', 'Leeward Islands', 'Lesotho',
           'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
           'Low-income countries', 'Lower-middle-income countries',
           'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia',
           'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
           'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
           'Micronesia (country)', 'Moldova', 'Mongolia', 'Montenegro',
           'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
           'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
           'Nicaragua', 'Niger', 'Nigeria', 'Niue',
           'North America (excl. USA)', 'North Korea', 'North Macedonia',
           'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine',
           'Panama', 'Panama Canal Zone', 'Papua New Guinea', 'Paraguay',
           'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
           'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda',
           'Ryukyu Islands', 'Saint Helena', 'Saint Kitts and Nevis',
           'Saint Lucia', 'Saint Pierre and Miquelon',
           'Saint Vincent and the Grenadines', 'Samoa',
           'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
           'Seychelles', 'Sierra Leone', 'Singapore',
           'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia',
           'Solomon Islands', 'Somalia', 'South Africa',
           'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
           'St. Kitts-Nevis-Anguilla', 'Sudan', 'Suriname', 'Sweden',
           'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
           'Thailand', 'Timor', 'Togo', 'Tonga', 'Trinidad and Tobago',
           'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands',
           'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
           'United Kingdom', 'United States', 'Upper-middle-income countries',
           'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam',
           'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe'))


    answer14 = st.selectbox(label="View from which year?",
    options=(1970, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908, 1907, 1906, 1905, 1904, 1903, 1902, 1901, 1900, 1899, 1898, 1897, 1896, 1895, 1894, 1893, 1892, 1891, 1890, 1889, 1888, 1887, 1886, 1885, 1884, 1883, 1882, 1881, 1880, 1879, 1878, 1877, 1876, 1875, 1874, 1873, 1872, 1871, 1870, 1869, 1868, 1867, 1866, 1865, 1864, 1863, 1862, 1861, 1860, 1859, 1858, 1857, 1856, 1855, 1854, 1853, 1852, 1851, 1850, 1849, 1848, 1847, 1846, 1845, 1844, 1843, 1842, 1841, 1840, 1839, 1838, 1837, 1836, 1835, 1834, 1833, 1832, 1831, 1830, 1829, 1828, 1827, 1826, 1825, 1824, 1823, 1822, 1821, 1820, 1819, 1818, 1817, 1816, 1815, 1814, 1813, 1812, 1811, 1810, 1809, 1808, 1807, 1806, 1805, 1804, 1803, 1802, 1801, 1800, 1799, 1798, 1797, 1796, 1795, 1794, 1793, 1792, 1791, 1790, 1789, 1788, 1787, 1786, 1785, 1784, 1783, 1782, 1781, 1780, 1779, 1778, 1777, 1776, 1775, 1774, 1773, 1772, 1771, 1770, 1769, 1768, 1767, 1766, 1765, 1764, 1763, 1762, 1761, 1760, 1759, 1758, 1757, 1756, 1755, 1754, 1753, 1752, 1751, 1750))

    def per_capita_bar_graph2(input_year, input_country):
        graph_data6=df_eng[df_eng.year > input_year]
        graph_data6=graph_data6[graph_data6.country == input_country]
        fig6 = px.bar(graph_data6, x='year', y= ['coal_cons_per_capita', 'gas_energy_per_capita',
        'hydro_energy_per_capita', 'nuclear_energy_per_capita', 'oil_energy_per_capita', 'solar_energy_per_capita',
        'wind_energy_per_capita','other_renewables_energy_per_capita', 'biofuel_cons_per_capita'],  title=input_country)
        fig6.update_layout(title_text=input_country, title_x=0.5, title_y=0.9)
        st.plotly_chart(fig6)

    per_capita_bar_graph2(answer14, answer13)

elif st.checkbox("Explore Breakdowns of Share Energy Use by Year"):
    answer15 = st.selectbox(label="What country or region would you like to view?",
    options=('World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America',
           'Afghanistan',  'Albania', 'Algeria', 'Andorra', 'Angola',
           'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina',
           'Armenia', 'Aruba', 'Asia (excl. China & India)',
           'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
           'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
           'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire Sint Eustatius and Saba',
           'Bosnia and Herzegovina', 'Botswana', 'Brazil',
           'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso',
           'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
           'Central African Republic', 'Chad', 'Chile', 'China',
           'Christmas Island', 'Colombia', 'Comoros', 'Congo', 'Cook Islands',
           'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao',
           'Cyprus', 'Czechia', 'Democratic Republic of Congo', 'Denmark',
           'Djibouti', 'Dominica', 'Dominican Republic', 'EU-27', 'Ecuador',
           'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
           'Eswatini', 'Ethiopia', 'Europe (excl. EU-27)',
           'Europe (excl. EU-28)', 'European Union (27)',
           'European Union (28)', 'Faeroe Islands', 'Fiji', 'Finland',
           'France', 'French Equatorial Africa', 'French Guiana',
           'French Polynesia', 'French West Africa', 'Gabon', 'Gambia',
           'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada',
           'Guadeloupe', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
           'Haiti', 'High-income countries', 'Honduras', 'Hong Kong',
           'Hungary', 'Iceland', 'India', 'Indonesia',
           'International transport', 'Iran', 'Iraq', 'Ireland', 'Israel',
           'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
           'Kiribati', 'Kosovo', 'Kuwait', 'Kuwaiti Oil Fires', 'Kyrgyzstan',
           'Laos', 'Latvia', 'Lebanon', 'Leeward Islands', 'Lesotho',
           'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
           'Low-income countries', 'Lower-middle-income countries',
           'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia',
           'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
           'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
           'Micronesia (country)', 'Moldova', 'Mongolia', 'Montenegro',
           'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
           'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
           'Nicaragua', 'Niger', 'Nigeria', 'Niue',
           'North America (excl. USA)', 'North Korea', 'North Macedonia',
           'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine',
           'Panama', 'Panama Canal Zone', 'Papua New Guinea', 'Paraguay',
           'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
           'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda',
           'Ryukyu Islands', 'Saint Helena', 'Saint Kitts and Nevis',
           'Saint Lucia', 'Saint Pierre and Miquelon',
           'Saint Vincent and the Grenadines', 'Samoa',
           'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
           'Seychelles', 'Sierra Leone', 'Singapore',
           'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia',
           'Solomon Islands', 'Somalia', 'South Africa',
           'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
           'St. Kitts-Nevis-Anguilla', 'Sudan', 'Suriname', 'Sweden',
           'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
           'Thailand', 'Timor', 'Togo', 'Tonga', 'Trinidad and Tobago',
           'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands',
           'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
           'United Kingdom', 'United States', 'Upper-middle-income countries',
           'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam',
           'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe'))


    answer16 = st.selectbox(label="View from which year?",
    options=(1970, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908, 1907, 1906, 1905, 1904, 1903, 1902, 1901, 1900, 1899, 1898, 1897, 1896, 1895, 1894, 1893, 1892, 1891, 1890, 1889, 1888, 1887, 1886, 1885, 1884, 1883, 1882, 1881, 1880, 1879, 1878, 1877, 1876, 1875, 1874, 1873, 1872, 1871, 1870, 1869, 1868, 1867, 1866, 1865, 1864, 1863, 1862, 1861, 1860, 1859, 1858, 1857, 1856, 1855, 1854, 1853, 1852, 1851, 1850, 1849, 1848, 1847, 1846, 1845, 1844, 1843, 1842, 1841, 1840, 1839, 1838, 1837, 1836, 1835, 1834, 1833, 1832, 1831, 1830, 1829, 1828, 1827, 1826, 1825, 1824, 1823, 1822, 1821, 1820, 1819, 1818, 1817, 1816, 1815, 1814, 1813, 1812, 1811, 1810, 1809, 1808, 1807, 1806, 1805, 1804, 1803, 1802, 1801, 1800, 1799, 1798, 1797, 1796, 1795, 1794, 1793, 1792, 1791, 1790, 1789, 1788, 1787, 1786, 1785, 1784, 1783, 1782, 1781, 1780, 1779, 1778, 1777, 1776, 1775, 1774, 1773, 1772, 1771, 1770, 1769, 1768, 1767, 1766, 1765, 1764, 1763, 1762, 1761, 1760, 1759, 1758, 1757, 1756, 1755, 1754, 1753, 1752, 1751, 1750))

    def share_bar_graph(input_year, input_country):
        graph_data7=df_eng[df_eng.year > input_year]
        graph_data7=graph_data7[graph_data7.country == input_country]
        fig7 = px.bar(graph_data7, x='year', y= ['coal_share_energy', 'gas_share_energy', 'oil_share_energy', 'hydro_share_energy', 'nuclear_share_energy', 'solar_share_energy',
        'wind_share_energy', 'other_renewables_share_energy', 'biofuel_share_energy'],  title=input_country)
        fig7.update_layout(title_text=input_country, title_x=0.5, title_y=0.9)
        st.plotly_chart(fig7)

    share_bar_graph(answer16, answer15)
    st.caption("Despite all the hype wind and solar combined to make up less than 4% of total energy consumption in 2020. The U.S has an abundance of potential for wind and solar but there are direct for many politicians against this transistion. For example, Democratic Senator Joe Manchin of West Virginia is a determining vote given the Democrats narrow majority in the Senate. The primary industry of West Virginia is coal, and Manchin collected 400 thousand dollars in fossil fuel donations in recent months. On top of that, he made approximately $500 thousand last year due to his ownership of a coal brokerage fund he founded (CNN, 2021). It is clear that Manchin has a direct financial incentive to keep the fossil fuel industry prosperous. Earlier this year, he had key climate provisions removed from the infrastructure bill, including a 150 billion dollar clean energy incentive.")


elif st.checkbox("Explore breakdown of Energy Trends over the Years"):
    answer17 = st.selectbox(label="What variable would you like to view?",
    options=("coal_prod_change_pct", "gas_prod_change_pct", "oil_prod_change_pct", "energy_cons_change_pct",
    "coal_cons_change_pct", "fossil_cons_change_pct", "gas_cons_change_pct", "hydro_cons_change_pct", "low_carbon_cons_change_pct",
    "nuclear_cons_change_pct", "renewables_cons_change_pct", "solar_cons_change_pct", 'wind_cons_change_pct'))

    answer18 = st.selectbox(label="What country or region would you like to view?",
    options=('World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America',
           'Afghanistan',  'Albania', 'Algeria', 'Andorra', 'Angola',
           'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina',
           'Armenia', 'Aruba', 'Asia (excl. China & India)',
           'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
           'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
           'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire Sint Eustatius and Saba',
           'Bosnia and Herzegovina', 'Botswana', 'Brazil',
           'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso',
           'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
           'Central African Republic', 'Chad', 'Chile', 'China',
           'Christmas Island', 'Colombia', 'Comoros', 'Congo', 'Cook Islands',
           'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao',
           'Cyprus', 'Czechia', 'Democratic Republic of Congo', 'Denmark',
           'Djibouti', 'Dominica', 'Dominican Republic', 'EU-27', 'Ecuador',
           'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
           'Eswatini', 'Ethiopia', 'Europe (excl. EU-27)',
           'Europe (excl. EU-28)', 'European Union (27)',
           'European Union (28)', 'Faeroe Islands', 'Fiji', 'Finland',
           'France', 'French Equatorial Africa', 'French Guiana',
           'French Polynesia', 'French West Africa', 'Gabon', 'Gambia',
           'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada',
           'Guadeloupe', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
           'Haiti', 'High-income countries', 'Honduras', 'Hong Kong',
           'Hungary', 'Iceland', 'India', 'Indonesia',
           'International transport', 'Iran', 'Iraq', 'Ireland', 'Israel',
           'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
           'Kiribati', 'Kosovo', 'Kuwait', 'Kuwaiti Oil Fires', 'Kyrgyzstan',
           'Laos', 'Latvia', 'Lebanon', 'Leeward Islands', 'Lesotho',
           'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
           'Low-income countries', 'Lower-middle-income countries',
           'Luxembourg', 'Macao', 'Madagascar', 'Malawi', 'Malaysia',
           'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
           'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
           'Micronesia (country)', 'Moldova', 'Mongolia', 'Montenegro',
           'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
           'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
           'Nicaragua', 'Niger', 'Nigeria', 'Niue',
           'North America (excl. USA)', 'North Korea', 'North Macedonia',
           'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine',
           'Panama', 'Panama Canal Zone', 'Papua New Guinea', 'Paraguay',
           'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
           'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda',
           'Ryukyu Islands', 'Saint Helena', 'Saint Kitts and Nevis',
           'Saint Lucia', 'Saint Pierre and Miquelon',
           'Saint Vincent and the Grenadines', 'Samoa',
           'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
           'Seychelles', 'Sierra Leone', 'Singapore',
           'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia',
           'Solomon Islands', 'Somalia', 'South Africa',
           'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
           'St. Kitts-Nevis-Anguilla', 'Sudan', 'Suriname', 'Sweden',
           'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
           'Thailand', 'Timor', 'Togo', 'Tonga', 'Trinidad and Tobago',
           'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands',
           'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
           'United Kingdom', 'United States', 'Upper-middle-income countries',
           'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam',
           'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe'))

    answer19 = st.selectbox(label="View from which year?",
    options=(1970, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1922, 1921, 1920, 1919, 1918, 1917, 1916, 1915, 1914, 1913, 1912, 1911, 1910, 1909, 1908, 1907, 1906, 1905, 1904, 1903, 1902, 1901, 1900, 1899, 1898, 1897, 1896, 1895, 1894, 1893, 1892, 1891, 1890, 1889, 1888, 1887, 1886, 1885, 1884, 1883, 1882, 1881, 1880, 1879, 1878, 1877, 1876, 1875, 1874, 1873, 1872, 1871, 1870, 1869, 1868, 1867, 1866, 1865, 1864, 1863, 1862, 1861, 1860, 1859, 1858, 1857, 1856, 1855, 1854, 1853, 1852, 1851, 1850, 1849, 1848, 1847, 1846, 1845, 1844, 1843, 1842, 1841, 1840, 1839, 1838, 1837, 1836, 1835, 1834, 1833, 1832, 1831, 1830, 1829, 1828, 1827, 1826, 1825, 1824, 1823, 1822, 1821, 1820, 1819, 1818, 1817, 1816, 1815, 1814, 1813, 1812, 1811, 1810, 1809, 1808, 1807, 1806, 1805, 1804, 1803, 1802, 1801, 1800, 1799, 1798, 1797, 1796, 1795, 1794, 1793, 1792, 1791, 1790, 1789, 1788, 1787, 1786, 1785, 1784, 1783, 1782, 1781, 1780, 1779, 1778, 1777, 1776, 1775, 1774, 1773, 1772, 1771, 1770, 1769, 1768, 1767, 1766, 1765, 1764, 1763, 1762, 1761, 1760, 1759, 1758, 1757, 1756, 1755, 1754, 1753, 1752, 1751, 1750))

    def line_graph2(input_year, input_country, input_var):
        graph_data8=df_eng[df_eng.year > input_year]
        graph_data8=graph_data8[graph_data8.country == input_country]
        fig8 = px.line(graph_data8, x='year', y=input_var,  title=input_country)
        fig8.update_layout(title_text=input_country, title_x=0.5, title_y=0.9)
        st.plotly_chart(fig8)

    line_graph2(answer19, answer18, answer17)
    st.caption("It is misleading to put too much stock in 2020 changes, given the exogenous shock covid provided in the energy markets.")

"""
##### Data Documentation
"""

if st.checkbox("Carbon Emmissions Codebook"):
    st.table(df_co2_cb)

if st.checkbox("Energy Codebook"):
    st.table(df_eng_cb)
