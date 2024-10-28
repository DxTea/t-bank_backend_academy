from src.handlers.menu_handler import Menu


def main() -> None:
    menu = Menu()
    menu.display_welcome_screen()
    while True:
        choice = menu.display_menu()
        menu.handle_choice(choice)


if __name__ == "__main__":
    main()
