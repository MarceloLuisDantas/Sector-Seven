#include <stdio.h>
#include "math.h"
#include "foo/foo.h"

int main() {
    Dot *dot1 = new_dot(10, 20);
    Dot *dot2 = new_dot(20, 30);
    Dot *dot3 = new_dot(sum(dot1->x, dot2->x), sum(dot1->y, dot2->y));
    printf("Dot 1 is at x=%d, y=%d\n", dot1->x, dot1->y);
    printf("Dot 2 is at x=%d, y=%d\n", dot2->x, dot2->y);
    printf("Dot 3 is at x=%d, y=%d\n", dot3->x, dot3->y);
    return 0;
}