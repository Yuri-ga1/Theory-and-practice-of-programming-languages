; command for start programm:
; nasm -felf64 square.asm && gcc -no-pie -fno-pie square.o && ./x1.out
%macro pushd 0
    push rax
    push rbx
    push rcx
    push rdx
%endmacro

%macro popd 0
    pop rdx
    pop rcx
    pop rbx
    pop rax
%endmacro

%macro printres 1
    pushd
    push rdi
    mov rdi, format
    mov rsi, %1
    call printf
    pop rdi
    popd
%endmacro

%macro sqrt 0
    mov rax, [number]
    mov rbx, 2
    xor rdx, rdx
    div rbx ; rax = rax/2

    mov [x1], rax
    xor rdx, rdx
    xor rax, rax

    mov rax, [number]
    mov rcx, [x1]
    div rcx  ;rax = (num/x1) or (rax/rcx)
    xor rdx, rdx
    add rax, rcx ;rax = (num/x1) + x1

    div rbx ; rax = ((num/x1) + x1)/2
    mov [x2], rax


    .while:
        mov rsi, [x1]
        sub rsi, [x2] ;x1-x2

        mov rax, [x2]
        mov [x1], rax ; x1 = x2

        xor rdx, rdx
        xor rax, rax

        mov rax, [number]
        mov rcx, [x1]
        div rcx  ;rax = (num/x1) or (rax/rcx)
        xor rdx, rdx
        add rax, rcx ;rax = (num/x1) + x1

        div rbx ; rax = ((num/x1) + x1)/2
        mov [x2], rax

        cmp rsi, 1
        jge .while

    printres [x2]
%endmacro

section .text
global main

extern printf

main:
    sqrt

    mov       rax, 60
    xor       rdi, rdi
    syscall

section .data
    number dq 49
    format db "Square of your number is %d", 0xA

section .bss
    x1 resq 1
    x2 resq 1