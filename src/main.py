from argparse import ArgumentParser, Namespace
from startup import Startup, StartupLoggerConfig


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', default="config.yaml")
    parser.add_argument('--disable-startup-logs', action='store_true', default=False)
    parser.add_argument('--disable-startup-file-logs', action='store_true', default=False)
    return parser.parse_args()

def main():
    args = parse_args()
    Startup()                                                   \
        .with_config(args.config)                               \
        .with_startup_logger(
            StartupLoggerConfig(
                args.disable_startup_logs,
                args.disable_startup_file_logs
            )
        )                                                       \
        .run()


if __name__ == "__main__":
    main()