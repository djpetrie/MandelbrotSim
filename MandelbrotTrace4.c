#include <stdlib.h>
#include <math.h>
#include <stdbool.h> 

double xStart = 0.0;
double yStart = 0.0;
int pixels = 1000;
int *array;
double delta = 0.0;
int numIterations = 100;

void freeMem(int *ptr) {
    free(ptr);
}

// standard bailout algorithm modified to set array value
int esc(int xx, int yy) {
    double x0 = xStart + delta * (double) (xx);
    double y0 = yStart + delta * (double) (yy);
    double x = 0.0;
    double y = 0.0;
    double x2 = 0.0;
    double y2 = 0.0;
    int count = 0;
    while (x2 + y2 <= 4 && count < numIterations) {
        y = 2 * x * y + y0;
        x = x2 - y2 + x0;
        x2 = x * x;
        y2 = y * y;
        count = count + 1;
    }
    int rtn = count % numIterations;
    array[xx + yy * pixels] = rtn;
    return rtn;
}


// Function to fill a chunk
int fill(int xx, int yy, int number) {
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            array[(xx + j) + (yy + i) * pixels] = number;
        }
    }
    return number;
}


// Function to map x,y array cell onto 1d array position
int get(int xx, int yy) {
    return array[xx + yy * pixels];
}

void processChunk(int j10, int i10) {
    int value = array[j10 + i10 * pixels];
    bool doFill = true;
    for (int k = 2; k < 10; k = k + 2) {
        if (get(j10 + k, i10) != value ||           // check if border cells are homogeneous by sampling
            get(j10, i10 + k) != value ||
            get(j10 + k, i10 + 10) != value ||
            get(j10 + 10, i10 + k) != value) 
        {
            doFill = false;
            break;
        }
    }
    if (doFill) {
        fill(j10, i10, value);
    } else {
        for (int i = 1; i < 10; i = i + 2) {    // calculate odd numbered chunk border cells
            esc(j10 + i, i10);
            esc(j10, i10 + i);
            esc(j10 + 10, i10 + i);
            esc(j10 + i, i10 + 10);
        }
        for (int i = 1; i < 10; i++) {          // calculate chunk interior
            for (int j = 1; j < 10; j++) {
                esc(j10 + j, i10 + i);
            }
        }
    }
}


int *MandelbrotFunction(double xCenter, double yCenter, double size, int numPixels, int iterations)
{
    pixels = numPixels;
    delta = size / (double) pixels;
    array = (int*) calloc(pixels * pixels, sizeof(int));
    xStart = xCenter - size / 2.0;
    yStart = yCenter - size / 2.0;
    numIterations = iterations;
    int chunks = pixels / 10;
    int j10;
    int i10;
    
    
    //collect every other pixel along gridlines where pixelcount is a multiple of 10
    for (int i = 0; i < pixels; i = i + 10) {
        for (int j = 0; j < pixels; j = j + 2) {
            esc(i, j);                          // calculate vertical gridlines
            if (j % 10 != 0) {                  // skip intersections
                esc(j, i);                      // calculate horizontal gridlines
            }
            
        }
    }
    
    //process the chunks divided by the gridlines
    for (int i = 0; i < chunks - 1; i++) {
        for (int j = 0; j < chunks - 1; j++) {
            i10 = i * 10;
            j10 = j * 10;
            processChunk(j10, i10);             // j10, i10 are x, y coordinates respectively for the bottom left pixel of the chunk
        }
    }
    
    //calculating leftover pixels
    int border = pixels - 10;
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < pixels; j++) {
            esc(border + i, j);
            esc(j, border + i);
        }
    }
    
    
    return array;
}