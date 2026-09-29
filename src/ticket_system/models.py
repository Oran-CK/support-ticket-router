from enum import Enum
from pydantic import BaseModel, Field

class Department(str, Enum):
    INFRASTRUCTURE = "Infrastructure"
    BILLING = "Billing"
    SECURITY = "Security"
    SUPPORT = "Support"

class Urgency(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ClassificationOutput(BaseModel):
    department: Department = Field(
        ...,
        description=(
            "Primary operational team to handle this request: "
            "Infrastructure for server/database/network downtime, "
            "Billing for payments/invoices/refunds, "
            "Security for unauthorized access/vulnerabilities, "
            "or Support for user accounts/how-to guidance."
        ),
    )
    urgency: Urgency = Field(
        ...,
        description=(
            "Operational severity: "
            "CRITICAL for production outages and system-wide downtime, "
            "HIGH for severe degradation or blocked workflows, "
            "MEDIUM for billing issues or single-user bugs, "
            "LOW for general questions and cosmetic requests."
        ),
    )