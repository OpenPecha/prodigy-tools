let tribute;
let isUnsupportedBrowser = false;
let wavesurfer2;


var soundtouchNode;
setTimeout(() => {
  wavesurfertool();
}, 0);
function setplaybackrate(rate) {
  if (!supportedBrowser()&& rate!==1  ) {
    alert('please use chrome or brave browser to use this feature properly')
  }
  wavesurfer2.pause();
  wavesurfer2.setPlaybackRate(rate);
  wavesurfer2.play();
}

setTimeout(() => {
  changeTitles();
   initTribute();

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
  let title = "pecha.tools";
  document.title = title;
  let sideBarTitle = document.querySelector(".prodigy-sidebar-title");
  sideBarTitle.innerHTML = "<h1>" + title + "</h1>";
}


function wavesurfertool() {
  wavesurfer2 = window.wavesurfer;
  let finished = false;
  let pauseClicked = false;
  wavesurfer2.on("ready", function () {
    console.log('ready')
     var st = new window.soundtouch.SoundTouch(
       wavesurfer2.backend.ac.sampleRate
     );
     var buffer = wavesurfer2.backend.buffer;
     var channels = buffer.numberOfChannels;
     var l = buffer.getChannelData(0);
     var r = channels > 1 ? buffer.getChannelData(1) : l;
     var length = buffer.length;
     var seekingPos = null;
     var seekingDiff = 0;
     var source = {
       extract: function (target, numFrames, position) {
         if (seekingPos != null) {
           seekingDiff = seekingPos - position;
           seekingPos = null;
          }
          
         position += seekingDiff;

         for (var i = 0; i < numFrames; i++) {
           target[i * 2] = l[i + position];
           target[i * 2 + 1] = r[i + position];
          }
          
          return Math.min(numFrames, length - position);
        },
      };
       if (!soundtouchNode) {
         const filter = new window.soundtouch.SimpleFilter(source, st);
         soundtouchNode = window.soundtouch.getWebAudioNode(
           wavesurfer2.backend.ac,
           filter
         );
       }
    
    wavesurfer2.on("play", function () {
      finished = false;
      pauseClicked = false;
      let pausebutton = document.querySelector(['[data-test="pause"]']);
      pausebutton?.addEventListener("click", () => {
        pauseClicked=true;
       })
      seekingPos = ~~(wavesurfer2.backend.getPlayedPercents() * length);
       st.tempo = wavesurfer2.getPlaybackRate();
       if (st.tempo === 1 || !supportedBrowser()) {
         wavesurfer2.backend.disconnectFilters();
       } else {
         wavesurfer2.backend.setFilter(soundtouchNode);
       }
     });

    wavesurfer2.on("pause", function () {
      if (pauseClicked) {
         soundtouchNode && soundtouchNode.disconnect();
      } else {
        if (!finished) soundtouchNode && soundtouchNode.disconnect();
        //  wavesurfer2.backend.setFilter(soundtouchNode);
       }
     });
    wavesurfer2.on("finish", function () { 
      finished = true;
    })
     wavesurfer2.on("seek", function () {
       console.log("seek");
       seekingPos = ~~(wavesurfer2.backend.getPlayedPercents() * length);
     });
     wavesurfer2.on("redraw", function () {
       soundtouchNode && soundtouchNode.disconnect();
       wavesurfer2.backend.disconnectFilters();
       soundtouchNode = null;
      })
   });
}


function supportedBrowser() {
  if (navigator.userAgent.indexOf("Chrome") !== -1) {
    return true;
  } else if (navigator.userAgent.indexOf("Firefox") !== -1) {
   return false;
  } else {
    console.log("Browser detection not supported or unknown browser.");
    return null;
  }
  
}

function initTribute() {
  let transcript = document.getElementById("transcript");
  tribute = new Tribute({
    values: function (text, callback) {
      fetch(`https://dictionaryprodigy.netlify.app/api/dictionary/${text}`)
        .then((res) => res.json())
        .then((data) => {
          let addedot = data.map((item) => {
            if (item.value.endsWith("་")) {
              value = item.value.slice(0, -1);
              return { key: value, value: value };
            }
            return item;
          });
          callback(addedot);
        })
        .catch((err) => console.log(err));
    },
    autocompleteMode: true,
    noMatchTemplate: function (item) {
      return null;
    },
    allowSpaces: true,
    replaceTextSuffix: "་",
    requireLeadingSpace: false,
    menuShowMinLength: 0,
  });
  tribute.attach(transcript);
}