from pathlib import Path

p = Path("src/main.rs")
s = p.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, found {count}")
    s = s.replace(old, new, 1)
    print(f"patched: {label}")


def replace_function(name: str, replacement: str) -> None:
    global s
    needle = f"fn {name}("
    start = s.find(needle)
    if start < 0:
        raise SystemExit(f"{name}: function not found")
    brace = s.find("{", start)
    if brace < 0:
        raise SystemExit(f"{name}: opening brace not found")
    depth = 0
    i = brace
    in_string = False
    escaped = False
    while i < len(s):
        ch = s[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    s = s[:start] + replacement + s[end:]
                    print(f"patched function: {name}")
                    return
        i += 1
    raise SystemExit(f"{name}: unterminated function")


# Once a key has been accepted and cached on this PC, startup is completely local.
# The online licensing endpoint is only used for a key that has never been accepted here.
replace_function(
    "license_monitor",
    "fn license_monitor(runtime: Arc<LicenseRuntime>) { unsafe { SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_BELOW_NORMAL); } while !runtime.stop.load(Ordering::Acquire) { thread::sleep(Duration::from_secs(2)); } }",
)

# Existing saved left/right mouse mappings are deliberately rejected on load.
replace_once(
    "if (1..=5).contains(&n) { return Some(KeyBinding::mouse(n)); }",
    "if (3..=5).contains(&n) { return Some(KeyBinding::mouse(n)); }",
    "reject saved mouse buttons 1 and 2",
)

# Left/right mouse can never be captured as a spam/macro/UI hotkey.
replace_once(
    "unsafe fn accept_capture(binding: KeyBinding) { if binding.kind == BindKind::None { return; }",
    "unsafe fn accept_capture(binding: KeyBinding) { if binding.kind == BindKind::None { return; } if binding.kind == BindKind::Mouse && (binding.mouse_button == 1 || binding.mouse_button == 2) { UI.get().unwrap().lock().unwrap().capture = CaptureTarget::None; InvalidateRect(HWND_MAIN, null(), 0); return; }",
    "block left/right mouse capture",
)

# Do not even translate left/right mouse clicks into Hika binding events.
for old, label in [
    ("WM_LBUTTONDOWN => (1u8,true,false), ", "ignore left mouse down"),
    ("WM_LBUTTONUP => (1u8,false,true), ", "ignore left mouse up"),
    ("WM_RBUTTONDOWN => (2u8,true,false), ", "ignore right mouse down"),
    ("WM_RBUTTONUP => (2u8,false,true), ", "ignore right mouse up"),
]:
    replace_once(old, "", label)

# Cached login never hits the licensing server again. It is accepted locally and the
# existing key->main GUI transition is reused, preserving the current UI/animation.
old_cached = 'if let Some(key) = cached_key { if !HWND_KEY_EDIT.is_null() { SetWindowTextW(HWND_KEY_EDIT, wide(key.trim()).as_ptr()); SendMessageW(HWND_KEY_EDIT, EM_SETSEL_LOCAL, 0, -1); } PostMessageW(hwnd, WM_AUTO_LICENSE, 0, 0); }'
new_cached = 'if let Some(key) = cached_key { let local_reply = LicenseApiReply { valid: true, reason: String::new(), remaining_seconds: u64::MAX }; begin_key_acceptance(hwnd, &key, &local_reply); }'
replace_once(old_cached, new_cached, "trust cached login locally")

p.write_text(s, encoding="utf-8")
print("main source patch completed")
