#include <stdio.h>
#include "../math.h"

int main() {
    int x = sum(10, 20);
    if (x != 30) {
        printf("X should be 30\n");
        return 0;
    }

    printf("X is 30\n");
    return 1;
}