import os
from dotenv import load_dotenv
from .preprocess import preprocess_and_save
import openai

def create_file(path:str):
    """Uploads file to OpenAI"""
    return openai.File.create(file=open(path, "rb"), purpose='fine-tune')

def run_fine_tuning(training_file:str, model:str):
    """Creates a job for fine tuning at OpenAI"""
    return openai.FineTuningJob.create(training_file=training_file, model=model)

def train(keys_path):
    """Run training pipeline"""
    load_dotenv(keys_path)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response_file = create_file(path="./datasets/data_prepared.jsonl")
    run_fine_tuning(training_file=response_file["id"], model = 'babbage-002')
    
if __name__ == "__main__":
    preprocess_and_save('./validation_dataset.csv', './datasets/data.csv')
    train('./secrets/keys.env')