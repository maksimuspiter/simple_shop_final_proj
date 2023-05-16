<h1>Simple Shop</h1>
<h2>Stack:</h2>
<ul>
  <li>Django 4.2</li>
  <li>Python >= 3.10</li>
   <li>PostgreSQL</li>
  <li>Bootstrap 5</li>
  <li>Celery</li>
  <li>Redis</li>
  <li>ajax</li>
  <li>Intersection Observer API</li>
</ul>

<h3>Elements:</h3>

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
<p>python3 -m venv venv </p>
<p>source venv/bin/activate</p>
<p>pip install -r requirements.txt</p>
<p>create file .env with</p>
<ul>
  <li>DEBUG</li>
  <li>SECRET_KEY</li>
  <li>DJANGO_ALLOWED_HOSTS</li>
  <li>DB_NAME</li>
  <li>DB_USER</li>
  <li>DB_PASS</li>
  <li>DB_HOST</li>
  <li>DB_PORT</li>
</ul>
<p>makemigrations and migrate</p>

#Future improvements:

<ul>
  <li>Refactor comment --> hide forms</li>
  <li>Add e-check</li>
  <li>Refactor product comparison</li>
  <li>Add Django REST framework</li>
  <li>Add EditorConfig</li>
  <li>Add Docker</li>
</ul>
