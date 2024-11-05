import tkinter as tk
from tkinter import messagebox, ttk, Canvas, Frame, VERTICAL, RIGHT, Y
from PIL import Image, ImageTk
import mysql.connector
import os

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",  # Make sure this is exactly "localhost" without any trailing characters
    user="root",
    password="anna1234",
    database="MobileStore",  # Make sure this is the correct database name
    port=3307  # Specify the correct port
)

cursor = db.cursor()

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Mobile Store")
root.geometry("600x400")
root.resizable(True, True)

cart = []  # Cart to hold selected items

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Username and Password cannot be empty.")
        return

    cursor.execute("SELECT * FROM Users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    if result:
        messagebox.showinfo("Success", "Login Successful!")
        open_home_page()
    else:
        messagebox.showerror("Error", "Invalid username or password. Please register if you haven't.")

def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Username and Password cannot be empty.")
        return

    cursor.execute("SELECT * FROM Users WHERE username=%s", (username,))
    result = cursor.fetchone()

    if result:
        messagebox.showerror("Error", "Username already exists.")
    else:
        cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        messagebox.showinfo("Success", "Registration successful! You can now login.")
        show_login_page()

def show_login_page():
    clear_window()
    root.geometry("400x300")

    login_frame = tk.Frame(root)
    login_frame.pack(expand=True, fill='both')

    tk.Label(login_frame, text="Login", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(login_frame, text="Username").pack()
    global username_entry
    username_entry = tk.Entry(login_frame)
    username_entry.pack()

    tk.Label(login_frame, text="Password").pack()
    global password_entry
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.pack()

    tk.Button(login_frame, text="Login", command=login).pack(pady=5)
    tk.Button(login_frame, text="Register", command=show_register_page).pack(pady=5)

def show_register_page():
    clear_window()
    root.geometry("400x300")

    register_frame = tk.Frame(root)
    register_frame.pack(expand=True, fill='both')

    tk.Label(register_frame, text="Register", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(register_frame, text="Username").pack()
    global reg_username_entry
    reg_username_entry = tk.Entry(register_frame)
    reg_username_entry.pack()

    tk.Label(register_frame, text="Password").pack()
    global reg_password_entry
    reg_password_entry = tk.Entry(register_frame, show="*")
    reg_password_entry.pack()

    tk.Button(register_frame, text="Register", command=register).pack(pady=5)
    tk.Button(register_frame, text="Back to Login", command=show_login_page).pack(pady=5)

def open_home_page():
    clear_window()
    root.geometry("600x500")

    home_label = tk.Label(root, text="Home Page", font=("Helvetica", 16, "bold"))
    home_label.pack(pady=10)

    # Load the cart icon
    try:
        cart_icon = Image.open("c:/Users/annaj/Desktop/Project-mobile/Images/cart.jpg")  # Ensure this path is correct
        cart_icon = cart_icon.resize((30, 30), Image.LANCZOS)  # Resize the icon as needed
        cart_photo = ImageTk.PhotoImage(cart_icon)
    except FileNotFoundError:
        messagebox.showerror("Error", "Cart icon image not found.")
        return  # Exit the function if the icon is missing

    # Cart Button positioned at the top right
    cart_button = tk.Button(root, image=cart_photo, command=open_checkout_page, relief="flat")
    cart_button.image = cart_photo  # Keep a reference to avoid garbage collection
    cart_button.place(x=root.winfo_width() - 40, y=10)  # Adjust x-position dynamically based on window width

    # Create frames for devices and offers
    devices_frame = Frame(root, bd=2, relief="solid")
    devices_frame.pack(pady=20, padx=20)
    
    devices_img = Image.open("c:/Users/annaj/Desktop/Project-mobile/Images/devices.jpg")
    devices_img = devices_img.resize((300, 225), Image.LANCZOS)
    devices_photo = ImageTk.PhotoImage(devices_img)
    devices_button = tk.Button(devices_frame, image=devices_photo, text="Devices", compound="top", command=show_devices)
    devices_button.image = devices_photo
    devices_button.pack()

    offers_frame = Frame(root, bd=2, relief="solid")
    offers_frame.pack(pady=20, padx=20)
    
    offers_img = Image.open("c:/Users/annaj/Desktop/Project-mobile/Images/offers.jpg")
    offers_img = offers_img.resize((300, 250), Image.LANCZOS)
    offers_photo = ImageTk.PhotoImage(offers_img)
    offers_button = tk.Button(offers_frame, image=offers_photo, text="Offers", compound="top", command=show_offers)
    offers_button.image = offers_photo
    offers_button.pack()


def show_devices():
    clear_window()
    root.geometry("600x500")

    device_label = tk.Label(root, text="Devices", font=("Helvetica", 16, "bold"))
    device_label.pack(pady=10)

    device_frame = Frame(root)
    device_frame.pack(fill='both', expand=True)
    canvas = Canvas(device_frame)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(device_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Bind mouse wheel scrolling
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    cursor.execute("SELECT * FROM Device")
    devices = cursor.fetchall()

    # Grid layout parameters
    row, col = 0, 0
    max_columns = 6 # Define how many columns per row
    frame_width = 300  # Fixed width for each item frame
    frame_height = 265  # Increased height for image display

    for device in devices:
        device_container = Frame(inner_frame, bd=1, relief="solid", width=frame_width, height=frame_height)
        device_container.grid(row=row, column=col, padx=5, pady=5)
        device_container.pack_propagate(False)  # Prevent resizing

        # Load device image
        try:
            # Assume images are named with device name or ID and stored in "Images/Devices/"
            image_path = f"c:/Users/annaj/Desktop/Project-mobile/Images/devices/{device[1]}.jpg"  # Adjust the path based on your file naming convention
            device_image = Image.open(image_path)
            device_image = device_image.resize((150, 150), Image.LANCZOS)  # Resize to fit within the frame
            device_photo = ImageTk.PhotoImage(device_image)
            image_label = tk.Label(device_container, image=device_photo)
            image_label.image = device_photo  # Keep a reference to avoid garbage collection
            image_label.pack()
        except FileNotFoundError:
            # If the image is not found, display a placeholder or skip the image
            placeholder_label = tk.Label(device_container, text="No Image", fg="grey")
            placeholder_label.pack()

        # Display truncated device details
        tk.Label(device_container, text=f"Name: {device[1][:15]}{'...' if len(device[1]) > 15 else ''}").pack(anchor="w")
        tk.Label(device_container, text=f"Type: {device[3][:15]}{'...' if len(device[3]) > 15 else ''}").pack(anchor="w")
        tk.Label(device_container, text=f"Price: ${device[4]}").pack(anchor="w")

        # Add to cart button
        tk.Button(device_container, text="Add to Cart", command=lambda d=device: add_to_cart(d)).pack(pady=5)

        # Update grid position
        col += 1
        if col >= max_columns:
            col = 0
            row += 1

    proceed_to_checkout_button = tk.Button(inner_frame, text="Proceed to Checkout", command=open_checkout_page)
    proceed_to_checkout_button.grid(row=row + 1, column=0, columnspan=max_columns, pady=10)

    back_to_home_button = tk.Button(inner_frame, text="Back to Home", command=open_home_page)
    back_to_home_button.grid(row=row + 2, column=0, columnspan=max_columns, pady=10)

def add_to_cart(device):
    # Assuming device[1] is the name and device[4] is the price
    device_name = device[1]  # Device name
    device_price = device[4]  # Device price

    # Append a tuple with the name and price to the cart
    cart.append((device_name, device_price))  
    messagebox.showinfo("Cart", f"{device_name} has been added to your cart.")


def show_offers():
    clear_window()
    root.geometry("600x500")

    offers_label = tk.Label(root, text="Offers", font=("Helvetica", 16, "bold"))
    offers_label.pack(pady=10)

    offers_frame = Frame(root)
    offers_frame.pack(fill='both', expand=True)
    canvas = Canvas(offers_frame)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(offers_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Bind mouse wheel scrolling
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    cursor.execute("SELECT * FROM Offers")
    offers = cursor.fetchall()

    # Grid layout parameters
    row, col = 0, 0
    max_columns = 6 # Define how many columns per row
    frame_width = 300  # Fixed width for each item frame
    frame_height = 265  # Increased height for image display

    for offer in offers:
        offer_container = Frame(inner_frame, bd=1, relief="solid", width=frame_width, height=frame_height)
        offer_container.grid(row=row, column=col, padx=5, pady=5)
        offer_container.pack_propagate(False)  # Prevent resizing

        # Load offer image
        try:
            # Construct the image path using the offer name or ID
            image_path = f"c:/Users/annaj/Desktop/Project-mobile/Images/offers/{offer[4]}.jpg"  # Adjust the path based on your naming convention
            
            if os.path.exists(image_path):  # Check if file exists
                offer_image = Image.open(image_path)
                offer_image = offer_image.resize((150, 150), Image.LANCZOS)  # Resize to fit within the frame
                offer_photo = ImageTk.PhotoImage(offer_image)
                image_label = tk.Label(offer_container, image=offer_photo)
                image_label.image = offer_photo  # Keep a reference to avoid garbage collection
                image_label.pack()
            else:
                print(f"Image not found for offer: {offer[4]} at path: {image_path}")
                placeholder_label = tk.Label(offer_container, text="No Image", fg="grey")
                placeholder_label.pack()

        except Exception as e:
            print(f"Error loading image for offer: {offer[4]} - {e}")
            placeholder_label = tk.Label(offer_container, text="No Image", fg="grey")
            placeholder_label.pack()

        # Display truncated offer details
        tk.Label(offer_container, text=f"Offer: {offer[4][:15]}{'...' if len(offer[4]) > 15 else ''}").pack(anchor="w")
        tk.Label(offer_container, text=f"Discount: {offer[1]}%").pack(anchor="w")
        tk.Label(offer_container, text=f"Price: ${offer[2]}").pack(anchor="w")

        # Add to cart button
        tk.Button(offer_container, text="Add to Cart", command=lambda o=offer: add_to_cart_offer(o)).pack(pady=5)

        # Update grid position
        col += 1
        if col >= max_columns:
            col = 0
            row += 1

    proceed_to_checkout_button = tk.Button(inner_frame, text="Proceed to Checkout", command=open_checkout_page)
    proceed_to_checkout_button.grid(row=row + 1, column=0, columnspan=max_columns, pady=10)

    back_to_home_button = tk.Button(inner_frame, text="Back to Home", command=open_home_page)
    back_to_home_button.grid(row=row + 2, column=0, columnspan=max_columns, pady=10)

def add_to_cart_offer(offer):
    device_name = offer[4] 
    device_price = offer[2]
    # Append a tuple with the required details to the cart
    cart.append((device_name, device_price))  # Change this if your offer structure is different
    messagebox.showinfo("Cart", f"{device_name} has been added to your cart.")


def open_checkout_page():
    clear_window()
    root.geometry("600x500")

    checkout_label = tk.Label(root, text="Cart", font=("Helvetica", 16, "bold"))
    checkout_label.pack(pady=10)

    checkout_frame = Frame(root)
    checkout_frame.pack(fill='both', expand=True)

    if not cart:
        tk.Label(checkout_frame, text="Your cart is empty.").pack(pady=10)
    else:
        total_price = 0  # Initialize total price

        for item in cart:
            item_name = item[0]  # Device name or offer name
            item_price = item[1]  # Device price or offer price

            # Display item name and price
            item_label = tk.Label(checkout_frame, text=f"{item_name} - ${item_price}")
            item_label.pack(pady=2)

            # Add to total price
            total_price += item_price

            # Remove button for each item
            remove_button = tk.Button(checkout_frame, text="Remove from Cart", command=lambda i=item: remove_from_cart(i))
            remove_button.pack(pady=2)

        # Display total price
        total_label = tk.Label(checkout_frame, text=f"Total Price: ${total_price:.2f}", font=("Helvetica", 14, "bold"))
        total_label.pack(pady=10)

    checkout_button = tk.Button(checkout_frame, text="Checkout", command=checkout)
    checkout_button.pack(pady=10)

    back_to_home_button = tk.Button(checkout_frame, text="Back to Home", command=open_home_page)
    back_to_home_button.pack(pady=10)



def remove_from_cart(item):
    if item in cart:
        cart.remove(item)
        messagebox.showinfo("Cart", f"{item[0]} has been removed from your cart.")  # Corrected the name display
        open_checkout_page()  # Refresh the checkout page


def checkout():
    global cart  # Declare cart as global before using it
    if not cart:
        messagebox.showerror("Checkout", "Your cart is empty. Please add items before checking out.")
    else:
        messagebox.showinfo("Checkout", "Thank You for Shopping!")
        cart = []  # Clear the cart after checkout
        open_checkout_page()  # Refresh the checkout page

show_login_page()
root.mainloop()