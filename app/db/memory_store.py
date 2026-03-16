# Copyright (c) Dario Pizzolante
from typing import Dict

from app.models.schemas import ApprovalItem, EmailWorkflowResponse


WORKFLOW_RUNS: Dict[str, EmailWorkflowResponse] = {}
APPROVALS: Dict[str, ApprovalItem] = {}
