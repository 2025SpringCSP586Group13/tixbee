import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import qrcode
from io import BytesIO
from datetime import datetime

class EmailService:
    def __init__(self):
        # Email configuration
        self.sender_email = "tixbee777@gmail.com"  # Replace with your Gmail
        self.sender_password = "eeso ufjs ppzj avfp"   # Replace with your app password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def generate_booking_qr(self, booking_details):
        """Generate QR code for booking details"""
        # Create QR code data
        qr_data = f"""
        Visitor Name: {booking_details['customer_name']}
        Booking ID: {booking_details['booking_id']}
        Attraction: {booking_details['attraction']}
        Visit Date: {booking_details['visit_date']}
        Tickets: {booking_details['ticket_count']}
        """
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return img_byte_arr

    def create_email_template(self, booking_details):
        try:
            # Convert date to more readable format
            date_obj = datetime.strptime(booking_details['visit_date'], '%Y-%m-%d')
            formatted_date = f"{date_obj.strftime('%d-%m-%Y')} ({date_obj.strftime('%A')})"
            
            # Create QR code with enhanced details
            qr_data = f"""
            Visitor: {booking_details['customer_name']}
            Booking ID: {booking_details['booking_id']}
            Attraction: {booking_details['attraction']}
            Visit Date: {formatted_date}
            Tickets: {booking_details['ticket_count']}
            Amount: ₹{booking_details['amount']}
            """
            
            return f"""
            <div style="font-family: Arial, sans-serif;">
                <h2 style="text-align: center; background-color: #4CAF50; color: white; padding: 20px; margin: 0;">
                    Booking Confirmation 🎫
                </h2>
                <p style="text-align: center; background-color: #4CAF50; color: white; padding: 10px; margin: 0;">
                    Thank you for choosing TixBee! ✨
                </p>
                
                <div style="padding: 20px;">
                    <p>Hey {booking_details['customer_name']}! 👋</p>
                    
                    <p>Your booking has been confirmed! Here are your booking details: 📋</p>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Booking ID</td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{booking_details['booking_id']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Attraction</td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{booking_details['attraction']} 🏰</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Visit Date</td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{formatted_date} 📅</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Tickets</td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{booking_details['ticket_count']} 🎟️</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Amount Paid</td>
                            <td style="padding: 8px; border: 1px solid #ddd;">₹{booking_details['amount']} 💰</td>
                        </tr>
                    </table>

                    <div style="text-align: center; margin: 20px 0;">
                        <p><strong>Your Entry QR Code:</strong></p>
                        <img src="cid:booking_qr" alt="Booking QR Code" style="width: 200px;">
                    </div>

                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Important Information:</strong> ℹ️</p>
                        <ul style="margin: 10px 0;">
                            <li>Please arrive 15 minutes before your scheduled time ⏰</li>
                            <li>Keep this QR code handy for entry 📱</li>
                            <li>This ticket is non-transferable 🚫</li>
                        </ul>
                    </div>

                    <p style="text-align: center; color: #666;">
                        For any queries, please contact us at support@tixbee.com
                    </p>
                </div>
            </div>
            """
        except Exception as e:
            print(f"Error creating email template: {e}")
            return None

    def send_confirmation_email(self, booking_details, recipient_email):
        """Send booking confirmation email"""
        try:
            print(f"Attempting to send email to: {recipient_email}")
            print(f"Booking details: {booking_details}")
            
            # Create message container
            msg = MIMEMultipart('related')
            msg['Subject'] = f"TixBee Booking Confirmation - {booking_details['booking_id']}"
            msg['From'] = self.sender_email
            msg['To'] = recipient_email

            # Generate booking QR code
            print("Generating booking QR code...")
            booking_qr = self.generate_booking_qr(booking_details)

            # Create HTML content
            print("Creating email template...")
            html_content = self.create_email_template(booking_details)
            msg.attach(MIMEText(html_content, 'html'))

            # Attach booking QR code
            print("Attaching QR code...")
            booking_qr_img = MIMEImage(booking_qr)
            booking_qr_img.add_header('Content-ID', '<booking_qr>')
            msg.attach(booking_qr_img)

            print("Connecting to SMTP server...")
            # Connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                print("Logging in...")
                server.login(self.sender_email, self.sender_password)
                print("Sending email...")
                server.send_message(msg)

            print("Email sent successfully!")
            return True, "Email sent successfully!"

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False, f"Error sending email: {str(e)}"

    def create_booking_qr(self, booking_details):
        """Create QR code for booking confirmation"""
        try:
            # Include customer name in QR data
            qr_data = f"""
            Visitor: {booking_details['customer_name']}
            Booking ID: {booking_details['booking_id']}
            Attraction: {booking_details['attraction']}
            Visit Date: {booking_details['visit_date']}
            Tickets: {booking_details['ticket_count']}
            Amount: ₹{booking_details['amount']}
            """
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            img_byte_arr = BytesIO()
            qr_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return img_byte_arr

        except Exception as e:
            print(f"Error creating QR code: {str(e)}")
            return None

# Example usage:
"""
booking_details = {
    'booking_id': 'TIX' + datetime.now().strftime('%Y%m%d%H%M%S'),
    'customer_name': 'John Doe',
    'attraction': 'Bangalore Palace',
    'visit_date': '2024-03-20',
    'ticket_count': '2 Adults, 1 Child',
    'amount': '1500'
}

email_service = EmailService()
success, message = email_service.send_confirmation_email(
    booking_details,
    'recipient@example.com'
)
print(message)
"""

# Test the email service
if __name__ == "__main__":
    # Test booking details
    test_booking = {
        'booking_id': 'TIX' + datetime.now().strftime('%Y%m%d%H%M%S'),
        'customer_name': 'Test User',
        'attraction': 'Bangalore Palace',
        'visit_date': '2024-03-20',
        'ticket_count': '2 Adults, 1 Child',
        'amount': '1500'
    }
    
    # Initialize email service
    email_service = EmailService()
    
    # Send test email
    success, message = email_service.send_confirmation_email(
        test_booking,
        "bbucky117@gmail.com"  # Replace this with your actual email address
    )
    
    print(message)