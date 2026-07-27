import pandas as pd;


df=pd.read_csv(r"data\population.csv",skiprows=1)


df=df.melt(id_vars=["ladcode23","laname23","country","sex","age"],value_vars=["population_2011","population_2012","population_2013","population_2014","population_2015","population_2016","population_2017","population_2018",
"population_2019","population_2020","population_2021","population_2022","population_2023","population_2024"
],value_name="population")


#print(df.head(10))


df.to_csv(r"data/cleaned_population.csv",index=False)

