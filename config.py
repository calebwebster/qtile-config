from libqtile import bar, layout, widget
from libqtile import extension
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
import widgets
import os
import subprocess

scripts_path = "/home/caleb/.config/qtile/"

script_autostart = scripts_path + "autostart.sh"
script_next_audio_device = scripts_path + "next-audio-device.sh"
script_prev_audio_device = scripts_path + "prev-audio-device.sh"
script_volume_down = scripts_path + "volume-down.sh"
script_volume_up = scripts_path + "volume-up.sh"
script_volume_mute = scripts_path + "volume-mute.sh"
script_screenshot_screen = scripts_path + "screenshot-screen.sh"
script_screenshot_window = scripts_path + "screenshot-window.sh"
script_screenshot_area = scripts_path + "screenshot-area.sh"


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([script_autostart])


mod = "mod4"
terminal = "alacritty"
browser = "google-chrome-stable"
dmenu_extension = extension.DmenuRun(
    dmenu_prompt="> ",
    dmenu_font="UbuntuMono Nerd Font",
)
fontawesome_icons = {
    "globe": "\uf0ac",
    "code": "\uf121",
    "terminal": "\uf120",
    "volume-high": "\uf028",
    "volume-low": "\uf027",
    "volume-off": "\uf026",
    "volume-xmark": "\uf6a9",
}


def window_to_next_screen():
    @lazy.function
    def __inner(qtile):
        if qtile.current_window is None:
            return
        screenIndex = qtile.current_screen.index
        nextScreenIndex = (screenIndex + 1) % len(qtile.screens)
        qtile.current_window.togroup(qtile.screens[nextScreenIndex].group.name)
        qtile.focus_screen(nextScreenIndex)

    return __inner


def window_to_prev_screen():
    @lazy.function
    def __inner(qtile):
        if qtile.current_window is None:
            return
        screenIndex = qtile.current_screen.index
        nextScreenIndex = (screenIndex - 1) % len(qtile.screens)
        qtile.current_window.togroup(qtile.screens[nextScreenIndex].group.name)
        qtile.focus_screen(nextScreenIndex)

    return __inner


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.next_screen(),
        desc="Focus previous screen"),
    Key([mod], "l", lazy.prev_screen(),
        desc="Focus next screen"),
    Key([mod], "j", lazy.layout.down(),
        desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(),
        desc="Move focus up"),
    Key([mod, "shift"], "h", window_to_next_screen(),
        desc="Focus previous screen"),
    Key([mod, "shift"], "l", window_to_prev_screen(),
        desc="Focus next screen"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(),
        desc="Move window up"),
    Key([mod], "i", lazy.layout.grow(),
        desc="Grow window"),
    Key([mod], "m", lazy.layout.shrink(),
        desc="Shrink window"),
    Key([mod], "o", lazy.layout.flip(),
        desc="Flip layout"),
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(),
        desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(),
        desc="Reset all window sizes"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal),
        desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(),
        desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(),
        desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(),
        desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(),
        desc="Shutdown Qtile"),
    Key([mod], "r", lazy.run_extension(dmenu_extension),
        desc="Open Dmenu prompt"),
    # Multimedia
    Key([], "XF86AudioRaiseVolume", lazy.spawn(script_volume_up),
        desc="Increase volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn(script_volume_down),
        desc="Decrease volume"),
    Key([], "XF86AudioMute", lazy.spawn(script_volume_mute),
        desc="Increase volume"),
    Key(["control"], "XF86AudioNext", lazy.spawn(script_next_audio_device),
        desc="Next Audio Device"),
    Key(["control"], "XF86AudioPrev", lazy.spawn(script_prev_audio_device),
        desc="Previous Audio Device"),
    # Applications
    KeyChord([], "print", [
        Key([], "s", lazy.spawn(script_screenshot_screen)),
        Key([], "w", lazy.spawn(script_screenshot_window)),
        Key([], "a", lazy.spawn(script_screenshot_area)),
    ]),
    Key([mod, "mod1"], "b", lazy.spawn(browser),
        desc="Open browser"),
    Key([mod, "mod1"], "c", lazy.spawn("code"),
        desc="Open VSCode"),
]

group_configs = [
    ("1", {"layout": "monadtall", "label": fontawesome_icons["code"]}),
    ("2", {"layout": "max", "label": fontawesome_icons["globe"]}),
    ("3", {"layout": "max", "label": fontawesome_icons["terminal"]}),
]

groups = [Group(name, **kwargs) for name, kwargs in group_configs]

for group in groups:
    keys.extend(
        [
            Key([mod], group.name, lazy.group[group.name].toscreen(),
                desc=f"Switch to group {group.name}"),
            Key([mod, "shift"], group.name, lazy.window.togroup(group.name),
                desc=f"Move focused window to group {group.name}"),
        ]
    )

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(
        border_width=5,
        border_normal="#222222",
        border_focus="#307AB0",
        margin=15,
    ),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

screens = [
    Screen(
        top=bar.Bar(
            [
                widgets.logo(),
                widgets.groupbox(),
                widgets.windowname(),
                widgets.tasklist(),

                widgets.separator("003049", "272727"),
                widgets.checkupdates("ffffff", "003049"),
                widgets.separator("fcbf49", "003049"),
                widgets.net("ffffff", "fcbf49"),
                widgets.separator("003049", "fcbf49"),
                widgets.brightness("ffffff", "003049"),
                widgets.separator("fcbf49", "003049"),
                widgets.memory("ffffff", "fcbf49"),
                widgets.separator("003049", "fcbf49"),
                widgets.cpu("ffffff", "003049"),
                widgets.separator("fcbf49", "003049"),
                widgets.volume("ffffff", "fcbf49"),
                widgets.separator("003049", "fcbf49"),
                widgets.clock("ffffff", "003049"),
                widgets.separator("fcbf49", "003049"),
                widgets.systray("fcbf49"),
                widgets.separator("003049", "fcbf49"),
                widgets.quickexit("ffffff", "003049"),
            ],
            30,
            # border_width=[2, 0, 2, 0],  # top, bottom, left, right
            # border_color=["#2B2B2B", "#000000", "#2B2B2B", "#000000"],
            background="#272727"
        ),
    )
    for _ in range(3)
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button1", lazy.window.bring_to_front()),
    Click([mod], "Button2", lazy.window.toggle_floating()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
