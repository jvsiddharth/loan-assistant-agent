import json
import os
import re

from dotenv import load_dotenv
from groq import Groq

from tools import (
    TOOLS_SCHEMA,
    execute_tool
)

load_dotenv()

SYSTEM_PROMPT = """
You are an AI Home Loan Assistant.

You help users with:

- Home loan questions
- Home loan eligibility
- Interest rates
- Loan process
- Advisor requests

Use tool results as the source of truth.

Never invent customer information.

Never expose internal tool names.
"""


class HomeLoanAgent:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found"
            )

        self.client = Groq(
            api_key=api_key
        )

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        self.customer_phone = None
        self.customer_name = None

        self.is_verified = False
        self.awaiting_otp = False

    def _extract_phone(
        self,
        text
    ):

        match = re.search(
            r"\b\d{10}\b",
            text
        )

        if match:
            return match.group()

        return None

    def process_message(
        self,
        user_message
    ):

        message_lower = (
            user_message.lower()
        )

        # ==========================================
        # OTP FLOW
        # ==========================================

        if self.awaiting_otp:

            result = execute_tool(
                "verify_otp",
                {
                    "phone":
                        self.customer_phone,
                    "otp":
                        user_message.strip()
                }
            )

            if result.get(
                "verified"
            ):

                self.awaiting_otp = False
                self.is_verified = True

                lookup = execute_tool(
                    "lookup_client",
                    {
                        "phone":
                            self.customer_phone
                    }
                )

                if lookup.get("found"):

                    self.customer_name = (
                        lookup["client"]["name"]
                    )

                    return (
                        f"Verification successful.\n\n"
                        f"Welcome back "
                        f"{self.customer_name}. "
                        f"How can I help you today?"
                    )

                return (
                    "Verification successful.\n\n"
                    "How may I assist you today?"
                )

            return (
                "Invalid OTP. "
                "Please try again."
            )

        # ==========================================
        # PHONE DETECTION
        # ==========================================

        phone = self._extract_phone(
            user_message
        )

        if (
            phone
            and not self.is_verified
        ):

            self.customer_phone = phone

            lookup = execute_tool(
                "lookup_client",
                {
                    "phone": phone
                }
            )

            execute_tool(
                "send_otp",
                {
                    "phone": phone
                }
            )

            self.awaiting_otp = True

            if lookup.get("found"):

                return (
                    "I found an account "
                    "associated with this "
                    "phone number.\n\n"
                    "I've sent an OTP.\n\n"
                    "Please enter it."
                )

            return (
                "I've sent an OTP.\n\n"
                "Please enter it."
            )

        # ==========================================
        # PROTECTED CUSTOMER ACTIONS
        # ==========================================

        if (
            not self.is_verified
            and any(
                word in message_lower
                for word in [
                    "status",
                    "application",
                    "document",
                    "pending"
                ]
            )
        ):

            return (
                "For security purposes, "
                "please provide your "
                "registered phone number "
                "first."
            )

        # ==========================================
        # APPLICATION STATUS
        # ==========================================

        if (
            self.is_verified
            and (
                "status" in message_lower
                or "application status"
                in message_lower
            )
        ):

            result = execute_tool(
                "get_application_status",
                {
                    "phone":
                        self.customer_phone
                }
            )

            if not result.get(
                "success"
            ):
                return (
                    "Unable to retrieve "
                    "application status."
                )

            return (
                f"Your application "
                f"{result['application_id']} "
                f"is currently in "
                f"{result['stage']} stage."
            )

        # ==========================================
        # PENDING DOCUMENTS
        # ==========================================

        if (
            self.is_verified
            and (
                "pending document"
                in message_lower
                or "pending documents"
                in message_lower
                or "documents pending"
                in message_lower
                or "what documents"
                in message_lower
            )
        ):

            result = execute_tool(
                "get_pending_documents",
                {
                    "phone":
                        self.customer_phone
                }
            )

            docs = result.get(
                "documents",
                []
            )

            if not docs:

                return (
                    "There are no pending "
                    "documents for your "
                    "application."
                )

            return (
                "Pending documents:\n\n- "
                + "\n- ".join(docs)
            )

        # ==========================================
        # DOCUMENT UPLOAD
        # ==========================================

        if (
            self.is_verified
            and (
                "uploaded"
                in message_lower
                or "submitted"
                in message_lower
            )
        ):

            document_name = (
                "Document"
            )

            if (
                "salary"
                in message_lower
            ):
                document_name = (
                    "Salary Slip"
                )

            elif (
                "bank"
                in message_lower
            ):
                document_name = (
                    "Bank Statement"
                )

            elif (
                "pan"
                in message_lower
            ):
                document_name = (
                    "PAN Card"
                )

            execute_tool(
                "log_document_submission",
                {
                    "phone":
                        self.customer_phone,
                    "document_name":
                        document_name
                }
            )

            execute_tool(
                "notify_advisor",
                {
                    "phone":
                        self.customer_phone,
                    "message":
                        f"{self.customer_name} "
                        f"uploaded "
                        f"{document_name}"
                }
            )

            return (
                f"Thank you. "
                f"I've recorded your "
                f"{document_name} "
                f"submission and "
                f"informed your advisor."
            )

        # ==========================================
        # ADVISOR REQUEST
        # ==========================================

        if (
            self.is_verified
            and (
                "advisor"
                in message_lower
                or "human"
                in message_lower
                or "call me"
                in message_lower
            )
        ):

            execute_tool(
                "notify_advisor",
                {
                    "phone":
                        self.customer_phone,
                    "message":
                        f"{self.customer_name} "
                        f"requested advisor "
                        f"assistance."
                }
            )

            return (
                "I've informed your "
                "advisor. They will "
                "contact you shortly."
            )

        # ==========================================
        # NORMAL LLM FLOW
        # ==========================================

        self.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        response = (
            self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=self.messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
                temperature=0.3
            )
        )

        message = (
            response.choices[0].message
        )

        if not message.tool_calls:

            reply = message.content

            self.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            return reply

        for tool_call in (
            message.tool_calls
        ):

            tool_name = (
                tool_call.function.name
            )

            arguments = json.loads(
                tool_call.function.arguments
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            self.messages.append(
                {
                    "role": "tool",
                    "tool_call_id":
                        tool_call.id,
                    "name":
                        tool_name,
                    "content":
                        json.dumps(result)
                }
            )

        second_response = (
            self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=self.messages
            )
        )

        reply = (
            second_response
            .choices[0]
            .message
            .content
        )

        self.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        return reply


def create_agent():
    return HomeLoanAgent()
