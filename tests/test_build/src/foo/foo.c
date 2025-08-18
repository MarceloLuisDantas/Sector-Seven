#include <stdlib.h>

typedef struct Dot {
    int x;
    int y;
} Dot;

Dot *new_dot(int x, int y) {
    Dot *dot = malloc(sizeof(Dot));
    dot->x = x;
    dot->y = y;
    return dot;
}