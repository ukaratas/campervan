"""Inject SDL2 cflags/libs via pkg-config (Homebrew on Apple Silicon: /opt/homebrew)."""
Import("env")
import os
import subprocess
import shutil

def try_pkg_config():
    if not shutil.which("pkg-config"):
        return None, None
    try:
        c = subprocess.check_output(["pkg-config", "--cflags", "sdl2"], text=True).split()
        l = subprocess.check_output(["pkg-config", "--libs", "sdl2"], text=True).split()
        return c, l
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, None

cflags, libs = try_pkg_config()
if cflags is None:
    # Apple Silicon Homebrew
    cflags = ["-I/opt/homebrew/include/SDL2", "-D_THREAD_SAFE"]
    libs = ["-L/opt/homebrew/lib", "-lSDL2"]
    # Intel Mac Homebrew fallback
    if not os.path.isdir("/opt/homebrew/include/SDL2") and os.path.isdir("/usr/local/include/SDL2"):
        cflags = ["-I/usr/local/include/SDL2", "-D_THREAD_SAFE"]
        libs = ["-L/usr/local/lib", "-lSDL2"]
    print("pio_sdl2_flags: using Homebrew default paths. Install: brew install sdl2")
else:
    print("pio_sdl2_flags: using pkg-config for SDL2")

env.Append(CCFLAGS=cflags)
env.Append(LINKFLAGS=libs)
