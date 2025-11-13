const express = require('express');
const cors = require('cors');
const fs = require('fs');
const { stringify } = require('querystring');

const app = express();
app.use(cors());
app.use(express.json());

app.get("/get", (req, res) => {
    let data = fs.readFileSync("./gamestate.txt", 'utf-8');
    res.send(data);
})

app.post("/send", (req, res) => {
    let data = req.body;
    // console.log(data);
    let move = "";
    
    move += data.turn;
    move += ":\n";
    
    for(let i = 0; i < 9; i++){
        for(let j = 0; j < 6; j++){
            move += data.current_board[i][j];
            move += " ";
        }
        move += "\n";
    }

    fs.writeFileSync('./gamestate.txt', move);

    res.status(200).end();

});

const PORT = 3000;

app.listen(PORT, ()=>{
    console.log(`server is running on ${PORT}`);
});