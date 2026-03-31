"""
Agent: Region (REGIONE section)
Type: reading
Usage: python agent_region.py --pdf "PDF's/Unit2/unit2_region.pdf" --unit 2
"""

from agents import Agent
from common import MODEL, TOOLS, run_agent, make_arg_parser, run_from_args

agent = Agent(
    name="RegionAgent",
    model=MODEL,
    instructions="""
You extract the REGIONE (region) section from an Italian language textbook unit.

STEPS:
1. Call get_unit_number() to get the unit number.
2. Call get_unit_text() to read the PDF content.
3. Extract all content as a READING lesson.
4. Call save_extracted_lessons() with the JSON.

TWO-COLUMN LAYOUT WARNING:
The REGIONE section is formatted as a two-column table in the PDF.
Because PDF text extraction reads left-to-right column by column, the raw extracted text
will appear BROKEN — all the left-column labels come first, then all the right-column
values come after. For example the raw text may look like:

  Confini:
  Monti:
  Fiumi:
  Capoluogo della regione:
  Nord: Lombardia, Veneto
  Appennini (Monte Cimone...)
  Po, Trebbia...
  Bologna

YOU MUST RECONSTRUCT the correct label → value pairs by matching labels (ending with ":")
to their corresponding values in order. The intended output for that example is:

  "Confini: Nord: Lombardia, Veneto | Sud: Toscana, Marche, Repubblica di San Marino | Est: Mare Adriatico | Ovest: Liguria, Piemonte"
  "Monti: Appennini (Monte Cimone, 2163 metri; Falterona, 1634 metri; Fumaiolo, 1408 metri)"
  "Fiumi: Po, Trebbia, Taro, Secchia, Enza, Panaro"
  "Capoluogo della regione: Bologna"

RULES:
- Title format: unit{N}_region
- Type: reading
- Articles: each LABEL + its VALUE = one article entry (label and value joined on the same line)
  - Format: "Label: value1 | value2 | value3" when a label has multiple sub-items (e.g. Confini has Nord/Sud/Est/Ovest)
  - Do NOT create separate article entries for lone labels without their value
  - Do NOT create separate article entries for values without their label
  - For Sigle automobilistiche (car codes), group all codes into a single article:
    e.g. "Sigle automobilistiche: BO = Bologna | PC = Piacenza | FE = Ferrara | ..."
- Questions: generate exactly 10 multiple choice questions from the content
  - Each question has exactly 4 answer options, only one correct
  - Questions must be in English and direct (no "according to the passage" phrasing)
- are_questions_english: true
- are_questions_generated_by_llm: true
- Use [PAGE X] markers for page_start and page_end

JSON FORMAT:
{
  "title": "unit1_region",
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
    {"sequence_id": 1, "text": "EMILIA-ROMAGNA"},
    {"sequence_id": 2, "text": "Confini: Nord: Lombardia, Veneto | Sud: Toscana, Marche, Repubblica di San Marino | Est: Mare Adriatico | Ovest: Liguria, Piemonte"},
    {"sequence_id": 3, "text": "Monti: Appennini (Monte Cimone, 2163 metri; Falterona, 1634 metri; Fumaiolo, 1408 metri)"},
    {"sequence_id": 4, "text": "Fiumi: Po, Trebbia, Taro, Secchia, Enza, Panaro"},
    {"sequence_id": 5, "text": "Capoluogo della regione: Bologna"},
    {"sequence_id": 6, "text": "Capoluoghi di provincia: Bologna, Ferrara, Forlì, Parma, Piacenza, Modena, Ravenna, Reggio-Emilia"},
    {"sequence_id": 7, "text": "Sigle automobilistiche: BO = Bologna | PC = Piacenza | FE = Ferrara | PR = Parma | RE = Reggio Emilia | FO = Forlì | MO = Modena | RA = Ravenna"},
    {"sequence_id": 8, "text": "Prodotti agricoli: grano, granoturco, canapa, barbabietole da zucchero, foraggi, frutta"},
    {"sequence_id": 9, "text": "Industrie: salumifici, caseifici, pastifici, zuccherifici"},
    {"sequence_id": 10, "text": "Curiosità: Terra del Sole (Forlì): una città costruita nel 1564, in perfetto stato di conservazione"}
  ],
  "metadata": {
    "page_start": 27,
    "page_end": 30,
    "are_questions_english": true,
    "are_questions_generated_by_llm": true
  }
}

Return ONLY valid JSON. No markdown, no explanations.
""",
    tools=TOOLS,
)

if __name__ == "__main__":
    args = make_arg_parser("Extract region reading lesson from Italian unit PDF").parse_args()
    run_from_args(agent, args)
