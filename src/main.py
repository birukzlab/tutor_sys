from sheets_integration import get_sheet_data, update_sheet_data
from calculations import update_billing_info
from pdf_generation import generate_invoice
from email_sending import send_email_with_invoice

RANGE_NAME_BILLING = 'Billing!A1:G'
RANGE_NAME_ATTENDANCE = 'Attendance!A1:D'
RANGE_NAME_STUDENT_INFO = 'StudentInformation!A1:I'

if __name__ == "__main__":
    billing_data = get_sheet_data(RANGE_NAME_BILLING)
    attendance_data = get_sheet_data(RANGE_NAME_ATTENDANCE)
    student_info_data = get_sheet_data(RANGE_NAME_STUDENT_INFO)

    updated_billing_data = update_billing_info(billing_data, attendance_data)
    for row in updated_billing_data[1:]:  
        student_name = row[0]
        hours_attended = row[1]
        hourly_rate = float(row[2])
        total_due = float(row[3])
        invoice_details = {
            "date": "2024-08-31",
            "due_date": "2024-09-15",
            "invoice_number": f"INV-{row[0].replace(' ', '_')}-{row[3]}",
            "hours_attended": hours_attended,
            "hourly_rate": hourly_rate,
            "total_due": total_due
        }

        print("Invoice details:", invoice_details)

        generate_invoice(student_name, invoice_details)

        parent_email = next((info[5] for info in student_info_data if info[1] == student_name), None)

        invoice_path = f"generated_invoices/{student_name}_invoice.pdf"
        if parent_email:
            send_email_with_invoice(parent_email, student_name, invoice_path)

    update_sheet_data(RANGE_NAME_BILLING, updated_billing_data)
