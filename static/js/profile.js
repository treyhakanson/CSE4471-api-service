(function() {
   document.getElementById("logout").addEventListener("click", function() {
      localStorage.setItem("token", "");
      window.location.assign("login");
   });
})();
