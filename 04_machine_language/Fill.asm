// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

	@R1 		// keep previous key value
	M=0

	@SCREEN     // screen begins
	D=A
	@R2
	M=D
	@8192       // num of pixels
	D=A
	@R3
	M=D  
	
	@4095
	D=A
	@R5
	M=D         // should be 65535 in 16 bit word, but some bugs prevent me from doing so

	@R6
	M=0
    
(MAIN_LOOP)
	@24576      // keyboard mem
	D=M;
	@R1
	D=M-D
	@DRAW_SCREEN
	D;JNE

	@MAIN_LOOP
	0;JMP
	
// function that used to draw the SCREEN
// D <> 0 black the screen
// D = 0  white the screen
(DRAW_SCREEN)
	@R4
	M=0         // counter

	@24576      // keyboard mem
	D=M;
	@R1
	M=D	        // save the new key code

(LOOP)
	@R4
	D=M
	@R3
	D=M-D
	@END
	D;JEQ       // draw finished
		
	@R1
	D=M
	@WHITE
	D;JEQ
	
	@R2         // TODO need to improve this part
	D=M
	@R4
	A=M+D       // current pixel	
	M=1
	@CONT
	0;JMP
(WHITE)
	@R2
	D=M
	@R4
	A=M+D       // current pixel
	M=0
(CONT)	
	@R4
	M=M+1       // increase the counter
	@LOOP
	0;JMP
	
(END)
	@MAIN_LOOP
	0;JMP

	