import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import random
import qrcode
from PIL import Image, ImageTk
from io import BytesIO

# Global variables to manage transitions and total
customer_proceeded = False
menu_proceeded = False
grand_total = 0
discount_applied = None  # Store applied discount code

# Generate random discount codes and descriptions
available_codes = {
    f"OFF{random.randint(100, 500)}": f"₹{random.randint(50, 300)} off on orders above ₹{random.randint(500, 1000)}"
    for _ in range(3)
}

# Function to proceed after entering customer details
def proceed_customer_details():
    global customer_proceeded
    if (not entry_name.get() or len(entry_no.get()) != 10 or 
        not entry_no.get().isdigit() or not entry_email.get() or 
        not entry_address.get()):
        messagebox.showerror("Input Error", "Please enter valid customer details.")
        return
    customer_proceeded = True
    notebook.select(1)  # Move to the Menu Items tab

# Function to proceed after selecting menu items
def proceed_menu_items():
    global menu_proceeded
    menu_proceeded = True
    notebook.select(2)  # Move to the Summary tab
    generate_summary()

# Function to generate the summary
def generate_summary():
    global grand_total
    receipt_text = ""
    total = 0
    for category, sub_items in menu.items():
        receipt_text += f"\n{category}\n"
        for item, (qty_var, price) in sub_items.items():
            qty = qty_var.get()
            if qty > 0:
                item_total = qty * price
                receipt_text += f"{item:<30}{qty:<10}{item_total:<10}\n"
                total += item_total

    tax_rate = 0.10  # 10% tax
    tax_amount = total * tax_rate
    grand_total = total + tax_amount

    summary_text = f"Total Amount: ₹{total:.2f}\n"
    summary_text += f"Tax (10%): ₹{tax_amount:.2f}\n"
    summary_text += f"Grand Total: ₹{grand_total:.2f}\n"
    
    text_summary.delete("1.0", tk.END)
    text_summary.insert(tk.END, summary_text)

# Function to apply discount and update summary
def apply_offer_code():
    global grand_total, discount_applied
    discount_code = discount_var.get()
    discount_amount = 0
    
    for code, desc in available_codes.items():
        if discount_code == code and grand_total >= int(desc.split('₹')[2].split(' ')[0]):
            discount_amount = int(desc.split('₹')[1].split(' ')[0])
            discount_applied = code  # Store the applied code
            break

    grand_total_after_discount = grand_total - discount_amount

    text_summary.insert(tk.END, f"\nDiscount Applied: {discount_applied} - ₹{discount_amount:.2f}\n")
    text_summary.insert(tk.END, f"Total after Discount: ₹{grand_total_after_discount:.2f}\n")

    grand_total = grand_total_after_discount

# Function to proceed to receipt after summary
def proceed_to_receipt():
    notebook.select(3)  # Move to the Receipt tab
    generate_receipt()

# Function to generate receipt with QR code
def generate_receipt():
    receipt_text = text_summary.get("1.0", tk.END)
    receipt_text += f"\n\nApplied Code: {discount_applied if discount_applied else 'None'}\n"
    payment_option = payment_var.get()
    receipt_text += f"Payment Option: {payment_option}\n"
    text_receipt.delete("1.0", tk.END)
    text_receipt.insert(tk.END, receipt_text)

    # Generate QR code for the receipt
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2
    )
    qr.add_data(receipt_text)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    qr_image = Image.open(BytesIO(img_byte_arr))
    qr_image = qr_image.resize((150, 150))  # Resize the QR code image
    qr_photo = ImageTk.PhotoImage(qr_image)

    label_qr_code.config(image=qr_photo)
    label_qr_code.image = qr_photo

# Function to save the receipt as a text file
def save_receipt():
    receipt_text = text_receipt.get("1.0", tk.END)
    if not receipt_text.strip():
        messagebox.showwarning("Save Error", "No receipt to save!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(receipt_text)
        messagebox.showinfo("Success", "Receipt saved successfully!")

# GUI setup
root = tk.Tk()
root.title("Restaurant Billing System")
root.geometry("1200x700")
root.configure(bg="#f0f0f0")

# Create a Notebook widget for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Customer details tab
tab_customer = tk.Frame(notebook, bg="#f0f0f0")
notebook.add(tab_customer, text="Customer Details")

# Customer details frame
frame_customer = tk.Frame(tab_customer, bg="#d1e7dd", padx=10, pady=10, bd=2, relief="groove")
frame_customer.pack(padx=10, pady=10, fill=tk.X)

# Customer Name
label_name = tk.Label(frame_customer, text="Customer Name", bg="#d1e7dd")
label_name.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_name = tk.Entry(frame_customer)
entry_name.grid(row=0, column=1, padx=5, pady=5)

# Customer No
label_no = tk.Label(frame_customer, text="Customer No (10 digits)", bg="#d1e7dd")
label_no.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_no = tk.Entry(frame_customer)
entry_no.grid(row=1, column=1, padx=5, pady=5)

# Customer Email
label_email = tk.Label(frame_customer, text="Email", bg="#d1e7dd")
label_email.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_email = tk.Entry(frame_customer)
entry_email.grid(row=2, column=1, padx=5, pady=5)

# Customer Address
label_address = tk.Label(frame_customer, text="Address", bg="#d1e7dd")
label_address.grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_address = tk.Entry(frame_customer)
entry_address.grid(row=3, column=1, padx=5, pady=5)

# Buttons for customer section
frame_buttons = tk.Frame(frame_customer, bg="#d1e7dd")
frame_buttons.grid(row=5, columnspan=2, pady=10)

btn_proceed = tk.Button(frame_buttons, text="Proceed", command=proceed_customer_details)
btn_proceed.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(frame_buttons, text="Clear", command=lambda: [entry_name.delete(0, tk.END), 
                                                                   entry_no.delete(0, tk.END), 
                                                                   entry_email.delete(0, tk.END), 
                                                                   entry_address.delete(0, tk.END)])
btn_clear.pack(side=tk.LEFT, padx=5)

# Menu items tab
tab_menu = tk.Frame(notebook, bg="#f0f0f0")
notebook.add(tab_menu, text="Menu Items")

# Menu items frame
frame_menu = tk.Frame(tab_menu, bg="#ffebcd", padx=10, pady=10, bd=2, relief="groove")
frame_menu.pack(padx=10, pady=10, fill=tk.BOTH)

# Define menu with sub-items (10 items in each category)
menu = {
    "Main Course": {
        "Pasta": (tk.IntVar(), 200),
        "Pizza": (tk.IntVar(), 250),
        "Burger": (tk.IntVar(), 150),
        "Biryani": (tk.IntVar(), 300),
        "Fried Rice": (tk.IntVar(), 220),
        "Paneer Tikka": (tk.IntVar(), 280),
        "Dal Makhani": (tk.IntVar(), 240),
        "Vegetable Curry": (tk.IntVar(), 200),
        "Naan": (tk.IntVar(), 40),
        "Chowmein": (tk.IntVar(), 180),
    },
    "Sweets": {
        "Ice Cream": (tk.IntVar(), 100),
        "Cake": (tk.IntVar(), 150),
        "Brownie": (tk.IntVar(), 120),
        "Gulab Jamun": (tk.IntVar(), 80),
        "Rasgulla": (tk.IntVar(), 70),
        "Kheer": (tk.IntVar(), 90),
        "Pudding": (tk.IntVar(), 110),
        "Pastry": (tk.IntVar(), 130),
        "Ladoo": (tk.IntVar(), 60),
        "Jalebi": (tk.IntVar(), 50),
    },
    "Starters": {
        "Spring Rolls": (tk.IntVar(), 150),
        "Paneer Pakora": (tk.IntVar(), 180),
        "Chili Chicken": (tk.IntVar(), 220),
        "French Fries": (tk.IntVar(), 120),
        "Onion Rings": (tk.IntVar(), 100),
        "Garlic Bread": (tk.IntVar(), 90),
        "Samosa": (tk.IntVar(), 60),
        "Nachos": (tk.IntVar(), 130),
        "Tandoori Chicken": (tk.IntVar(), 250),
        "Fish Fry": (tk.IntVar(), 240),
    },
    "Drinks": {
        "Coke": (tk.IntVar(), 60),
        "Lemonade": (tk.IntVar(), 50),
        "Coffee": (tk.IntVar(), 80),
        "Tea": (tk.IntVar(), 40),
        "Water": (tk.IntVar(), 20),
        "Mocktail": (tk.IntVar(), 120),
        "Smoothie": (tk.IntVar(), 150),
        "Juice": (tk.IntVar(), 70),
        "Milkshake": (tk.IntVar(), 90),
        "Mineral Water": (tk.IntVar(), 30),
    },
}

# Display menu items in horizontal frames
for category, items in menu.items():
    category_frame = tk.Frame(frame_menu, bg="#ffebcd")
    category_frame.pack(pady=5, fill=tk.X)
    
    tk.Label(category_frame, text=category, font=("Arial", 16, "bold"), bg="#ffebcd").pack(pady=5)

    for item, (qty_var, price) in items.items():
        quantity_label = tk.Label(category_frame, text="Qty:", bg="#ffebcd")
        quantity_label.pack(side=tk.LEFT, padx=5)

        entry_quantity = tk.Entry(category_frame, textvariable=qty_var, width=5)
        entry_quantity.pack(side=tk.LEFT, padx=5)

        tk.Label(category_frame, text=f"{item} - ₹{price}", bg="#ffebcd").pack(side=tk.LEFT, padx=5)

# Proceed to summary button
btn_menu_proceed = tk.Button(frame_menu, text="Proceed to Summary", command=proceed_menu_items)
btn_menu_proceed.pack(pady=10)

# Summary tab
tab_summary = tk.Frame(notebook, bg="#f0f0f0")
notebook.add(tab_summary, text="Summary")

frame_summary = tk.Frame(tab_summary, bg="#ffe6e6", padx=10, pady=10, bd=2, relief="groove")
frame_summary.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Area to display summary
text_summary = tk.Text(frame_summary, height=15, width=50)
text_summary.pack()

# Offer code section
frame_code = tk.Frame(frame_summary, bg="#ffe6e6")
frame_code.pack(pady=10)

label_code = tk.Label(frame_code, text="Enter Offer Code:", bg="#ffe6e6")
label_code.pack(side=tk.LEFT, padx=5)

discount_var = tk.StringVar()
entry_code = tk.Entry(frame_code, textvariable=discount_var)
entry_code.pack(side=tk.LEFT, pady=5, padx=5)

# Apply button beside offer code
btn_apply = tk.Button(frame_code, text="Apply", command=apply_offer_code)
btn_apply.pack(side=tk.LEFT, padx=5)

# Display available offer codes and descriptions in a table-like structure
label_available_codes = tk.Label(frame_summary, text="Available Codes:", bg="#ffe6e6")
label_available_codes.pack(pady=5)

codes_frame = tk.Frame(frame_summary, bg="#ffe6e6")
codes_frame.pack(pady=5)

tk.Label(codes_frame, text="Code", bg="#ffe6e6").grid(row=0, column=0, padx=5)
tk.Label(codes_frame, text="Description", bg="#ffe6e6").grid(row=0, column=1, padx=5)

for i, (code, description) in enumerate(available_codes.items(), start=1):
    tk.Label(codes_frame, text=code, bg="#ffe6e6").grid(row=i, column=0, padx=5)
    tk.Label(codes_frame, text=description, bg="#ffe6e6").grid(row=i, column=1, padx=5)

# Proceed to receipt button near summary box
btn_summary_proceed = tk.Button(frame_summary, text="Proceed to Receipt", command=proceed_to_receipt)
btn_summary_proceed.pack(pady=20)

# Receipt tab
tab_receipt = tk.Frame(notebook, bg="#f0f0f0")
notebook.add(tab_receipt, text="Receipt")

# Receipt display
frame_receipt = tk.Frame(tab_receipt, bg="#f0f0f0", padx=10, pady=10, bd=2, relief="groove")
frame_receipt.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

text_receipt = tk.Text(frame_receipt, height=15, width=70)
text_receipt.pack()

# QR Code for receipt
label_qr_code = tk.Label(frame_receipt, bg="#f0f0f0")
label_qr_code.pack(side=tk.LEFT, padx=10)

# Payment options
frame_payment = tk.Frame(frame_receipt, bg="#f0f0f0")
frame_payment.pack(pady=10)

payment_var = tk.StringVar(value="Cash")  # Default payment option
payment_options = ["Cash", "Credit Card", "Debit Card", "UPI"]
for option in payment_options:
    tk.Radiobutton(frame_payment, text=option, variable=payment_var, value=option, bg="#f0f0f0").pack(anchor="w")

# Make Payment button
btn_make_payment = tk.Button(frame_payment, text="Make Payment", command=lambda: messagebox.showinfo("Payment", "Payment successful!"))
btn_make_payment.pack(pady=5)

# Save receipt button
btn_save_receipt = tk.Button(frame_receipt, text="Save Receipt", command=save_receipt)
btn_save_receipt.pack(pady=10)

# Customer feedback section
tab_feedback = tk.Frame(notebook, bg="#f0f0f0")
notebook.add(tab_feedback, text="Feedback")

frame_feedback = tk.Frame(tab_feedback, bg="#d1e7dd", padx=10, pady=10, bd=2, relief="groove")
frame_feedback.pack(padx=10, pady=10, fill=tk.BOTH)

label_feedback = tk.Label(frame_feedback, text="Customer Feedback", bg="#d1e7dd")
label_feedback.pack(pady=5)

feedback_var = tk.StringVar()
entry_feedback = tk.Entry(frame_feedback, textvariable=feedback_var, width=50)
entry_feedback.pack(pady=5)

btn_submit_feedback = tk.Button(frame_feedback, text="Submit Feedback", command=lambda: messagebox.showinfo("Feedback", "Thank you for your feedback!"))
btn_submit_feedback.pack(pady=5)

root.mainloop()
