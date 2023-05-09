function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function change_quantity_cart(url, action, product_id) {
  $.ajax({
    url: url,
    type: "POST",
    data: jQuery.param({ action: action, product_id: product_id }),
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    success: (data) => {
      console.log(data);
      if (data.result) {
        change_buttons(product_id, data.final_quantity_in_cart);
        change_quantity_cart_navbar(data.all_products_in_cart_quantity);
      }
    },

    error: (error) => {
      console.log(error);
    },
  });
}

function change_quantity_cart_navbar(quantity) {
  let navbar_quantity_element = document.getElementById(
    "product_in_cart_quantity_navbar"
  );
  navbar_quantity_element.innerHTML = quantity;
}

function change_buttons(product_id, quantity) {
  let button_groap_div = document.getElementById(
    "buttons-group-product-" + product_id
  );
  let button_quantity = document.getElementById(
    "product-in-cart-quantity-" + product_id
  );
  switch (quantity) {
    case 0:
      button_groap_div.innerHTML = `<button type="button" class="btn btn-info" onclick="add_in_cart(${product_id})">В карзину</button>`;
      break;
    case 1:
      button_groap_div.innerHTML = `<button class="btn btn-outline-primary btn-sm" onclick="remove_in_cart(${product_id})">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="x5-e"><path fill="currentColor" d="M5 11a1 1 0 1 0 0 2h14a1 1 0 1 0 0-2H5Z"></path></svg>
    </button>
    <span id="product-in-cart-quantity-${product_id}">${quantity} шт.</span>
    <button class="btn btn-outline-primary btn-sm" onclick="add_in_cart(${product_id})">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="x5-e"><path fill="currentColor" d="M12 4a1 1 0 0 0-1 1v6H5a1 1 0 1 0 0 2h6v6a1 1 0 1 0 2 0v-6h6a1 1 0 1 0 0-2h-6V5a1 1 0 0 0-1-1Z"></path></svg>
    </button>`;
      break;
    default:
      button_quantity.innerHTML = quantity + " шт.";
  }
}
