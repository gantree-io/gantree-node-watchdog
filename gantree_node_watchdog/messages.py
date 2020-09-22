"""Collection of various messages to be printed."""

import colorama

colorama.init()


def node_secret_rejected(config):
    """Message to be printed when Gantree rejects the node secret."""
    return (
        "\n"
        + "⮞ Your node secret was rejected by the server."
        + "\n⮞ Most likely this node has recently been deregistered."
        + "\n"
        + "\n⮞ If this is unexpected, please check the client id shown here"
        + "\nis still associated with the following network in the Gantree web app."
        + "\n"
        + "\nclient id: "
        + colorama.Fore.LIGHTYELLOW_EX
        + config.client_id
        + colorama.Style.RESET_ALL
        + f"\nproject id: "
        + colorama.Fore.LIGHTYELLOW_EX
        + config.project_id
        + colorama.Style.RESET_ALL
        + "\n"
    )
