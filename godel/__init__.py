# This file is based on https://github.com/stopachka/godel-numbers
import itertools
import functools
import operator
import collections
from functools import partial

def aseq(x):
  return isinstance(x, (tuple, list))

def vector(*args):
  return list(args)

def frequencies(l):
  return dict(collections.Counter(l))

def sort(l):
  if isinstance(l, dict):
    l = l.items()
  return list(sorted(l))

# https://stackoverflow.com/questions/16739290/composing-functions-in-python
def compose2(f, g):
    return lambda *a, **kw: f(g(*a, **kw))

def comp(*fs):
    return functools.reduce(compose2, fs)

# https://stackoverflow.com/questions/6365128/is-there-a-way-to-construct-lazy-sequences-in-python
def conj(seq, *vals):
  if isinstance(seq, list):
    return [*seq, *vals]
  elif isinstance(seq, tuple):
    return (*seq, *vals)
  else:
    return itertools.chain(vals[::-1], seq)

def reduce(f, val, coll):
  for x in coll:
    val = f(val, x)
  return val

def take_while(f, l):
  for x in l:
    if f(x):
      yield x
    else:
      break

def some(f, l):
  for x in l:
    if f(x):
      return True
  return False

def primes():
  current = 2
  known_primes = []
  while True:
    factors = take_while(lambda x: ((x * x) <= current), known_primes)
    remainders = map(lambda x: (current % x), factors)
    if some(lambda x: x == 0, remainders):
      current += 1
    else:
      known_primes.append(current)
      yield current
      current += 1

def factorize(num, acc = None, primes_ = None):
  acc = acc or [1]
  primes_ = primes_ or primes()
  it = iter(primes_)
  while True:
    if num == 1:
      return acc
    factor = next(it)
    if num % factor == 0:
      num //= factor
      acc.append(factor)
      it = iter(conj(it, factor))

open_bracket = "("
close_bracket = ")"

token_to_num = {
    open_bracket: 1,
    close_bracket: 3,
    '0': 5,
    "next": 7,
    "+": 9,
    "*": 11,
    "=": 13,
    "not": 15,
    "or": 17,
    "when": 19,
    "there-is": 21,
    "a": 2,
    "b": 4,
    "c": 6,
    }

num_to_token = {v: k for k, v in token_to_num.items()}

def token_num(x): return token_to_num[x]
def num_token(x): return num_to_token[x]

def parse_tokens (*args):
  if len(args) == 1:
    res, form = [], args[0]
  else:
    res, form = args
  if res is None:
    res = []
  if aseq(form):
    res_after_open_bracket = conj(res, open_bracket)
    res_after_seq = reduce(parse_tokens, res_after_open_bracket, form)
    return conj(res_after_seq, close_bracket)
  else:
    return conj(res, form)

def bigpow(a, b):
  return a ** b

def apply(f, args, **kws):
  return f(*args, **kws)

def pm_lisp_to_godel_num(form):
  r = parse_tokens(form)
  r = [token_to_num[v] for v in r]
  r = list(map(vector, primes(), r))
  r = list(map(partial(apply, bigpow), r))
  r = reduce(operator.mul, 1, r)
  return r

class Parser:
  def __init__(self, seq):
    self.seq = seq
    self.pos = 0
    self.len = len(seq)
  def peek(self):
    if self.pos < self.len:
      return self.seq[self.pos]
  def next(self):
    x = self.peek()
    if self.pos < self.len:
      self.pos += 1
    return x
  def read(self):
    x = self.next()
    if x == open_bracket:
      r = [x]
      while x != close_bracket:
        x = self.read()
        r.append(x)
      return r[1:-1]
    else:
      return x

def godel_num_to_pm_lisp(godel_num):
  r = factorize(godel_num)
  r = r[1:]
  r = frequencies(r)
  r = sort(r)
  r = list(map(comp(num_token, lambda x: x[1]), r))
  r = Parser(r).read()
  return r
