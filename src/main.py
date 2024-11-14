import setup_path
import asyncio
from src.handlers.input_handler import parse_args, format_date, validate_paths
from src.render.renderer import show_program_info
from src.reporter.report_generator import generate_reports


async def main():
    args = parse_args()

    if args.i:
        show_program_info()
        return

    log_source = args.path
    from_date = format_date(args.from_date)
    to_date = format_date(args.to_date)
    agent = args.agent
    general = args.general
    report_extension = args.format
    status_code = int(args.status_code) if args.status_code else None
    request_method = args.request_method
    if not validate_paths(log_source):
        return

    await generate_reports(log_source, report_extension, from_date, to_date,
                           agent, general, status_code, request_method)


if __name__ == '__main__':
    asyncio.run(main())
