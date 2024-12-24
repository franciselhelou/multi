from langflow.load import run_flow_from_json


def critic_agent(Original_Text, Topic_Input, Context_Input):
    TWEAKS = {
        "TextInput-p2N2a": {
            "input_value": Original_Text
        },
        "TextInput-bKcWn": {
            "input_value": Topic_Input
        },
        "TextInput-47Ke9": {
            "input_value": Context_Input
        },
    }

    result = run_flow_from_json(flow="flows\Critic-Agent.json",
                            input_value="message",
                            session_id="", # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)
    return result[0].outputs[0].results['text'].data['text']


def ethical_agent(input_value):
    input_value = input_value.split("**Changes Made:**")
    TWEAKS = {
        "TextInput-C3ibS": {
            "input_value": input_value[0]
        },
    }

    result = run_flow_from_json(flow="flows\Ethical-Agent.json",
                    input_value="message",
                    session_id="", # provide a session id if you want to use session state
                    fallback_to_env_vars=True, # False by default
                    tweaks=TWEAKS)
    return result[0].outputs[0].results['text'].data['text']

def restructuring_agent(input_value):
    input_value = input_value.split("**Changes Made:**")
    TWEAKS = {
        "TextInput-yxN8H": {
            "input_value": input_value[0]
        },
    }

    result = run_flow_from_json(flow="flows\Restructuring-Agent.json",
                    input_value="message",
                    session_id="", # provide a session id if you want to use session state
                    fallback_to_env_vars=True, # False by default
                    tweaks=TWEAKS)

    return result[0].outputs[0].results['text'].data['text']

def schema_formatter_agent(input_value):
    input_value = input_value.split("**Changes Made:**")
    TWEAKS = {
        "TextInput-ZUyXN": {
            "input_value": input_value[0]
        },
    }

    result = run_flow_from_json(flow="flows\Schema-Formatter-Agent.json",
                    input_value="message",
                    session_id="", # provide a session id if you want to use session state
                    fallback_to_env_vars=True, # False by default
                    tweaks=TWEAKS)

    return result[0].outputs[0].results['text'].data['text']

