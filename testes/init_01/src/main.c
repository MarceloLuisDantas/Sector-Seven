#include <stdio.h>
#include "bar.h"
#include "foo/foo.h"

int main() {
    int x = soma(10, 30);
    int y = mult(2, 10);
    printf("%d \n", x);
    printf("%d \n", y);
    return 0;
}