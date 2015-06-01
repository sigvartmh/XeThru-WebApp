var markdownpdf = require("markdown-pdf")
  , fs = require("fs")

  fs.createReadStream("/Users/sigvart.hovland/Documents/xethru_demo_01_app-1.0.5-SNAPSHOT/doc/XethruSerialProtocol_xethru_demo_01.md")
  .pipe(markdownpdf())
  .pipe(fs.createWriteStream("./document.pdf"))
