import json
import sys

import requests

# input your api key
API_KEY = "<api_key>"


def get_user_content():
    args = sys.argv[1:]
    if not args:
        print("Error: No user content provided.")
        sys.exit(1)
    return " ".join(args)


def make_api_request(user_content):
    instructions = """
    Please correct any syntax errors and grammar issues in the following user content.
    Make the sentences grammatically correct and improve readability, ensuring that the style and tone remain consistent with the original text.
    Do not add extraneous information — just fix the mistakes. Provide the corrected sentence directly without any introductory phrases.
    Do not preface your response with "Response", provide the improved sentence directly.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_content},
        ],
    }

    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


def main():
    user_content = get_user_content()
    refactored_content = make_api_request(user_content)

    print("Original content: " + user_content)
    print(refactored_content)


if __name__ == "__main__":
    main()
