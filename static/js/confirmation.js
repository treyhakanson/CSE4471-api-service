(function() {
   // set the phrase, and then begin listening for completion
   setPhrase().then(function() {
      listenForCompletion();
   });

   function listenForCompletion() {
      let interval = setInterval(function() {
         axios
            .post(API_BASE_URL + "/dual-factor-token")
            .then(function(res) {
               if (res.data && res.data.outcome === "successful") {
                  clearInterval(interval);
                  window.location.assign("/demo/profile");
               } else if (res.data && res.data.outcome !== "successful") {
                  clearInterval(interval);
                  setError(
                     "Passphrase could not be validated successfully. Please try again."
                  );
               } else {
                  hideError();
               }
            })
            .catch(function(err) {
               console.error(err);
            });
      }, 2000); // check for updates every 2 seconds
   }

   function setPhrase() {
      return axios
         .post(API_BASE_URL + "/phrase", {
            token: localStorage.getItem("token")
         })
         .then(function(res) {
            if (res.data.phrase) {
               hideError();
               document.getElementById("speak-icon").style.display = "inline";
               document.getElementById("passphrase-text").textContent =
                  res.data.phrase;
            } else {
               setError(
                  "Unable to retrieve passphrase. Please try again later."
               );
            }
         })
         .catch(function(err) {
            console.log(err);
            setError("An error occurred, please try again later.");
         });
   }

   function setError(text) {
      var errorBlock = document.getElementById("error-block");
      errorBlock.textContent = text;
      errorBlock.style.display = "block";
   }

   function hideError() {
      var errorBlock = document.getElementById("error-block");
      errorBlock.style.display = "none";
   }
})();
