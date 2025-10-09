import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

#Create a path for all players file
file_path = Path(__file__).parent / "all_players.csv"

#Create dataframe for manipulation
df = pd.read_csv(file_path, encoding='ISO-8859-1')

