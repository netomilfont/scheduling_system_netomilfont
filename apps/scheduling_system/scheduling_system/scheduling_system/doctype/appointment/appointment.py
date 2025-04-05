# Copyright (c) 2025, Aglaisio Neto and contributors
# For license information, please see license.txt


from frappe.model.document import Document
from datetime import datetime, timedelta
import frappe


class Appointment(Document):
	
	def before_save(self):
		if self.start_date and self.duration:
			start_date_time = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
			
			hour, minute, second = map(int, self.duration.split(":"))
			duration_delta = self.duration = timedelta(hours=hour, minutes=minute, seconds=second)
			
			self.end_date = start_date_time + duration_delta

			conflicting_appointments = frappe.get_all(
				"Appointment",
				filters={
					"seller": self.seller,
					"start_date": ["<", self.end_date],
					"end_date": [">", start_date_time],
					"name": ["!=", self.name]
				}
			)

			if conflicting_appointments:
				frappe.throw("This appointment conflicts with another appointment.")

@frappe.whitelist()
def get_events(start, end, filters=None):
	filters = frappe.parse_json(filters) if filters else {}

	return frappe.get_all(
		"Appointment",
		filters={"start_date": ["between", [start, end]]},
		fields=["name", "client_name", "start_date", "end_date", "status"],
		order_by="start_date asc"
	)