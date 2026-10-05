import re, pathlib
p = pathlib.Path(r'D:\Wank\laporan\laporangenerator\raw-md\laporan-ctf-5009-5013.md')
text = p.read_text(encoding='utf-8')
pattern = re.compile(r'<div align="center">\s*<img src="([^"]+)" alt="([^"]*)" width="[^"]+">\s*</div>\s*<p align="center"><em>(.*?)</em></p>', re.S)
text2 = pattern.sub(lambda m: '![' + m.group(3) + '](' + m.group(1) + ')', text)
p.write_text(text2, encoding='utf-8')
print(text2.count('!['), 'image refs now')
