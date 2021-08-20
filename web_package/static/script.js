window.onload = function() {
  console.log('hello');
  let buttons = document.querySelectorAll('.like-button');
  buttons.forEach((button)=>{if (button.dataset.like==='True') {
    button.innerHTML = 'unlike';
  } else {
    button.innerHTML = 'like';
  }});
};

function toggleLike (button, post_id) {
  if (button.dataset.like === 'True') {
    unlike(button, post_id);
    button.dataset.like = 'False';
  } else {
    like(button, post_id);
    button.dataset.like = 'True';
  }
};

function helper (button, action, xhttp, post_id) {
  console.log(`call ${action} function`);
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      let data = JSON.parse(this.responseText);
      console.log(data.likes);
      console.log(`num-like-${post_id}`)
      let likeCount = document.getElementById(`num-like-${post_id}`); 
      likeCount.innerHTML = data.likes;
      if (action === 'like') {
        document.getElementById(`like-${post_id}`).className = "btn btn-info";
        document.getElementById(`like-${post_id}`).innerHTML = "unlike"
      } else {
        document.getElementById(`like-${post_id}`).className = "btn btn-outline-info";
        document.getElementById(`like-${post_id}`).innerHTML = "like"
      }
    }
  };
}

function like (button, post_id) {
  var xhttp = new XMLHttpRequest();
  helper(button, 'like', xhttp, post_id);
  xhttp.open("GET", `/like/${post_id}/like`);
  xhttp.send();
}

function unlike (button, post_id){
  var xhttp = new XMLHttpRequest();
  helper(button, 'unlike', xhttp, post_id);
  xhttp.open("GET", `/like/${post_id}/unlike`);
  xhttp.send();
}