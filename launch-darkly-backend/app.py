# Flask and core imports
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient, AIConfig, ModelConfig, LDMessage, ProviderConfig
import pprint
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize LaunchDarkly SDK with environment key
ldclient.set_config(Config(os.environ["LD_SDK_KEY"]))
# Initialize LaunchDarkly AI client
aiclient = LDAIClient(ldclient.get())
# Initialize OpenAI client with API key
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Create Flask app and configure CORS for allowed origins
app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://launchdarklydemo-env.eba-k3kcg8hp.us-east-2.elasticbeanstalk.com"
], supports_credentials=True, allow_headers="*")

# API endpoint to process context and interact with LaunchDarkly AI Config and OpenAI
@app.route('/context', methods=['POST'])
def create_context():
    # Parse incoming JSON payload as LaunchDarkly multi-context
    data = request.get_json()
    multi_context = Context.from_dict(data)
    ai_config_key = "the-voice"  # LD AI Config key

    # Default AI config if none is returned from LD
    default_value = AIConfig(
        enabled=True,
        model=ModelConfig(name='my-default-model'),
        messages=[],
    )

    # Get AI config and tracker from LaunchDarkly
    config, tracker = aiclient.config(
        ai_config_key,
        multi_context,
        default_value
    )

    # Log config details for debugging
    app.logger.info(f"Config value: {config}")
    app.logger.info(f"Model config: {pprint.pformat(getattr(config, 'model', None).__dict__ if getattr(config, 'model', None) else None)}")
    app.logger.info(f"Provider: {pprint.pformat(getattr(config, 'provider', None).__dict__ if getattr(config, 'provider', None) else None)}")
    app.logger.info(f"Messages: {getattr(config, 'messages', None)}")

    # Prepare messages for OpenAI
    messages = [] if config.messages is None else config.messages
    # Track metrics and get OpenAI completion
    completion = tracker.track_openai_metrics(
        lambda:
            openai_client.chat.completions.create(
                model=config.model.name,
                messages=[message.to_dict() for message in messages],
        )
    )
    # Return the AI's response
    return completion.choices[0].message.content, 200

# Serve static index.html at the base route
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# Serve static assets from the assets directory
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('static/assets', filename)
