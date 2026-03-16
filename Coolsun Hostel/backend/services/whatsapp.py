class WhatsAppService:
    def __init__(self, api_key=None):
        self.api_key = api_key
        # Stub: Future implementation for Meta API

    def send_template_message(self, phone_number, template_name, variables=None):
        """
        Send a template message to a user.
        Stub implementation.
        """
        print(f"[WhatsApp Stub] Sending {template_name} to {phone_number} with {variables}")
        return True

    def send_task_alert(self, admin_phone, task_title, priority):
        """
        Send a task alert with interactive buttons.
        """
        variables = {"task_title": task_title, "priority": priority}
        return self.send_template_message(admin_phone, "task_alert", variables)
