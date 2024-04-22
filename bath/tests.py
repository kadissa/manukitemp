def decor(func):
    def wrapper(*args):
        print(func(*args)[0])
        return {func(*args)[0][_]: func(*args)[1][_] for _ in range(len(
            func(*args)[0]))}

    return wrapper


@decor
def get_split(s_1, s_2):
    return s_1.split(), s_2.split()


print(get_split('moscow berlin', 'москва берлин'))
