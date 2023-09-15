; command for start programm:
; nasm -felf64 Average.asm && gcc -no-pie -fno-pie Average.o && ./a.out
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

%macro print 2
    pushd
    mov rax, 1
    mov rdi, 1
    mov rdx, %1 ; len
    mov rsi, %2 ; message
    syscall
    popd
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

section .text
global main

extern printf

main:
    mov ecx, [count]
    xor edx, edx

Sum:
    mov eax, [x+ecx*4-4]
    mov ebx, [y+ecx*4-4]
    sub eax, ebx
    
    add edx, eax
    mov [result], edx

    dec ecx
    test ecx, ecx
    jnz Sum

Avg:
    xor rax, rax
    xor rcx, rcx

    mov eax, [result]
    mov ebx, [count]

    xor edx, edx
    cdq
    idiv ebx

    mov [result], eax
    printres [result]

    mov rax, 60
    xor rdi, rdi
    syscall


section .data
    x dd 5, 3, 2, 6, 1, 7, 4
    y dd 0, 10, 1, 9, 2, 8, 5
    count dd 7
    result dd 0

    format db "result: %d", 0xA

    message db 'Done', 0xA
    mlen equ $ - message