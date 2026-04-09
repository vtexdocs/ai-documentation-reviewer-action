from utils import read_file
from google import genai
from google.genai import types
from pydantic import BaseModel

class DocType(BaseModel):
    type: str
    explanation: str
    product: str

documentation_types = read_file('/action/config/documentation_types.json')

def categorize_doc(file_path: str, client: genai.Client) -> dict:
    doc_content = read_file(file_path)
    print(f"Content of {file_path}:")
    print(doc_content)

    identify_content_type = {
        "role": "Your goal is to classify documentation based on its characteristics. You will analyze the purpose, use cases, tone, and intended audience to assign the appropriate documentation type.",
        "prompt": f"""
        TASK:
        You are tasked with identifying the type of the document provided. Read the content carefully and select the documentation type based on the following categories. Consider the purpose, tone, intended audience, and use case when making your decision.
        The output should include the documentation type, explanation, and related VTEX product (e.g., Catalog, FastStore, etc).

        ## Documentation types
        {documentation_types}

        ## Documentation
        {doc_content}
        """,
        "temperature": 0.2
    }

    system_instruction_part = f"Role: {identify_content_type['role']}"

    generate_content_config = types.GenerateContentConfig(
        temperature=identify_content_type["temperature"],
        system_instruction=[system_instruction_part],
        response_mime_type="application/json",
        response_schema=DocType,
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=identify_content_type['prompt'])]
        )
    ]

    GEMINI_MODELS = (
        "gemini-2.5-flash",
        "gemini-3.1-flash-lite-preview",
    )

    last_error: BaseException | None = None
    for model in GEMINI_MODELS:
        try:
            print(f"Trying model {model} ...")
            response_text = client.models.generate_content(
                model=model,
                contents=contents,
                config=generate_content_config,
            )
            documentation: DocType = response_text.parsed
            return documentation.model_dump()
        except Exception as e:
            last_error = e
            print(f"Model {model} failed: {e}. Retrying with next model...")

    raise RuntimeError("All Gemini models failed for categorization.") from last_error

