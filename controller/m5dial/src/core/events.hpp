#pragma once

#include <cstdint>

namespace m5dial {

enum class AppEventType : uint8_t {
    EncoderLeft,
    EncoderRight,
    ButtonPress,
    LongPress,
    Touch,
    Tick,
};

struct AppEvent {
    AppEventType type;
    /** e.g. touch x/y or tick ms — optional */
    int32_t param0{0};
    int32_t param1{0};
};

} // namespace m5dial
