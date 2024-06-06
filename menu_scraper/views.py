from django.shortcuts import render
import requests
import pytesseract
from PIL import Image
from io import BytesIO
from .models import MenuItem

def scrape_menus(request):
    # URL of the menu image
    url = 'https://lh3.googleusercontent.com/AIAvE3YBVtK1B1TpkC1MN-4pNQsLqzrZWE1yeaKZCma7DtTnPaMNmWchZ_2BUt4DAXns-hSuZ7M-B8jun-J1tOT0yII=w192-rw'

    try:
        # Get the image content
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Open the image using PIL
        image = Image.open(BytesIO(response.content))

        # Use Tesseract OCR to extract text from the image
        text = pytesseract.image_to_string(image)

        # Split the text into lines and process each line
        for line in text.split('\n'):
            if line.strip():
                # Example logic to split item name and price
                parts = line.rsplit(' ', 1)  # Split on the last space
                if len(parts) == 2:
                    name = parts[0].strip()
                    price = parts[1].strip()

                    # Save to database
                    MenuItem.objects.create(name=name, price=price, restaurant_name="Restaurant Name")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image {url}: {e}")
    except Exception as e:
        print(f"Error processing image {url}: {e}")

    # Render the template with the menu items
    return render(request, 'menu_scraper/menu_list.html', {'menu_items': MenuItem.objects.all()})

def home(request):
    return render(request, 'home.html')
