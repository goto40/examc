#!/usr/bin/python3

import base64, json, sys, glob, re, os, zlib
from examc import settings

maxLinkLen = 0

def create_link(code: str, opts: str = "-std=c++23", stdin: str|None = None, asm: bool = False, compiler_id="gcc_trunk") -> str:
  if asm:
    print("ASSEMBLY!!!")
    compilers = [
          {
            "id": compiler_id,
            "options": opts
          }
        ]
  else:
    compilers = []
  client_config = {
    "sessions": [
      {
        "id": 1,
        "language": "c++",
        "source": code,
        "compilers": compilers,
        "executors": [
          {
            "arguments": "",
            "compiler": {
              "id": compiler_id,
              "libs": [],
              "options": opts
            },
            "compilerOutputVisible": True
          }
        ]
      }
    ]
  }
  if stdin is not None:
    client_config["sessions"][0]["executors"][0]["stdinVisible"] = True
    client_config["sessions"][0]["executors"][0]["stdin"] = stdin

  bin_data = json.dumps(client_config).encode("ascii")
  #state64 = base64.b64encode(bin_data).decode('ascii')
  state64c = base64.b64encode(zlib.compress(bin_data,level=9)).decode('ascii')

  if (len(state64c)>2000):
    print("compressed length>2000:", len(state64c))
    #print(bin_data)
    exit(1)
  # if (len(state64)>2000):
  #   print("length>2000 (",len(state64),"compressed length=",len(state64c),")")
  
  global maxLinkLen
  maxLinkLen = max(maxLinkLen, len(state64c))

  return f"https://godbolt.org/clientstate/{state64c}"

def process(your_code: str) -> str|None:
  your_code = your_code.replace('\r\n','\n')
  text = your_code
  listings = list(re.finditer(r'(?:(\\begin\{lstlisting\}[^\n]*style=custom'+settings.lang+r'[^\n]*\n)(.*?)(§[^§]*§)?([ \t]*\n)(\\end\{lstlisting\})|((?:\\playsimple\{[^}\n]*\}([^%\n]*))?% GODBOLT))(\s*%(?:\n%|[^\n])*)?', text, re.MULTILINE|re.DOTALL))
  previous_code = ''
  new_text = ''
  pos = 0
  need_write = False
  for (idx, lst) in enumerate(listings):
    new_text += text[pos:lst.start()]
    pos = lst.end()
    start = lst.group(1)
    code1 = lst.group(2).rstrip()
    postfix = lst.group(3)
    code2 = lst.group(4).rstrip()
    if code1 is not None and code2 is not None:
      code = code1+code2
      orig_code1 = code1
      orig_code2 = code2
    end = lst.group(5)
    godbolt = lst.group(6)
    godbolt2 = lst.group(7)
    if godbolt2 is None:
      godbolt2=' '
    if godbolt is not None:
      #print("GODBOLT detected "+godbolt)
      code=''
    comment = lst.group(8)
    orig_comment = comment
    if orig_comment is None:
      orig_comment = ''
    if comment is not None:
      comment = comment.replace('\n%','\n')
    if postfix is None:
      postfix = '§§'
    ignore = comment is not None and re.match(r'.*ignore.*', comment) is not None
    asm = comment is not None and re.match(r'.*asm_output.*', comment) is not None
    do_continue = comment is not None and re.match(r'.*continue.*', comment) is not None
    add_main = comment is not None and re.match(r'.*add_main.*', comment) is not None
    insert = None
    append = None
    stdin = None
    delete_first = None
    delete_last = None
    compiler_flags = '-std=c++23'
    compiler_id ="gsnapshot" #"clang_trunk" #curl -sL https://compiler-explorer.org/api/compilers/c++ |grep trunk

    if comment is not None:
      delete_first = re.match(r'.*delete_first\s+(\d+)', comment, re.DOTALL|re.MULTILINE)
      delete_last = re.match(r'.*delete_last\s+(\d+)', comment, re.DOTALL|re.MULTILINE)
      insert = re.match(r'.*insert\s([^§]*)', comment, re.DOTALL|re.MULTILINE)
      append = re.match(r'.*append\s([^§]*)', comment, re.DOTALL|re.MULTILINE)
      stdin_match = re.match(r'.*stdin\s([^§]*)', comment, re.DOTALL|re.MULTILINE)
      if stdin_match is not None:
        stdin = stdin_match.group(1).replace(r'\n','\n')
      compiler_flags_match = re.match(r'.*compiler_flags ([^§]*)', comment, re.DOTALL|re.MULTILINE)
      if compiler_flags_match is not None:
        compiler_flags = compiler_flags_match.group(1)
      compiler_id_match = re.match(r'.*compiler_id ([^§]*)', comment, re.DOTALL)
      if compiler_id_match is not None:
        compiler_id = compiler_id_match.group(1)
    if delete_first:
      n = int(delete_first.group(1))
      lines = code.split('\n')
      if len(lines)>n:
        lines = lines[n:]
      else:
        lines = []
      code = '\n'.join(lines)
    if delete_last:
      n = int(delete_last.group(1))
      lines = code.split('\n')
      if len(lines)>n:
        lines = lines[:(-n-1)]
      else:
        lines = []
      code = '\n'.join(lines)
    if add_main:
      code = 'int main() {\n' + code + '\n}\n'
    if insert is not None:
      code = insert.group(1).replace(r'\n','\n') + "\n" + code
    if append is not None:
      code = code + '\n' + append.group(1).replace(r'\n','\n')
    #if comment is not None:
    #  print(comment, do_continue)
    code = previous_code+'\n'+code
    if do_continue:
      previous_code = code
      #print(f" - {idx} continue")
    else:
      previous_code = ''
    if godbolt is not None:
      if not ignore and not do_continue:
        goal_play = f"\playsimple{{{create_link(code, compiler_flags, stdin, asm, compiler_id)}}}{godbolt2}% GODBOLT"
        new_text_goal = goal_play+orig_comment
        if godbolt!=goal_play:
          print(f" - {idx} ({lst.start()}..{lst.end()})")  # goal_play
      else:
        new_text_goal = godbolt+godbolt2+orig_comment
    else:
      if not ignore and not do_continue:
        m = re.match(r'(§\\play\{[^}]*\}§)', postfix)
        if m is not None:
          play = m.group(1)
        else:
          play = ""
        goal_play = f"§\play{{{create_link(code, compiler_flags, stdin, asm, compiler_id)}}}§"
        new_text_goal = start+orig_code1+goal_play+orig_code2+end+orig_comment
        if m is not None and play!=goal_play:
          print(f" - {idx} ({lst.start()}..{lst.end()})")  # goal_play
      else:
        new_text_goal = start+orig_code1+orig_code2+end+orig_comment
    if (new_text_goal != lst.group()):
      need_write = True
    new_text += new_text_goal
  new_text += text[pos:]
  if need_write:
    return new_text
  else:
    return your_code 
