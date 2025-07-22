# agents/company_info_extractor_agent.py

from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict, List
from textwrap import dedent

import os
from dotenv import load_dotenv
load_dotenv()

# 1. Define output schema using Pydantic
class CompanyInfo(BaseModel):
    description: str = Field(..., description="Short description of the business")
    unique_selling_points: List[str] = Field(..., description="List of USPs")
    target_audience: str = Field(..., description="Ideal customer profile")
    emails: List[str] = Field(..., description="Collected email addresses")
    social_links: List[str] = Field(..., description="Collected social profiles")

# 2. Create the output parser from the schema
parser = JsonOutputParser(pydantic_object=CompanyInfo)

# 3. Template prompt with format instructions
prompt = PromptTemplate.from_template(dedent("""
    You are a B2B market research assistant. Analyze the following business website content and extract the structured details.

    ### Website Raw Text:
    {raw_text}

    ### Emails:
    {emails}

    ### Social Links:
    {social_links}

    ### About Section:
    {about_section}

    {format_instructions}
"""), partial_variables={"format_instructions": parser.get_format_instructions()})

# 4. LangChain chain
def get_company_info_chain(chat_model) -> RunnableLambda:
    return prompt | chat_model | parser

# 5. Call this function from your pipeline
def extract_company_info(scraped_data: Dict, chat_model) -> Dict:
    chain = get_company_info_chain(chat_model)
    return chain.invoke(scraped_data)
