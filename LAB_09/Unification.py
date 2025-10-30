def occurs_check(var, expr):
    if var == expr:
        return True
    elif isinstance(expr, tuple):
        return any(occurs_check(var, sub) for sub in expr)
    return False

def unify(x, y, subst={}):
    if subst is None:
        return None
    elif x == y:
        return subst
    elif isinstance(x, str) and x.islower():  # x is a variable
        return unify_var(x, y, subst)
    elif isinstance(y, str) and y.islower():  # y is a variable
        return unify_var(y, x, subst)
    elif isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x) != len(y):
            return None
        for a, b in zip(x[1:], y[1:]):
            subst = unify(apply(subst, a), apply(subst, b), subst)
            if subst is None:
                return None
        return subst
    else:
        return None

def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    elif occurs_check(var, x):
        return None
    else:
        subst[var] = x
        return subst

def apply(subst, expr):
    if isinstance(expr, str):
        return subst.get(expr, expr)
    elif isinstance(expr, tuple):
        return (expr[0],) + tuple(apply(subst, arg) for arg in expr[1:])
    else:
        return expr

# Represent terms as tuples: ('P', arg1, arg2), ('g', arg), etc.
expr1 = ('P', 'x', ('g', 'x'))
expr2 = ('P', ('g', 'y'), ('g', ('g', 'z')))

result = unify(expr1, expr2)
print("Unification result:", result)
