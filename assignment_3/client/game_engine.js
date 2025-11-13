let board = document.getElementsByClassName("board")[0];

let board_width = 600;
let board_height = 500;

let board_row = 9;
let board_col = 6;

for(let i = 0; i < board_row; i++){
    for(let j = 0; j < board_col; j++){
        let atom_container = document.createElement("div");
        atom_container.classList.add("atom-container");
        atom_container.classList.add(`r${i+1}c${j+1}`);
        atom_container.style.top = `${i * board_height/board_row}px`;
        atom_container.style.left = `${j * board_width/board_col}px`; 
        board.appendChild(atom_container);
    }
}


let turn = "R";
board.classList.add(turn);

let change_turn = ()=>{
    let turn_select = document.querySelector(".turn.select");

    if(turn == "R"){
        turn = "B";
        turn_select.classList.add("bottom");
    }else{
        turn = "R";
        turn_select.classList.remove("bottom");
    }

}

let board_state = [];
// initializing the board_state with "0"
for(let i=0;i<board_row;i++){
    board_state.push([]);
    for(let j=0;j<board_col;j++){
        board_state[i].push("0");
    }
}

let corner_cells = [
    [1, 1],
    [1, board_col],
    [board_row, 1],
    [board_row, board_col]
];

const get_from_server = async () => {
    fetch("http://localhost:3000/get")
    .then(response => response.text())
    .then((data)=>{
        data = data.split("\n");
        for(let i = 1; i< data.length; i++){
            let vals = data[i].split(" ");
            for(let j = 0; j < 6; j++){
                board_state[i - 1][j] = vals[j];
            }
        }
    })
}

const send_to_server = (current_board, current_turn) => {

    let data = {
        turn : (current_turn == "R"? "Human Move" : "AI Move"),
        current_board: current_board
    }
    
    fetch("http://localhost:3000/send",{
        method: "POST",
        headers:{"content-type":"application/json"},
        body:JSON.stringify(data)
    })
}

let count_down = false;

let score_update = (current_board) => {
    let r_score = 0;
    let b_score = 0;

    for(let i = 0; i < board_row; i++){
        for(let j = 0; j < board_col; j++){
            if(current_board[i][j] == "0")
                continue;

            if(current_board[i][j][1] == "R")
                r_score++;
            else if(current_board[i][j][1] == "B")
                b_score++;
        }
    }

    if(r_score > 0 && b_score > 0)
        count_down  = true;

    if(count_down && (r_score == 0 || b_score == 0)){
        game_over = true;
        document.querySelector(".result").classList.remove("n_visible");
        let curtain = document.querySelector(".result .curtain");
        let message = document.querySelector(".result .message");
        if(r_score == 0){
            curtain.classList.add("B");
            message.innerHTML = `Blue has won: ${b_score}`;
        }else{
            message.innerHTML = `Red has won: ${r_score}`;
        }

    }

    document.querySelector(".score.r_score").innerHTML = r_score;
    document.querySelector(".score.b_score").innerHTML = b_score;

}

let check_corner_cells = (current_row, current_col)=>{
    for (const cell of corner_cells){
        if(cell[0] == current_row && cell[1] == current_col)
            return true;
    }

    return false;
}

let check_side_cells = (current_row, current_col)=>{
    if(!check_corner_cells(current_row, current_col)
        && (current_row == 1 || current_row == board_row
        || current_col == 1 || current_col == board_col)){
            return true;
    }

    return false;
}

const propagate = (board_state, current_row, current_col, current_turn) => {

    let state = board_state[current_row - 1][current_col - 1];

    if(state == "0"){

        board_state[current_row - 1][current_col - 1] = "1"+ current_turn;
        return true;
    }

    let atoms_in_cell = parseInt(state[0]);

    if(check_corner_cells(current_row, current_col)){
        
        if(atoms_in_cell + 1 < 2){

            atoms_in_cell++;
            board_state[current_row - 1][current_col - 1] = String(atoms_in_cell) + current_turn;

        }else{
            
            board_state[current_row - 1][current_col - 1] = "0";
            
            if(current_row == 1 && current_col == 1){
                propagate(board_state, current_row + 1, current_col, current_turn);
                propagate(board_state, current_row, current_col + 1, current_turn);
            }else if(current_row == 1 && current_col == board_col){
                propagate(board_state, current_row + 1, current_col, current_turn);
                propagate(board_state, current_row, current_col - 1, current_turn);
            }else if(current_row == board_row && current_col == 1){
                propagate(board_state, current_row - 1, current_col, current_turn);
                propagate(board_state, current_row, current_col + 1, current_turn);
            }else if(current_row == board_row && current_col == board_col){
                propagate(board_state, current_row - 1, current_col, current_turn);
                propagate(board_state, current_row, current_col - 1, current_turn);
            }

            return true;
        }
    
    }else if(check_side_cells(current_row, current_col)){

        if(atoms_in_cell + 1 < 3){
            atoms_in_cell++;
            board_state[current_row - 1][current_col - 1] = String(atoms_in_cell) + current_turn;
            return true;
        }else{
            board_state[current_row - 1][current_col - 1] = "0";
           if(current_row == 1){
                propagate(board_state, current_row, current_col - 1, current_turn);
                propagate(board_state, current_row + 1, current_col, current_turn);
                propagate(board_state, current_row, current_col + 1, current_turn);
            }else if(current_row == board_row){
                propagate(board_state, current_row - 1, current_col, current_turn);
                propagate(board_state, current_row, current_col - 1, current_turn);
                propagate(board_state, current_row, current_col + 1, current_turn);
            }else if(current_col == 1){
                propagate(board_state, current_row - 1, current_col, current_turn);
                propagate(board_state, current_row + 1, current_col, current_turn);
                propagate(board_state, current_row, current_col + 1, current_turn);
            }else if(current_col == board_col){
                propagate(board_state, current_row - 1, current_col, current_turn);
                propagate(board_state, current_row + 1, current_col, current_turn);
                propagate(board_state, current_row, current_col - 1, current_turn);
            }
        }

    }else{

        if(atoms_in_cell + 1 < 4){
            atoms_in_cell++;
            board_state[current_row - 1][current_col - 1] = String(atoms_in_cell) + current_turn;
            return true;
        }else{
            board_state[current_row - 1][current_col - 1] = String(0);
            propagate(board_state, current_row + 1, current_col, current_turn);
            propagate(board_state, current_row - 1, current_col, current_turn);
            propagate(board_state, current_row, current_col + 1, current_turn);
            propagate(board_state, current_row, current_col - 1, current_turn);
        }
        
    }

    return true;
}

const render = () =>{
    
    for(let i = 0; i < board_row; i++){
        for(let j = 0; j < board_col; j++){
            
            let state = board_state[i][j];
            if(state == "0"){
                
                let prev = board.getElementsByClassName(`r${i+1}c${j+1}`)[0];
                prev.innerHTML = "";
                continue;
            
            }else if(state[0] == "1"){
                
                let prev = board.getElementsByClassName(`r${i+1}c${j+1}`)[0];
                prev.innerHTML = "";

                let mono_atom = document.createElement("div");
                mono_atom.classList.add("mono-atom");
                mono_atom.innerHTML = `<div class="atom atom1"></div>`;
                
                if(state[1] == "R"){
                    mono_atom.classList.add("R");
                }else if(state[1] == "B"){
                    mono_atom.classList.add("B");
                }

                prev.appendChild(mono_atom);
            }else if(state[0] == "2"){

                let prev = board.getElementsByClassName(`r${i+1}c${j+1}`)[0];
                prev.innerHTML = "";

                let di_atom = document.createElement("div");
                di_atom.classList.add("di-atom");
                di_atom.classList.add("rotating-slow");
                di_atom.innerHTML = 
                `<div class="atom atom1"></div>
                <div class="atom atom2"></div>`;

                if(state[1] == "R"){
                    di_atom.classList.add("R");
                }else if(state[1] == "B"){
                    di_atom.classList.add("B");
                }

                prev.appendChild(di_atom);

            }else if(state[0] == "3"){

                let prev = board.getElementsByClassName(`r${i+1}c${j+1}`)[0];
                prev.innerHTML = "";

                let tri_atom = document.createElement("div");
                tri_atom.classList.add("tri-atom");
                tri_atom.classList.add("rotating-fast");
                tri_atom.innerHTML =
                `<div class="atom atom1"></div>
                <div class="atom atom2"></div>
                <div class="atom atom3"></div>`;

                if(state[1] == "R"){
                    tri_atom.classList.add("R");
                }else if(state[1] == "B"){
                    tri_atom.classList.add("B");
                }

                prev.appendChild(tri_atom);
            }
        }
    }
}

const place_count_difference = (current_board)=>{
    let mx_agent_score = 0;

    for(let i = 0; i < board_row; i++){
        for(let j = 0; j < board_col; j++){
            if(current_board[i][j] == "0")
                continue;
            else if(current_board[i][j][1] == "R")
                mx_agent_score--;
            else 
                mx_agent_score++;
        }
    }

    return mx_agent_score;
}

const atom_count_difference = (current_board) => {
    let red = 0, blue = 0;
    for (let row of current_board) {
        for (let cell of row) {
            if (cell !== "0") {
                if (cell[1] === "R") red += parseInt(cell[0]);
                else if (cell[1] === "B") blue += parseInt(cell[0]);
            }
        }
    }
    return blue - red;
}

const critical_mass = (row, col) => {
    let neighbors = 0;
    if (row > 0) neighbors++;
    if (row < 8) neighbors++;
    if (col > 0) neighbors++;
    if (col < 5) neighbors++;
    return neighbors;
}

const critical_mass_score = (board) => {
    let score = 0;
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 6; j++) {
            let cell = board[i][j];
            if (cell !== "0") {
                let atoms = parseInt(cell[0]);
                let owner = cell[1];
                let diff = atoms - critical_mass(i, j);
                if (owner === "B") score += diff;
                else if (owner === "R") score -= diff;
            }
        }
    }
    return score;
}

const front_line_pressure = (board) => {
    let score = 0;
    const dirs = [[1,0],[-1,0],[0,1],[0,-1]];

    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 6; j++) {
            let cell = board[i][j];
            if (cell !== "0" && cell[1] === "B") {
                for (let [dx, dy] of dirs) {
                    let ni = i + dx, nj = j + dy;
                    if (ni >= 0 && ni < 9 && nj >= 0 && nj < 6) {
                        let neighbor = board[ni][nj];
                        if (neighbor !== "0" && neighbor[1] === "R") {
                            score++;
                        }
                    }
                }
            }
        }
    }
    return score;
}

const survivability_score = (board) => {
    let score = 0;
    const dirs = [[1,0],[-1,0],[0,1],[0,-1]];

    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 6; j++) {
            let cell = board[i][j];
            if (cell !== "0") {
                let owner = cell[1];
                let danger = 0;
                for (let [dx, dy] of dirs) {
                    let ni = i + dx, nj = j + dy;
                    if (ni >= 0 && ni < board_row && nj >= 0 && nj < board_col) {
                        let neighbor = board[ni][nj];
                        if (neighbor !== "0" && neighbor[1] !== owner) {
                            danger++;
                            // console.log(2.2);
                        }
                    }
                }
                if (owner === "B"){score -= 2*danger;}
                else if (owner === "R") score += danger;
            }
        }
    }
    // console.log(score);

    return score;
}

const combined_score = (current_board) => {
    return 0.4*place_count_difference(current_board) 
            + 0.1*atom_count_difference(current_board) 
            + 0.1*critical_mass_score(current_board)
            + 0.2*survivability_score(current_board)
            + 0.1*front_line_pressure(current_board);
}

const find_max_agent_moves = (current_board)=>{
    let mx_agent_moves = [];

    for(let i = 0; i < board_row; i++){
        for(let j = 0; j < board_col; j++){
            if(current_board[i][j] != "0" && current_board[i][j][1] == "R")
                continue;
            else 
                mx_agent_moves.push([i + 1, j + 1]);
        }
        // console.log("mx_moves ", mx_agent_moves);
    }

    return mx_agent_moves;
}

const find_min_agent_moves = (current_board)=>{
    let mn_agent_moves = [];

    for(let i = 0; i < board_row; i++){
        for(let j = 0; j < board_col; j++){
            if(current_board[i][j] != "0" && current_board[i][j][1] == "B")
                continue;
            else 
                mn_agent_moves.push([i + 1, j + 1]);
        }
    }

    return mn_agent_moves;
}


const init_depth = 3;
const min_max = (current_board, depth, alpha, beta, maximizing_agent, bst_move, score_heuristic)=>{
    if(depth == 0){
        return score_heuristic(current_board);
    }

    if(maximizing_agent){
        // console.log(2.1);
        let max_val = - Infinity;
        let mx_agent_moves = find_max_agent_moves(current_board);
        for(let pos of mx_agent_moves){
            let new_board = current_board.map(row => [...row]);
            propagate(new_board, pos[0], pos[1], "B");
            
            let val = min_max(new_board, depth - 1, alpha, beta,false, bst_move, score_heuristic);
            if(max_val < val && depth == init_depth){
                bst_move[0] = pos[0];
                bst_move[1] = pos[1];
            }
            
            max_val = Math.max(max_val, val);
            // console.log(pos, " ", val, " ", max_val);
            alpha = Math.max(alpha, val);
            
            if(alpha >= beta)
                break;
        }

        return max_val;
    }else{
        // console.log(2.3);
        let min_val = Infinity;
        let min_agent_moves = find_min_agent_moves(current_board);
        for(let pos of min_agent_moves){
            let new_board = current_board.map(row => [...row]);
            propagate(new_board, pos[0], pos[1], "R");
            
            let val = min_max(new_board, depth - 1, alpha, beta, true, bst_move, score_heuristic);
            
            min_val = Math.min(min_val, val);
            // if(min_val == val){
            //     // console.log("pos ", pos, " bst moves ", bst_move);
            //     bst_move[0] = pos[0];
            //     bst_move[1] = pos[1];
            // }
            beta = Math.min(beta, val);
            
            if(alpha >= beta)
                break;
        }

        return min_val;
    }
}

let focus_cell;

const AI_move = (score_heuristic) => {
    let bst_move = [0, 0];
    let new_board = board_state.map(row => [...row]);
    let val = min_max(new_board, init_depth, -Infinity, +Infinity, true, bst_move, score_heuristic);
    // console.log(bst_move);

    // if(bst_move[0] == 0 && bst_move[1] == 0){
    //     bst_move = find_max_agent_moves(board_state)[0];
    // //     for(let i = 0; i < bst_move.length; i++){

    // //     }
    //     console.log("2.6 ",bst_move);

    // }
    // console.log(1.2, new_board);
    propagate(board_state, bst_move[0], bst_move[1], "B");

    score_update(board_state);

    if(focus_cell)
        focus_cell.style.backgroundColor = "";
    focus_cell = board.getElementsByClassName(`r${bst_move[0]}c${bst_move[1]}`)[0];
    focus_cell.style.backgroundColor = "gold";
}

let game_over = false;

board.addEventListener("click",(e)=>{
    // console.log(e);
    e.preventDefault();
    e.stopPropagation();
    // send_to_server(board_state, turn);
    if(turn == "B" || game_over)
        return;

    let board_top_left = [board.getBoundingClientRect().top, board.getBoundingClientRect().left];
    let click_location = [e.clientX, e.clientY];

    let cell_col = Math.ceil( (click_location[0] - board_top_left[1]) / (600/6) );
    let cell_row = Math.ceil( (click_location[1] - board_top_left[0]) / (500/9) );
    let current_cell = [cell_col, cell_row]
    // console.log(current_cell);
    
    if((board_state[cell_row - 1][cell_col - 1][1] 
        && board_state[cell_row - 1][cell_col - 1][1] == turn)
        || board_state[cell_row - 1][cell_col - 1] == "0"){

        // console.log(1.4);
        // try{
            propagate(board_state, cell_row, cell_col, turn);
            // console.log(board_state);
        // }catch(error){
        //     console.log(error);
        //     game_over = true;
        //     document.querySelector(".result").classList.remove("n_visible");
        //     let curtain = document.querySelector(".result .curtain");
        //     let message = document.querySelector(".result .message");
        //     message.innerHTML = `Red has won: ${r_score}`;
        // }

        score_update(board_state);
        
        board.classList.remove(turn); 
        change_turn();
        board.classList.add(turn); 
        // console.log(board_state);
        
        if(focus_cell)
            focus_cell.style.backgroundColor = "";
        focus_cell = board.getElementsByClassName(`r${cell_row}c${cell_col}`)[0];
        focus_cell.style.backgroundColor = "gold";
        render();

        // we have considered the Blue turn to be the turn of AI
        setTimeout(() => {
            if(turn == "B" && !game_over){
                // AI will choose the best move and propagate it 
                // try{
                    AI_move(survivability_score);
                // }catch(error){
                //     console.log(error);
                //     game_over = true;
                //     document.querySelector(".result").classList.remove("n_visible");
                //     let curtain = document.querySelector(".result .curtain");
                //     let message = document.querySelector(".result .message");
                //     curtain.classList.add("B");
                //     message.innerHTML = `Blue has won: ${b_score}`;
                // }


                // change turn
                board.classList.remove(turn); 
                change_turn();
                board.classList.add(turn); 
                
                
                render();
            }
        }, 1000);

    }
    
})

document.querySelector(".replay").addEventListener("click", (e)=>{
    e.preventDefault();
    location.reload();
})
