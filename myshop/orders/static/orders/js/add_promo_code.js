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

function add_promo_code(
  url,
  coupon_code,
  promocode_data_id,
  promocode_add_result_id,
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
      let result = data.result;
      let coupon_code = data.coupon_code;
      let promocode_add_result = document.getElementById(
        promocode_add_result_id
      );
      let price_before_discount = data.price_before_discount;
      let price_after_discount = data.price_after_discount;
      let total_price_result_before_and_after_cupon = document.getElementById(
        total_price_result_first
      );
      let total_price_result = document.getElementById(
        total_price_result_second
      );
      let promocode_field = document.getElementById(promocode_data_id);

      if (result) {
        promocode_field.innerHTML = `<span>Промокод применен: </span> <span class="p-1 bg-success text-white rounded-pill">${coupon_code}</span>`;
        promocode_add_result.innerHTML = `<div class="alert alert-success alert-dismissible fade show" role="alert">
        <strong id="promocode_add_success">success!</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
        total_price_result_before_and_after_cupon.innerHTML = `<span><s>${price_before_discount}</s></span><span> ${price_after_discount}</span>`;
        total_price_result.innerHTML = price_after_discount;
      } else {
        promocode_add_result.innerHTML = `<span>Промокод применен: </span> <span class="p-1 bg-success text-white rounded-pill">${coupon_code}</span>`;
        promocode_add_result.innerHTML = `<div class="alert alert-warning alert-dismissible fade show" role="alert">
        <strong>Error!</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
      }
    },

    error: (error) => {
      console.log(error);
    },
  });
}
