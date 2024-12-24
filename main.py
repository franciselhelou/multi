from agents import critic_agent, ethical_agent, restructuring_agent, schema_formatter_agent
from browser import perform_search_google, save_content, scrape_content

def main():
    # Prompt the user to enter topic and original input
    topic_input = input("Enter the topic: ")
    original_input = input("Enter the original input: ")

    try:
        #Step 1: Search web 
        results = perform_search_google(topic_input)
        urls=[]
        final_content=""
        # Display results
        for idx, result in enumerate(results, 1):
            print(f"{idx}. {result['title']}: {result['url']}")
            #Scrape content
            content_url = scrape_content(result['url']) #scrapped content from 1 url
            #append scrapped content to final_content
            final_content+=content_url+"\n\n"
            urls.append(result['url'])
        #Scrape content
        save_content(urls)
        
        #Step 2: Critic Agent
        critic_output = critic_agent(original_input, topic_input, final_content)
        print("\n\n--------------------------------------------------------------------\n\n")
        print("Critic Agent Output:")
        print(critic_output[1])
        
        #Step 3: Ethical Agent
        ethical_output = ethical_agent(critic_output[0])
        print("\n\n--------------------------------------------------------------------\n\n")
        print("Ethical Agent Output:")
        print(ethical_output[1])
        
        #Step 4: Restructuring Agent
        restructuring_output = restructuring_agent(ethical_output[0])
        print("\n\n--------------------------------------------------------------------\n\n")
        print("Restructuring Agent Output:")
        print(restructuring_output)
        
        #Step 5: Schema Formatter Agent
        schema_formatter_output = schema_formatter_agent(restructuring_output)
        print("\n\n--------------------------------------------------------------------\n\n")
        print("Schema Formatter Agent Output:")
        print(schema_formatter_output)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

