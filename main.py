import app

if __name__ == "__main__":
    my_app = app.App(
        title="Simple music app",
        geometry="400x250"
    )

    #tworzenie obiektu klasy functions
    app_func = app.Functions()

    #tworzenie przycisków
    button_names = {
        "Select files": app_func.open_files,
        "Combine": app_func.combine_files,
        "Select track": app_func.open_file,
        "Play": app_func.play_track,
        "Stop": app_func.stop,
    }
    for k, v in button_names.items():
        my_app.add_button(k, v)

    my_app.mainloop()
