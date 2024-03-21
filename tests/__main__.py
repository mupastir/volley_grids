if __name__ == '__main__':
    from os import path as os_path
    from sys import path

    from pytest import main

    tests_dir = os_path.dirname(__file__)

    path.insert(0, tests_dir)
    path.insert(0, os_path.join(tests_dir, '..', 'volley_grids'))

    exit(main())
