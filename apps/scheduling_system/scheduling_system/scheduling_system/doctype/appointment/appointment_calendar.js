frappe.views.calendar["Appointment"] = {
    field_map: {
        start: "start_date",     
        end: "end_date",       
        title: "client_name",    
        status: "status",         
        allDay: "all_day",       
        id: "name",                        
    },

    get_css_class: function(data) {
        if (data.status === "Scheduled") {
            return "blue";
        } else if (data.status === "Finished") {
            return "green";
        } else if (data.status === "Canceled") {
            return "red";
        }
        return "";
    },
    order_by: "start_date",
    get_events_method: "scheduling_system.scheduling_system.doctype.appointment.appointment.get_events"
};