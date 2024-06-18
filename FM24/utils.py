from typing import Optional
import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

def get_best(ratings ,pos_qtd_dict, age_constraint=None): 
    ratings = ratings.reset_index(drop=True)
    # Define the linear programming problem
    prob = LpProblem(name="Player_Selection", sense=LpMaximize)

    # Define binary variables
    players = range(len(ratings))
    x = LpVariable.dicts("x", (players, list(pos_qtd_dict.keys())), 0, 1, cat="Binary")

    # Objective function
    prob += lpSum(ratings.loc[player, position] * x[player][position] for player in players for position in list(pos_qtd_dict.keys()))

    # Constraints
    for player in players:
        prob += lpSum(x[player][position] for position in list(pos_qtd_dict.keys())) <= 1  # Each player assigned to one position

    for position in list(pos_qtd_dict.keys()):
        prob += lpSum(x[player][position] for player in players) >= 1  # Number of players for each position type

    # Additional constraints for specified numbers of players for each position type
    for position,qtd in pos_qtd_dict.items():
        prob += lpSum(x[player][position] for player in players) <= qtd 

    # Adding age mean constraint
    if age_constraint:
        total_players = sum(pos_qtd_dict.values())
        prob += lpSum(ratings.loc[player, "Age"] * x[player][position] for player in players for position in list(pos_qtd_dict.keys())) / total_players <= age_constraint

    # Total number of players
    prob += lpSum(x[player][position] for player in players for position in list(pos_qtd_dict.keys())) >= sum(pos_qtd_dict.values())

    # Solve the problem
    prob.solve()

    # Print the results
    result = []
    for player in players:
        aux={}
        for position in list(pos_qtd_dict.keys()):
            if value(x[player][position]) == 1:
                aux["name"] = ratings.loc[player, "Name"]
                aux["position"] = position
                aux["score"] = ratings.loc[player, position]
                result.append(aux)
    
    return result, value(prob.objective)

def remove_players(ratings, players):
    return ratings.query("Name not in @players")

def prepare_ratings(ratings, formation):
    return ratings[["Name"] + ["Age"] +list(formation.keys())].fillna(0).reset_index(drop=True)

def treat_transfer_value(df):
    # Remove "£" Symbol
    df["Transfer Value"] = df["Transfer Value"].str.replace("£", "")

    # Split Range Values
    df[["lower_bound", "upper_bound"]] = df["Transfer Value"].str.split(" - ", expand=True)

    # Handle Million (M) Values
    df["lower_bound"] = df["lower_bound"].str.replace("M", "e6")
    df["upper_bound"] = df["upper_bound"].str.replace("M", "e6")

    # Handle Thousand (K) Values
    df["lower_bound"] = df["lower_bound"].str.replace("K", "e3")
    df["upper_bound"] = df["upper_bound"].str.replace("K", "e3")

    # Remove commas and convert to numeric
    df["lower_bound"] = df["lower_bound"].str.replace(",", "")
    df["upper_bound"] = df["upper_bound"].str.replace(",", "")

    df["lower_bound"] = df["lower_bound"].astype(float)
    df["upper_bound"] = df["upper_bound"].astype(float)

    # Convert to Numeric
    df["lower_bound"] = pd.to_numeric(df["lower_bound"])
    df["upper_bound"] = pd.to_numeric(df["upper_bound"])

    # Create a column for mean between upper and lower bounds
    df["mean_value"] = df.apply(lambda row: row["lower_bound"] if pd.isna(row["upper_bound"]) else (row["lower_bound"] + row["upper_bound"]) / 2, axis=1)

    # Display the formatted DataFrame
    return df

