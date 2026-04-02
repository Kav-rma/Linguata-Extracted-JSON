"""
Agent: Vocabulary 2 (additional vocabulary block in TAKING IT APART)
Type: vocabulary
Usage: python agent_vocab2.py --pdf "PDF's/Unit2/unit2_vocab2.pdf" --unit 2
"""

from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="Vocab2Agent",
    model=MODEL,
    instructions="""
You extract the additional vocabulary block (vocab2) from an Italian language textbook unit pdf.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Extract all Italian → English phrase pairs as a VOCABULARY lesson.
4. Call save_extracted_lessons() with the JSON.

RULES:
- Title format: unit{N}_vocab2
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
  "title": "unit1_vocab2",
  "type": "vocabulary",
  "questions_and_answers": [
    {
      "sequence_id": 1,
      "question_text": "il passaporto",
      "has_answer": true,
      "type": "short_answer",
      "answers": [
        {"answer_text": "the passport", "is_correct": true}
      ]
    }
  ],
  "articles": [],
  "metadata": {
    "page_start": 12,
    "page_end": 13,
    "are_questions_english": false,
    "are_questions_generated_by_llm": false
  }
}

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    args = make_arg_parser("Extract vocab2 Additional vocabulary lesson from Italian unit PDF").parse_args()
    run_from_args(agent, args)
