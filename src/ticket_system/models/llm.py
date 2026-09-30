from pydantic import BaseModel, Field

from ticket_system.models.enum import (
    Department,
    Urgency
)

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