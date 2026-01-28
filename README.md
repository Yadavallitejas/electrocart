# ElectroCart

[Watch it Live](https://electrocart-nqts.onrender.com/)


ElectroCart is a full-featured ecommerce web application designed for selling electronic items online. Built with Django, this web app provides a seamless shopping experience with product browsing, detailed product views, cart management, order placement, and payment processing. It also supports user accounts, product reviews, and an intuitive interface for customers to explore and purchase electronics.

## Demo

<video width="640" height="360" controls>
  <source src="static/demo/demo_video.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Features

- **Product Catalog:** Browse a wide range of electronic products organized by categories.
- **Product Variations:** Support for product variations such as color and size.
- **Product Details:** Detailed product pages with descriptions, images, and user reviews.
- **User Reviews and Ratings:** Customers can submit and update reviews and ratings for products.
- **Search Functionality:** Search products by keywords in name or description.
- **Shopping Cart:** Add products with variations to the cart, update quantities, and remove items.
- **Checkout Process:** Secure checkout page with tax calculation and order summary.
- **Order Management:** Place orders, process payments, and track order status.
- **Stock Management:** Automatic stock reduction upon successful order placement.
- **Email Notifications:** Order confirmation emails sent to customers.
- **User Accounts:** User registration, login, profile management, and order history.
- **Responsive Design:** Mobile-friendly and responsive UI for a smooth shopping experience.

## Technologies Used

- Python 3.x
- Django Web Framework
- SQLite (default database)
- HTML, CSS, JavaScript for frontend
- Bootstrap for responsive design
- Django Templates for rendering views

## Installation and Setup

1. Clone the repository:
   ```
   git clone <https://github.com/Yadavallitejas/electrocart.git>
   ```
2. Navigate to the project directory:
   ```
   cd electrocart
   ```
3. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/Scripts/activate   # On Windows
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Apply migrations to set up the database:
   ```
   python manage.py migrate
   ```
6. Create a superuser for admin access:
   ```
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```
   python manage.py runserver
   ```
8. Open your browser and visit `http://127.0.0.1:8000/` to access the app.

## Usage

- Browse products by category or search for specific items.
- View detailed product information including images and reviews.
- Add products with desired variations to your shopping cart.
- Manage your cart by updating quantities or removing items.
- Proceed to checkout and place your order securely.
- Register and log in to view your order history and manage your profile.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests for improvements or new features.

## License

This project is licensed under the MIT License.

## Contact

For any questions or support, please contact the project maintainer.
