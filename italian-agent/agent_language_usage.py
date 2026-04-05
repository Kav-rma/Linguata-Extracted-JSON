"""
Agent: Language Usage Notes (grammar explanation in TAKING IT APART)
Type: grammar
Usage: python agent_language_usage.py --pdf "PDF's/Unit2/unit2_language_usage.pdf" --unit 2
"""

from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="LanguageUsageAgent",
    model=MODEL,
    instructions="""
You extract the Language Usage Notes (grammar explanation) from an Italian language textbook unit.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Extract the full grammar explanation as ONE article, then generate questions.
4. Call save_extracted_lessons() with the JSON.

RULES:
- Title format: unit{N}_language_usage
- Type: grammar
- Articles: extract the ENTIRE explanation text as exactly ONE article (sequence_id: 1)
  - Do NOT split into multiple articles
  - Copy the text exactly as written in the book
- Questions:
  - If the book contains questions, extract them
  - If no questions exist, generate exactly 10 multiple choice questions from the article
  - Each question has exactly 4 answer options, only one correct
  - Questions must be in English and direct (no "according to the passage" phrasing)
- are_questions_english: true
- are_questions_generated_by_llm: true if generated, false if from book
- Use [PAGE X] markers for page_start and page_end
- even if there are some translation to some text or sentence extract that as well, don't skip that part. in short extract everything.

JSON FORMAT:
{
  "title": "unit1_language_usage",
  "type": "grammar",
  "questions_and_answers": [
    {
      "sequence_id": 1,
      "question_text": "What does the word 'Lei' mean in formal Italian?",
      "type": "multiple_choice",
      "has_answer": true,
      "answers": [
        {"answer_text": "You (formal)", "is_correct": true},
        {"answer_text": "He", "is_correct": false},
        {"answer_text": "She", "is_correct": false},
        {"answer_text": "They", "is_correct": false}
      ]
    }
  ],
  "articles": [
    {
      "sequence_id": 1,
      "text": "Full grammar explanation text here, copied exactly from the book..."
    }
  ],
  "metadata": {
    "page_start": 9,
    "page_end": 11,
    "are_questions_english": true,
    "are_questions_generated_by_llm": true
  }
}

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    args = make_arg_parser("Extract language usage grammar lesson from Italian unit PDF").parse_args()
    run_from_args(agent, args)
