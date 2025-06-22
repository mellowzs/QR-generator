import customtkinter as ctk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image
import os
import sys


class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("400x530")
        self.root.resizable(width=True, height=True)  # Allow resizing
        
        # Set theme
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")


        # Create scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            root,
            width=360,
            height=460
        )
        self.scroll_frame.pack(fill="both", expand=True)

        # URL Input (move all widgets to scroll_frame instead of main_frame)
        url_label = ctk.CTkLabel(self.scroll_frame, text="Enter URL:", font=("Arial Bold", 14))
        url_label.pack(pady=1, anchor="w", padx=10)  # anchor="w" aligns to west/left
        self.url_entry = ctk.CTkTextbox(
            self.scroll_frame, 
            width=350,
            height=100,
            font=("Arial", 14)
        )
        self.url_entry.insert("1.0", "https://example.com")
        self.url_entry.pack(pady=5)
        
        ctk.CTkLabel(
            self.scroll_frame, 
            text="(ex. Google Map, Facebook Page, Plaintext)"
        ).pack(pady=5)

        # Logo Selection
        ctk.CTkLabel(self.scroll_frame, text="Select Logo (optional):", font=("Arial Bold", 14)).pack(anchor="w", padx=10)
        self.logo_path = ""
        
        # Create logo container frame
        self.logo_container = ctk.CTkFrame(self.scroll_frame)
        self.logo_container.pack(fill="x", padx=10, pady=5)
        
        # Left side - Logo Button
        self.logo_button = ctk.CTkButton(
            self.logo_container,
            text="Choose Logo",
            font=("Arial", 13),
            command=self.choose_logo,
            width=120,  # Fixed width for button
            height=100
        )
        self.logo_button.pack(side="left", pady=1, padx=5)
        
        # Right side - Preview Frame and Label
        self.preview_frame = ctk.CTkFrame(self.logo_container, height=100, width=200)
        self.preview_frame.pack(side="left", pady=5, padx=5, fill="both", expand=True)
        self.preview_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="No logo selected", font=("Arial", 12))
        self.preview_label.pack(expand=True)

        # Logo Label below container
        self.logo_label = ctk.CTkLabel(self.scroll_frame, text="")
        self.logo_label.pack(pady=30)

        # Create button container frame
        self.button_container = ctk.CTkFrame(self.scroll_frame)
        self.button_container.pack(fill="x", padx=20, pady=5)
        
        # Exit Button
        self.exit_button = ctk.CTkButton(
            self.button_container,
            text="Exit",
            font=("Arial Bold", 13),
            command=self.root.destroy,
            height=40,
            fg_color="red",  # Dark red for normal state
            hover_color="#8B0000"  # Dark red for hover
        )
        self.exit_button.pack(side="left", padx=5)

        # Generate Button (modified to be in the button container)
        self.generate_button = ctk.CTkButton(
            self.button_container,
            text="Generate QR Code",
            font=("Arial Bold", 13),
            fg_color="green",  # Dark green for normal state
            command=self.generate_qr,
            height=40
        )
        self.generate_button.pack(side="right", padx=5)

        # Add developer credit
        self.credit_label = ctk.CTkLabel(
            self.scroll_frame,
            text="Developed by Mel\n2025",
            font=("Arial", 12),
            text_color="gray"  # Makes it subtle
        )
        self.credit_label.pack(pady=(20, 10))  # Add more top padding to separate from buttons

          # Version Label
        self.version_label = ctk.CTkLabel(
            self.scroll_frame,
            text="Version 1.3",
            font=("Arial", 12),
            text_color="gray"  # Makes it subtle
        )
        self.version_label.pack(pady=(1, 1))  # Add more top padding to separate from buttons

    def choose_logo(self):
        self.logo_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")]
        )
        if self.logo_path:
            self.logo_label.configure(text=os.path.basename(self.logo_path))
            # Display preview
            try:
                logo = Image.open(self.logo_path)
                logo.thumbnail((100, 100))  # Resize for preview
                photo = ctk.CTkImage(
                    light_image=logo,
                    dark_image=logo,
                    size=logo.size
                )
                self.preview_label.configure(image=photo, text="")  # Clear the text when setting image
                self.preview_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Error loading logo preview: {str(e)}")

    def generate_qr(self):
        url = self.url_entry.get("1.0", "end-1c").strip()  # Get text from Text widget
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        try:
            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=2
            )
            qr.add_data(url)
            qr.make()
            qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

            # Add logo if selected
            if self.logo_path:
                try:
                    # Open and resize logo
                    logo = Image.open(self.logo_path)
                    basewidth = 100
                    wpercent = basewidth / float(logo.size[0])
                    hsize = int(float(logo.size[1]) * wpercent)
                    logo = logo.resize((basewidth, hsize))

                    # Calculate position
                    pos = (
                        (qr_img.size[0] - logo.size[0]) // 2,
                        (qr_img.size[1] - logo.size[1]) // 2
                    )
                    qr_img.paste(logo, pos)
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing logo: {str(e)}")
                    return

            # Save QR Code
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")]
            )
            if save_path:
                qr_img.save(save_path)
                messagebox.showinfo("Success", "QR Code generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error generating QR code: {str(e)}")

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    root = ctk.CTk()
    app = QRGeneratorApp(root)
    root.mainloop()
