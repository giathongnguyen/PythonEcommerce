audit_log = []

def log_event(event):
    audit_log.append(event)

def view_audit_log():
    print("\n===== AUDIT LOG =====")
    for entry in audit_log:
        print("-", entry)

