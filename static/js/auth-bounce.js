(function() {
   if (!localStorage.getItem("token")) {
      window.location.assign("/demo/login");
   }
})();
