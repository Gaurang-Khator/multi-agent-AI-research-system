from agents import build_search_agent , build_reader_agent , writer_chain , critic_chain
from rich import print

def run_research_pipeline(topic : str) -> dict:
    
    state = {}

    # Step 1: Search Agent Working

    print("\n"+"="*50)
    print("Search Agent is working...")
    print("\n"+"="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [( "user", f"Conduct a web search to gather recent, reliable and detailed information on the topic: {topic}" )]
    })
    
    state['search_results'] = search_result['messages'][-1].content

    print("\n Search Result: \n", state['search_results'])

    # Step 2: Reader Agent Working

    print("\n"+"="*50)
    print("Reader Agent is scraping top resources...")
    print("\n"+"="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [( "user",
                      f"Based on the following search results about '{topic}', "
                      f"pick the most relevant URLs and scrape their content for deeper insights."
                      f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n Scraped Content: \n", state['scraped_content'])

    # Step 3: Writer Chain Working

    print("\n"+"="*50)
    print("Writer Chain is drafting the report...")
    print("\n"+"="*50)

    research_combined_data = (
        f"SEARCH RESULTS: \n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT: \n{state['scraped_content']}"
    )

    state['writer_report'] = writer_chain.invoke({
        "topic": topic,
        "research_data": research_combined_data
    })

    print("\n Final Research Report: \n", state['writer_report'])

    # Step 4: Critic Chain Working

    print("\n"+"="*50)
    print("Critic Chain is reviewing the report...")
    print("\n"+"="*50)

    state['critic_feedback'] = critic_chain.invoke({
        "report": state['writer_report']
    })

    print("\n Critic Feedback: \n", state['critic_feedback'])

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)