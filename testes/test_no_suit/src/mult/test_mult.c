#include <stdio.h>
#include "mult.h"

int main() {
    int total = mult(10, 10);
    if (total != 100)
        return 0;
    return 1;
}