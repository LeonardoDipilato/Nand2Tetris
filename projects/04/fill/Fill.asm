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

(START)
    @KBD
    D=M

    //If (key) then GOTO BLACK
    @BLACK
    D;JNE

    //Else GOTO WHITE
    @WHITE
    0;JMP

(BLACK)
    @8191
    D=A

    (BLACK_LOOP)
        @SCREEN
        A=A+D
        M=-1
        D=D-1
        
        //If D>=0 then GOTO LOOP
        @BLACK_LOOP
        D+1;JNE

        //Else GOTO START
        @START
        0;JMP

(WHITE)
    @8191
    D=A

    (WHITE_LOOP)
        @SCREEN
        A=A+D
        M=0
        D=D-1
        
        //If D>=0 then GOTO LOOP
        @WHITE_LOOP
        D+1;JNE

        //Else GOTO START
        @START
        0;JMP