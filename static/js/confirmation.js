(function() {
   axios
      .post(API_BASE_URL + "/phrase", {
         token: localStorage.getItem("token")
      })
      .then(function(res) {
         console.log(res);
      })
      .catch(function(err) {
         console.log(err);
      });
   var icon = document.getElementById("speak-icon");
   icon.style.display = "inline";
})();
