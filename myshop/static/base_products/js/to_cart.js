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
    data: jQuery.param({ action: action }),
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    success: (data) => {
      if (data.result) {
        let products_quantity_new = document.getElementById(
          "product-in-cart-quantity-" + product_id
        );
        products_quantity_new.innerHTML = data.final_quantity_in_cart;
      }
    },

    error: (error) => {
      console.log(error);
    },
  });
}
