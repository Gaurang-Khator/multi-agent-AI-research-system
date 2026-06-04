from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url

# model setup
llm = ChatMistralAI(model="mistral-small-2506", temperature=0)

# 1st agent
def build_search_agent():
    return create_agent(
        model = llm, 
        tools = [web_search]
    )


# 2nd agent
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


parser = StrOutputParser()


# Writer Chain

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert research writer. Your job is to synthesize raw research data 
into a well-structured, comprehensive research report.

Guidelines:
- Write in clear, professional academic prose
- Organize content with logical flow: Introduction → Key Findings → Analysis → Conclusion
- Cite sources inline where relevant
- Avoid redundancy; consolidate overlapping information
- Target length: 400-600 words unless specified otherwise
"""
    ),
    (
        "human",
        """Based on the following scraped research content, write a detailed research report.

Topic: {topic}

Raw Research Data:
{research_data}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional.

Write a structured report now."""
    )
])

writer_chain = writer_prompt | llm | parser


# Critic Chain

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a rigorous research editor and fact-checker. Your job is to critically 
evaluate a research report and provide actionable improvement feedback.

Evaluate along these dimensions:
1. **Accuracy** - Are claims well-supported? Flag anything unverified or speculative.
2. **Completeness** - Are there obvious gaps or missing angles on the topic?
3. **Clarity** - Is the writing clear, concise, and free of jargon overload?
4. **Structure** - Does the report flow logically from intro to conclusion?
5. **Bias** - Is the tone neutral and balanced?

Output format:
- Overall Score: X/10
- Strengths: (bullet points)
- Issues Found: (bullet points with severity: low/medium/high)
- Suggested Improvements: (bullet points)
- Revised Sections (if needed): (rewrite only the weak parts)
"""
    ),
    (
        "human",
        """Please critically review the following research report.

Report to Review:
{report}

Provide your detailed critique now."""
    )
])

critic_chain = critic_prompt | llm | parser