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
function add_result_window(result_div_id, acion, error_message) {
  let promocode_add_result = document.getElementById(result_div_id);
  let message;
  let window_class;
  switch (acion) {
    case "success":
      message = "Успешно добавлен";
      window_class = "alert alert-success alert-dismissible fade show";
      break;
    case "error":
      message = error_message;
      window_class = "alert alert-warning alert-dismissible fade show";
      break;
  }
  promocode_add_result.innerHTML = `<div class="${window_class}" role="alert">
  <strong>${message}</strong>
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>`;
}
function add_promocode_field(promocode_data_id, coupon_code) {
  let promocode_field = document.getElementById(promocode_data_id);

  promocode_field.innerHTML = `<span>Промокод применен: </span> <span class="p-1 bg-success text-white rounded-pill">${coupon_code}</span>`;
}
function change_price(
  total_price_result_first_id,
  total_price_result_second_id,
  price_before_discount,
  price_after_discount
) {
  let total_price_result_before_and_after_cupon = document.getElementById(
    total_price_result_first_id
  );
  let total_price_result = document.getElementById(
    total_price_result_second_id
  );

  total_price_result_before_and_after_cupon.innerHTML = `<span><s>${price_before_discount}</s></span><span> ${price_after_discount}</span>`;
  total_price_result.innerHTML = price_after_discount;
}
function change_discount_value(value) {
  document.getElementById("discount_value").innerHTML = `<span>Скидка: </span><span>${value}</span>`;
}

function add_promo_code_ajax(
  url,
  coupon_code,
  promocode_data_id,
  promocode_window_result_id,
  total_price_result_first,
  total_price_result_second
) {
  $.ajax({
    url: url,
    type: "POST",
    data: jQuery.param({ coupon_code: coupon_code }),
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    success: (data) => {
      console.log(data);

      if (data.result) {
        add_promocode_field(promocode_data_id, data.coupon_code);
        add_result_window(
          promocode_window_result_id,
          "success",
          data.error_message
        );
        change_price(
          total_price_result_first,
          total_price_result_second,
          data.price_before_discount,
          data.price_after_discount
        );
        change_discount_value(data.discount_value);
      } else {
        add_result_window(
          promocode_window_result_id,
          "error",
          data.error_message
        );
      }
    },

    error: (error) => {
      console.log(error);
    },
  });
}
