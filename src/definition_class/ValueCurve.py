def defend_curve(defend):
    """
    防禦減傷曲線
    :param defend: 防禦力
    :return:
    """
    return round(defend ** (7 / 8), 0)
