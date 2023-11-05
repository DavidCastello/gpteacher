import openai
import json
from typing import List, Tuple
import re

# Replace with your own API key
openai.api_key = "INSERT YOUR KEY HERE!"

def split_into_chunks(text: str, chunk_size: int = 3) -> List[str]:
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    chunks = [' '.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]
    return chunks

def correct_text(chunk: str) -> Tuple[str, List[dict], List[dict]]:
    prompt=f'Act as a spelling, punctuation, and grammar corrector. The output of the response is a JSON file, nothing else. The JSON response should have three fields, corrected_text, spelling_errors and grammar_errors. The corrected_text field will contain the corrected version of the text you provided. The spelling_errors field will contain a list of dictionaries, each representing a spelling or capitalization error found in the text. Each dictionary in the errors list will have reference and correction fields, representing the reference error and its corrected version, respectively. The grammar errors field will contain a list of dictionaries, each representing a grammar error found in the text. Each dictionary in the grammar_errors list will have reference and correction fields, representing the reference error and its corrected version, respectively. The text to correct is the following: {chunk}'
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        temperature=0.5,
    )

    json_response_raw = response['choices'][0]['text'].strip()
    json_response = json.loads(json_response_raw)
    
    return json_response['corrected_text'], json_response['spelling_errors'], json_response['grammar_errors']   

def gpteacher(input_text: str) -> Tuple[str, List[dict], List[dict]]:
    chunks = split_into_chunks(input_text)
    corrected_text = []
    spelling_errors = []
    grammar_errors = []

    for chunk in chunks:
        ct, se, ge = correct_text(chunk)
        corrected_text.append(ct)
        spelling_errors.extend(se)
        grammar_errors.extend(ge)

    return ' '.join(corrected_text), spelling_errors, grammar_errors
