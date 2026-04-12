#include "sim_adapter.hpp"
#include <SDL.h>

namespace m5dial {

void SimAdapter::poll(EventQueue& events) {
    const Uint8* keys = SDL_GetKeyboardState(nullptr);

    const bool left = keys[SDL_SCANCODE_LEFT] != 0;
    const bool right = keys[SDL_SCANCODE_RIGHT] != 0;
    const bool enter = keys[SDL_SCANCODE_RETURN] != 0 || keys[SDL_SCANCODE_KP_ENTER] != 0;
    const bool esc = keys[SDL_SCANCODE_ESCAPE] != 0;

    if (left && !prev_left_) {
        events.push(AppEvent{AppEventType::EncoderLeft});
    }
    if (right && !prev_right_) {
        events.push(AppEvent{AppEventType::EncoderRight});
    }

    if (esc && !prev_esc_) {
        events.push(AppEvent{AppEventType::LongPress});
    }

    if (enter && !prev_enter_) {
        enter_down_ms_ = SDL_GetTicks();
        enter_pending_ = true;
    }
    if (!enter && prev_enter_ && enter_pending_) {
        enter_pending_ = false;
        const uint32_t dur = SDL_GetTicks() - enter_down_ms_;
        if (dur >= kLongPressMs) {
            events.push(AppEvent{AppEventType::LongPress});
        } else if (dur >= kMinTapMs) {
            events.push(AppEvent{AppEventType::ButtonPress});
        }
    }

    prev_left_ = left;
    prev_right_ = right;
    prev_enter_ = enter;
    prev_esc_ = esc;
}

} // namespace m5dial
