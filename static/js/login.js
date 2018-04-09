(function() {
   document
      .getElementById("login-form")
      .addEventListener("submit", function(e) {
         e.preventDefault();
         e.stopImmediatePropagation();
         var username = e.target.querySelector('[name="user"]').value;
         var password = e.target.querySelector('[name="pass"]').value;
         axios
            .post(API_BASE_URL + "/login", {
               email: username,
               password: password
            })
            .then(function(res) {
               if (res.data.outcome === "successful") {
                  localStorage.setItem("token", res.data.token);
                  document.getElementById("error-block").display = "none";
                  window.location.assign("/demo/confirmation");
               } else {
                  let errBlock = document.getElementById("error-block");
                  errBlock.textContent =
                     "Please check your username and password.";
                  errBlock.display = "block";
               }
            })
            .catch(function(err) {
               console.error(err);
               let errBlock = document.getElementById("error-block");
               errBlock.textContent =
                  "Something went wrong, please try again later.";
               errBlock.display = "block";
            });
      });
})();
