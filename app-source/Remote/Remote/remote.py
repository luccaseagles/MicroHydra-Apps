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
        # ~~~~ MINIMAL ADDITION: handle single character keys ~~~~~~
        else:
            # If keys contains a single printable character (letter/number)
            # Modify as needed to support your kb.get_new_keys() format
            for key in keys:
                if len(key) == 1 and key.isprintable():
                    # Use Roku's /keypress/Lit_<char> endpoint
                    create_keypress(f"Lit_{key}")

    time.sleep_ms(10)
