.data

.code
ALIGN 16

;RCX, b in RDX, c in R8

l_open PROC
	sub		rsp, 28h		; shadow stack

	push	rdi
	push	rsi

	mov		rax, 2

	mov		rdi, rcx
	mov		rsi, rdx
	mov		rdx, r8

	syscall

	pop		rsi
	pop		rdi

	add		rsp, 28h		; restoring shadow stack
	ret
l_open ENDP

l_read PROC
	sub		rsp, 28h		; shadow stack

	push	rdi
	push	rsi

	mov		rax, 0

	mov		rdi, rcx
	mov		rsi, rdx
	mov		rdx, r8

	syscall

	pop		rsi
	pop		rdi

	add		rsp, 28h		; restoring shadow stack
	ret
l_read ENDP

l_close PROC
	sub		rsp, 28h		; shadow stack

	push	rdi

	mov		rax, 3

	mov		rdi, rcx

	syscall

	pop		rdi

	add		rsp, 28h		; restoring shadow stack
	ret
l_close ENDP

l_socket PROC
	sub		rsp, 28h		; shadow stack

	push	rdi
	push	rsi

	mov		rax, 41

	mov		rdi, rcx
	mov		rsi, rdx
	mov		rdx, r8

	syscall

	pop		rsi
	pop		rdi

	add		rsp, 28h		; restoring shadow stack
	ret
l_socket ENDP

l_connect PROC
	sub		rsp, 28h		; shadow stack

	push	rdi
	push	rsi

	mov		rax, 42

	mov		rdi, rcx
	mov		rsi, rdx
	mov		rdx, r8

	syscall

	pop		rsi
	pop		rdi

	add		rsp, 28h		; restoring shadow stack
	ret
l_connect ENDP

END