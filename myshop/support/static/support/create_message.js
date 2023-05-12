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

function send_message(url, chat_id, text, user_name, user_avatar_url) {
  $.ajax({
    url: url,
    type: "POST",
    data: jQuery.param({ text: text, chat_id: chat_id }),
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    success: (data) => {
      console.log(data);
      if (data.result) {
        clear_form_input();
        add_new_message(text, user_name, user_avatar_url);
        scroll_to_end();
      } else {
        show_error();
      }
    },

    error: (error) => {
      console.log(error);
    },
  });
}

function add_new_message(text, user_name, user_avatar_url) {
  let messages_div = document.getElementById("messages");
  messages_div.innerHTML += `<div class="card">
    <div class="card-header row m-0">
      <div class="col-10">
        <span class="fw-bold">${user_name}</span>
      </div>
  
      <div class="col-2">
        <img
          src=${user_avatar_url}
          alt="avatar"
          class="rounded-circle d-flex align-self-start ms-3 shadow-1-strong"
          width="40"
        />
      </div>
    </div>
  
    <div class="card-body">
      <p>${text}</p>
    </div>
  </div>
  `;
}
function clear_form_input() {
  let form = document.getElementById("create-message");
  form.reset();
}

function show_error() {
  console.log("error");
}
function scroll_to_end() {
  document.getElementById("end_messanger").scrollIntoView(true);
}

function read_all_messages(url, chat_id) {
  $.ajax({
    url: url,
    type: "POST",
    data: jQuery.param({ chat_id: chat_id }),
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    success: (data) => {
      console.log(data);
      if (data.result) {
        document.getElementById("chat-unread-" + chat_id).innerHTML = 0;
      }
    },

    error: (error) => {
      console.log(error);
    },
  });
}
