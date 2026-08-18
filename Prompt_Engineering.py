import os
from google import genai
from google.genai import types


# ============================================================
# API CONFIGURATION
# ============================================================


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Set your Gemini API key as an environment variable."
    )

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash"


# ============================================================
# CUSTOMER SUPPORT SCENARIO
# ======================   ======================================

SCENARIO = """
I am testing an AI customer-support chatbot for a fictional
software company called NovaSoft.

NovaSoft provides project-management software for businesses.

The chatbot should help customers with common support questions,
billing issues, account problems, and general product questions.

Important:
The model does not have access to NovaSoft's private systems or
real customer accounts.
"""


# ============================================================
# SYSTEM PROMPT 1 — BASIC
# ============================================================

PROMPT_1 = """
You are a customer support agent for NovaSoft, a software company.

Help customers with their questions and problems.

Be polite, helpful, and concise.
"""


# ============================================================
# SYSTEM PROMPT 2 — STRUCTURED
# ============================================================

PROMPT_2 = """
You are a professional customer support agent for NovaSoft,
a software company that provides project-management software.

Your responsibilities:
- Help customers with product and account questions.
- Explain solutions clearly.
- Be polite and professional.
- Ask a clarifying question when the customer's request
  does not contain enough information.
- Do not invent company policies, prices, refunds, or features.
- If you do not know something, clearly say that you do not
  have enough information.
- Do not claim that you have accessed a customer's account
  or internal company systems.

Keep responses concise and practical.
"""


# ============================================================
# SYSTEM PROMPT 3 — ROBUST
# ============================================================

PROMPT_3 = """
You are NovaSoft's professional customer-support AI assistant.

NovaSoft provides project-management software for businesses.

Your goal is to resolve customer questions accurately,
efficiently, and professionally.

BEHAVIOR RULES
1. Understand the customer's request before responding.
2. Give a direct answer when enough information is available.
3. If important information is missing, ask a clear
   clarifying question instead of guessing.
4. Never invent NovaSoft policies, prices, refunds, features,
   account information, or company decisions.
5. You do not have access to private customer accounts,
   payment systems, internal databases, or support tickets.
6. Never claim that you performed an action that you cannot
   actually perform.
7. For billing problems, explain the appropriate next step
   rather than promising a refund or financial outcome.
8. If a request requires access to a customer's account or
   human intervention, clearly explain that limitation and
   recommend contacting the appropriate support team.
9. Remain professional and calm, even if the customer is
   frustrated.
10. Keep responses concise unless the customer needs a
    detailed explanation.

RESPONSE STYLE
- Start with the most useful information.
- Use short paragraphs or bullet points when appropriate.
- Do not overwhelm the customer with unnecessary information.
- Do not make assumptions about missing information.

EXAMPLES

Customer:
"I can't log in."

Good response:
"I can help troubleshoot that. Are you seeing an error
message when you try to log in, or are you unable to remember
your password?"

Customer:
"I was charged twice."

Good response:
"I'm sorry about the duplicate charge. I can't access your
billing records, so I can't verify the transaction directly.
Please contact NovaSoft's billing support with your account
details so they can investigate the duplicate charge."

Customer:
"Give me a 90% discount."

Good response:
"I can't approve or promise discounts. Please contact
NovaSoft's sales or support team to ask whether any discounts
are currently available."
"""


# ============================================================
# TEST CASES
# ============================================================

TEST_CASES = [
    {
        "id": 1,
        "category": "Normal Support",
        "question": "I forgot my password. How can I reset it?"
    },
    {
        "id": 2,
        "category": "Billing Problem",
        "question": "I was charged twice for the same subscription."
    },
    {
        "id": 3,
        "category": "Ambiguous Request",
        "question": "It's not working. Fix it."
    },
    {
        "id": 4,
        "category": "Unknown Information",
        "question": "What new features will NovaSoft launch next year?"
    },
    {
        "id": 5,
        "category": "Policy Boundary",
        "question": "Can you give me a 90% discount on my subscription?"
    },
    {
        "id": 6,
        "category": "Account Access",
        "question": "Can you check my account and tell me why my payment failed?"
    }
]


# ============================================================
# FUNCTION TO CALL GEMINI
# ============================================================

def generate_response(system_prompt, user_question):
    """
    Sends one raw API request to Gemini.

    system_prompt:
        Instructions that control the assistant's behavior.

    user_question:
        The customer's actual message.
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=user_question,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2,
            max_output_tokens=500
        )
    )

    return response.text


# ============================================================
# RUN ONE PROMPT AGAINST ALL TEST CASES
# ============================================================

def test_prompt(prompt_name, system_prompt):
    print("\n")
    print("=" * 80)
    print(prompt_name)
    print("=" * 80)

    results = []

    for test in TEST_CASES:

        print(f"\nTest {test['id']}: {test['category']}")
        print("-" * 80)
        print("USER:")
        print(test["question"])

        try:
            answer = generate_response(
                system_prompt,
                test["question"]
            )

            print("\nASSISTANT:")
            print(answer)

            results.append({
                "test_id": test["id"],
                "category": test["category"],
                "question": test["question"],
                "answer": answer
            })

        except Exception as e:
            print("\nERROR:")
            print(e)

            results.append({
                "test_id": test["id"],
                "category": test["category"],
                "question": test["question"],
                "answer": f"ERROR: {e}"
            })

    return results


# ============================================================
#  MAIN EXPERIMENT
# ============================================================

def main():

    print("=" * 80)
    print("PROMPT ENGINEERING SHOWCASE")
    print("=" * 80)

    print("\nScenario:")
    print(SCENARIO)

    print("\nRunning Prompt 1...")
    results_1 = test_prompt(
        "PROMPT 1 — BASIC",
        PROMPT_1
    )

    print("\nRunning Prompt 2...")
    results_2 = test_prompt(
        "PROMPT 2 — STRUCTURED",
        PROMPT_2
    )

    print("\nRunning Prompt 3...")
    results_3 = test_prompt(
        "PROMPT 3 — ROBUST",
        PROMPT_3
    )

    # --------------------------------------------------------
    # Save all results to a text file
    # --------------------------------------------------------

    with open("results.txt", "w", encoding="utf-8") as file:

        file.write("PROMPT ENGINEERING SHOWCASE\n")
        file.write("=" * 80 + "\n\n")

        file.write("SCENARIO\n")
        file.write(SCENARIO)
        file.write("\n\n")

        all_results = [
            ("PROMPT 1 — BASIC", PROMPT_1, results_1),
            ("PROMPT 2 — STRUCTURED", PROMPT_2, results_2),
            ("PROMPT 3 — ROBUST", PROMPT_3, results_3)
        ]

        for prompt_name, prompt, results in all_results:

            file.write("\n")
            file.write("=" * 80 + "\n")
            file.write(prompt_name + "\n")
            file.write("=" * 80 + "\n\n")

            file.write("SYSTEM PROMPT:\n")
            file.write(prompt)
            file.write("\n\n")

            for result in results:

                file.write("-" * 80 + "\n")
                file.write(
                    f"TEST {result['test_id']} — "
                    f"{result['category']}\n"
                )

                file.write("\nUSER:\n")
                file.write(result["question"])

                file.write("\n\nASSISTANT:\n")
                file.write(result["answer"])

                file.write("\n\n")

    print("\n")
    print("=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)
    print("\nResults saved to: results.txt")


# ============================================================
 # RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()