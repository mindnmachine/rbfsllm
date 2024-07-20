'''import openai

# Set your OpenAI API key
openai.api_key = 'sk-proj-t9INIZ4qJSmEO4cBhRUVT3BlbkFJ27VHl3NNERhzaEHPDXuy'

class CustomLLM:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def invoke(self, input_text):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo-0125",  # You can use "gpt-3.5-turbo" or any other available model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": input_text},
                ]
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def generate(self, prompt, **kwargs):
        prompt_str = prompt if isinstance(prompt, str) else prompt.to_string()
        response_text = self.invoke(prompt_str)
        return response_text

# Create an instance of the custom LLM
custom_llm = CustomLLM(api_key=openai.api_key)

# Define the input text
input_text = "Once upon a time"

# Call the invoke method with the input text
response = custom_llm.invoke(input_text)
print(response)

# Alternatively, use the generate method
result = custom_llm.generate(input_text)
print(result)
'''
import os
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

def rbfs_response(technology):

    # Initialize the OpenAI language model instance
    llm_instance = OpenAI(api_key= os.getenv('OPEN_AI_KEY'), temperature=0.7)
    prompt_template = PromptTemplate(input_variables=['technology'],
                                     template = "How do I configure RtBrick's FullStack routing software's {technology}") 
    try:
        name_chain = LLMChain(llm=llm_instance, prompt=prompt_template, output_key= "response")
        response = name_chain({'technology':technology})
        print(response)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    response = rbfs_response("bgp","evpn")
    print("Generated Result:", response)
else:
        print("Failed to get RBFS details")