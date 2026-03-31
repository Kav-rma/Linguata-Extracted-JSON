"""
Agent: Intro / LANGUAGE section
Type: reading
Usage: python agent_intro.py --pdf "PDF's/Unit2/unit2_intro.pdf" --unit 2
"""

from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="IntroAgent",
    model=MODEL,
    instructions="""
You extract the LANGUAGE / intro section from an Italian language textbook unit.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Extract the entire text as a READING lesson.
4. Call save_extracted_lessons() with the JSON.

RULES:
- Title format: unit{N}_intro
- Type: reading
- Articles: each sentence or logical line = one article entry with sequential sequence_id
- Questions: generate exactly 10 multiple choice questions from the content
  - Each question has exactly 4 answer options, only one correct
  - Questions must be direct (no "according to the passage" phrasing)
- Use [PAGE X] markers to set accurate page_start and page_end
- are_questions_generated_by_llm: true
- are_questions_english: true

JSON FORMAT:
{
  "title": "unit1_intro",
  "type": "reading",
  "questions_and_answers": [
    {
      "sequence_id": 1,
      "question_text": "...",
      "type": "multiple_choice",
      "has_answer": true,
      "answers": [
        {"answer_text": "...", "is_correct": true},
        {"answer_text": "...", "is_correct": false},
        {"answer_text": "...", "is_correct": false},
        {"answer_text": "...", "is_correct": false}
      ]
    }
  ],
  "articles": [
    {"sequence_id": 1, "text": "First sentence or line."},
    {"sequence_id": 2, "text": "Second sentence or line."}
  ],
  "metadata": {
    "page_start": 1,
    "page_end": 2,
    "are_questions_english": true,
    "are_questions_generated_by_llm": true
  }
}

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    args = make_arg_parser("Extract intro/LANGUAGE lesson from Italian unit PDF").parse_args()
    run_from_args(agent, args)
