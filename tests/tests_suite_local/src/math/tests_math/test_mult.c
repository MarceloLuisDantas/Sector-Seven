#include <stdio.h>
#include "../math.h"

int main() {
    int x = mult(10, 20);
    if (x != 200) {
        printf("X should be 200\n");
        return 0;
    }

    printf("X is 200\n");
    return 1;
}