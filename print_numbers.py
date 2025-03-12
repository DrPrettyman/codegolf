from itertools import cycle

_UNITS={0:'zero',1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine'}
_UNITS2={1:'a', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine'}
_SEVENTHS={1:'142857',2:'285714',3:'428571',4:'571428',5:'714285',6:'857142'}
_TENS={1:'ten',2:'twenty',3:'thirty',4:'forty',5:'fifty',6:'sixty',7:'seventy',8:'eighty',9:'ninety'}
_TEENS={1:'eleven',2:'twelve',3:'thirteen',4:'fourteen',5:'fifteen',6:'sixteen',7:'seventeen',8:'eighteen',9:'nineteen'}
_POW = {3:'thousand',6:'million',9:'billion',12:'trillion',15:'quadrillion'}
_FRAC = {'1':'a tenth','5':'a half','25':'a quarter','75':'three quarters','2':'a fifth','3':'three tenths','4':'two fifths','6':'three fifths','7':'seven tenths','8':'four fifths','9':'nine tenths','125':'an eighth','375':'three eighths','625':'five eighths','875':'five eighths'}

def _int_split(n):
    s = str(n)
    s2 = ''
    for i, c in enumerate(s[-1::-1]):
        if i%3==0:
            c = c+','
        s2 = c+s2
    return [int(k) for k in s2.strip(',').split(',')]

def _int_split_dict(n):
    sp = _int_split(n)
    return {3*i: m for i, m in enumerate(sp[-1::-1])}

def _float_split_dict(x):
    s = str(x).split('.')
    d = _int_split_dict(int(s[0]))
    if len(s) == 1:
        return d
    elif int(s[1]) == 0:
        return d
    else:
        d[-1] = s[1]
        return d

def _get_tens(n):
    """n is in the range 0 to 99 inc."""
    t, u=n//10%10, n%10
    if t:
        if t==1 and u>0:
            s = _TEENS[u]
        elif u>0:
            s = _TENS[t] + '-' + _UNITS[u]
        else:
            s = _TENS[t]
    elif u>0:
        s = _UNITS[u]
    else:
        s = ''
    return s

def _get_group_of_three(n: int) -> str:
    """n is in the range 0 to 999 inc."""
    h = n//100
    s0 = ''
    if h:
        s0 = _UNITS[h] + ' hundred'
    s1 = _get_tens(n % 100)
    if s0 and s1:
        return s0 + ' and ' + s1
    else:
        return s0 + s1

def _identify_sevenths(s: str):
    k=0
    for i in range(1,7):
        c = cycle(_SEVENTHS.get(i))
        if all(_s==_r for _s, _r in zip(s[:-1], c)):
            k=i
            break
    if k:
        w = f'and {_UNITS2.get(k)} seventh'
        if k>1:
            w += 's'
        return w
    else:
        return None


def _identify_ninths(s: str):
    k=0
    for i in range(1,10):
        if all(_s==str(i) for _s in s[:-1]):
            k=i
            break
    if k:
        if k==9:
            return 'NINE_NINTHS'
        w = f'and {_UNITS2.get(k)} ninth'
        if k>1:
            w += 's'
        return w
    else:
        return None


def _decimal_fraction_repr(s: str, fractions: bool = True):
    standard_repr = ' '.join(['point'] + [_UNITS[int(_)] for _ in s])
    if not fractions:
        return standard_repr

    r = _FRAC.get(s)
    if r:
        return 'and ' + r

    if all(_=='3' for _ in s[:-1]):
        return 'and a third'
    elif all(_=='6' for _ in s[:-1]):
        return 'and two thirds'
    elif len(s)>6:
        if s[0] == '1' and all(_=='6' for _ in s[1:-1]):
            return 'and a sixth'
        elif s[0] == '8' and all(_=='3' for _ in s[1:-1]):
            return 'and five sixths'
        elif _sevenths := _identify_sevenths(s):
            return _sevenths
        elif _ninths := _identify_ninths(s):
            return _ninths

    return standard_repr

def spell(x: float, fractions: bool = True):
    d = _float_split_dict(x)

    frac_part = ''
    if -1 in d.keys():
        frac_part = _decimal_fraction_repr(d[-1], fractions=fractions)
        if frac_part == 'NINE_NINTHS':
            n = d.get(0,0)
            frac_part = ''
            if n < 999:
                d[0] = n+1
            else:
                d = _float_split_dict(int(x)+1)

    int_part_big = ''
    for pow in sorted(d, reverse=True):
        if pow < 3:
            break
        power_suffix = ''
        if pow in _POW.keys():
            power_suffix = _POW[pow]
        # print(d.get(pow, 0))
        trip = _get_group_of_three(d.get(pow, 0))
        s = ''
        if trip:
            s = trip + ' ' + power_suffix

        if s:
            if int_part_big:
                int_part_big = int_part_big + ', ' + s
            else:
                int_part_big = s

    int_part_small = _get_group_of_three(d.get(0, 0))

    int_part = 'zero'
    if int_part_big and int_part_small:
        if 'hundred' in int_part_small:
            int_part = int_part_big + ', ' + int_part_small
        else:
            int_part = int_part_big + ' and ' + int_part_small
    elif int_part_big:
        int_part = int_part_big
    elif int_part_small:
        int_part = int_part_small

    if int_part and frac_part:
        return int_part + ', ' + frac_part
    else:
        return int_part + frac_part

def print_number(x: float, fractions: bool = True):
    s = spell(x, fractions=fractions)
    print(s)