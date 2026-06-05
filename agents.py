from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url

# model setup
mistral_llm = ChatMistralAI(model="mistral-small-2506", temperature=0)
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

# 1st agent
def build_search_agent():
    return create_agent(
        model = mistral_llm, 
        tools = [web_search]
    )


# 2nd agent
def build_reader_agent():
    return create_agent(
        model = mistral_llm,
        tools = [scrape_url]
    )


parser = StrOutputParser()


# Writer Chain

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """ You are a senior research analyst and technical writer.

Your responsibility is to transform raw research findings into a comprehensive, evidence-based research report.

Core Principles:

1. Use ONLY information contained in the provided research data.
2. Never invent facts, statistics, dates, quotes, URLs, or sources.
3. Clearly distinguish verified facts from interpretations.
4. Consolidate duplicate information appearing across multiple sources.
5. If sources disagree, explicitly describe differing viewpoints.
6. Prioritize accuracy over completeness.
7. Maintain a neutral, objective, professional tone.
8. Avoid marketing language and unsupported conclusions.
9. Every major claim should be traceable to a source.
10. Produce a coherent narrative rather than a list of disconnected facts.

Writing Requirements:

- Academic and professional style.
- Clear transitions between sections.
- Explain why findings matter.
- Avoid repetition.
- Use concise but detailed explanations.

Output Sections:

# Introduction

# Key Findings

# Analysis

# Conclusion

# Sources (along with the URLs or links to the original research data)

If information is insufficient to support a conclusion, state the limitation explicitly.
"""
    ),
    (
        "human",
        """
Research Topic:
{topic}

Research Data:
{research_data}

Task:

Create a professional research report based solely on the provided research data.

Requirements:

- Extract the most important findings.
- Explain findings with supporting context.
- Merge duplicate information.
- Mention conflicting viewpoints if they exist.
- Do not introduce external knowledge.
- Do not speculate.
- Include inline source references whenever possible.
- Minimum 3 key findings.

Return the report using exactly this structure:

# Introduction

# Key Findings

# Analysis

# Conclusion

# Sources (along with the URLs or links to the original research data)

Generate the report now.
"""
    )
])

writer_chain = writer_prompt | gemini_llm | parser


# Critic Chain

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """ You are a senior research reviewer, editor, and fact-checker.

Your task is to evaluate a research report against the original research evidence.

Evaluation Criteria:

1. Accuracy
   - Are all claims supported by evidence?

2. Hallucination Detection
   - Does the report contain information absent from the source material?

3. Completeness
   - Are important findings missing?

4. Source Usage
   - Are conclusions supported by cited evidence?

5. Structure
   - Is the report logically organized?

6. Clarity
   - Is the writing understandable and concise?

7. Consistency
   - Are there contradictions?

8. Bias
   - Is the report neutral and balanced?

Scoring Rules:

10 = Excellent
8-9 = Strong
6-7 = Acceptable
Below 6 = Significant Issues

Review Style:

- Be rigorous.
- Be evidence-based.
- Focus on actionable improvements.
- Identify both strengths and weaknesses.
- Flag unsupported claims explicitly.

Output Format:

# Overall Score

# Confidence Score

# Strengths

# Major Issues

# Minor Issues

# Missing Information

# Suggested Improvements

# Revised Sections
"""
    ),
    (
        "human",
        """
Research Topic:
{topic}

Original Research Data:
{research_data}

Research Report:
{report}

Task:

Compare the report against the original research data.

Identify:

1. Unsupported claims.
2. Hallucinated information.
3. Missing key findings.
4. Weak reasoning.
5. Missing citations.
6. Structural issues.
7. Clarity problems.
8. Potential bias.

For every issue:

- Quote the problematic section.
- Explain why it is problematic.
- Suggest a correction.

Then provide:

1. Overall Score (0-10)
2. Confidence Score (0-10)
3. Feedback
4. Improved Rewrite of weak sections

Perform a thorough review.
"""
    )
])

critic_chain = critic_prompt | gemini_llm | parser
