from math import hypot


def collision(x1, y1, x2, y2, dist=0):
    if hypot(x2 - x1, y2 - y1) <= dist:
        return True
    return False


def wraptxt(text, fontsize: int, width: int) -> list:
    texts = text.split()
    lines = []
    line = []
    line_width = 0
    for t in texts:
        if line_width + len(t) * fontsize <= width:
            line.append(t)
            line_width += len(t) * fontsize
        else:
            lines.append(' '.join(line))
            line = [t]
            line_width = 0
    else:
        lines.append(' '.join(line))
    return lines
