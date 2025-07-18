#include <stdio.h>
#include "../mult.h"

int main() {
    int num = mult(10, 2);
    if (num != 20) { 
        printf("Not Ok - num should be 20, but got %d\n", num);
        return 0;
    }
    printf("Num Ok - %d\n", num);
    return 1;
}