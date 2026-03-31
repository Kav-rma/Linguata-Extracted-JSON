"""
Agent: Vocabulary 1 (first vocabulary block in TAKING IT APART)
Type: vocabulary
Usage: python agent_vocab1.py --pdf "PDF's/unit1_vocab1.pdf" --unit 1
"""

from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="Vocab1Agent",
    model=MODEL,
    instructions="""
You extract the first vocabulary block (vocab1) from an Italian language textbook unit.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Extract all Italian → English phrase pairs as a VOCABULARY lesson.
4. Call save_extracted_lessons() with the JSON.

RULES:
- Title format: unit{N}_vocab1
- Type: vocabulary
- Each Italian phrase = one question, its English meaning = the answer
- Question type: short_answer
- Questions are in Italian (foreign language), answers in English
- articles array must be empty []
- are_questions_english: false
- are_questions_generated_by_llm: false
- Use [PAGE X] markers for page_start and page_end

JSON FORMAT:
{
  "title": "unit1_vocab1",
  "type": "vocabulary",
  "questions_and_answers": [
    {
      "sequence_id": 1,
      "question_text": "buongiorno",
      "has_answer": true,
      "type": "short_answer",
      "answers": [
        {"answer_text": "good morning", "is_correct": true}
      ]
    },
    {
      "sequence_id": 2,
      "question_text": "arrivederci",
      "has_answer": true,
      "type": "short_answer",
      "answers": [
        {"answer_text": "goodbye", "is_correct": true}
      ]
    }
  ],
  "articles": [],
  "metadata": {
    "page_start": 7,
    "page_end": 8,
    "are_questions_english": false,
    "are_questions_generated_by_llm": false
  }
}

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    args = make_arg_parser("Extract vocab1 vocabulary lesson from Italian unit PDF").parse_args()
    run_from_args(agent, args)
