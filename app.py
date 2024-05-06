import streamlit as st
import uuid
import qrcode
from PIL import Image
import io

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

def login(username, password):
    """Check if the provided username and password match the hardcoded admin credentials."""
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

def generate_voucher(company_name, amount):
    """Generate a voucher and corresponding QR code."""
    voucher_number = str(uuid.uuid4())
    voucher_info = f"Company: {company_name}\nAmount: {amount}\nVoucher Number: {voucher_number}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(voucher_info)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return voucher_info, img_byte_arr

def main():
    """Main function for the Streamlit app."""
    st.title("Voucher Generator App")

    # Initialize or reset the session state for login
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Check login status
    if not st.session_state['logged_in']:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(username, password):
                st.session_state['logged_in'] = True
                st.experimental_rerun()  # Rerun the script to transition to voucher generation
            else:
                st.error("Incorrect username or password")
    else:
        # Voucher generation form
        company_name = st.text_input("Company Name", max_chars=50)
        amount = st.text_input("Amount", max_chars=15)
        if st.button("Generate Voucher"):
            if company_name and amount:
                voucher_info, img_data = generate_voucher(company_name, amount)
                st.image(img_data, caption='Voucher QR Code')
                st.text(voucher_info)
            else:
                st.warning("Please enter both company name and amount")

if __name__ == "__main__":
    main()
