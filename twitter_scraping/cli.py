import argparse
from . import scraper
def twitter_scraping():
    parser = argparse.ArgumentParser(description="Run a twitter scraper")
    parser.add_argument("--follow", action='append', help="User to track (overwrites config)")
    parser.add_argument("--track", action='append', help="Query to track (overwrites config)")
    parser.add_argument("--language", action='append', help="Language to track (overwrites config)")
    parser.add_argument("-c", "--config", type=str, help="JSON configuration")
    parser.add_argument("-o", "--output-file", type=str, required=True, help="Output file", dest='output_file')
    parser.add_argument('-s', '--seconds', type=int, help="Notification frequency (in seconds)")
    parser.add_argument('-m', '--minutes', type=int, help="Notification frequency (in minutes)")
    parser.add_argument('--hours', type=int, help="Notification frequency (in hours)")
    parser.add_argument('-n', '--notify-every', type=int, help="Notification frequency (in tweets)", dest='notify_count')

    args = parser.parse_args()

    if len([x for x in [args.seconds, args.minutes, args.hours] if x is not None]) > 1:
        print("Options are mutually exclusive: --seconds, --minutes, and --hours.")
        return 1
    
    if args.config is None:
        builder = scraper.ScraperBuilder()
    else:
        builder = scraper.ScraperBuilder.load_config(args.config)
    builder = builder.output_file(args.output_file).notify_count(args.notify_count)
    if args.seconds is not None:
        builder = builder.notify_seconds(args.seconds)
    if args.minutes is not None:
        builder = builder.notify_seconds(args.minutes * 60)
    if args.hours is not None:
        builder = builder.notify_seconds(args.hours * 60 * 60)
    if args.follow is not None:
        builder = builder.follow(args.follow)
    if args.track is not None:
        builder = builder.track(args.track)
    if args.language is not None:
        builder = builder.languages(args.language)
    with builder.build() as s:
        # Context manages things like files
        pass