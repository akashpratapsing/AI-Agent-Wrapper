from flask import Flask, request, jsonify
from retell import Retell
from vapi import Vapi
import os
import requests

app = Flask(__name__)

# I does not have any of the API keys, this is only for demonstration purposes.
RETELL_API_KEY = os.getenv("RETELL_API_KEY", "RETELL_API_KEY")
VAPI_API_KEY = os.getenv("VAPI_API_KEY", "VAPI_API_KEY")

@app.route("/create-agent", methods=["POST"])
def create_agent():
    data = request.get_json()
    selected_ai_agent = data.get("selected_ai_agent")

    if not selected_ai_agent:
        return jsonify({"error": "Missing 'selected_ai_agent' in request"}), 400

    if selected_ai_agent.lower() == "retell":
        try:
            client = Retell(api_key=RETELL_API_KEY)
            agent_response = client.agent.create(
                response_engine={
                    "conversation_flow_id": "conversation_flow_02b5c15134f0",
                    "type": "conversation-flow"
                    },
                voice_id="11labs-Adrian"
            )
            return jsonify({
                "selected_ai_agent": "retell",
                "agent_id": agent_response.agent_id
            }), 200
        except Exception as e:
            return jsonify({"error": f"Retell agent creation failed: {str(e)}"}), 500

    elif selected_ai_agent.lower() == "vapi":
        try:
            headers = {
                "Authorization": f"Bearer {VAPI_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "voice": {
                    "provider": "azure",
                    "voiceId": "andrew"
                },
                "name": "Jarvis",
                "model": {
                    "provider": "deep-seek",
                    "model": "deepseek-chat"
                }
            }

            response = requests.post("https://api.vapi.ai/assistant", headers=headers, json=payload)
            response_data = response.json()

            if response.status_code not in [200, 201]:
                return jsonify({"error": "VAPI API error", "details": response_data}), 500

            return jsonify({"selected_ai_agent": "vapi", "assistant": response_data}), 200

        except Exception as e:
            return jsonify({"error": f"VAPI assistant creation failed: {str(e)}"}), 500

    else:
        return jsonify({"error": "Unsupported AI agent selected."}), 400

if __name__ == "__main__":
    app.run(debug=True)
