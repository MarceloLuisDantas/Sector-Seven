#include <raylib.h>

int main() {
    InitWindow(800, 450, "Raylib Test");
    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);
        DrawText("Hello, World!!", 335, 200, 20, BLACK);
        EndDrawing();
    }
    CloseWindow();
    return 0;
}
