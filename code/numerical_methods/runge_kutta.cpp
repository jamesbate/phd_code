#include <iostream>
#include <cmath>//pow

float func2int(int x);



int main(){
    std::cout << func2int(2);
    return 0;
}

float func2int(int x){
    return pow(x, 2);
}