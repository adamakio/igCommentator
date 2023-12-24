# Instagram Commentator

This Python program connects to Instagram and automatically comments on a post every 10 minutes (+/- 3 minutes random). It generates comments using a Language Model (LLM).

## Setup

1. Install required packages:

`pip install -r requirements.txt`

2. Create a `.env` file in the project root with your Instagram and OpenAI API keys:
```
INSTAGRAM_API_KEY='your_instagram_api_key_here'
OPENAI_API_KEY='your_openai_api_key_here'
```
## Usage

Run the script:

`python main.py`

## Disclaimer

This tool is for educational purposes only. Automated interactions on social media platforms can violate their terms of service. Use responsibly.
