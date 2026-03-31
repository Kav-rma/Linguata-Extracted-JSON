"""
Agent: Speaking 2 (Interpreter Situation in MAKING IT WORK)
Type: speaking
Usage: python agent_speaking2.py --pdf "PDF's/unit1_speaking2.pdf" --unit 1
"""

from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="Speaking2Agent",
    model=MODEL,
    instructions="""
You extract the Interpreter Situation (speaking2) lesson from the MAKING IT WORK section
of an Italian language textbook unit.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Extract all interactions as a SPEAKING lesson.
4. Call save_extracted_lessons() with the JSON.

RULES:
- Title format: unit{N}_speaking2
- Type: speaking
- questions_and_answers must be empty []
- Articles: each interaction becomes FOUR consecutive article entries in this sequence:
    1 (odd)  → Italian question/statement
    2 (even) → English translation of the question (generate if missing)
    3 (odd)  → Italian response (generate if missing)
    4 (even) → English translation of the response
  Continue incrementing sequence_id across all interactions.
- Each article text must begin with a SPEAKER_LABEL: prefix
- Generate missing Italian responses or English translations as needed
- are_questions_english: false
- are_questions_generated_by_llm: false
- Use [PAGE X] markers for page_start and page_end

JSON FORMAT:
{
  "title": "unit1_speaking2",
  "type": "speaking",
  "questions_and_answers": [],
  "articles": [
    {"sequence_id": 1, "text": "TOURIST: Dov'è l'albergo?"},
    {"sequence_id": 2, "text": "TOURIST: Where is the hotel?"},
    {"sequence_id": 3, "text": "GUIDE: È in Via Roma."},
    {"sequence_id": 4, "text": "GUIDE: It is on Via Roma."},
    {"sequence_id": 5, "text": "TOURIST: Grazie mille."},
    {"sequence_id": 6, "text": "TOURIST: Thank you very much."},
    {"sequence_id": 7, "text": "GUIDE: Prego."},
    {"sequence_id": 8, "text": "GUIDE: You're welcome."}
  ],
  "metadata": {
    "page_start": 22,
    "page_end": 24,
    "are_questions_english": false,
    "are_questions_generated_by_llm": false
  }
}

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    args = make_arg_parser("Extract speaking2 interpreter lesson from Italian unit PDF").parse_args()
    run_from_args(agent, args)
