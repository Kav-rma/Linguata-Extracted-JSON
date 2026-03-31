"""
Agent: Putting It Together (PUTTING IT TOGETHER section)
Type: reading
Usage: python agent_putting_it_together.py --pdf "PDF's/Unit2/unit2_putting_it_together.pdf" --unit 2
"""

from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="PuttingItTogetherAgent",
    model=MODEL,
    instructions="""
You extract the PUTTING IT TOGETHER section from an Italian language textbook unit.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Extract all content as a READING lesson.
4. Call save_extracted_lessons() with the JSON.

RULES:
- Title format: unit{N}_putting_it_together
- Type: reading
- Articles: each sentence or logical line = one article entry with sequential sequence_id
- Questions: generate exactly 10 multiple choice questions from the content
  - Each question has exactly 4 answer options, only one correct
  - Questions must be in English and direct (no "according to the passage" phrasing)
- are_questions_english: true
- are_questions_generated_by_llm: true
- Use [PAGE X] markers for page_start and page_end
- Extract it till the "MAKING IT WORK" heading, if it comes that means it has content beyond putting it together, so ignore everything after that.

JSON FORMAT:
{
  "title": "unit1_putting_it_together",
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
    {"sequence_id": 1, "text": "First sentence or line."}
  ],
  "metadata": {
    "page_start": 19,
    "page_end": 21,
    "are_questions_english": true,
    "are_questions_generated_by_llm": true
  }
}

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    args = make_arg_parser("Extract putting_it_together reading lesson from Italian unit PDF").parse_args()
    run_from_args(agent, args)
