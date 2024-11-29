def reload_process(executable, new_program, file_path):
    # executable: sys.executable
    # new_program: 'python'
    # file_path: __file__
    import os
    import sys
    from .log_re import log

    log(f"Reloading process with {executable} {new_program} {file_path} {sys.argv[1:]}")
    os.execl(executable, new_program, file_path, *sys.argv[1:])
