"""
Agent: Writing Models (Working with the Language in GETTING THE FEEL OF IT)
Type: writing
Usage: python agent_model.py --pdf "PDF's/unit1_model1.pdf" --unit 1 --model-num 1
       python agent_model.py --pdf "PDF's/unit1_models.pdf" --unit 1   (extracts all models)
"""

import argparse
from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="ModelAgent",
    model=MODEL,
    instructions="""
You extract Writing Model exercises (Working with the Language) from an Italian language textbook unit.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Identify how many MODELs exist in the PDF.
4. For EACH MODEL, create a separate JSON lesson object.
5. Call save_extracted_lessons() with a JSON array containing ALL model lessons.

TWO-COLUMN LAYOUT WARNING:
The exercise section is formatted as a two-column layout in the PDF.
The left column contains the QUESTIONS and the right column contains the ANSWERS.
PDF extraction reads all left-column questions first, then all right-column answers — so they appear separated.
YOU MUST reconstruct the correct question → answer pairs by matching them in order.

STRUCTURE OF EACH MODEL SECTION:
A model section looks like this in the PDF:

  Model 1
  (affirmative)  Q: Scusi, Lei è americano/a?
                 A: Sì, sono americano/a.
  (negative)     A: No, non sono americano/a.

  [then the exercise table:]
  Scusi, Lei è americano/a?       Sì, sono americano/a.
                                  No, non sono americano/a.
  Scusi, Lei è dell'Ambasciata?   Sì, sono dell'Ambasciata.
                                  No, non sono dell'Ambasciata.

WHAT GOES WHERE:
- model_conversation = ONLY the "Model N" template block (the Q/A lines labeled with affirmative/negative).
  Do NOT include the exercise rows in model_conversation.
- questions_and_answers = the exercise rows below the model template.
  Each exercise row = one question with its answer(s) extracted EXACTLY from the PDF.

RULES:
- Title format: unit{N}_model{M}  (e.g., unit1_model1, unit1_model2)
- Type: writing
- questions_and_answers:
  - question_text: extracted EXACTLY from the PDF left column — do not rephrase or make up text
  - type: writing
  - has_answer: true
  - answers: extracted EXACTLY from the PDF right column
      with is_correct: true (they are both valid responses)
    - Do not make up or paraphrase answers
- articles array must be empty []
- metadata must include "model_conversation" containing ONLY the Model template Q/A block text
- are_questions_english: false (questions are in Italian)
- are_questions_generated_by_llm: false
- Use [PAGE X] markers for page_start and page_end

JSON FORMAT (single model based on the image example):
{
  "title": "unit1_model1",
  "type": "writing",
  "questions_and_answers": [
    {
      "sequence_id": 1,
      "question_text": "Scusi, Lei è americano/a?",
      "type": "writing",
      "has_answer": true,
      "answers": [
        {"answer_text": "Sì, sono americano/a., No, non sono americano/a.", "is_correct": true},
      ]
    },
    {
      "sequence_id": 2,
      "question_text": "Scusi, Lei è dell'Ambasciata?",
      "type": "writing",
      "has_answer": true,
      "answers": [
        {"answer_text": "Sì, sono dell'Ambasciata., No, non sono dell'Ambasciata.", "is_correct": true},
      ]
    },
    {
      "sequence_id": 3,
      "question_text": "Scusi, Lei è italiano/a?",
      "type": "writing",
      "has_answer": true,
      "answers": [
        {"answer_text": "Sì, sono italiano/a., No, non sono italiano/a.", "is_correct": true}
      ]
    }
  ],
  "articles": [],
  "metadata": {
    "page_start": 16,
    "page_end": 18,
    "are_questions_english": false,
    "are_questions_generated_by_llm": false,
    "model_conversation": "Model 1\n(affirmative) Q: Scusi, Lei è americano/a?\n(affirmative) A: Sì, sono americano/a.\n(negative) A: No, non sono americano/a."
  }
}

If multiple models exist, return a JSON array: [{...model1...}, {...model2...}]

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    parser = make_arg_parser("Extract writing model lessons from Italian unit PDF")
    args = parser.parse_args()
    run_from_args(agent, args)
