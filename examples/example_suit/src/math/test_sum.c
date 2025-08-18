#include <stdio.h>
#include "sum.h"

int main() {
    int x = sum(10, 20);
    if (x != 30) {
        printf("Error: x should be 30, but is %d.\n", x);
        return 0;
    }

    printf("X is 30.\n");
    return 1;
}