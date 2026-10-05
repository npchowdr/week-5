import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

# update/add code below ...
def survival_demographics():
  df['Age_group'] = pd.cut(df['Age'], bins=[0, 12, 19, 59, 120], labels=['Child', 'Teen', 'Adult', 'Senior'])
  grouped_df = df.groupby(["Pclass", "Sex", "Age_group"], observed=False).agg(
    n_passengers=("PassengerId", "count"),
    n_survivors=("Survived", "sum"),
    survival_rate=("Survived", "mean")
  ).reset_index().sort_values(["Pclass", "Sex", "Age_group"])
  return grouped_df

#plot did first class passengers have a higher survival rate than second and third class passengers?
def visualize_demographic():
  grouped_df = survival_demographics()

  #regroup the data to be by class and survival rate
  grouped_df = grouped_df.groupby(["Pclass"]).agg(
    n_passengers=("n_passengers", "sum"),
    n_survivors=("n_survivors", "sum"),
    survival_rate=("survival_rate", "mean")
  ).reset_index().sort_values(["Pclass"])

  fig = px.bar(grouped_df, x="Pclass", y="survival_rate",
               labels={"Pclass": "Passenger Class", "survival_rate": "Survival Rate"},
               title="Survival Rate by Passenger Class")
  return fig

def family_groups():
  df['family_size'] = df['SibSp'] + df['Parch'] + 1
  grouped_df = df.groupby(["Pclass", "family_size"], observed=False).agg(
    n_passengers=("PassengerId", "count"),
    avg_fare=("Fare", "mean"),
    min_fare=("Fare", "min"),
    max_fare=("Fare", "max")
  ).reset_index().sort_values(["Pclass", "family_size"])
  return grouped_df

#plot the distribution of family sizes across different passenger classes?
def visualize_families():
  grouped_df = family_groups()

  fig = px.bar(grouped_df, x="family_size", y="n_passengers", color="Pclass",
               labels={"family_size": "Family Size", "n_passengers": "Number of Passengers", "Pclass": "Passenger Class"},
               title="Number of Passengers by Family Size and Class")
  return fig