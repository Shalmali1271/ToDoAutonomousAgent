import json

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from document import create_word_document
from prompt import PLAN_PROMPT, STEP_PROMPT

load_dotenv()


class AutonomousAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.25,
        )

    async def run(self, user_request: str):

        if not user_request or not user_request.strip():
            raise ValueError("Request cannot be empty.")

        
        
        # PLAN
        plan = await self.create_plan(user_request)

        if "title" not in plan or "plan" not in plan:
            raise ValueError("Planning response is invalid.")

        # Content generation fr
        sections = await self.execute_plan(
            user_request,
            plan["plan"]
        )

        # for creating docx
        document_path = create_word_document(
            title=plan["title"],
            sections=sections
        )

        # response
        return {
            "status": "completed",
            "request": user_request,
            "title": plan["title"],
            "plan": plan["plan"],
            "document": document_path,
        }


    async def create_plan(self, request: str):
        # Get that todo list going.

        parser = JsonOutputParser()
        # Kinda like convo, system says PLAN_PROMPT and user give the request in json format.
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", PLAN_PROMPT),
                ("human", "{request}"),
            ]
        )

        chain = prompt | self.llm | parser

        try:
            ### We can test this fallback plan once, uncomment below line to proceed.
            # raise Exception("Testing fallback")
            
            result = await chain.ainvoke(
                {
                    "request": request
                }
            )
            # fingers crossed
            if "plan" not in result or "title" not in result:
                raise ValueError("Invalid planning response.")

            return result

        except Exception:
            # Simple fallback plan!!
            return {
                "title": "Business Document",
                "plan": [
                    "Write Introduction",
                    "Write Objectives",
                    "Write Scope",
                    "Write Timeline",
                    "Write Conclusion",
                ]
            }


    async def execute_plan(self, user_request: str, plan: list):
        sections = []

        for step in plan:

            section = await self.execute_step(
                user_request=user_request,
                step=step
            )

            sections.append(section)

        return sections


    async def execute_step(self, user_request: str, step: str):
        parser = JsonOutputParser()

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", STEP_PROMPT),
                (
                    "human",
                    """
                    User Request:
                    {request}

                    Current Step:
                    {step}
                    """
                )
            ]
        )

        chain = prompt | self.llm | parser

        try:
            result = await chain.ainvoke(
                {
                    "request": user_request,
                    "step": step
                }
            )
            if "heading" not in result or "content" not in result:
                raise ValueError("Invalid section returned by LLM.")

            return result

        except Exception:
            # Fallback if the model fails
            return {
                "heading": step,
                "content": (
                    f"This section describes '{step}' for the following request:\n\n"
                    f"{user_request}"
                )
            }