"""Run the one-room looper and print the receipts."""

from .loop import Looper


def main():
    loop = Looper()
    packets = loop.run_until_done()
    for packet in packets:
        state = packet["new_state_after_action"]
        print(
            "%s  %s  -> %s  (%s)"
            % (
                packet["step_index"],
                packet["what_is_happening_now"],
                packet["chosen_next_action"],
                state["result"],
            )
        )
        print("  why: %s" % packet["why_this_action"])
    print("done" if loop.body.done else "stopped before the mark")
    return 0 if loop.body.done else 1


if __name__ == "__main__":
    raise SystemExit(main())
