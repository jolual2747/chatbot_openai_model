import pandas as pd

def preprocess_and_save(file, path):
    """Preprocess .csv file and save it in the format for OpenAI fine tuning."""

    df = pd.read_csv(file, delimiter='|')
    df["question"] = df["question"].apply(lambda x: x.replace('"question": ', ''))
    df["recommendation"] = df["recommendation"].apply(lambda x: str(x).replace('"recommendation": ', ''))
    df.drop(columns=['title', 'url', 'answer'], inplace=True)
    df.rename(columns={'question':'prompt', 'recommendation':'completion'}, inplace=True)
    # save processed dataframe as csv
    df.to_csv(path, index=False)