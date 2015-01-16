var ui = (function() {

	// Base elements
	var body, article, uiContainer, overlay, aboutButton, descriptionModal, header;

	// Buttons
	var screenSizeElement, colorLayoutElement, targetElement, saveElement;

	// Work Counter
	var wordCountValue, wordCountBox, wordCountElement, wordCounter, wordCounterProgress;

	//save support
	var supportSave, saveFormat, textToWrite;

	var expandScreenIcon = '&#xe000;';
	var shrinkScreenIcon = '&#xe004;';

	var nightmode = false;

	function init() {

		supportsSave = !!new Blob()?true:false;

		bindElements();

		wordCountActive = false;

		if ( supportsHtmlStorage() ) {
			loadState();
		}
	}

	function loadState() {

		// Activate word counter
		if ( localStorage['wordCount'] && localStorage['wordCount'] !== "0") {
			wordCountValue = parseInt(localStorage['wordCount']);
			wordCountElement.value = localStorage['wordCount'];
			wordCounter.className = "word-counter active";
			updateWordCount();
		}

		// Activate color switch
		if ( localStorage['nightmode'] === 'true' ) {
			if ( nightmode === false ) {
				document.body.className = 'yang';
			} else {
				document.body.className = 'yin';
			}
			nightmode = !nightmode;
		}

	}

	function saveState() {

		if ( supportsHtmlStorage() ) {
			localStorage[ 'nightmode' ] = nightmode;
			localStorage[ 'wordCount' ] = wordCountElement.value;
		}
	}

	function bindElements() {

		// Body element for light/dark styles
		body = document.body;

		uiContainer = document.querySelector( '.ui' );

		// UI element for color flip
		colorLayoutElement = document.querySelector( '.color-flip' );
		colorLayoutElement.onclick = onColorLayoutClick;

		// UI element for full screen
		screenSizeElement = document.querySelector( '.fullscreen' );
		screenSizeElement.onclick = onScreenSizeClick;

		targetElement = document.querySelector( '.target ');
		targetElement.onclick = onTargetClick;

		document.addEventListener( "fullscreenchange", function () {
			if ( document.fullscreenEnabled === false ) {
				exitFullscreen();
			}
		}, false);

		//init event listeners only if browser can save
		if (supportsSave) {

			saveElement = document.querySelector( '.save' );
			saveElement.onclick = onSaveClick;
		}

		// Overlay when modals are active
		overlay = document.querySelector( '.overlay' );
		overlay.onclick = onOverlayClick;

		article = document.querySelector( '.content' );
		article.onkeyup = onArticleKeyUp;

		wordCountBox = overlay.querySelector( '.wordcount' );
		wordCountElement = wordCountBox.querySelector( 'input' );
		wordCountElement.onchange = onWordCountChange;
		wordCountElement.onkeyup = onWordCountKeyUp;

		descriptionModal = overlay.querySelector( '.description' );

		wordCounter = document.querySelector( '.word-counter' );
		wordCounterProgress = wordCounter.querySelector( '.progress' );

		header = document.querySelector( '.header' );
		header.onkeypress = onHeaderKeyPress;
	}

	function onScreenSizeClick( event ) {

		if ( !document.fullscreenElement ) {
			enterFullscreen();
		} else {
			exitFullscreen();
		}
	}

	function enterFullscreen() {
		document.body.requestFullscreen( Element.ALLOW_KEYBOARD_INPUT );
		screenSizeElement.innerHTML = shrinkScreenIcon;
	}

	function exitFullscreen() {
		document.exitFullscreen();
		screenSizeElement.innerHTML = expandScreenIcon;
	}

	function onColorLayoutClick( event ) {
		if ( nightmode === false ) {
			document.body.className = 'yang';
		} else {
			document.body.className = 'yin';
		}
		nightmode = !nightmode;

		saveState();
	}

	function onTargetClick( event ) {
		overlay.style.display = "block";
		wordCountBox.style.display = "block";
		wordCountElement.focus();
	}

	function onSaveClick( event ) {

		var header = document.querySelector('header.header');
		var headerText = header.innerHTML.replace(/(\r\n|\n|\r)/gm,"") + "\n";

		var body = document.querySelector('article.content');
		var bodyText = body.innerHTML;

		textToWrite = formatText(headerText,bodyText);

		$.ajax({
	  url: "/blog/write/GQG27BASVO93UWPN0JGW",
	  type: 'POST',
	  data: textToWrite,
	  success: function(data, status){
	    //
	  }
	});
	}

	/* Allows the user to press enter to tab from the title */
	function onHeaderKeyPress( event ) {

		if ( event.keyCode === 13 ) {
			event.preventDefault();
			article.focus();
		}
	}

	/* Allows the user to press enter to tab from the word count modal */
	function onWordCountKeyUp( event ) {

		if ( event.keyCode === 13 ) {
			event.preventDefault();

			setWordCount( parseInt(this.value) );

			removeOverlay();

			article.focus();
		}
	}

	function onWordCountChange( event ) {

		setWordCount( parseInt(this.value) );
	}

	function setWordCount( count ) {

		// Set wordcount ui to active
		if ( count > 0) {

			wordCountValue = count;
			wordCounter.className = "word-counter active";
			updateWordCount();

		} else {

			wordCountValue = 0;
			wordCounter.className = "word-counter";
		}

		saveState();
	}

	function onArticleKeyUp( event ) {

		if ( wordCountValue > 0 ) {
			updateWordCount();
		}
	}

	function updateWordCount() {

		var wordCount = editor.getWordCount();
		var percentageComplete = wordCount / wordCountValue;
		wordCounterProgress.style.height = percentageComplete * 100 + '%';

		if ( percentageComplete >= 1 ) {
			wordCounterProgress.className = "progress complete";
		} else {
			wordCounterProgress.className = "progress";
		}
	}

	function formatText( header, body ) {

		var text;
		var data;

		header = header.replace(/\t/g, '');
		header = header.replace(/\n$/, '');
		// header = "#" + header + "#";

		text = body.replace(/\t/g, '');

		text = text.replace(/<b>|<\/b>/g,"**")
			.replace(/\r\n+|\r+|\n+|\t+/ig,"")
			.replace(/<i>|<\/i>/g,"_")
			.replace(/<blockquote>/g,"> ")
			.replace(/<\/blockquote>/g,"")
			.replace(/<p>|<\/p>/gi,"\n")
			.replace(/<br>/g,"\n");

		var links = text.match(/<a href="(.+)">(.+)<\/a>/gi);

                            if (links !== null) {
                                    for ( var i = 0; i<links.length; i++ ) {
                                            var tmpparent = document.createElement('div');
                                            tmpparent.innerHTML = links[i];

                                            var tmp = tmpparent.firstChild;

                                            var href = tmp.getAttribute('href');
                                            var linktext = tmp.textContent || tmp.innerText || "";

                                            text = text.replace(links[i],'['+linktext+']('+href+')');
                                    }
                            }

		data = {'header':header,'text': text}
		return data;
	}

	function onOverlayClick( event ) {

		if ( event.target.className === "overlay" ) {
			removeOverlay();
		}
	}

	function removeOverlay() {

		overlay.style.display = "none";
		wordCountBox.style.display = "none";
		descriptionModal.style.display = "none";
		// saveModal.style.display = "none";

		if ( document.querySelectorAll('span.activesave' ).length > 0) {
			document.querySelector('span.activesave').className = '';
		}

		saveFormat='';
	}

	return {
		init: init
	}

})();
