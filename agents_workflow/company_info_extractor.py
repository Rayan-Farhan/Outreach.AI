from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict, List
from textwrap import dedent

import os
from dotenv import load_dotenv
load_dotenv()

class CompanyInfo(BaseModel):
    description: str = Field(..., description="Short description of the business")
    unique_selling_points: List[str] = Field(..., description="List of USPs")
    target_audience: str = Field(..., description="Ideal customer profile")
    emails: List[str] = Field(..., description="Collected email addresses")
    social_links: List[str] = Field(..., description="Collected social profiles")

parser = JsonOutputParser(pydantic_object=CompanyInfo)

prompt = PromptTemplate.from_template(dedent("""
You are an expert B2B market research and positioning assistant. Given the extracted website content, analyze and distill the information to produce compelling, structured marketing insights for outbound sales and CRM enrichment.

### Website Raw Text:
{raw_text}

### Extracted Emails:
{emails}

### Social Media Links:
{social_links}

### About Section (if available):
{about_section}

Your task is to extract and format the following structured information in JSON:

1. "description" (str): A clear and informative summary of what the company does, including its key industry, services/products, and value proposition.
2. "unique_selling_points" (List[str]): A list of points that highlight the company’s competitive advantages, innovative features, or distinctive qualities.
3. "target_audience" (str): Describe the ideal customer profile using firmographic or demographic traits (e.g., "small e-commerce brands", "enterprise HR teams", "local restaurants looking for POS systems").

Be precise, businesslike, and avoid filler. Structure the output according to the format below.

{format_instructions}
"""), partial_variables={"format_instructions": parser.get_format_instructions()})

def get_company_info_chain(chat_model) -> RunnableLambda:
    return prompt | chat_model | parser

def extract_company_info(scraped_data: Dict, chat_model) -> Dict:
    chain = get_company_info_chain(chat_model)
    return chain.invoke(scraped_data)