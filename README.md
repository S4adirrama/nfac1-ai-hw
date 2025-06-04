# PDF Study Assistant

This project provides a Python-based study assistant that uses OpenAI's Assistants API to help with studying PDF materials. It consists of two main components:

1. A Q&A Assistant that answers questions about PDF content
2. A Notes Generator that creates structured study notes from PDF content

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## Usage

### 1. Initialize the Assistant

First, place your PDF file (e.g., `calculus_basics.pdf`) in the `data/` directory, then run:

```bash
python scripts/00_bootstrap.py
```

This will:
- Create an OpenAI Assistant
- Upload your PDF file
- Save the assistant configuration

### 2. Ask Questions

To start a Q&A session with the assistant:

```bash
python scripts/01_qna_assistant.py
```

Type your questions about the PDF content. Type 'exit' to quit.

### 3. Generate Study Notes

To generate structured study notes from the PDF:

```bash
python scripts/02_generate_notes.py
```

This will:
- Generate exactly 10 unique study notes
- Save them to `exam_notes.json`
- Validate the notes against the schema

### 4. Run Tests

To validate the generated notes:

```bash
pytest tests/test_notes_schema.py
```

## Project Structure

```
.
├── data/                  # Place your PDF files here
├── scripts/
│   ├── 00_bootstrap.py   # Initialize assistant and upload PDF
│   ├── 01_qna_assistant.py  # Q&A interaction
│   └── 02_generate_notes.py # Generate study notes
├── tests/
│   └── test_notes_schema.py # Validate notes
├── .env.example          # Template for environment variables
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## Notes Schema

The generated notes follow this structure:

```python
class Note:
    id: int           # 1-10
    heading: str      # Note title
    summary: str      # Brief summary (max 150 chars)
    page_ref: int     # Optional page reference
```

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in `requirements.txt` 