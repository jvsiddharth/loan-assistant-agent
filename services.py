from mock_data import (
    CLIENTS,
    OTP_STORE,
    DOCUMENT_LOGS,
    ADVISOR_NOTIFICATIONS,
    LEADS,
    HOME_LOAN_APPLICATION_LINK
)


# =====================================================
# HELPERS
# =====================================================

def normalize_phone(phone: str) -> str:
    """
    Convert phone into a normalized
    10-digit format.
    """

    digits = "".join(
        c for c in str(phone)
        if c.isdigit()
    )

    return digits[-10:]


# =====================================================
# CLIENT LOOKUP
# =====================================================

def lookup_client_service(phone: str):

    phone = normalize_phone(phone)

    client = CLIENTS.get(phone)

    if not client:

        return {
            "success": False,
            "found": False,
            "message": "Client not found"
        }

    return {
        "success": True,
        "found": True,
        "client": {
            "name": client["name"],
            "phone": client["phone"],
            "application_id": client["application_id"],
            "stage": client["stage"],
            "advisor": client["advisor"]
        }
    }


# =====================================================
# OTP
# =====================================================

def send_otp_service(phone: str):

    phone = normalize_phone(phone)

    otp = "1234"

    OTP_STORE[phone] = otp

    print(
        f"\n[MOCK OTP SENT]"
        f"\nPhone: {phone}"
        f"\nOTP: {otp}\n"
    )

    return {
        "success": True,
        "phone": phone
    }


def verify_otp_service(
    phone: str,
    otp: str
):

    phone = normalize_phone(phone)

    stored_otp = OTP_STORE.get(phone)

    verified = (
        stored_otp is not None
        and str(stored_otp) == str(otp)
    )

    return {
        "success": verified,
        "verified": verified
    }


# =====================================================
# APPLICATION STATUS
# =====================================================

def get_application_status_service(
    phone: str
):

    phone = normalize_phone(phone)

    client = CLIENTS.get(phone)

    if not client:

        return {
            "success": False,
            "message": "Client not found"
        }

    return {
        "success": True,
        "application_id":
            client["application_id"],
        "stage":
            client["stage"],
        "loan_amount":
            client["loan_amount"]
    }


# =====================================================
# PENDING DOCUMENTS
# =====================================================

def get_pending_documents_service(
    phone: str
):

    phone = normalize_phone(phone)

    client = CLIENTS.get(phone)

    if not client:

        return {
            "success": False,
            "message": "Client not found"
        }

    return {
        "success": True,
        "documents":
            list(
                client["documents_pending"]
            )
    }


# =====================================================
# DOCUMENT SUBMISSION
# =====================================================

def log_document_submission_service(
    phone: str,
    document_name: str
):

    phone = normalize_phone(phone)

    DOCUMENT_LOGS.append(
        {
            "phone": phone,
            "document_name":
                document_name
        }
    )

    client = CLIENTS.get(phone)

    if client:

        pending_docs = (
            client["documents_pending"]
        )

        if (
            document_name
            in pending_docs
        ):
            pending_docs.remove(
                document_name
            )

    return {
        "success": True,
        "document_name":
            document_name
    }


# =====================================================
# ADVISOR NOTIFICATION
# =====================================================

def notify_advisor_service(
    phone: str,
    message: str
):

    phone = normalize_phone(phone)

    client = CLIENTS.get(phone)

    if not client:

        return {
            "success": False,
            "message": "Client not found"
        }

    notification = {
        "advisor":
            client["advisor"],
        "advisor_email":
            client["advisor_email"],
        "message":
            message
    }

    ADVISOR_NOTIFICATIONS.append(
        notification
    )

    print(
        f"\n[ADVISOR NOTIFIED]"
        f"\nAdvisor: "
        f"{client['advisor']}"
        f"\nMessage: "
        f"{message}\n"
    )

    return {
        "success": True,
        "advisor":
            client["advisor"]
    }


# =====================================================
# CREATE LEAD
# =====================================================

def create_lead_service(
    name: str,
    phone: str,
    requirement: str
):

    phone = normalize_phone(phone)

    lead = {
        "name": name,
        "phone": phone,
        "requirement": requirement
    }

    LEADS.append(
        lead
    )

    print(
        f"\n[NEW LEAD CREATED]"
        f"\nName: {name}"
        f"\nPhone: {phone}"
        f"\nRequirement: "
        f"{requirement}\n"
    )

    return {
        "success": True,
        "lead": lead
    }


# =====================================================
# HOME LOAN JOURNEY LINK
# =====================================================

def get_home_loan_link_service():

    return {
        "success": True,
        "url":
            HOME_LOAN_APPLICATION_LINK
    }

