"""
Agent: AT THE AIRPORT (or similar location-based section)
Type: reading
Usage: python agent_at_the_airport.py --pdf "PDF's/Unit2/unit2_at_the_airport.pdf" --unit 2
"""

from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="AtTheAirportAgent",
    model=MODEL,
    instructions="""
You extract the "AT THE AIRPORT" (or similar location-based reading section) from an Italian language textbook unit.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Extract all content as a READING lesson.
4. Call save_extracted_lessons() with the JSON.

TITLE NAMING RULE:
- Read the main section heading from the PDF (e.g. "AT THE AIRPORT", "AT THE EXCHANGE OFFICE", "AT THE HOTEL I", "GOING BY TAXI", etc.)
- Convert it to snake_case (all lowercase, spaces replaced with underscores, roman numerals kept as-is)
- Title format: unit{N}_{snake_case_lesson_name}
- Examples:
    "AT THE AIRPORT I"         → unit1_at_the_airport_i
    "AT THE AIRPORT II"        → unit1_at_the_airport_ii
    "AT THE EXCHANGE OFFICE"   → unit3_at_the_exchange_office
    "GETTING THE LOCAL TIME"   → unit4_getting_the_local_time
    "AT THE HOTEL I"           → unit5_at_the_hotel_i
    "AT THE HOTEL II"          → unit6_at_the_hotel_ii
    "AT THE HOTEL III"         → unit7_at_the_hotel_iii
    "AT THE HOTEL IV"          → unit8_at_the_hotel_iv
    "GOING BY TAXI"            → unit9_going_by_taxi
    "GETTING AROUND"           → unit10_getting_around
    "AT THE EMBASSY I"         → unit11_at_the_embassy_i
    "AT THE EMBASSY II"        → unit12_at_the_embassy_ii
    "SHOPPING FOR CLOTHES"     → unit13_shopping_for_clothes
    "AT THE SHOE STORE"        → unit14_at_the_shoe_store
    "EATING OUT I"             → unit15_eating_out_i
    "EATING OUT II"            → unit16_eating_out_ii
    "PHONE CALL"               → unit17_phone_call

RULES:
- Type: reading
- Articles: each sentence or logical line = one article entry with sequential sequence_id
- The PDF may contain Fill-in-the-Blank. For each:
  - Extract the full question exactly as written
  - Convert to MULTIPLE CHOICE format
  - Generate exactly 4 answer options, only one correct
  - The correct answer must match the book's intended answer or be derived from context.
  - Extract all the fill in the blanks as questions, even if more than 10.
- If the PDF has no questions at all, generate 10 multiple choice questions from the content
- Use [PAGE X] markers to set accurate page_start and page_end
- are_questions_english: true
- are_questions_generated_by_llm: true if questions were generated, false if from book
- if the last page contain "TAKING IT APART" heading don't include it thats the next section.
- in "SEEING IT also extract the dialogs as articles with sequence_id and text."
- in answer_text give commas between multiple answers.
- don't forget to extract the speaker of the dialog as part of the article text which is under "SEEING IT" heading, for example: "Lei: 2. Sì, sono io." extract the whole thing as text, don't just extract "Sì, sono io."

JSON FORMAT:
{
  "title": "unit{N}_{snake_case_lesson_name}",
  "type": "reading",
  "questions_and_answers": [
    {
      "sequence_id": 1,
      "question_text": "Buongiorno. ________, prego.",
      "type": "multiple_choice",
      "has_answer": true,
      "answers": [
        {"answer_text": "Passaporto", "is_correct": true},
        {"answer_text": "Carrello", "is_correct": false},
        {"answer_text": "Consolato", "is_correct": false},
        {"answer_text": "Biglietto", "is_correct": false}
      ]
    }
  ],
  "articles": [
    {"sequence_id": 1, "text": "First sentence or line."}
  ],
  "metadata": {
    "page_start": 3,
    "page_end": 6,
    "are_questions_english": true,
    "are_questions_generated_by_llm": false
  }
}

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    args = make_arg_parser("Extract AT THE AIRPORT reading lesson from Italian unit PDF").parse_args()
    run_from_args(agent, args)
