//block special characters in input
function alpha(e) {
  // var k;
  // document.all ? k = e.keyCode : k = e.which;
  // //submit form when enter is pressed
  // if(e && e.keyCode == 13) {
  //     document.forms[0].submit();
  //  }
  // return ((k > 64 && k < 91) || (k > 96 && k < 123) || k == 8 || k == 32 || (k >= 48 && k <= 57));

  //Prevent # from being typed
  var input = document.getElementById("input");
  input.addEventListener("input", function() {
    input.value = input.value.replaceAll("#", "");
  })
}
