// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R2
M=0
@R1 // Times the loop has to be executed
D=M
@counter
M=D

// if counter > 0 GOTO LOOP
@LOOP
D;JGT

// else GOTO END
@END
0;JMP

// assumes it is executed at least once, so checks happen at the end
(LOOP)
    @R0
    D=M

    @R2
    M=M+D
    
    // counter--
    @counter
    M=M-1
    
    // if counter > 0 GOTO LOOP
    D=M
    @LOOP
    D;JGT

    // else GOTO END
    @END
    0;JMP

(END)
    @END
    0;JMP