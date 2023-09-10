.data

.code
ALIGN 16

;RCX, b in RDX, c in R8
; https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions?view=msvc-170#x64-register-usage
; https://syscall.sh/

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

l_read_int80h PROC
	sub		rsp, 28h		; shadow stack

	push	rbx

	mov		rax, 3
	mov		rbx, rcx
	mov		rcx, rdx
	mov		rdx, r8
	int		80h

	pop		rbx

	add		rsp, 28h		; restoring shadow stack
	ret
l_read_int80h ENDP

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

l_close_int80h PROC
	sub		rsp, 28h		; shadow stack

	push	rbx

	mov		rax, 6
	mov		rbx, rcx
	int		80h

	pop		rbx

	add		rsp, 28h		; restoring shadow stack
	ret
l_close_int80h ENDP

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

l_socket_int80h PROC
	sub		rsp, 28h		; shadow stack

	push	rbx

	mov		eax, 359
	mov		ebx, ecx
	mov		ecx, edx
	mov		edx, r8d
	int		80h

	pop		rbx

	add		rsp, 28h		; restoring shadow stack
	ret
l_socket_int80h ENDP

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

l_connect_int80h PROC
	sub		rsp, 28h		; shadow stack

	push	rbx

	mov		rax, 362
	mov		rbx, rcx
	mov		rcx, rdx
	mov		rdx, r8
	int		80h

	pop		rbx

	add		rsp, 28h		; restoring shadow stack
	ret
l_connect_int80h ENDP

END