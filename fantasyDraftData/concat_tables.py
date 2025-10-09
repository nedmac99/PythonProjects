import pandas as pd
from pathlib import Path

#Stats come from: https://www.pff.com/fantasy/stats/finishes

# Folder where this script is located
base_folder = Path(__file__).parent
output_file = base_folder / "all_players.csv"

# Get all CSV files except the output CSV
csv_files = [f for f in base_folder.glob("*.csv") if f != output_file]

all_df = []

for csv_file in csv_files:
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    
    # Extract prefix from filename
    prefix = csv_file.stem.split('-')[0].lower()
    
    # Assign POS
    if prefix == "qb":
        df['POS'] = "QB"
    elif prefix == "rb":
        df['POS'] = "RB"
    elif prefix == "wr":
        df['POS'] = "WR"
    elif prefix == "te":
        df['POS'] = "TE"
    else:
        df['POS'] = "Unknown"
    
    all_df.append(df)

# Combine all DataFrames
all_players = pd.concat(all_df, ignore_index=True)

# Move POS column right after Name
cols = all_players.columns.tolist()
if 'POS' in cols and 'Name' in cols:
    cols.remove('POS')
    name_index = cols.index('Name')
    cols.insert(name_index + 1, 'POS')
    all_players = all_players[cols]

# Save combined DataFrame
all_players.to_csv(output_file, index=False)

print("All players saved to all_players.csv")
print(all_players.head(100))
