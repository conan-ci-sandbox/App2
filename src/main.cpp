
#include <iostream>

#include "libC/libC.h"

int main() {
    std::cout << "App2: v1.0" << std::endl;
    hello_libC(1, "called from App2");    
    return 0;
}