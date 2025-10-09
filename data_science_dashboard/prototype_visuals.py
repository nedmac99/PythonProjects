#notebook_prototype.py (run in a Jupyter cell)

import pandas as pd
import plotly.express as px
from pathlib import Path

#Load CSV
file_path = Path(__file__).parent / "model_results.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

#Display info and first 6 entries
df.info()
print(df.head(6))

# 1) Grouped bar: Accuracy vs F1
# (Plotly supports passing multiple y columns in wide form)

fig1 = px.bar(df, x='Model', y=['Accuracy', 'F1'], barmode='group', title="Accuracy and F1 by Model")
fig1.update_layout(xaxis_tickangle=-45, yaxis_title="Score")
fig1.show()

#Alternative if you prefer to melt first:
'''
df_melt = df.melt(id_vars='Model', value_vars=['Accuracy','F1'], var_name='Metric', value_name='Scores')
fig1 = px.bar(df_melt, x='Model', y='Score', color='Metric', barmode='group')
'''

# 2) Precision vs Recall scatter (size = F1)
fig2 = px.scatter(df, x='Precision', y='Recall', size='F1', hover_name='Model', title="Precision vs Recall (point size ~ F1)")
fig2.show()

# 3) Correlation heatmap for numeric metrics
metrics = ['Accuracy', 'Precision', 'Recall', 'F1', 'AUC', 'Train_Time']
corr = df[metrics].corr()
fig3 = px.imshow(corr, text_auto=True, title="Correlation matrix (metrics)")
fig3.show()