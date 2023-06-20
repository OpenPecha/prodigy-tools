let tribute;
setTimeout(() => {
  changeTitles();
  let transcript = document.getElementById("transcript");
   tribute = new Tribute({
  values: function (text, callback) {
    let data = dict
      .filter((item) => {
        return item.includes(text);
      })
      .slice(0, 5);
    let newDictionary = data.map((item) => ({ key: item, value: item }));
    callback(newDictionary);
  },
  autocompleteMode: true,
  noMatchTemplate: function (item) {
    return null;
  },
  requireLeadingSpace: false,
  menuShowMinLength: 0,
});
  if (transcript) {
    tribute.attach(transcript);
  }
}, 100);

let buttons = [
  ".prodigy-button-accept",
  ".prodigy-button-reject",
  ".prodigy-button-ignore",
  ".prodigy-button-undo",
];

for (let i = 0; i < buttons.length; i++) {
  document.querySelector(buttons[i]).addEventListener("click", () => {
    setTimeout(() => {
      let transcript = document.getElementById("transcript");
      tribute.detach(transcript);
      tribute.attach(transcript);
    }, 1000);
  });
}

function changeTitles() {
  let title = "Pecha Tools";
  document.title = title;
  let sideBarTitle = document.querySelector(".prodigy-sidebar-title");
  sideBarTitle.innerHTML = "<h1>" + title + "</h1>";
}
