while True:
    keys = kb.get_new_keys()
    kb.ext_dir_keys(keys)

    if keys:
        # Roku key mappings
        if "UP" in keys:
            create_keypress("Up")
        elif "DOWN" in keys:
            create_keypress("Down")
        elif "LEFT" in keys:
            create_keypress("Left")
        elif "RIGHT" in keys:
            create_keypress("Right")
        elif "ESC" in keys:
            create_keypress("Home")
        elif "BSPC" in keys:
            create_keypress("Back")
        elif "ENT" in keys:
            create_keypress("Select")
        elif "SPC" in keys:
            create_keypress("Play")
        else:
            for key in keys:
                create_keypress(f"Lit_{key}")

    time.sleep_ms(10)
