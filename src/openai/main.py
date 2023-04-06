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

    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        model=model,  # The model to use for generating the response
        prompt=prompt,  # The text prompt to generate the response from
        temperature=0.7,  # Controls randomness: higher value -> more random, lower value -> more focused
        max_tokens=60,  # Maximum number of tokens (words) in the generated response
        top_p=1.0,  # Controls diversity: higher value -> more diverse, lower value -> less diverse
        frequency_penalty=0.0,  # Controls token frequency: lower value -> penalizes frequent tokens, higher value -> allows frequent tokens
        presence_penalty=1  # Controls token presence: lower value -> penalizes new tokens, higher value -> allows new tokens
    )

    # Return the generated text from the response, removing any leading/trailing whitespace
    return response.choices[0].text.strip()
