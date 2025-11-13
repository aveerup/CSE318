import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

df = df.drop(columns=["local_search_iterations"])

df = df.rename(columns={
    "file_no": "File No",
    "randomized_cut_weight": "Randomized",
    "greedy_cut_weight": "Greedy",
    "grasp_cut_weight": "GRASP",
    "local_search_avg_cut_weight": "Local Search (avg)",
    "semi_greedy_cut_weight": "Semi-Greedy"
})

df_melted = pd.melt(df, id_vars=["File No"], 
                    value_vars=["Randomized", "Greedy", "GRASP", "Local Search (avg)", "Semi-Greedy"],
                    var_name="Algorithm", value_name="Cut Weight")

plt.figure(figsize=(12, 6))
sns.barplot(x="File No", y="Cut Weight", hue="Algorithm", data=df_melted)

plt.title("Comparison of Cut Weights per File")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("cut_weight_plot.png")  

