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


function wavesurfertool() {
  wavesurfer2 = window.wavesurfer;
   wavesurfer2.on("ready", function () {
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
       seekingPos = ~~(wavesurfer2.backend.getPlayedPercents() * length);
       st.tempo = wavesurfer2.getPlaybackRate();
       if (st.tempo === 1 || !supportedBrowser()) {
         wavesurfer2.backend.disconnectFilters();
       } else {
         wavesurfer2.backend.setFilter(soundtouchNode);
       }
     });

     wavesurfer2.on("pause", function () {
       soundtouchNode && soundtouchNode.disconnect();
     });
   
     wavesurfer2.on("seek", function () {
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
    console.log("You are using Google Chrome.");
    return true;
  } else if (navigator.userAgent.indexOf("Firefox") !== -1) {
    console.log("You are using Mozilla Firefox.");
   return false;
  } else {
    console.log("Browser detection not supported or unknown browser.");
    return null;
  }
}