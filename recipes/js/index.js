setTimeout(() => {
  changeTitles();
  let transcript = document.getElementById("transcript");

  let tribute = new Tribute({
    values: function (text, callback) {
       fetch(`https://dictionaryprodigy.netlify.app/api/dictionary/${text}`)
         .then((res) => res.json())
         .then((data) => {
           callback(data);
         }).catch(err=>console.log(err))
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
function changeTitles() {
  let title = "Pecha Tools";
  document.title = title;
  let sideBarTitle = document.querySelector(".prodigy-sidebar-title");
  sideBarTitle.innerHTML = "<h1>" + title + "</h1>";
}
