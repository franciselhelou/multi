from flask import Flask, render_template, request, jsonify
from agents import critic_agent, ethical_agent, restructuring_agent, schema_formatter_agent
from browser import perform_search_google, save_content, scrape_content

app = Flask(__name__)

# API Endpoints

# Backend server running
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    number_of_results = data.get('number_of_results', 5)
    results = perform_search_google(query, number_of_results)
    return jsonify(results)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    content = scrape_content(url)
    return jsonify({'content': content})

@app.route('/critic_agent', methods=['POST'])
def critic_agent_endpoint():
    data = request.get_json()
    original_text = data.get('original_text')
    topic_input = data.get('topic_input')
    results = perform_search_google(topic_input)
    final_content = ""
    # For each result, scrape content
    for result in results:
        content_url = scrape_content(result['url'])  # Scraped content from 1 URL
        final_content += content_url + "\n\n"
    output_text = critic_agent(original_text, topic_input, final_content)
    return jsonify({'output_critic_agent': output_text})

@app.route('/ethical_agent', methods=['POST'])
def ethical_agent_endpoint():
    data = request.get_json()
    input_value = data.get('input_value')
    output_text = ethical_agent(input_value)
    return jsonify({"output_ethical_agent": output_text})

@app.route('/restructuring_agent', methods=['POST'])
def restructuring_agent_endpoint():
    data = request.get_json()
    input_value = data.get('input_value')
    output_text = restructuring_agent(input_value)
    return jsonify({'output_restructuring_agent': output_text})

@app.route('/schema_formatter_agent', methods=['POST'])
def schema_formatter_agent_endpoint():
    data = request.get_json()
    input_value = data.get('input_value')
    output_text = schema_formatter_agent(input_value)
    return jsonify({'output_schema_formatter_agent': output_text})

@app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    data = request.get_json()
    topic_input = data.get('topic_input')
    original_input = data.get('original_input')

    try:
        # Step 1: Search web
        results = perform_search_google(topic_input)
        urls = []
        final_content = ""
        # For each result, scrape content
        for result in results:
            content_url = scrape_content(result['url'])  # Scraped content from 1 URL
            final_content += content_url + "\n\n"
            urls.append(result['url'])

        # Step 2: Critic Agent
        critic_output = critic_agent(original_input, topic_input, final_content)
        # Step 3: Ethical Agent
        ethical_output = ethical_agent(critic_output)
        # Step 4: Restructuring Agent
        restructuring_output = restructuring_agent(ethical_output)
        # Step 5: Schema Formatter Agent
        schema_formatter_output = schema_formatter_agent(restructuring_output)

        return jsonify({
            "critic_agent_output": critic_output,
            "ethical_agent_output": ethical_output,
            "restructuring_agent_output": restructuring_output,
            "schema_formatter_agent_output": schema_formatter_output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
