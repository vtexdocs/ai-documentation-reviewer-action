# AI Documentation Reviewer Action

A GitHub Action that analyzes documentation using Google Gemini AI to provide intelligent feedback and validation for documentation based on predefined types and rules.

## Features

- Automatically categorizes documentation into predefined types (Guide, Tutorial, Reference, API Reference, Explanation, Release Note)
- Validates documentation against type-specific rules and guidelines
- Provides detailed feedback on documentation structure, content, and adherence to VTEX standards
- Supports multiple documentation types with specific validation rules
- Uses Google Gemini AI for intelligent analysis and feedback generation

## Usage

```yaml
name: Documentation Review

on:
  pull_request:
    paths:
      - 'docs/**'

jobs:
  review-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Review Documentation
        uses: vtexdocs/ai-reviewer-action@v1
        with:
          gemini_api_key: ${{ secrets.GEMINI_API_KEY }}
          file_paths: 'test.md'
```

### Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `gemini_api_key` | Google Gemini API key | Yes | - |
| `file_paths` | Path to the documentation file to analyze | Yes | '.' |

### Output

The action provides detailed feedback including:

1. **General Feedback**: Overall summary of findings
2. **Actionable Feedback**: Specific areas requiring changes
3. **Suggested Revision**: Improved version of the document or sections

## Customization

### Adding new documentation types

To add a new documentation type, follow these steps:

1. Open the `config/documentation_types.json` file and declare the new documentation type with the following fields:

    ```json
    {
        "type": "Type name",
        "purpose": "Description of the type's purpose",
        "tone": "Expected tone of the documentation",
        "audience": "Target audience",
        "use_case": "When to use this type"
    }
    ```

    **Example:**

    ```json
    {
        "type": "Guide",
        "purpose": "Shows how to complete specific tasks in the VTEX ecosystem.",
        "tone": "Practical and task-oriented",
        "audience": "Users with some prior knowledge",
        "use_case": "Setup, configuration, deployment"
    }
    ```

2. Update the `config/rules_mapping.json` file to map the new doc type to its corresponding rules file:

    ```json
    {
        "Type name": "/action/rules/type_rules.json"
    }
    ```

    **Example:**
    
    ```json
    {
        "Guide": "/action/rules/guides_rules.json"
    }
    ```

3. Create a new rules file inside the `rules/` folder for the new documentation type (e.g., `guides_rules.json`), following the instructions in [Updating documentation rules](#updating-documentation-rules).

### Updating documentation rules

1. Open the relevant rules file in the `rules/` directory.
2. Define the rules structure as desired using the following template. 

```json
{
  "metadata": {
    "purpose": "Description of the documentation type's purpose"
  },
  "frontmatter": {
    "title": {
      "description": "The title of the document",
      "mandatory": true,
      "validation_heuristic": "Must be clear and descriptive"
    },
    "slug": {
      "description": "URL-friendly version of the title",
      "mandatory": true,
      "validation_heuristic": "Must be lowercase with hyphens"
    }
  },
  "body": [
    {
      "section": "Introduction",
      "description": "Brief overview of the topic"
    },
    {
      "section": "Prerequisites",
      "description": "Required knowledge or setup"
    }
  ],
  "style_guide": {
    "tone_and_voice": {
      "rules": [
        {
          "id": "R1.1",
          "description": "Use clear, direct language",
          "validation_heuristic": [
            "Avoid marketing adjectives",
            "Use active voice"
          ]
        }
      ],
      "examples": [
        {
          "rule": "R1.1",
          "correct": "Configure your store settings in the Admin panel",
          "incorrect": "Simply tweak your store settings in the Admin thing",
          "explanation": "The correct version uses clear, professional language without unnecessary words"
        }
      ]
    }
  }
}
```

- `metadata`: This section includes general information about the documentation type, such as its purpose.
- `frontmatter`: Specifies the rules for essential metadata that typically appears at the start of a document:
- `body`: A list of sections that should appear in the document body (e.g., Introduction, Prerequisites). Each section should have a description of its purpose.
- `style_guide`: This section is flexible and can have multiple categories that address different aspects of writing style (e.g., `tone_and_voice`, `clarity_and_brevity`). Each category should include:
    - `rules`: Lists the rules that should be followed in terms of writing style, such as avoiding marketing adjectives and using active voice.
    - `examples`: Provides examples of how the rules should be applied.

This template can be adapted and extended to fit the needs of different documentation types.