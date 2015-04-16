__author__ = 'yairgrosu'

INLINE_DELIM = '-'
PH_CONST = '${ENV}'


def inline_item(item, env, delimiter=INLINE_DELIM, place_holder=PH_CONST):
    inl_item = item
    if item and place_holder in item:
        # this inserts  the env without the prefix/suffix delimiter at the edges
        steps = item.split(place_holder)
        inl_item = ("%s%s%s" % (delimiter, env, delimiter)).join(steps)
        if env is None:
            # print "inlined: (%s) with env: (%s) to => (%s)" % (item, env, "".join(steps))
            return "".join(steps)
        if steps[-1] == '': inl_item = inl_item[:-1 * len(delimiter)]
        if steps[0] == '': inl_item = inl_item[len(delimiter):]
        print "inlined: (%s) with env: (%s) to => (%s)" % (item, env, inl_item)

    return inl_item
