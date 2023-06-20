setTimeout(() => {
  changeTitles();
  let transcript = document.getElementById("transcript");

  let tribute = new Tribute({
    values: function (text, callback) {
      fetchWithDebounce(text, callback);
    },
    autocompleteMode: true,
    noMatchTemplate: function (item) {
      return null;
    },
    requireLeadingSpace: false,
    menuShowMinLength: 0,
  });

  tribute.attach(transcript);
}, 100);



function fetchWithDebounce(text, callback) {
  if (fetchWithDebounce.controller) {
    fetchWithDebounce.controller.abort(); // Cancel previous request
  }

  fetchWithDebounce.controller = new AbortController();

  debounce(function () {
    fetch(`https://dictionaryprodigy.netlify.app/api/dictionary/${text}`, {
      signal: fetchWithDebounce.controller.signal,
    })
      .then((res) => res.json())
      .then((data) => {
        callback(data);
      })
      .catch((error) => {
        if (error.name === "AbortError") {
          console.log("Previous fetch request was aborted.");
        } else {
          console.log("Error occurred during fetch:", error);
        }
      });
  }, 500)();
}

function debounce(func, delay) {
  let timeoutId;

  return function (...args) {
    clearTimeout(timeoutId);

    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}

function changeTitles() {
  let title = "Pecha Tools";
  document.title = title;
  let sideBarTitle = document.querySelector(".prodigy-sidebar-title");
  sideBarTitle.innerHTML = "<h1>" + title + "</h1>";
}

