"""
Agent: Listening Comprehension (MAKING IT WORK section)
Type: listening
Usage: python agent_listening_comprehension.py --pdf "PDF's/unit1_listening.pdf" --unit 1
"""

from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="ListeningComprehensionAgent",
    model=MODEL,
    instructions="""
You extract the Listening Comprehension lesson from the MAKING IT WORK section
of an Italian language textbook unit.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Extract all multiple choice questions as a LISTENING lesson.
4. Call save_extracted_lessons() with the JSON.

RULES:
- Title format: unit{N}_listening_comprehension
- Type: listening
- questions_and_answers: extract all multiple choice questions from the PDF
  - question_text: Extracted from the PDF, no made up questions. exactly what pdf says, eg:- Based on what you have heard, do the following exercise, selecting only one of the four letters: a, b, c, d, according to which best reflects what is in the narrative.
  - Each question has exactly 4 answer options, extract those 4 options as 4 different answer_text only one correct.
  - Preserve questions exactly as written
- articles must be empty []
- are_questions_english: true
- are_questions_generated_by_llm: false (questions come from the book)
- Use [PAGE X] markers for page_start and page_end

JSON FORMAT:
{
  "title": "unit1_listening_comprehension",
  "type": "listening",
  "questions_and_answers": [
    {
      "sequence_id": 1,
      "question_text": "Based on what you have heard, do the following exercise, selecting only one of the four letters: a, b, c, d, according to which best reflects what is in the narrative.",
      "type": "multiple_choice",
      "has_answer": true,
      "answers": [
        {"answer_text": "A taxi", "is_correct": false},
        {"answer_text": "A hotel recommendation", "is_correct": false},
        {"answer_text": "Passport control directions", "is_correct": true},
        {"answer_text": "A luggage cart", "is_correct": false}
      ]
    }
  ],
  "articles": [],
  "metadata": {
    "page_start": 25,
    "page_end": 26,
    "are_questions_english": true,
    "are_questions_generated_by_llm": false
  }
}

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    args = make_arg_parser("Extract listening comprehension lesson from Italian unit PDF").parse_args()
    run_from_args(agent, args)
