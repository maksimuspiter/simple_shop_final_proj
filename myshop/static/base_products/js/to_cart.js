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
    data: jQuery.param({ "action": action,  "product_id":product_id}),
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    success: (data) => {
      console.log(data);
      if (data.result) {
        document.getElementById(
          "product-in-cart-quantity-" + product_id
        ).innerHTML = data.final_quantity_in_cart;
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