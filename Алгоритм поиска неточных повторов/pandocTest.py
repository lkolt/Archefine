from pandocfilters import stringify, Str, applyJSONFilters, walk, toJSONFilter, Para, Header, Space, toJSONFilters, \
    BulletList, Strong


divider = "A%@%@%@%@@@@%@"


def add_marks_to_header(key, val, fmt, meta):
    if key == 'Header':
        # res = []
        [c, lol, d] = val
        d.append(Str("%$#@!"))
        # for v in d:
        #     k = v['t']
        #     if k == 'Str':
        #         value = v['c']
        #         res.append(Str(value))
        #     else:
        #         res.append(v)
        # return Header(4, lol, d)
        return Para([Str(divider)])                   # TODO: divider


def remove_code(key, val, fmt, meta):
    if key == 'CodeBlock':
        return Para([])
    if key == 'Code':
        return Str("")


def remove_links(key, val, fmt, meta):
    if key == 'Link':
        return Str("")


def bullet_list_to_para(key, val, fmt, meta):
    if key == 'BulletList':

        # with open("kekresult.txt", "a") as file:
        #     file.write(str(val))
        res = []
        for lst in val:
            for snd in lst:
                keys = snd['t']
                if keys == 'Para':
                    value = snd['c']
                    res.append(Para(value))
                    # lst = []
                    # for st in value:
                    #     p = st['t']
                    #     if p == 'Str':
                    #         vp = st['c']
                    #         lst.append(vp)
                            # with open("kekresult.txt", "a") as file:
                            #     file.write(vp + '\n')
                    # res.append(lst)
        # BulletList(val)
        return res


def ordered_list_to_para(key, val, fmt, meta):
    if key == 'OrderedList':

        [attr, v] = val
        res = []
        for lst in v:
            for snd in lst:
                keys = snd['t']
                if keys == 'Para':
                    value = snd['c']
                    res.append(Para(value))

        return res


def deflists(key, value, format, meta):
    if key == 'DefinitionList':
        return BulletList([tobullet(t, d) for [t, d] in value])


def tobullet(term, defs):
    # return [Para(term)] + [b for d in defs for b in d]
    return [Para([Str(divider)])] + [b for d in defs for b in d]


def deemph(key, val, fmt, meta):
    if key == 'Emph' or key == 'Strong':
        res = []
        for d in val:
            res.append(d)
        return res


def dediv(key, val, fmt, meta):
    if key == 'Div':
        res = []
        [_, d] = val
        for v in d:
            res.append(v)
        return res


def deblockquoted(key, val, fmt, meta):
    if key == 'BlockQuote':
        res = []
        for d in val:
            res.append(d)
        return res


if __name__ == "__main__":
    toJSONFilters([remove_code, add_marks_to_header, remove_links, deflists, bullet_list_to_para, ordered_list_to_para,
                   deemph, dediv, deblockquoted])
