{% extends "base.html" %}

{% block title %}View Study Set{% endblock %}

{% block content %}

<!-- need this to add css to just this page for the flashcard -->
<head>
  <style>
    /* The flashcard container to format whole card on page,
       margin is to center it horizontally, width & height of card,
       bottom padding is distance of cards between each other */
    .flashcard {
      background-color: transparent;  /* the color behind the card while it flips */
      margin: auto;
      width: 650px;
      height: 200px;
      padding-top: 10px;
      padding-bottom: 10px;
    }

    /* This container joins the front and back, it is the container that flips when hovered over*/
    .flashcard-join {
      height: 100%; 
      transition: transform 1s;
      transform-style: preserve-3d;
    }

    /* add the hover selector to the flashcard when you move the mouse over it */
    .flashcard-join:hover {
      transform: rotateX(180deg);
      transition-duration: 1s;
    }

    /* style for both the term and definiton side of the flashcard */
    .flashcard-term, .flashcard-back {
      -webkit-backface-visibility: hidden; /* need this one to hide the opposite side for each */
      text-align: center;
      position: absolute;
      width: 100%;
      height: 100%;
      background-color: white;
      color: #000000;
    }

    /* the css for the term side */
    .flashcard-term {
      margin: auto;
      background-color: #39aea9;
      box-shadow: 2px 2px 4px #000000;
    }

    /* css for the definiton side */
    .flashcard-back {
      transform: rotateX(180deg);
      background-color: #A2D5AB;
      box-shadow: 2px 2px 4px #000000;
      font-size: 20px;
    }
    
    .flashcard-center {
      padding: 70px 0;
      margin: auto;
    }

    /*css code for my button */

    /* style for the title and add a card button */
    .title-container {
      display: flex;
      justify-content: center;
      padding-top: 20px; 
      margin-bottom: 20px;
    }

    /* style for the title button */
    .title-button {
      background-color: #39aea9;
      border: none;
      color: white;
      padding: 10px 20px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 20px;
      margin-right: 10px;
    }

    
  </style>
</head>

<!-- Button to edit the title of the set -->
<div class="title-container">
    <button class="title-button">{{ title }}</button>
</div>

<!-- create a flashcard for every card in the set -->
{% for term in cards %}
  <div class="flashcard">
    <div class="flashcard-join">
      <div class="flashcard-term">
        <div class="flashcard-center">
          <h2>{{term}}</h2>
        </div>
      </div>
      <div class="flashcard-back">
        <div class="flashcard-center">
          <p>{{cards[term]}}</p>
        </div>
      </div>
    </div>
  </div>
{% endfor %}


<!-- Add a card button -->
<div class="title-container">
    <button class="title-button">Add a card</button>
</div>


<!-- original before i spiced it up -Mariela -->
<!-- <div class="col-lg px-lg-5">
    {% for term in cards %}
            <div class="row">
              {{term}}
            </div>
            <div class="row">
               {{cards[term]}}
            </div>
    {% endfor %}
</div> -->


{% endblock %}


<!--

    <!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {font-family: Arial, Helvetica, sans-serif;}

/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  background-color: #fefefe;
  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

/* The Close Button */
.close {
  color: #aaaaaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}
</style>
</head>
<body>

<h2>Modal Example</h2>

<!-- Trigger/Open The Modal -->
<button id="myBtn">Open Modal</button>

<!-- The Modal -->
<div id="myModal" class="modal">

  <!-- Modal content -->
  <div class="modal-content">
    <span class="close">&times;</span>
    <p>Some text in the Modal..</p>
  </div>

</div>

<script>
// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
</script>

</body>
</html>


-->