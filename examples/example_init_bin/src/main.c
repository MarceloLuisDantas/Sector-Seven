#include <stdio.h>
#include "./funcs/mult.h"
#include "./funcs/sum.h"

int main() { 
    int num1 = sum(10, 20);
    int num2 = mult(num1, 2);
    printf("(10 + 20) * 2 = %d\n", num2);
    return 0;
}            
