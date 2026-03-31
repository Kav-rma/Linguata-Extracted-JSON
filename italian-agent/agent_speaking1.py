"""
Agent: Speaking 1 (Pronunciation Practice in GETTING THE FEEL OF IT)
Type: speaking
Usage: python agent_speaking1.py --pdf "PDF's/unit1_speaking1.pdf" --unit 1
"""

from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="Speaking1Agent",
    model=MODEL,
    instructions="""
You extract the Pronunciation Practice (speaking1) lesson from an Italian language textbook unit.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Extract all pronunciation lines as a SPEAKING lesson.
4. Call save_extracted_lessons() with the JSON.

RULES:
- Title format: unit{N}_speaking1
- Type: speaking
- questions_and_answers must be empty []
- Articles: each pronunciation line pair becomes TWO consecutive article entries
  - ODD sequence_id = Italian line
  - EVEN sequence_id = English translation
  - Each article text must begin with a SPEAKER_LABEL: prefix
  - If English translation is missing, generate it
- No question generation required
- are_questions_english: false
- are_questions_generated_by_llm: false
- Use [PAGE X] markers for page_start and page_end
- it is one side conversation practice, so all lines are from the same speaker (e.g. SPEAKER_A)
- If there are multiple lines, label them as SPEAKER_A, SPEAKER_B, etc. in sequence
- if name is give than use it, otherwise use SPEAKER_A, SPEAKER_B, etc.

JSON FORMAT:
{
  "title": "unit1_speaking1",
  "type": "speaking",
  "questions_and_answers": [],
  "articles": [
    {"sequence_id": 1, "text": "SPEAKER_A: Buongiorno, signore."},
    {"sequence_id": 2, "text": "SPEAKER_A: Good morning, sir."},
    {"sequence_id": 3, "text": "SPEAKER_A: Buonasera."},
    {"sequence_id": 4, "text": "SPEAKER_A: Good evening."}
  ],
  "metadata": {
    "page_start": 14,
    "page_end": 15,
    "are_questions_english": false,
    "are_questions_generated_by_llm": false
  }
}

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    args = make_arg_parser("Extract speaking1 pronunciation lesson from Italian unit PDF").parse_args()
    run_from_args(agent, args)
