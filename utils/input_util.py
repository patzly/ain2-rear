from utils import print_util as cprint


def invalid():
    print(cprint.red("Ungültige Eingabe. Erneut versuchen:"))


def string():
    # Prevent KeyboardInterrupt from being thrown when program is stopped
    try:
        return input().strip()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit(0)


def integer(mini=None, maxi=None):
    # Prevent ValueError from being thrown when input is not a number or not in min max bounds
    try:
        user = int(string())
    except ValueError:
        invalid()
        return integer(mini, maxi)

    if mini is not None and maxi is not None:
        if mini <= user <= maxi:
            return user
        else:
            invalid()
            return integer(mini, maxi)
    elif mini is not None and maxi is None:
        if user >= mini:
            return user
        else:
            invalid()
            return integer(mini, maxi)
    elif mini is None and maxi is not None:
        if user <= maxi:
            return user
        else:
            invalid()
            return integer(mini, maxi)
    else:
        return user
