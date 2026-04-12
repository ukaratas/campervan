#include "sdl_display.hpp"
#include "../../hardware/sim_adapter.hpp"
#include "../../ui/renderer.hpp"
#include "../../ui/screen_manager.hpp"
#include "../../core/app_state.hpp"
#include "../../core/event_queue.hpp"
#include "../../mqtt/mqtt_client_mock.hpp"
#include <SDL.h>

namespace m5dial {

int run_native_app() {
    if (!platform::sdl_display_init()) {
        return 1;
    }

    MqttClientMock mqtt; // reserved for later wiring
    (void)mqtt;

    Renderer renderer;
    renderer.init();

    AppState state;
    ScreenManager screens;
    SimAdapter adapter;
    EventQueue queue;

    renderer.sync(state);

    bool running = true;
    uint32_t last_tick = SDL_GetTicks();

    while (running) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT) {
                running = false;
            }
        }

        const uint32_t now = SDL_GetTicks();
        lv_tick_inc(now - last_tick);
        last_tick = now;

        adapter.poll(queue);

        AppEvent ev;
        while (queue.pop(ev)) {
            screens.handle_event(ev, state);
        }

        renderer.sync(state);
        lv_timer_handler();

        SDL_Delay(5);
    }

    platform::sdl_display_deinit();
    return 0;
}

} // namespace m5dial
