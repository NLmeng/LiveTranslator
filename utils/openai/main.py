import os
import openai

def generate_response(model, prompt, api_key_path="key.txt"):
    """
    Generates a response from the OpenAI API using the specified model and prompt
    :param model: The model to use for generating the response
    :type model: str, one of "gpt-3.5-turbo", "gpt-3.5-turbo-0301", "text-davinci-003", "text-davinci-002", ...
    :param prompt: The text prompt to generate the response from
    :type prompt: str
    :return: The generated text from the response
    """
    # Set the API key path
    openai.api_key_path = api_key_path
    # Use the chat endpoint instead of completions
    # The model to use for generating the response
    # The text prompt to generate the response from
    # Controls randomness: higher value -> more random, lower value -> more focused
    # Maximum number of tokens (words) in the generated response
    # Controls diversity: higher value -> more diverse, lower value -> less diverse
    # Controls token frequency: lower value -> penalizes frequent tokens, higher value -> allows frequent tokens
    # Controls token presence: lower value -> penalizes new tokens, higher value -> allows new tokens
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You can help people with their questions by providing answers as accurate as possible."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.66,
        max_tokens=3333,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )

    return response.choices[0].message['content'].strip()