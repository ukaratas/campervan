#if defined(PLATFORM_NATIVE)

namespace m5dial {
int run_native_app();
}

int main() {
    return m5dial::run_native_app();
}

#else

#include <Arduino.h>

void setup() {
    // TODO: M5Unified + LVGL init + M5DialAdapter
}

void loop() {
    // TODO
}

#endif
