#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


#define max_n 20
#define max_x 20
#define max_y 20

int memo[max_n][max_x][max_y];

bool isValidMove(int x, int y, int **path, int len) {
    for (int i = 0; i < len; i++) {
        if (path[i][0] == x && path[i][1] == y) {
            return false;
        }
    }
    return true;
}

void printWalk(int **path, int len) {
    for (int i = 0; i < len; i++) {
        printf("(%d, %d) ", path[i][0], path[i][1]);
    }
    printf("\n");
}

void generateWalks(int n, int x, int y, int **path, int *len) {
    if (n == 0) {
        // print or save the current walk
        printWalk(path, *len);
        return;
    }
    if(memo[n][x][y]!=-1){
        return memo[n][x][y];
    }
    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};
    for (int i = 0; i < 4; i++) {
        int newx = x + dx[i];
        int newy = y + dy[i];
        if (isValidMove(newx, newy, path, *len)) {
            path[*len][0] = newx;
            path[*len][1] = newy;
            (*len)++;
            generateWalks(n-1, newx, newy, path, len);
            (*len)--;
        }
    }
    
    memo[n][x][y]=result;
    return result;
}



int main() {
    int n = 10; // chain length
    int x = 0, y = 0; // starting position
    int len = 1;
    int **path;
    path = (int **)malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++) {
        path[i] = (int *)malloc(2 * sizeof(int));
    }
    path[0][0] = x;
    path[0][1] = y;
    memset(memo,-1,sizeof(memo));
    generateWalks(n, x, y, path, &len);
    for (int i = 0; i < n; i++) {
        free(path[i]);
    }
    free(path);
    return 0;
}