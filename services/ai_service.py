from ai.service import generate_response
from ai.prompts import SYSTEM_PROMPTS
from services.router_service import RouterService

from services.pdf_service import PDFService
from services.web_service import WebService
from services.memory_service import MemoryService

import streamlit as st


class AIService:

    @staticmethod
    def get_response(messages):

        # ---------------- Personality ---------------- #

        personality = st.session_state.get(
            "personality",
            "Default"
        )

        personality_prompt = SYSTEM_PROMPTS.get(
            personality,
            SYSTEM_PROMPTS["Default"]
        )

        system_prompt = personality_prompt

        # ---------------- Latest User Question ---------------- #

        user_question = messages[-1]["content"]

        pdf_sources = []

        # ---------------- PDF Search ---------------- #

        if st.session_state.get("use_pdf", True):

            try:

                pdf_context, pdf_sources = PDFService.get_context(
                    user_question
                )

                if pdf_context:

                    system_prompt += f"""

==================================================
PDF CONTEXT
==================================================

{pdf_context}

==================================================

Instructions:

1. Use the PDF context whenever it contains the answer.

2. If the answer is partially available,
combine the PDF with your own knowledge.

3. If Web Search results are also available,
combine both intelligently.

4. Never invent information that contradicts the PDF.
"""

            except Exception as e:

                print("PDF Error:", e)

        # ---------------- Web Search ---------------- #

        if st.session_state.get("use_web", False):

            try:

                web_context = WebService.search(
                    user_question
                )

                if web_context:

                    system_prompt += f"""

==================================================
WEB SEARCH RESULTS
==================================================

{web_context}

==================================================

Use the web search results when they help answer
the user's question.

If the answer comes from web search,
mention it naturally in your response.
"""

            except Exception as e:

                print("Web Error:", e)

        # ---------------- Conversation Memory ---------------- #

        conversation = MemoryService.build_context(
            messages=messages,
            max_messages=12
        )

        # ---------------- Final Prompt ---------------- #

        final_messages = [

            {
                "role": "system",
                "content": system_prompt
            }

        ]

        final_messages.extend(conversation)

        # ---------------- AI Response ---------------- #

        try:

            answer = generate_response(
                final_messages
            )

        except Exception as e:

            print("AI Error:", e)

            return (
                "❌ Sorry, something went wrong while "
                "generating the response."
            )

        # ---------------- PDF Sources ---------------- #

        if pdf_sources:

            answer += "\n\n---\n"

            answer += "📄 **Sources**\n"

            seen = set()

            for source in pdf_sources:

                key = (
                    source["document"],
                    source["page"]
                )

                if key in seen:
                    continue

                seen.add(key)

                answer += (
                    f"\n• {source['document']} "
                    f"(Page {source['page']})"
                )

        return answer