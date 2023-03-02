from libqtile import widget
from libqtile.lazy import lazy
import subprocess

qtile_icon = "~/.config/qtile/logo-grey.png"
scripts_path = "/home/caleb/.config/qtile/"
script_get_volume = scripts_path + "get-volume.sh"
script_volume_down = scripts_path + "volume-down.sh"
script_volume_up = scripts_path + "volume-up.sh"
script_volume_mute = scripts_path + "volume-mute.sh"
script_brightness_up = scripts_path + "brightness-up.sh {}"
script_brightness_down = scripts_path + "brightness-down.sh {}"
volume_app = "pavucontrol"

_logo_static = None
_cpu_static = None
_volume_static = None
_clock_static = None
_quickexit_static = None
_memory_static = None
_checkupdates_static = None
_net_static = None
_systray_static = None


def logo():
    global _logo_static
    if _logo_static is None:
        _logo_static = widget.Image(filename=qtile_icon)
    return _logo_static


def cpu(fg, bg):
    global _cpu_static
    if _cpu_static is None:
        _cpu_static = widget.CPU(
            format="{load_percent:.0f}%",
            fmt="\uF85A  {}",
            font="UbuntuMono Nerd Font Bold",
            fontsize=16,
            padding=10,
            foreground=fg,
            background=bg,
            # width=72,
            mouse_callbacks={
                "Button1": lazy.spawn("alacritty -e htop --sort-key=PERCENT_CPU"),
                "Button3": lazy.spawn("killall htop"),
            }
        )
    return _cpu_static


def volume(fg, bg):
    global _volume_static
    if _volume_static is None:
        _volume_static = widget.Volume(
            fmt="\uFA7D  {}",
            font="UbuntuMono Nerd Font Bold",
            fontsize=16,
            padding=10,
            # width=72,
            foreground=fg,
            background=bg,

            update_interval=0.1,
            volume_app=volume_app,
            get_volume_command=script_get_volume,
            volume_up_command=script_volume_up,
            volume_down_command=script_volume_down,
            mute_command=script_volume_mute,
        )
    return _volume_static


def memory(fg, bg):
    global _memory_static
    if _memory_static is None:
        _memory_static = widget.Memory(
            format="{MemPercent:.0f}%",
            fmt="{}  \uFCBF",
            font="UbuntuMono Nerd Font Bold",
            foreground=fg,
            background=bg,
            fontsize=16,
            padding=10,
            # width=72,
            mouse_callbacks={
                "Button1": lazy.spawn("alacritty -e htop --sort-key=PERCENT_MEM"),
            }
        )
    return _memory_static


def clock(fg, bg):
    global _clock_static
    if _clock_static is None:
        _clock_static = widget.Clock(
            format="%Y-%m-%d %a %I:%M %p",
            foreground=fg,
            background=bg,
            padding=10,
            font="UbuntuMono Nerd Font Bold",
            fontsize=16,
        )
    return _clock_static


def quickexit(fg, bg):
    global _quickexit_static
    if _quickexit_static is None:
        _quickexit_static = widget.QuickExit(
            countdown_format="{}",
            default_text="\u23FB ",
            foreground=fg,
            background=bg,
            padding=10,
            fontsize=18,
            font="UbuntuMono Nerd Font Bold",
        )
    return _quickexit_static


def checkupdates(fg, bg):
    global _checkupdates_static
    if _checkupdates_static is None:
        _checkupdates_static = widget.CheckUpdates(
            initial_text="Checking...",
            display_format="{updates} Updates",
            no_update_string="No Updates",
            padding=10,
            font="UbuntuMono Nerd Font Bold",
            fontsize=16,
            distro="Ubuntu",
            foreground=fg,
            background=bg,
            execute="alacritty -e bash -c 'apt list --upgradable; $SHELL'"
        )
    return _checkupdates_static


def net(fg, bg):
    global _net_static
    if _net_static is None:
        _net_static = widget.Net(
            foreground=fg,
            background=bg,
            font="UbuntuMono Nerd Font Bold",
            fontsize=16,
            padding=10,
            format="{down} ↓↑ {up}",
        )
    return _net_static


def systray(bg):
    global _systray_static
    if _systray_static is None:
        _systray_static = widget.Systray(
            background=bg,
        )
    return _systray_static


def brightness_up():
    @lazy.function
    def __inner(qtile):
        screen_index = qtile.current_screen.index
        brightness_string = subprocess.getoutput(
            script_brightness_up.format(screen_index))
        brightness_value = float(brightness_string)
        for widget in qtile.current_screen.top.widgets:
            if widget.name == "brightness":
                widget.update(
                    f"{widget.text[0:3]}{(brightness_value * 100):.0f}%")
                break

    return __inner


def brightness_down():
    @lazy.function
    def __inner(qtile):
        screen_index = qtile.current_screen.index
        brightness_string = subprocess.getoutput(
            script_brightness_down.format(screen_index))
        brightness_value = float(brightness_string)
        for widget in qtile.current_screen.top.widgets:
            if widget.name == "brightness":
                widget.update(
                    f"{widget.text[0:3]}{(brightness_value * 100):.0f}%")
                break

    return __inner


def windowname():
    return widget.WindowName(
        width=200,
        max_chars=27,
    )

# Separate widgets: initialized for each screen


def groupbox():
    return widget.GroupBox(
        highlight_method="line",
        font="Font Awesome 6 Free Solid",
    )


def tasklist():
    return widget.TaskList(
        parse_text=lambda text: "",
        margin=0,
        padding=0,
        icon_size=20,
        fontsize=23,
        highlight_method='block',
        border="ffffff",
        borderwidth=4,
        txt_minimized="",
        txt_maximized="",
        txt_floating="",
    )


def separator(fg, bg):
    return widget.TextBox(
        text="\ue0c7",
        font="UbuntuMono Nerd Font Bold",
        fontsize=31,
        padding=0,
        foreground=fg,
        background=bg,
    )


def brightness(fg, bg):
    return widget.TextBox(
        name="brightness",
        text="\uFAA7  100%",
        font="UbuntuMono Nerd Font Bold",
        fontsize=16,
        padding=10,
        # width=72,
        foreground=fg,
        background=bg,
        mouse_callbacks={
            "Button4": brightness_up(),
            "Button5": brightness_down(),
        },
    )
