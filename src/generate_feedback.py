from utils import read_file, set_multiline_output
from google.genai import types

def generate_feedback(file_path, documentation, rules, client):
    doc_content = read_file(file_path)

    identify_content_type = {
        "role": f"Your role is to validate whether the given {documentation['type']} follows the specified rules for {documentation['type']} writing. You will review the markdown content and ensure it adheres to the guidelines. If the documentation deviates from the rules, provide clear feedback on what needs to be corrected. Pay attention to the structure, content, and type tags.",
        "prompt": f"""
        TASK:
        Please review the {documentation['type']} and identify any areas where the content deviates from the rules. If corrections are needed, provide specific feedback on the changes required. 

        Your feedback must be structured in three parts:
        1. **General Feedback**: An overall summary of your findings.
        2. **Actionable Feedback**: Specific areas where changes are needed and what exactly should be fixed.
        3. **Suggested Revision**: A revised version of the document or sections with the necessary improvements. Wrap the entire revision inside a fenced code block starting and ending with four backticks (````).

        The content relates to the following VTEX product: {documentation['product']}.

        ## Rules for {documentation['type']}
        {rules}

        ## Documentation in markdown format
        {doc_content}
        """,
        "temperature": 0.2
    }

    system_instruction_part = f"Role: {identify_content_type['role']}"
    generate_content_config = types.GenerateContentConfig(
        temperature=identify_content_type["temperature"],
        system_instruction=[system_instruction_part],
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=identify_content_type['prompt'])]
        )
    ]

    GEMINI_MODELS = (
        "gemini-3.5-flash",
        "gemini-3-flash-preview",
        "gemini-2.5-flash",
        "gemini-3.1-flash-lite",
    )

    last_error: BaseException | None = None
    for model in GEMINI_MODELS:
        try:
            print(f"Trying model {model} ...")
            response_text = ""
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                print(chunk.text, end="", flush=True)
                response_text += chunk.text
            set_multiline_output("response", response_text)
            return
        except Exception as e:
            last_error = e
            print(f"Model {model} failed: {e}. Retrying with next model...")

    raise RuntimeError(
        "All Gemini models failed for feedback generation.") from last_error
