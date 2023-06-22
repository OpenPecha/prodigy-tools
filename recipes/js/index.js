let tribute;
let isUnsupportedBrowser = false;
let wavesurfer2;
var soundtouchNode;

if (navigator.userAgent.indexOf("Chrome") !== -1) {
  console.log("You are using Google Chrome.");
} else if (navigator.userAgent.indexOf("Firefox") !== -1) {
  console.log("You are using Mozilla Firefox.");
  isUnsupportedBrowser=true;
} else {
  console.log("Browser detection not supported or unknown browser.");
}

setTimeout(() => {
  wavesurfertool();
}, 0);

function setplaybackrate(rate) {
  var wavesurfer2 = window.wavesurfer;
  wavesurfer2.pause();
  wavesurfer2.setPlaybackRate(rate);
  wavesurfer2.play();
}

setTimeout(() => {
  changeTitles();
  let transcript = document.getElementById("transcript");

  tribute = new Tribute({
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
     console.log("audio wavesurfer ready");
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
       console.log(wavesurfer2.getDuration())
       seekingPos = ~~(wavesurfer2.backend.getPlayedPercents() * length);
       st.tempo = wavesurfer2.getPlaybackRate();
       if (st.tempo === 1 || isUnsupportedBrowser) {
         wavesurfer2.backend.disconnectFilters();
       } else {
         wavesurfer2.backend.setFilter(soundtouchNode);
       }
     });

     wavesurfer2.on("pause", function () {
       console.log("paused");
       soundtouchNode && soundtouchNode.disconnect();
     });
     wavesurfer2.on("finish", function () {
       console.log("finished");
     });
     wavesurfer2.on("interaction", function () {
       console.log("interaction");
     });
     wavesurfer2.on("seek", function () {
       console.log("seek");
       seekingPos = ~~(wavesurfer2.backend.getPlayedPercents() * length);
     });

     wavesurfer2.on("redraw", function () {
       console.log('redraw')
       soundtouchNode && soundtouchNode.disconnect();
         wavesurfer2.backend.disconnectFilters();
       soundtouchNode = null;
      })
   });
}