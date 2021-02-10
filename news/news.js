const CORS_PROXY = "https://api.allorigins.win/raw?url="

let parser = new RSSParser();
let journalducameroun = `https://www.journalducameroun.com/feed/`
let investiraucameroun = `https://www.investiraucameroun.com/component/obrss/fullrss`
let futurasciences = `https://www.futura-sciences.com/rss/actualites.xml`
let developpez = `https://www.developpez.com/index/rss`

function addElement (newsElement, newsClassID) {
  var newDiv = document.createElement("div");
  newDiv.innerHTML = newsElement;

  var currentDiv = document.getElementById(newsClassID);
  currentDiv.append(newDiv)
}

function showNews(url, newsClassID) {
    parser.parseURL(CORS_PROXY + url, function(err, feed) {
      if (err) throw err;
      feed.items.forEach(function(entry) {
        var newsElement = `<div>
            <h4><a href=${entry.link} target='_blank'>${entry.title}</a></h4>
        </div>`
        document.body.onload = addElement(newsElement, newsClassID);
      })
  })
}

showNews(journalducameroun, 'journalducameroun')
showNews(investiraucameroun, 'investiraucameroun')
showNews(futurasciences, 'futurasciences')
showNews(developpez, 'developpez')




