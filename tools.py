"""
tools.py

Defines:

1. Tool schemas exposed to the LLM
2. Tool registry mapping tool names to services

No business logic should exist here.
"""

from services import (
    lookup_client_service,
    send_otp_service,
    verify_otp_service,
    get_application_status_service,
    get_pending_documents_service,
    log_document_submission_service,
    notify_advisor_service,
    create_lead_service,
)

# =====================================================
# TOOL REGISTRY
# =====================================================

TOOL_REGISTRY = {
    "lookup_client": lookup_client_service,
    "send_otp": send_otp_service,
    "verify_otp": verify_otp_service,
    "get_application_status": get_application_status_service,
    "get_pending_documents": get_pending_documents_service,
    "log_document_submission": log_document_submission_service,
    "notify_advisor": notify_advisor_service,
    "create_lead": create_lead_service,
}


# =====================================================
# OPENAI / GROQ TOOL SCHEMAS
# =====================================================

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "lookup_client",
            "description": (
                "Lookup an existing home loan client using phone number."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string",
                        "description": "Customer phone number"
                    }
                },
                "required": ["phone"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "send_otp",
            "description": (
                "Generate and send OTP to an unrecognized user."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string"
                    }
                },
                "required": ["phone"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "verify_otp",
            "description": (
                "Verify OTP submitted by the user."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string"
                    },
                    "otp": {
                        "type": "string"
                    }
                },
                "required": [
                    "phone",
                    "otp"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_application_status",
            "description": (
                "Get the current application status of an existing customer."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string"
                    }
                },
                "required": ["phone"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_pending_documents",
            "description": (
                "Get pending documents required for a customer's application."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string"
                    }
                },
                "required": ["phone"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "log_document_submission",
            "description": (
                "Record that a customer submitted a document."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string"
                    },
                    "document_name": {
                        "type": "string"
                    }
                },
                "required": [
                    "phone",
                    "document_name"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "notify_advisor",
            "description": (
                "Notify the assigned advisor regarding a customer action."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {
                        "type": "string"
                    },
                    "message": {
                        "type": "string"
                    }
                },
                "required": [
                    "phone",
                    "message"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "create_lead",
            "description": (
                "Create a lead for a new prospect who wants to speak with an advisor."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "phone": {
                        "type": "string"
                    },
                    "requirement": {
                        "type": "string"
                    }
                },
                "required": [
                    "name",
                    "phone",
                    "requirement"
                ]
            }
        }
    }
]


# =====================================================
# EXECUTION HELPER
# =====================================================

def execute_tool(tool_name: str, arguments: dict):
    """
    Executes a tool selected by the LLM.
    """

    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    try:
        return TOOL_REGISTRY[tool_name](**arguments)

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }