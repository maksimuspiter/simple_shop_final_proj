# Simple Shop
#### Backend
- Django 4.2
- PostgreSQL
- Bootstrap 5
- Celery
- Redis
- ajax
- Intersection Observer API

##### Elements:

<ul>
  <li>Product List with category, tags and filters</li>
  <li>Product cart and list_of_comparison in session (CART_SESSION_ID:dict, COMPARE_SESSION_ID:list)</li>
  <li>Cart with ajax (add/remove in cart/compare, add coupon)</li>
  <li>Order form without payment</li>
  <li>Related products in product_detail</li>

  <li>Customer feedback:
    <p>Customers can write a review and rate the product</p>
    <p>Rating displayed as star system</p>
    <p>Review: advantages, disadvantages, comment and product images<p>
    <p>Feedback create task in celery (change avg rating)</p>
  </li>

  <li>Coupons in Orders and Account, coupon changes total price</li>
  <li>Customer account page: all orders, favorite products, personal coupons, all reviews, messenger with support </li>
  <li>Account support chat:
    <p>Scrolling into unread messages when user open messanger</p>
    <p>Ajax-change unread messages in selected chat when user scrolls down the page (used Intersection Observer API)</p>
    <p>Ajax form window to send message</p>
  </li>
  <li>Account = OneToOneField, account page only for LoginRequired (when creating a superuser, you need to create an account for him)</li>

</ul>

<h4>To start:</h4>
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
touch .env (DEBUG, SECRET_KEY, DJANGO_ALLOWED_HOSTS, DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT)
./manage.py makemigrations 
./manage.py migrate
```

