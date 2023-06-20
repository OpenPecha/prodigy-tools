setTimeout(() => {
    changeTitles();
    let transcript = document.getElementById("transcript");
  
    let tribute = new Tribute({
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
  
    tribute.attach(transcript);
  }, 100);
  function changeTitles() {
    let title = "Pecha Tools";
    document.title = title;
    let sideBarTitle = document.querySelector(".prodigy-sidebar-title");
    sideBarTitle.innerHTML = "<h1>" + title + "</h1>";
  }
  
  