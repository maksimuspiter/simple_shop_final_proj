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

function change_quantity_ajax(
  url,
  product_id,
  quantity,
  product_price_id
) {
  $.ajax({
    url: url,
    type: "POST",
    data: jQuery.param({ product_id: product_id, quantity: quantity }),
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    success: (data) => {
      console.log(data);
      if (data.result) {
        change_product_sum_price(product_price_id, data.product_total_price);
        change_product_total_price_and_quantity(
          data.cart_quantity,
          data.total_price
        );
      }
    },

    error: (error) => {
      console.log(error);
    },
  });
}

function change_product_sum_price(element_id, new_price) {
  document.getElementById(element_id).innerHTML = new_price;
}
function change_product_total_price_and_quantity(
  cart_quantity,
  cart_total_price
) {
  document.getElementById("cart_quantity").innerHTML = cart_quantity;
  document.getElementById("cart_total_price").innerHTML = cart_total_price;
}
