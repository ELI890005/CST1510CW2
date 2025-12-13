class ITTicket:
    def __init__(self, row):
        self.id = row["id"]
        self.category = row["category"]
        self.assigned_to = row["assigned_to"]
        self.status = row["status"]
        self.created_at = row["created_at"]
        self.resolved_at = row["resolved_at"]

class SecurityIncident:
    def __init__(self, row):
        self.id = row["id"]
        self.threat_type = row["threat_type"]
        self.severity = row["severity"]
        self.status = row["status"]
        self.opened_at = row["opened_at"]
        self.closed_at = row["closed_at"]
