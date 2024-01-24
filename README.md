# LLM_Text2SQL
performance evaluation of LLM models on Text to SQL

## Below are the various LLM models tested on the SPIDER Dataset on the Text to SQL problem
### Model Name - Parameter size
1. Mistral - 7B
2. LLaMA 2 - 7B
3. WizardLM - 7B
4. Flan-T5 - 11B
5. PaLM    - 540B

## HOW TO RUN THE LLM
All the open-source models were run locally using the module [llama-cpp-python](https://github.com/abetlen/llama-cpp-python). The GGUF files for the open-source models were downloaded from HuggingFace Repositories. For the PaLM model, the PaLM API was used to send requests and receive the results of the query.

Once the gguf files are downloaded, place them in a directory named models.
The test set used for this is the dev_set from SPIDER dataset. The test set is in the location : "spider/dev.json. The spider directory must also contain the database to use when we want to provide the schema for the DB along with the user query. 

For the PaLM testing, run the following command
- python main_Palm.py --test "test_file " --schema 1

 The --schema 1 queries the database manually for the schema of the database and appends it to the model prompt as additional information. Set it to 0 to not include this information

For the other gguf files, the python file internally uses the llama-cpp-python to run the inference locally.
- python main.py --model_name "" --test "" --schema ""

Create a folder "results" to store results of the inference. The result file is of csv format which contains
- The question queried
- Gold query
- Predicted query

The file name will be "model_name/with_schema" if schema bit is 1. Otherwise it will be "model_name/without_schema"

Spider dataset provides an evaluator to test the accuracy of the predictions. To run the Python program, use the following command
- python3 evaluators/evaluation.py --gold "Gold_file --pred "Pred_file" --etype all

The Gold_file must contain only the Gold queries where each query is separated by a newline
The pred_file must contain only the predicted queries where each query is separated by a newline

## Results on Zero-shot performance of models
![exact_without](https://github.com/Saivignesh-05/LLM_Text2SQL/assets/61779051/c6b9b068-b9e4-4bf5-bc97-50852f05fd22)
![exact_with](https://github.com/Saivignesh-05/LLM_Text2SQL/assets/61779051/94f0f9c5-fbc8-4ef9-9cd1-9139352ad5ea)
![exec_without](https://github.com/Saivignesh-05/LLM_Text2SQL/assets/61779051/bb4fc29c-1ae0-46da-bdf2-2c693046dea6)
![exec_with](https://github.com/Saivignesh-05/LLM_Text2SQL/assets/61779051/21975b51-4d47-4793-88a0-d6dd2380e3f8)

![component_without](https://github.com/Saivignesh-05/LLM_Text2SQL/assets/61779051/c2014ea8-aba4-4389-86c3-667bc26ff9d3)
![component_with](https://github.com/Saivignesh-05/LLM_Text2SQL/assets/61779051/ca0c9a43-6e5c-4894-a0a8-fc62fa4ca969)

![sim_without](https://github.com/Saivignesh-05/LLM_Text2SQL/assets/61779051/484852e5-367a-4ed4-b341-9d8dcc62f3bc)
![sim_with](https://github.com/Saivignesh-05/LLM_Text2SQL/assets/61779051/fa1f9572-00a1-48c3-83a1-2fa10df3ba04)


## CONSISTENCY METRIC
### MISTRAL 7B
![consistency_mistral](https://github.com/Saivignesh-05/LLM_Text2SQL/assets/61779051/b8e77a2e-50d8-425b-bb8c-aacdc6c381f5)
### LLaMA 2 7B
![consistency_PaLM](https://github.com/Saivignesh-05/LLM_Text2SQL/assets/61779051/5c336ca2-6e28-48db-9704-5a7466e18627)



## Description of each model
### 1. Mistral LLM
HIGHLIGHTS
- Uses Grouped-query attention
    * Speeds up inference of the model
    * Reduces memory req during decoding
- Uses Sliding window attention
    * Handles longer sequences with a reduced computation cost

CAPABILITIES
- Code generation
- Reasoning
- Mathematics

LIMITATIONS
- Prone to hallucination 
- Prone to prompt injections
- Low knowledge store due to low parameter size

### 2. WizardLM LLM
HIGHLIGHTS
- It is a fine-tuned LLaMA LLM using the evol-instruct method
  - trained with fully evolved instructions
- Optimized to perform highly complex instructions
- Outperforms Vicuna and Alpaca

CAPABILITIES
- instruction-following LLMs
- Code Generation

LIMITATIONS
- Prone to hallucination
- Low knowledge store due to low parameter size

### 2. LLaMA 2 LLM by META

HIGHLIGHTS
- Llama 2 is pre-trained using publicly available online data (2 trillion "tokens").
- Iteratively refined using (RLHF), which includes rejection sampling and proximal policy optimization (PPO)
- Only open-source model on par with ChatGPT, Anthropic, and PaLM on all general NLP tasks

CAPABILITIES
- Applied to many different use cases for example
- Code Generation
- Sentence completion
- Summarization
- Sentiment analysis

LIMITATIONS
- Prone to hallucination
- Inappropriate content (if not used responsibly)
- Potential for bias

### Flan-T5 LLM

Highlights
- Enhanced T5: Builds upon the powerful T5 model with further fine-tuning 
- Multi-task learning: Trained on diverse tasks, making it versatile for various NLP applications.
- Five sizes: small, base, large, XL, and XXL for different performance and resource requirements.
- Open-sourced: Accessible through Hugging Face and can be fine-tuned for specific tasks.

CAPABILITIES:
- Text summarization
- Question answering
- Text generation
- Language Translation

LIMITATIONS:
- Potential for bias
- Inappropriate content (if not used responsibly)
- Significant computational resources for training and inference.

### PaLM

HIGHLIGHTS
- Massive parameter size: advanced reasoning and understanding capabilities.
- Multi-task learning: Trained on a diverse set of tasks
- Improved zero-shot and few-shot learning.
- Handles multiple languages with fluency and accuracy.

CAPABILITIES
- Advanced reasoning tasks: Solves complex problems, comprehends riddles 
- Question answering
- Natural language generation: creative text formats like poems, scripts, emails
- Code understanding and generation: Analyzes existing code, generates new code snippets, and helps with code completion.

Limitations:
- Potential for bias: Trained on a massive dataset that may contain inherent biases, reflected in its outputs.
- Ethical considerations: Can generate inappropriate content if not used responsibly.
- Demands significant computational resources for training and inference.



















