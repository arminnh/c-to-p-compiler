ldc i 0
ldc i 0
ldc i 0
ssp 17
lda 0 5
ldc c 'h'
sto c
lda 0 6
ldc c 'e'
sto c
lda 0 7
ldc c 'l'
sto c
lda 0 8
ldc c 'l'
sto c
lda 0 9
ldc c 'o'
sto c
lda 0 10
ldc c 27
sto c
lda 0 11
ldc c 'w'
sto c
lda 0 12
ldc c 'o'
sto c
lda 0 13
ldc c 'r'
sto c
lda 0 14
ldc c 'l'
sto c
lda 0 15
ldc c 'd'
sto c
lda 0 16
ldc c 27
sto c
mst 0
cup 0 function_main
hlt

function_main:
ssp 21
lda 0 5
ldc c 'h'
sto c
lda 0 6
ldc c 'e'
sto c
lda 0 7
ldc c 'l'
sto c
lda 0 8
ldc c 'l'
sto c
lda 0 9
ldc c 'o'
sto c
lda 0 10
ldc c 27
sto c
lda 1 5
str a 0 11
lda 0 12
ldc c 'h'
sto c
lda 0 13
ldc c 'e'
sto c
lda 0 14
ldc c 'l'
sto c
lda 0 15
ldc c 'l'
sto c
lda 0 16
ldc c 'o'
sto c
lda 0 17
ldc c 27
sto c
lda 1 5
lda 1 11
str a 0 18
ldc c hello
str c 0 19
ldc c world
str c 0 20
retf