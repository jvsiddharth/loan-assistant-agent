"""
mock_data.py

Mock database for the Home Loan AI Assistant.

In production these would come from:

- PostgreSQL
- Supabase
- CRM
- Loan Management System
"""

# =====================================================
# CLIENTS
# =====================================================

CLIENTS = {
    "9876543210": {
        "name": "Rahul Sharma",
        "phone": "9876543210",
        "application_id": "HL1001",
        "loan_amount": 4500000,
        "property_value": 6500000,
        "stage": "Credit Review",
        "advisor": "Priya Mehta",
        "advisor_email": "priya@homeloans.com",
        "documents_pending": [
            "Salary Slip",
            "Bank Statement"
        ]
    },

    "9999999999": {
        "name": "Ananya Patel",
        "phone": "9999999999",
        "application_id": "HL1002",
        "loan_amount": 6200000,
        "property_value": 8500000,
        "stage": "Sanction Approved",
        "advisor": "Rohit Gupta",
        "advisor_email": "rohit@homeloans.com",
        "documents_pending": []
    },

    "8888888888": {
        "name": "Vikram Singh",
        "phone": "8888888888",
        "application_id": "HL1003",
        "loan_amount": 3500000,
        "property_value": 5000000,
        "stage": "Documents Pending",
        "advisor": "Neha Kapoor",
        "advisor_email": "neha@homeloans.com",
        "documents_pending": [
            "PAN Card",
            "Property Documents"
        ]
    },

    "7777777777": {
        "name": "Sneha Joshi",
        "phone": "7777777777",
        "application_id": "HL1004",
        "loan_amount": 5200000,
        "property_value": 7000000,
        "stage": "Disbursed",
        "advisor": "Amit Verma",
        "advisor_email": "amit@homeloans.com",
        "documents_pending": []
    }
}


# =====================================================
# OTP STORE
# =====================================================

OTP_STORE = {}

# Example:
#
# {
#     "9123456789": "4821"
# }


# =====================================================
# DOCUMENT SUBMISSION LOGS
# =====================================================

DOCUMENT_LOGS = []

# Example:
#
# [
#     {
#         "phone": "9876543210",
#         "document_name": "Salary Slip"
#     }
# ]


# =====================================================
# ADVISOR NOTIFICATIONS
# =====================================================

ADVISOR_NOTIFICATIONS = []

# Example:
#
# [
#     {
#         "advisor": "Priya Mehta",
#         "message": "Customer uploaded Salary Slip"
#     }
# ]


# =====================================================
# LEADS
# =====================================================

LEADS = []

# Example:
#
# [
#     {
#         "name": "John Doe",
#         "phone": "9123456789",
#         "requirement": "Need home loan consultation"
#     }
# ]


# =====================================================
# HOME LOAN JOURNEY
# =====================================================

HOME_LOAN_APPLICATION_LINK = (
    "https://apply.homeloans.demo"
)