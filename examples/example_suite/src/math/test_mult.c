#include <stdio.h>
#include "mult.h"

int main() {
    int x = mult(10, 20);
    if (x != 200) {
        printf("Error: x should be 200, but is %d.\n", x);
        return 0;
    }

    printf("X is 200.\n");
    return 1;
}