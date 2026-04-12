#pragma once

#include "../core/app_state.hpp"
#include "../core/events.hpp"

namespace m5dial {

/** Pure logic: maps input events → AppState (no LVGL). */
class ScreenManager {
public:
    void handle_event(const AppEvent& e, AppState& state);
};

} // namespace m5dial
