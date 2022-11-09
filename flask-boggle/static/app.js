class BoggleGame {
    // Creates a new instance of Boggle
    constructor(boardId, secs = 60) {
        this.words = new Set();
        this.board = $("#" + boardId);
        this.score = 0;

        this.secs = secs;
        this.showTimer();

        // every 1000 msec, "tick"
        this.timer = setInterval(this.tick.bind(this), 1000);

        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }    

    // show word in list of words
    showWord(word) {
        $(".words", this.board).append($("<li>", {text: word}));
    }

    // show score in html
    showScore() {
        $(".score", this.board).text(this.score);
    }

    // show status message
    showMessage(msg, cls) {
        $(".msg", this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }

    // check if word submitted is unique and valid
    async handleSubmit(e) {
        e.preventDefault();
        const $word = $(".word", this.board);

        let word = $word.val()
        if(!word) return; 

        if (this.words.has(word)){
            this.showMessage(`You've already found the word, "${word}"`, "error");
            return; 
        }
        // check server for validity
        const response = await axios.get("/check-word", {params: {word: word}});
        if (response.data.result === "not-word") {
            this.showMessage(`${word} is not a valid word`, "err");
        } else if (response.data.result === "not-on-board") {
            this.showMessage(`${word} is not on the board`, "err");
        } else {
            this.showWord(word);
            this.words.add(word);
            this.showMessage(`${word} added!`, "ok");
            this.score += word.length;
            this.showScore();
        }

        $word.val("").focus();
    }

    // Update timer in DOM
    showTimer() {
        $(".timer", this.board).text(this.secs);
    }

    // Tick: handle a second passing in game
    async tick() {
        this.secs -= 1;
        this.showTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    // end of game: score and update message
    async scoreGame() {
        $(".add-word", this.board).hide();
        const response = await axios.post("/post-score", {score: this.score});
        if (response.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`, "ok");
        } else {
            this.showMessage(`Final score: ${this.score}`, "ok");
        }
    }
}   
