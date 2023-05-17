# OpenAI API Example
# Summary: Make a call to the OpenAI API using a prompt and get a response

# Input: Prompt entered by user, max length of 256 characters to avoid excessive resource usage  

# Output: Response from the OpenAI API based on the input prompt

# IMPORTS  
import os  
import openai

# VARIABLES
openai.api_key = os.getenv("OPENAI_API_KEY") #check at the bottom how to use this
engine = "text-davinci-002"
max_tokens = 100  
temperature = 0.3  

# FUNCTIONS
def query_openai(prompt, engine, max_tokens, temperature): 
    response = openai.Completion.create(engine=engine,  
                                       prompt=prompt,     
                                       max_tokens=max_tokens,  
                                       temperature=temperature)
    return response.choices[0].text  

# COMPLETE LOGIC
# prompt = input("what's your question? (max length 256 characters): ")  
prompt = "How do I write code that is ethical and responsible? Provide a top 10 list, use no more than 1000 characters in your answer"
response = query_openai(prompt, engine, max_tokens, temperature)
print(response)

# REVIEW 
# Analyze system and prompts  for biases. Ensure safety.

# CODE OF ETHICS
# Call OpenAI API. Discuss AI ethics.

# ENVIRONMENTAL VARIABLES 
# 1. create a ".env" file
# 2. Add the following: OPENAI_API_KEY=sk-KkYczyd3SSEKX49IW0i50tlGgh1Nbv6JiQ6z7WJ9V3SQM
