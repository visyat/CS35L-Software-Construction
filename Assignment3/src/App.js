//Vishal Yathish

import { useState } from "react";

function Square({value, onSquareClick}) {
  return <button className="square" onClick={onSquareClick}>{value}</button>;
}

//function that determines the victor of the game - 3 in a row 
function determineVictor(values)
{
  const boardRows = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
  ];

  for (let i = 0; i < boardRows.length; i++)
  {
    const [a,b,c] = boardRows[i];
    if (values[a] && values[a] === values [b] && values[a] === values[c])
      return values[a]; 
  }
  return null;
}

export default function Board() 
{
  const [values, setValues] = useState(Array(9).fill(null));
  const [savedCopy, setSavedCopy] = useState(Array(9).fill(null));

  //const [values, setValues] = useState([0,1,2,3,4,5,6,7,8]);
  const [xIsNext, setXIsNext] = useState(true);

  const [moveCount, setMoveCount] = useState(1); 
  const [movingPiece, setMovingPiece] = useState(-1); 

  function centerSquareFull()
  {
    if (xIsNext && savedCopy[4]=="X")
      return "X";
    else if (!xIsNext && savedCopy[4]=="O")
      return "O"; 
    else  
      return null;
  }

  function checkValidMove(i) 
  {
    if (values[i] == null)
    {
      //console.log("Error 1");
      if (movingPiece != i)
      {
        if (movingPiece == 0)
          return (i == 1 || i == 3 || i == 4);
        if (movingPiece == 1)
          return (!(i==6 || i==7 || i==8));
        if (movingPiece==2)
          return (i==1 || i==4 || i==5);
        if (movingPiece==3)
          return (! (i==2 || i==5 || i==8));
        if (movingPiece==4)
          return (true);
        if (movingPiece==5)
          return (! (i==0 || i==3 || i==6));
        if (movingPiece==6)
          return (i==3 || i==4 || i==7);
        if (movingPiece==7)
          return (! (i==0 || i==1 || i==2)); 
        if (movingPiece==8)
          return (i==7 || i==4 || i==5);
      }
      else
        return false;
    }
    else 
    {
      return false;
    }
  }

  function handleClick(i) 
  {
    if (determineVictor(values))
      return;

    const newValues = values.slice();
    if (moveCount <= 6)
    {
      if (values[i])
        return; 

      if (xIsNext) {
        newValues[i] = "X"; 
      }
      else {
        newValues[i] = "O"; 
      } 
      setMoveCount(moveCount+1);
      setXIsNext(!xIsNext);
    }
    else
    {
      if (movingPiece == -1) 
      {
        //console.log("MP Before Change" + movingPiece);
        if (values[i] == null)
          return; 
        else if (xIsNext && values[i] != "X")
          return; 
        else if (!xIsNext && values[i] != "O")
          return;

        newValues[i] = null;
        setMovingPiece(i); 
        setSavedCopy(values.slice());
        //console.log("MP After Change" + movingPiece);
      }
      else 
      {
        //console.log("MP in Else: " + movingPiece);
        if (!checkValidMove(i))
        {
          console.log("Invalid Move!");
          setValues(savedCopy); 
          setMovingPiece(-1);
          return;
        }
        if (xIsNext) {
          newValues[i] = "X"; 
        }
        else {
          newValues[i] = "O"; 
        }
        setMoveCount(moveCount+1);
        if (centerSquareFull() != null)
        {
          //console.log(centerSquareFull());
          if (determineVictor(newValues)==centerSquareFull()) {}
          else if (newValues[4]==null) {}
          else 
          {
            console.log("Your Move Must Either Empty the Center Square or Win!");
            setValues(savedCopy);
            setMovingPiece(-1);
            return;
          }
        }
        setXIsNext(!xIsNext);
        setMovingPiece(-1);
        setSavedCopy(Array(9).fill(null));
      }
    }
    setValues(newValues);
  }

  const victor = determineVictor(values);
  let status; 
  if (victor)
  {
    status = "Victor: " + victor + "!!"; 
  }
  else 
  {
    status = "Next Player: " + (xIsNext ? "X" : "O");
  }

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={values[0]} onSquareClick={() => handleClick(0)} />
        <Square value={values[1]} onSquareClick={() => handleClick(1)} />
        <Square value={values[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={values[3]} onSquareClick={() => handleClick(3)} />
        <Square value={values[4]} onSquareClick={() => handleClick(4)} />
        <Square value={values[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={values[6]} onSquareClick={() => handleClick(6)} />
        <Square value={values[7]} onSquareClick={() => handleClick(7)} />
        <Square value={values[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}
