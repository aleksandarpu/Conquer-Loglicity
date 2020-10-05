# Conquer-Loglicity
Simple board like game for the lower grades of the primary school
"Conquer-Loglicity"

### The game
1. On the start page select how many players will play (1..5)
2. Before the player can move, press the spacebar to roll dice for (1..4) moves
3. Move player smile icon on the table pressing cursor keys
4. You can't go trough the walls (red lines on table)
5. If you step onto one of symbol, the random question will pop-up
   There is 4 category of questions
   1. Language ('L' icon)
   2. Math ('5' icon)
   3. Assotiations ('A' icon)
   4. Logical questions ('star' icon)
6. Select answer with up and down cursor keys and press <enter>
7. If answer is correct, you get points and additional 2 moves
8. If answer is wrong, you lose all your moves and next player turns
9. Game is finished when player reach 'crown' icon
  
## Python project 
Opensource code

## Require
pygame

## Other files
### Question icons location
The positions of the question icons are in data/fields.txt
Format is 
 #type, column, row
 L,0,8
Description:
L - language questions
0 - column 0 - the leftmost column
8 - row 8 - the postion above last row

### Walls location
The positions of the walls are in data/walls.txt
For horizontal walls the column and the position of the cell above the wall is set

#Horizontal walls: H column and the position
H 0 2

For the vertical walls the row and the position of the cell left of the wall is set
#Vertica walls: V row position
V 0 7, V 1 0, V 1 2, V 1 7, V 2 2, V 3 6, V 4 5, V 4 6, V 4 8

### Questions
The questions are in 

  data/questions-asoc.txt 
  data/questions-math.txt 
  data/questions-srpski.txt 
  data/questions-zvezda.txt 
  
Not all questions have the image attached, but you can se path in header of each question. e.g.
  
  Q5:4:'QuestionImagesMatematika\_01.jpeg'

1. first part is Q5
Q - Question header row
5 - math question (L for language, A for assotiations, Z for star)
2. second part is
4 - correct answer index
3. optional third part is relative path to question image
