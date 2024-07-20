
import os
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

def generate_beach_location(country, attribute):

    # Initialize the OpenAI language model instance
    
    llm_instance = OpenAI(api_key= os.getenv('OPEN_AI_KEY'), temperature=0.7)
    prompt_template = PromptTemplate(input_variables=['country', 'attribute'],
                                     template = "I want to visit a beach in {country} which has the following {attribute}. Describe ten exciting beach locations that I can visit")

    try:
        name_chain = LLMChain(llm=llm_instance, prompt=prompt_template, output_key= "beach_location")
        response = name_chain({'country':country, 'attribute':attribute})
        print(response)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    beach_name = generate_beach_location("Spain", "Sunny and Party")
    print("Generated Result:",beach_name)
else:
        print("Failed to generate beach name.")


