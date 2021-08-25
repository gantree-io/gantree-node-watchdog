"""Collection of various messages to be printed."""

# import colorama  # TEMP: DISABLE COLOR

# colorama.init()  # TEMP: DISABLE COLOR


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
        # + colorama.Fore.LIGHTYELLOW_EX  # TEMP: DISABLE COLOR
        + config.client_id
        # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
        + f"\nproject id: "
        # + colorama.Fore.LIGHTYELLOW_EX  # TEMP: DISABLE COLOR
        + config.project_id
        # + colorama.Style.RESET_ALL  # TEMP: DISABLE COLOR
        + "\n"
    )
