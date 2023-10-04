# chatbot_openai_model
Fine tuned chatbot with OpenAI models


For training we need an appropiate format (JSONL) that OpenAI models require for fine tunning. We can convert the data with the following command:

```bash 
openai tools fine_tunes.prepare_data -f data.csv
```