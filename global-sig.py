import argparse
import config
import time
from pwiki.waction import WAction
from pwiki.wiki import Wiki

SW_VERSION = "0.0.1"
DRY = False
VERBOSE = False
HEADERS = {"User-Agent": f"global-sig_v{SW_VERSION}(https://w.wiki/69K7)"}


def get_attached_wikis(wiki: Wiki):
    if VERBOSE:
        print("Getting attached accounts")
    params = {
        "meta": "globaluserinfo",
        "guiprop": "merged",
    }
    return WAction._post_action(
        wiki, "query", params, timeout=10, extra_args={"headers": HEADERS}
    )


def set_signature(wiki: Wiki):
    if DRY:
        print(
            f"[DRY] Would have set signature on {wiki.domain} to `{config.USER_SIGNATURE}`"
        )
        return False
    params = {
        "change": "fancysig=1",
        "optionname": "nickname",
        "optionvalue": config.USER_SIGNATURE,
    }
    if VERBOSE:
        print(f"Setting signature on {wiki.domain} to {config.USER_SIGNATURE}")
    out = WAction._post_action(
        wiki, "options", params, timeout=10, extra_args={"headers": HEADERS}
    )
    print(out)


if __name__ == "__main__":
    print(f"global-sig v{SW_VERSION}")
    parser = argparse.ArgumentParser(
        prog="global-sig.py",
        description="global-sig, v" + SW_VERSION,
    )
    parser.add_argument("--all", help="Run on all attached wikis", action="store_true")
    parser.add_argument(
        "-w",
        "--wiki",
        help="The wiki domain to run on",
        default="meta.wikimedia.org",
    )
    parser.add_argument(
        "-d", "--dry", help="Don't make any changes", action="store_true"
    )
    parser.add_argument("-v", "--verbose", help="Be verbose", action="store_true")
    args = parser.parse_args()

    DRY = args.dry
    VERBOSE = args.verbose

    if DRY:
        print("Dry run, no changes will be made")

    if args.all:
        all_wikis = get_attached_wikis(
            Wiki(args.wiki, config.BOT_USER, config.BOT_PASS)
        )
        print(f"Running on {len(all_wikis['query']['globaluserinfo']['merged'])} wikis")
        for wiki in all_wikis["query"]["globaluserinfo"]["merged"]:
            wiki_domain = wiki["url"].replace("https://", "")
            print(f"Setting signature on {wiki_domain}...")
            try:
                set_signature(Wiki(wiki_domain, config.BOT_USER, config.BOT_PASS))
            except Exception as e:
                print(f"Error on {wiki_domain}: {e}")
            time.sleep(1)
    else:
        print(f"Setting signature on {args.wiki}...")
        set_signature(Wiki(args.wiki, config.BOT_USER, config.BOT_PASS))
