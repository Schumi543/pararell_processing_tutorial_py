import os

pid_list = []


def main():
    pid_list.append(os.getpid())
    child_pid = os.fork()

    if child_pid == 0:
        pid_list.append(os.getpid())
        print()
        print("child: Hello! I'm child process.")
        print(f"child: I know PID {pid_list}")
    else:
        pid_list.append(os.getpid())
        print()
        print("parent: Hello! I'm parent process")
        print(f"parent: My child PID is {child_pid}")
        print(f"parent: I know PID {pid_list}")


if __name__ == '__main__':
    main()
