from fpdf import FPDF
import os

class PDFInvoice(FPDF):
    def header(self):
        self.image('/Users/birukzewdie/Desktop/Tutoring/tutor_sys/templates/images/logo.png', 10, 8, 33)  # Add your logo here
        self.set_font('Arial', 'B', 12)
        self.cell(80)
        self.cell(30, 10, 'Your Company Name', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(80)
        self.cell(30, 10, 'Your Company Address', 0, 1, 'C')
        self.cell(80)
        self.cell(30, 10, 'Phone: +1-234-567-890 | Email: info@yourcompany.com', 0, 1, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def invoice_body(self, student_name, invoice_details):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Invoice', 0, 1, 'C')
        self.set_font('Arial', '', 12)
        self.cell(100, 10, f'Student Name: {student_name}', 0, 1)
        self.cell(100, 10, f'Invoice Date: {invoice_details["date"]}', 0, 1)
        self.cell(100, 10, f'Due Date: {invoice_details["due_date"]}', 0, 1)
        self.cell(100, 10, f'Invoice Number: {invoice_details["invoice_number"]}', 0, 1)
        
        self.ln(10)
        self.set_font('Arial', 'B', 12)
        self.cell(40, 10, 'Description', 1)
        self.cell(40, 10, 'Hours Attended', 1)
        self.cell(40, 10, 'Hourly Rate', 1)
        self.cell(40, 10, 'Amount Due', 1)
        self.ln()

        # Table body
        self.set_font('Arial', '', 12)
        self.cell(40, 10, 'Tutoring Services', 1)
        self.cell(40, 10, str(invoice_details['hours_attended']), 1)
        self.cell(40, 10, f"${invoice_details['hourly_rate']:.2f}", 1)
        self.cell(40, 10, f"${invoice_details['total_due']:.2f}", 1)
        self.ln()

        # Total
        self.set_font('Arial', 'B', 12)
        self.cell(120, 10, 'Total Amount Due', 1)
        self.cell(40, 10, f"${invoice_details['total_due']:.2f}", 1, 1, 'R')
        # Payment instructions
        self.ln(10)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 10, 'Please make payment by the due date. Contact us if you have any questions about this invoice.\n\nThank you for your business!')

def generate_invoice(student_name, invoice_details, output_folder='generated_invoices/'):
    """Generate a PDF invoice for the student."""
    # Check the structure of invoice_details
    if not isinstance(invoice_details, dict):
        raise TypeError("invoice_details must be a dictionary")

    # Ensure the necessary keys are present
    required_keys = ["date", "due_date", "invoice_number", "hours_attended", "hourly_rate", "total_due"]
    for key in required_keys:
        if key not in invoice_details:
            raise KeyError(f"Missing key in invoice_details: {key}")
    
    pdf = PDFInvoice()
    pdf.add_page()
    pdf.invoice_body(student_name, invoice_details)

    pdf_filename = os.path.join(output_folder, f"{student_name}_invoice.pdf")
    pdf.output(pdf_filename)

    print(f"Invoice generated for {student_name}: {pdf_filename}")


