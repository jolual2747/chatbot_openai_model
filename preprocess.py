import pandas as pd

df = pd.read_csv('./validation_dataset.csv', delimiter='|')

df["question"] = df["question"].apply(lambda x: x.replace('"question": ', ''))
df["recommendation"] = df["recommendation"].apply(lambda x: str(x).replace('"recommendation": ', ''))
df.drop(columns=['title', 'url', 'answer'], inplace=True)
df.rename(columns={'question':'prompt', 'recommendation':'completion'}, inplace=True)

df.to_csv('./datasets/data.csv', index=False)