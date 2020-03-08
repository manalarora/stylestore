const navbarCart = document.getElementById("navbarCart");
const cartButton = document.getElementById("cartButton");
const minCartQty = 1, maxCartQty = 5;

$(document).ready(function(){
    navbarCart.style.marginTop = (cartButton.offsetTop).toString() + "px";
    navbarCart.style.right = (cartButton.offsetWidth / 2).toString() + "px";
    // console.log(navbarCart.style.right);
});

function fadeToggleCart() {
    if(navbarCart.style.display == "block") {
        navbarCart.style.display = "none";
    }
    else if(navbarCart.style.display == "none") {
        navbarCart.style.display = "block";
    }
}

function showProductImg(e) {
    var product_image = e.getElementsByClassName("product_image")[0];
    product_image.style.display = "block";
}
function hideProductImg(e) {
    var product_image = e.getElementsByClassName("product_image")[0];
    product_image.style.display = "none";
}

// Handle cart quantity
function disableQty(e) {
    e.style.color = "#a6a6a6";
}
function enableQty(e) {
    e.style.color = "black";
}
var decQtyClass = document.getElementsByClassName("decQty");
var currQtyClass = document.getElementsByClassName("currQty");
var incQtyClass = document.getElementsByClassName("incQty");
for(var i = 0;i < currQtyClass.length;i++) {
    var n = parseInt(currQtyClass[i].innerHTML);
    if(n <= minCartQty) {
        disableQty(decQtyClass[i]);
    }
    if(n >= maxCartQty) {
        disableQty(incQtyClass[i]);
    }
}
function  changeCartQuantity(e, changeValue) {
    var decQtyTag = e.parentElement.getElementsByClassName("decQty")[0];
    var incQtyTag = e.parentElement.getElementsByClassName("incQty")[0];
    var quantityTag = e.parentElement.getElementsByTagName("span")[0];
    var quantityTagNewValue = parseInt(quantityTag.innerHTML) + changeValue;

    enableQty(decQtyTag);
    enableQty(incQtyTag);
    if(quantityTagNewValue == minCartQty) {
        disableQty(decQtyTag);
    }
    if(quantityTagNewValue == maxCartQty) {
        disableQty(incQtyTag);
    }
    if(quantityTagNewValue < minCartQty) {
        disableQty(decQtyTag);
        return false;
    }
    if(quantityTagNewValue > maxCartQty) {
        disableQty(incQtyTag);
        return false;
    }
    quantityTag.innerHTML = quantityTagNewValue;
}
